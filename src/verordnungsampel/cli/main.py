"""CLI-Entry-Point fuer VerordnungsAmpel.

Beispiele:
    PYTHONIOENCODING=utf-8 python -m verordnungsampel.cli.main init
    PYTHONIOENCODING=utf-8 python -m verordnungsampel.cli.main check --icd I10 --atc C09AA02
    PYTHONIOENCODING=utf-8 python -m verordnungsampel.cli.main check --icd K21.0 --atc A02BC02 --json
    PYTHONIOENCODING=utf-8 python -m verordnungsampel.cli.main justify --icd F41 --atc N05BA01 --alter 72 --answers antworten.json
    PYTHONIOENCODING=utf-8 python -m verordnungsampel.cli.main log --tail 5
    PYTHONIOENCODING=utf-8 python -m verordnungsampel.cli.main verify
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from verordnungsampel import __version__
from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.db.connection import open_database
from verordnungsampel.db.seed import (
    ensure_seed_data,
    get_last_meta,
    load_meta_only,
    load_seed_data,
)
from verordnungsampel.engine.coverage import (
    CoverageCase,
    CoverageReport,
    analyze_cases,
)
from verordnungsampel.engine.evaluator import Ampel, AmpelErgebnis, evaluate
from verordnungsampel.engine.justification_fsm import (
    STEPS,
    Justification,
    JustificationAnswers,
    JustificationError,
    JustificationFSM,
    JustificationState,
)
from verordnungsampel.engine.praxisbesonderheit import (
    Praxisbesonderheit,
    build_quartal_reminder,
    find_matching as find_praxisbesonderheiten,
    render_reminder,
)
from verordnungsampel.output import (
    WorkflowContext,
    WorkflowOutput,
    WorkflowType,
    build_workflow,
    determine_workflow,
)
from verordnungsampel.utils.logger import get_logger

logger = get_logger("verordnungsampel.cli")

_STARTBANNER = (
    "VerordnungsAmpel: Informationswerk, nicht klinisch validiert. "
    "Nutzung auf eigenes Risiko. `--help` fuer Details."
)


def _print_startbanner(args: argparse.Namespace) -> None:
    """Druckt den CLI-Startbanner (nur bei ``init`` und ``gui``).

    Empfehlung 10.1/10.3 aus RECHTSGUTACHTEN_HAFTUNG.md. Wird durch
    ``--quiet`` oder ``--no-banner`` unterdrueckt.
    """
    if getattr(args, "quiet", False) or getattr(args, "no_banner", False):
        return
    print(_STARTBANNER, file=sys.stderr)


_AMPEL_GLYPHEN = {
    Ampel.GRUEN: "GRUEN",
    Ampel.GELB:  "GELB",
    Ampel.ROT:   "ROT",
}


def _format_ergebnis(erg: AmpelErgebnis) -> str:
    lines = []
    lines.append("=" * 64)
    lines.append(
        f"VerordnungsAmpel  ICD={erg.icd}  ATC={erg.atc}"
        + (f"  Alter={erg.alter}" if erg.alter is not None else "")
    )
    lines.append("-" * 64)
    lines.append(f"Gesamtbewertung: [{_AMPEL_GLYPHEN[erg.gesamt]}]")
    lines.append("")
    lines.append("Begruendungen:")
    for i, t in enumerate(erg.treffer, 1):
        lines.append(f"  {i}. ({_AMPEL_GLYPHEN[t.ampel]}) [{t.regel_kuerzel}]")
        lines.append(f"     {t.begruendung}")
        if t.quelle:
            stand = f", Stand {t.quelle.stand}" if t.quelle.stand else ""
            lines.append(f"     Quelle: {t.quelle.kuerzel} — {t.quelle.titel}{stand}")
        if t.container:
            lines.append(f"     Container: {t.container}")
    if erg.container_hinweise:
        lines.append("")
        lines.append("Container-Hinweise: " + ", ".join(erg.container_hinweise))
    lines.append("=" * 64)
    lines.append(
        "Hinweis: Dies ist ein Informationswerk. Es ersetzt NICHT die "
        "aerztliche Pruefung im Einzelfall."
    )
    return "\n".join(lines)


def _format_justification(just: Justification) -> str:
    lines = []
    lines.append("-" * 64)
    lines.append("Begruendung (strukturiert, versiegelt im Compliance-Log):")
    if not just.required_states:
        lines.append("  [keine Begruendung erforderlich — Ampel GRUEN]")
        return "\n".join(lines)
    for state_str in just.required_states:
        if state_str == JustificationState.CONFIRM.value:
            continue
        step = STEPS[JustificationState(state_str)]
        answer = just.answers.get(state_str)
        lines.append(f"  - {step.prompt}")
        if isinstance(answer, dict):
            for key, val in answer.items():
                lines.append(f"      {key}: {val}")
        elif answer:
            lines.append(f"      {answer}")
        else:
            lines.append(f"      (keine Angabe)")
    lines.append(f"  Bestaetigt: {'ja' if just.confirmed else 'nein'}")
    if just.off_label:
        lines.append("  BSG-Off-Label-Kriterien dokumentiert: ja")
    return "\n".join(lines)


def cmd_init(args: argparse.Namespace) -> int:
    """Initialisiert die DB und laedt Seed-Daten."""
    _print_startbanner(args)
    conn, path = open_database()
    counts = load_seed_data(conn)
    conn.close()
    print(f"Datenbank initialisiert: {path}")
    print("Seed-Daten geladen:")
    for table, n in counts.items():
        print(f"  {table:25s} {n:5d}")
    return 0


def _interactive_answers(fsm: JustificationFSM) -> JustificationAnswers:
    """Sammelt Antworten per Terminal-Prompt (Nutzer sitzt am CLI)."""
    answers = JustificationAnswers()
    print()
    print("=" * 64)
    print("Strukturierte Begruendungspflicht")
    print("=" * 64)
    for step in fsm.iter_steps():
        print()
        print(f"[{step.state.value.upper()}]")
        print(step.help_text)
        if step.state == JustificationState.CONFIRM:
            raw = input("Bestaetigen? (j/N): ").strip().lower()
            answers.set(step.state, raw in ("j", "ja", "y", "yes"))
            continue
        if step.subfields:
            sub_dict: Dict[str, str] = {}
            for sub in step.subfields:
                sub_val = input(f"  {sub}: ").strip()
                sub_dict[sub] = sub_val
            answers.set(step.state, sub_dict)
            continue
        hint = " (optional — leer lassen wenn nicht zutreffend)" if step.min_length == 0 else ""
        raw = input(f"{step.prompt}{hint}\n> ").strip()
        answers.set(step.state, raw)
    return answers


def _load_answers_file(path: Path) -> JustificationAnswers:
    """Laedt Antworten aus einer JSON-Datei (non-interactive Modus)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(
            f"Antwortdatei {path} muss ein JSON-Objekt enthalten, "
            f"nicht {type(data).__name__}"
        )
    return JustificationAnswers(data=data)


def _run_justification(
    erg: AmpelErgebnis, args: argparse.Namespace
) -> Optional[Justification]:
    """Fuehrt die FSM durch und liefert das Ergebnis (oder None bei GRUEN).

    Returns:
        ``Justification`` wenn etwas zu begruenden war, sonst ``None``.
    Raises:
        JustificationError: Wenn die Antworten unvollstaendig sind.
    """
    fsm = JustificationFSM(erg)
    if fsm.is_empty:
        return None

    if args.answers:
        answers = _load_answers_file(Path(args.answers))
    else:
        answers = _interactive_answers(fsm)

    return fsm.run(answers)


def cmd_check(args: argparse.Namespace) -> int:
    """Fuehrt eine Verordnungspruefung durch.

    Wenn ``--justify`` gesetzt ist, wird bei GELB/ROT die strukturierte
    Begruendung direkt erfasst und zusammen mit der Ampel in den
    Compliance-Log geschrieben. Zusaetzlich werden einschlaegige
    Praxisbesonderheiten erkannt und als Hinweis ausgegeben sowie in den
    Log versiegelt.
    """
    conn, _ = open_database()
    try:
        ensure_seed_data(conn)
        erg = evaluate(args.icd, args.atc, alter=args.alter, conn=conn)
        pbs = find_praxisbesonderheiten(args.icd, args.atc, conn=conn)
    finally:
        conn.close()

    if args.json:
        d = erg.to_dict()
        d["praxisbesonderheiten"] = [pb.to_dict() for pb in pbs]
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(_format_ergebnis(erg))
        if pbs:
            print()
            print("Praxisbesonderheit(en) einschlaegig:")
            for pb in pbs:
                print(f"  - {pb.bezeichnung}")
                if pb.quelle:
                    print(f"    Quelle: {pb.quelle.kuerzel}")
            print(
                "  -> KV-Kennziffer auf dem Behandlungsschein markieren "
                "(LSG BW 15.11.2023)."
            )

    justification: Optional[Justification] = None
    if args.justify:
        try:
            justification = _run_justification(erg, args)
        except JustificationError as e:
            print("FEHLER: Begruendung unvollstaendig:", file=sys.stderr)
            for err in e.errors:
                print(f"  - {err}", file=sys.stderr)
            return 3
        if justification is not None and not args.json:
            print(_format_justification(justification))

    if not args.no_log:
        extra: Dict[str, Any] = {"version": __version__}
        if justification is not None:
            extra["justification"] = justification.to_dict()
        if pbs:
            extra["praxisbesonderheiten"] = [pb.to_dict() for pb in pbs]
        with ComplianceLog() as log:
            zusammenfassung = "; ".join(t.begruendung for t in erg.treffer)
            log.append(
                icd=erg.icd,
                atc=erg.atc,
                alter=erg.alter,
                ampel=erg.gesamt.value,
                begruendung=zusammenfassung,
                container=";".join(erg.container_hinweise) or None,
                nutzer=args.nutzer,
                extra=extra,
            )

    return 0


def cmd_justify(args: argparse.Namespace) -> int:
    """Fuehrt Pruefung + strukturierte Begruendung in einem Schritt durch.

    Kurzform fuer ``check --justify``. Einziger Unterschied: Bei GRUEN
    meldet der Befehl explizit, dass keine Begruendungspflicht besteht.
    """
    # Mirror cmd_check, aber mit impliziter --justify-Logik.
    args.justify = True
    return cmd_check(args)


def _build_context_from_args(args: argparse.Namespace) -> WorkflowContext:
    """Baut einen WorkflowContext aus den CLI-Argumenten."""
    return WorkflowContext(
        praxis_name=getattr(args, "praxis", None),
        praxis_adresse=getattr(args, "praxis_adresse", None),
        arzt_name=getattr(args, "arzt", None),
        bsnr=getattr(args, "bsnr", None),
        lanr=getattr(args, "lanr", None),
        kk_name=getattr(args, "kk", None),
        patient_kennung=getattr(args, "patient", None),
    )


def cmd_workflow(args: argparse.Namespace) -> int:
    """Generiert einen Vorab-Klaerungs-Workflow-Text.

    Abhaengig vom Container-Hinweis der Ampel wird einer von vier Texten
    erzeugt:
        - PFLICHT_ANTRAG fuer pflicht_vorab (z.B. Cannabis)
        - VERBOTEN_HINWEIS fuer verboten_vorab (§ 29 BMV-AE)
        - STELLUNGNAHME fuer stellungnahme (Grauzonen, z.B. GLP-1)
        - KEINE_AKTION wenn kein Container

    Optional wird der Text in eine Datei geschrieben (``--out``) und der
    Workflow-Typ in den Compliance-Log versiegelt (``extra.workflow``).
    """
    conn, _ = open_database()
    try:
        ensure_seed_data(conn)
        erg = evaluate(args.icd, args.atc, alter=args.alter, conn=conn)
    finally:
        conn.close()

    context = _build_context_from_args(args)
    output: WorkflowOutput = build_workflow(erg, context)

    rendered = output.render_full()

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"Workflow-Text geschrieben: {out_path}")
        if args.json:
            print(json.dumps(output.to_dict(), ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(output.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(rendered)

    if not args.no_log:
        with ComplianceLog() as log:
            zusammenfassung = "; ".join(t.begruendung for t in erg.treffer)
            log.append(
                icd=erg.icd,
                atc=erg.atc,
                alter=erg.alter,
                ampel=erg.gesamt.value,
                begruendung=zusammenfassung,
                container=";".join(erg.container_hinweise) or None,
                nutzer=args.nutzer,
                extra={
                    "version": __version__,
                    "workflow": {
                        "workflow_type": output.workflow_type.value,
                        "betreff": output.betreff,
                        "empfaenger": output.empfaenger,
                        "rechtsgrundlage": output.rechtsgrundlage,
                    },
                },
            )

    # Exit-Code 0 ausser wenn KEINE_AKTION und trotzdem nach Workflow gefragt —
    # das ist aber kein Fehler, nur Info.
    return 0


def cmd_remind(args: argparse.Namespace) -> int:
    """Erzeugt einen Quartals-Reminder fuer Praxisbesonderheiten.

    Geht alle Compliance-Log-Eintraege des gewuenschten Quartals durch
    und listet diejenigen auf, bei denen eine Praxisbesonderheit
    einschlaegig war — damit der Arzt vor Quartalsende die KV-Kennziffer
    auf dem Behandlungsschein pruefen kann.
    """
    with ComplianceLog() as log:
        entries = [e.to_dict() for e in log.all_entries()]

    try:
        reminder = build_quartal_reminder(entries, args.quartal)
    except ValueError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(reminder.to_dict(), ensure_ascii=False, indent=2))
        return 0

    print(render_reminder(reminder))
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    """Listet Eintraege aus dem Compliance-Log."""
    with ComplianceLog() as log:
        entries = log.all_entries()
    if args.tail and args.tail > 0:
        entries = entries[-args.tail :]
    if args.json:
        print(json.dumps([e.to_dict() for e in entries], ensure_ascii=False, indent=2))
        return 0
    if not entries:
        print("Compliance-Log ist leer.")
        return 0
    for e in entries:
        markers = []
        if isinstance(e.extra, dict):
            if "justification" in e.extra and e.extra["justification"].get("required_states"):
                markers.append("+begruendung")
            if "workflow" in e.extra:
                wf_type = e.extra["workflow"].get("workflow_type", "?")
                markers.append(f"+wf:{wf_type}")
            if "praxisbesonderheiten" in e.extra and e.extra["praxisbesonderheiten"]:
                markers.append(f"+pb:{len(e.extra['praxisbesonderheiten'])}")
        marker_str = f"  [{', '.join(markers)}]" if markers else ""
        print(
            f"#{e.seq:05d} {e.timestamp}  ICD={e.icd:8s} ATC={e.atc:9s} "
            f"-> {e.ampel.upper():5s}  hash={e.hash[:12]}...{marker_str}"
        )
    return 0


def cmd_gui(args: argparse.Namespace) -> int:
    """Startet das PySide6-basierte Tray-Frontend.

    Gibt einen benutzerfreundlichen Fehler aus, wenn PySide6 nicht
    installiert ist.
    """
    _print_startbanner(args)
    try:
        from verordnungsampel.gui.app import run_gui
    except ImportError as exc:  # pragma: no cover - umgebungsabhaengig
        print(
            "FEHLER: Die GUI benoetigt PySide6.\n"
            "Installation:  pip install 'PySide6>=6.6.0'\n"
            f"Originalfehler: {exc}",
            file=sys.stderr,
        )
        return 4
    return int(run_gui() or 0)


def cmd_web(args: argparse.Namespace) -> int:
    """Startet den lokalen Flask-Prototyp fuer Browser-/PWA-Tests."""
    _print_startbanner(args)
    try:
        from verordnungsampel.web import create_app
    except ImportError as exc:  # pragma: no cover - umgebungsabhaengig
        print(
            "FEHLER: Der Web-Prototyp benoetigt Flask.\n"
            "Installation:  pip install -e \".[web]\"\n"
            f"Originalfehler: {exc}",
            file=sys.stderr,
        )
        return 5

    config: Dict[str, Any] = {}
    if args.db:
        config["DATABASE"] = args.db
    app = create_app(config)
    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


def _load_seed_meta(conn) -> Dict[str, Dict[str, Any]]:
    """Holt Seed-Metadaten bevorzugt aus settings (persistiert), sonst aus JSON."""
    row = conn.execute(
        "SELECT value FROM settings WHERE key=?", ("seed_meta_json",)
    ).fetchone()
    if row and row[0]:
        try:
            data = json.loads(row[0])
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, TypeError):
            pass
    # Fallback: frisch von Platte laden
    return load_meta_only()


def cmd_sources(args: argparse.Namespace) -> int:
    """Listet die geladenen Regelwerke mit Stand-Datum und Eintragszahlen.

    Zeigt pro AM-RL-Anlage: Stand, Eintragszahl in der DB (aus `amrl_anlage`
    gruppiert nach Anlage), Extraktions-Datum und Quelle. Ergaenzt um
    PRISCUS und GKV-SV-Praxisbesonderheiten aus der `quelle`-Tabelle.
    """
    conn, db_path = open_database()
    try:
        ensure_seed_data(conn)
        meta_map = _load_seed_meta(conn)
        # Gruppe anlage -> anzahl aus DB
        anlage_counts: Dict[str, int] = {}
        for row in conn.execute(
            "SELECT anlage, COUNT(*) FROM amrl_anlage GROUP BY anlage"
        ).fetchall():
            anlage_counts[str(row[0])] = int(row[1])

        pb_count = conn.execute("SELECT COUNT(*) FROM praxisbesonderheit").fetchone()[0]
        regel_count = conn.execute("SELECT COUNT(*) FROM regel").fetchone()[0]
        quellen = conn.execute(
            "SELECT kuerzel, titel, stand, url FROM quelle ORDER BY kuerzel"
        ).fetchall()

        last_init_row = conn.execute(
            "SELECT value FROM settings WHERE key='last_init'"
        ).fetchone()
        last_init = last_init_row[0] if last_init_row else "(unbekannt)"
    finally:
        conn.close()

    if args.json:
        out = {
            "datenbank": str(db_path),
            "letzte_init": last_init,
            "anlagen": [],
            "weitere_quellen": [],
        }
        # Reihenfolge stabil
        for fname in (
            "amrl_anlage_III.json",
            "amrl_anlage_V.json",
            "amrl_anlage_VI_A.json",
            "amrl_anlage_VI_B.json",
        ):
            meta = meta_map.get(fname, {})
            out["anlagen"].append({
                "datei": fname,
                "anlage": meta.get("anlage"),
                "stand": meta.get("stand"),
                "eintraege_db": anlage_counts.get(str(meta.get("anlage", "")), 0),
                "eintraege_json": meta.get("eintraege_anzahl"),
                "extraktion_datum": meta.get("extraktion_datum"),
                "extraktion_version": meta.get("extraktion_version"),
                "extraktion_methode": meta.get("extraktion_methode"),
                "quelle_url": meta.get("quelle_url"),
                "quelle_datei": meta.get("quelle_datei"),
                "lizenz": meta.get("lizenz"),
            })
        for k, t, s, u in quellen:
            if str(k).startswith("AMRL_"):
                continue
            out["weitere_quellen"].append({
                "kuerzel": k,
                "titel": t,
                "stand": s,
                "url": u,
            })
        out["praxisbesonderheiten_gesamt"] = pb_count
        out["regeln_gesamt"] = regel_count
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print("Regelwerke in der aktuellen Installation:")
    print("-" * 72)
    anlage_order = [
        ("amrl_anlage_III.json", "AM-RL Anlage III"),
        ("amrl_anlage_V.json", "AM-RL Anlage V"),
        ("amrl_anlage_VI_A.json", "AM-RL Anlage VI-A"),
        ("amrl_anlage_VI_B.json", "AM-RL Anlage VI-B"),
    ]
    for fname, label in anlage_order:
        meta = meta_map.get(fname)
        if not meta:
            print(f"  {label:18s} (keine Metadaten — Seed-Datei fehlt?)")
            continue
        anlage_key = str(meta.get("anlage", ""))
        db_n = anlage_counts.get(anlage_key, 0)
        json_n = meta.get("eintraege_anzahl", "?")
        stand = meta.get("stand", "?")
        extr = meta.get("extraktion_datum", "?")
        count_str = f"{db_n} Eintraege" if db_n == json_n else f"{db_n} (JSON: {json_n})"
        print(
            f"  {label:18s}  Stand {stand}  |  {count_str:20s}  |  extrahiert {extr}"
        )
        if args.verbose:
            print(f"      Quelle:      {meta.get('quelle_url', '-')}")
            print(f"      Methode:     {meta.get('extraktion_methode', '-')}")
            print(f"      Version:     {meta.get('extraktion_version', '-')}")
            print(f"      Lizenz:      {meta.get('lizenz', '-')}")

    # Weitere Quellen
    print()
    print("Weitere Quellen / Regelwerke:")
    print("-" * 72)
    other = [(k, t, s, u) for (k, t, s, u) in quellen if not str(k).startswith("AMRL_")]
    if not other:
        print("  (keine)")
    for k, t, s, u in other:
        stand = s or "?"
        short_title = (t or "")[:60]
        print(f"  {k:16s}  Stand {stand:10s}  |  {short_title}")
        if args.verbose and u:
            print(f"      URL: {u}")

    print()
    print(f"PRISCUS/Container-Regeln in DB:  {regel_count}")
    print(f"Praxisbesonderheiten in DB:      {pb_count}")
    print()
    print(f"Datenbank:   {db_path}")
    print(f"Letzte init: {last_init}")
    return 0


_AMPEL_SORT = {"rot": 0, "gelb": 1, "gruen": 2}


def cmd_rules(args: argparse.Namespace) -> int:
    """Zeigt die tatsaechlich in der DB gespeicherten AM-RL-Regeln.

    Filter ``--anlage`` verpflichtend (``III|V|VI_A|VI_B|alle``), optional
    ``--atc`` (Praefix, mit ``%`` wildcard) und ``--ampel`` (``rot|gelb|gruen``).
    Output-Format ``--output table|json|csv``.
    """
    anlage_arg = (args.anlage or "").strip()
    filter_map = {
        "III": ("III",),
        "V": ("V",),
        "VI_A": ("VI-A",),
        "VI_B": ("VI-B",),
        "VI": ("VI-A", "VI-B"),
        "ALLE": ("III", "V", "VI-A", "VI-B"),
    }
    key = anlage_arg.upper().replace("-", "_")
    if key not in filter_map:
        print(
            "FEHLER: --anlage muss einer von III, V, VI_A, VI_B, VI, alle sein.",
            file=sys.stderr,
        )
        return 2
    anlagen_filter = filter_map[key]

    sql = (
        "SELECT a.id, a.anlage, a.atc_pattern, a.ampel, a.bedingung, "
        "a.begruendung, q.kuerzel, q.stand "
        "FROM amrl_anlage a LEFT JOIN quelle q ON a.quelle_id = q.id "
        "WHERE a.anlage IN (" + ",".join("?" for _ in anlagen_filter) + ")"
    )
    params: list = list(anlagen_filter)
    if args.atc:
        atc_pattern = args.atc if "%" in args.atc else args.atc.rstrip("*") + "%"
        sql += " AND a.atc_pattern LIKE ?"
        params.append(atc_pattern)
    if args.ampel:
        sql += " AND LOWER(a.ampel) = ?"
        params.append(args.ampel.lower())
    sql += " ORDER BY a.anlage, a.id"

    conn, _ = open_database()
    try:
        ensure_seed_data(conn)
        rows = conn.execute(sql, params).fetchall()
    finally:
        conn.close()

    if args.output == "json":
        out = []
        for r in rows:
            out.append({
                "id": r[0],
                "anlage": r[1],
                "atc_pattern": r[2],
                "ampel": r[3],
                "bedingung": r[4],
                "begruendung": r[5],
                "quelle_kuerzel": r[6],
                "quelle_stand": r[7],
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if args.output == "csv":
        import csv
        writer = csv.writer(sys.stdout, delimiter=";", lineterminator="\n")
        writer.writerow([
            "id", "anlage", "atc_pattern", "ampel",
            "bedingung", "begruendung", "quelle", "stand",
        ])
        for r in rows:
            writer.writerow(r)
        return 0

    # table (default)
    if not rows:
        print("(keine Regeln fuer diesen Filter)")
        return 0
    print(f"AM-RL-Regeln fuer Anlage(n) {','.join(anlagen_filter)}: {len(rows)} Treffer")
    print("-" * 78)
    for r in rows:
        (rid, anl, atcp, ampel, bed, begr, qk, qs) = r
        ampel_label = (ampel or "").upper()
        print(f"  [{anl:5s}] #{rid:3d} {ampel_label:5s}  ATC={atcp}")
        snippet = (bed or "").strip().replace("\n", " ")
        if len(snippet) > 120:
            snippet = snippet[:117] + "..."
        print(f"          {snippet}")
        if args.verbose and begr:
            begr_s = begr.strip().replace("\n", " ")
            if len(begr_s) > 160:
                begr_s = begr_s[:157] + "..."
            print(f"          Begruendung: {begr_s}")
        if qk:
            print(f"          Quelle: {qk} (Stand {qs or '?'})")
    return 0


def _load_coverage_cases(path: Path) -> list[CoverageCase]:
    """Laedt Coverage-Faelle aus JSON.

    Erwartet entweder eine Liste von Faellen oder ein Objekt mit Feld
    ``cases``. Jeder Fall braucht mindestens ``icd`` und ``atc``.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("cases")
    if not isinstance(data, list):
        raise ValueError("Coverage-Datei muss eine Liste oder {'cases': [...]} sein.")
    return [CoverageCase.from_mapping(item) for item in data]


def _format_coverage_report(report: CoverageReport) -> str:
    """Formatiert einen CoverageReport fuer die CLI."""
    by_ampel = report.by_ampel
    lines = [
        "Coverage-Analyse fuer Ampel-Regelwerk",
        "-" * 64,
        f"Faelle gesamt:     {report.total}",
        f"Erklaert:          {report.explained_count}",
        f"Nicht erklaert:    {report.unexplained_count}",
        f"C(S):              {report.coverage_ratio:.3f} "
        f"({report.coverage_ratio * 100:.1f}%)",
        "Ampel-Verteilung:  "
        f"ROT={by_ampel['rot']}  GELB={by_ampel['gelb']}  GRUEN={by_ampel['gruen']}",
    ]
    if report.rule_hits:
        lines.append("")
        lines.append("Regel-Treffer:")
        for kuerzel, count in report.rule_hits.items():
            lines.append(f"  - {kuerzel}: {count}")
    if report.unexplained_cases:
        lines.append("")
        lines.append("Nicht erklaerte Faelle:")
        for case in report.unexplained_cases:
            label = f"{case.case_id}: " if case.case_id else ""
            alter = f" Alter={case.alter}" if case.alter is not None else ""
            lines.append(f"  - {label}ICD={case.icd} ATC={case.atc}{alter}")
    lines.append("")
    lines.append(
        "Hinweis: C(S) ist Regelwerksabdeckung, keine medizinische Validierung."
    )
    return "\n".join(lines)


def cmd_coverage(args: argparse.Namespace) -> int:
    """Berechnet C(S)=erklaerte Faelle / alle Faelle fuer JSON-Falllisten."""
    try:
        cases = _load_coverage_cases(Path(args.cases))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(
            f"FEHLER: Coverage-Faelle konnten nicht geladen werden: {exc}",
            file=sys.stderr,
        )
        return 2

    conn, _ = open_database()
    try:
        ensure_seed_data(conn)
        report = analyze_cases(cases, conn=conn)
    finally:
        conn.close()

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_format_coverage_report(report))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Prueft die Hash-Chain des Compliance-Logs."""
    with ComplianceLog() as log:
        ok = log.verify_chain()
        n = len(log)
    if ok:
        print(f"Hash-Chain intakt. {n} Eintrag/Eintraege geprueft.")
        return 0
    print("FEHLER: Hash-Chain ist GEBROCHEN.", file=sys.stderr)
    return 2


def _add_check_args(p: argparse.ArgumentParser) -> None:
    """Wiederverwendbare Argumente fuer check/justify."""
    p.add_argument("--icd", required=True, help="ICD-10-GM-Code (z.B. I10)")
    p.add_argument("--atc", required=True, help="ATC-Code (z.B. C09AA02)")
    p.add_argument("--alter", type=int, default=None, help="Alter in Jahren")
    p.add_argument(
        "--nutzer", default=None, help="Optionaler Nutzerbezeichner fuer den Audit-Log"
    )
    p.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    p.add_argument(
        "--no-log", action="store_true", help="Kein Eintrag im Compliance-Log"
    )
    p.add_argument(
        "--answers",
        default=None,
        help="Pfad zu einer JSON-Datei mit vordefinierten Antworten (non-interactive)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="verordnungsampel",
        description=(
            "Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren. "
            "Pruefe ICD+ATC-Kombinationen gegen oeffentliche Regelwerke und "
            "fuehre einen manipulationssicheren Compliance-Log."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"verordnungsampel {__version__}"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Unterdrueckt den Haftungs-Startbanner (bei init/gui).",
    )
    parser.add_argument(
        "--no-banner",
        dest="no_banner",
        action="store_true",
        help="Alias zu --quiet (Haftungs-Startbanner unterdruecken).",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Datenbank anlegen und Seed-Daten laden")
    p_init.set_defaults(func=cmd_init)

    p_check = sub.add_parser("check", help="Verordnung pruefen (ICD + ATC)")
    _add_check_args(p_check)
    p_check.add_argument(
        "--justify",
        action="store_true",
        help="Bei GELB/ROT strukturierte Begruendung erfassen (HSM)",
    )
    p_check.set_defaults(func=cmd_check)

    p_justify = sub.add_parser(
        "justify",
        help="Verordnung pruefen UND strukturierte Begruendung erfassen",
    )
    _add_check_args(p_justify)
    p_justify.set_defaults(func=cmd_justify)

    p_workflow = sub.add_parser(
        "workflow",
        help="Vorab-Klaerungs-Workflow generieren (Antrag/Hinweis/Stellungnahme)",
    )
    p_workflow.add_argument("--icd", required=True, help="ICD-10-GM-Code")
    p_workflow.add_argument("--atc", required=True, help="ATC-Code")
    p_workflow.add_argument("--alter", type=int, default=None, help="Alter in Jahren")
    p_workflow.add_argument("--praxis", default=None, help="Praxisname")
    p_workflow.add_argument("--praxis-adresse", default=None, help="Praxisadresse")
    p_workflow.add_argument("--arzt", default=None, help="Name des verordnenden Arztes")
    p_workflow.add_argument("--bsnr", default=None, help="Betriebsstaettennummer")
    p_workflow.add_argument("--lanr", default=None, help="Lebenslange Arztnummer")
    p_workflow.add_argument("--kk", default=None, help="Name der Krankenkasse")
    p_workflow.add_argument(
        "--patient",
        default=None,
        help="Praxis-internes Patientenkuerzel (NICHT Klarname)",
    )
    p_workflow.add_argument("--out", default=None, help="Dateipfad fuer den Workflow-Text")
    p_workflow.add_argument("--json", action="store_true", help="Metadaten als JSON ausgeben")
    p_workflow.add_argument(
        "--no-log", action="store_true", help="Kein Eintrag im Compliance-Log"
    )
    p_workflow.add_argument(
        "--nutzer", default=None, help="Optionaler Nutzerbezeichner fuer den Audit-Log"
    )
    p_workflow.set_defaults(func=cmd_workflow)

    p_log = sub.add_parser("log", help="Compliance-Log auflisten")
    p_log.add_argument("--tail", type=int, default=20, help="Letzte N Eintraege")
    p_log.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    p_log.set_defaults(func=cmd_log)

    p_verify = sub.add_parser("verify", help="Hash-Chain des Compliance-Logs pruefen")
    p_verify.set_defaults(func=cmd_verify)

    p_remind = sub.add_parser(
        "remind",
        help="Quartals-Reminder fuer Praxisbesonderheiten aus dem Compliance-Log",
    )
    p_remind.add_argument(
        "--quartal",
        required=True,
        help="Quartalsbezeichner im Format YYYY-Qn (z.B. 2026-Q2)",
    )
    p_remind.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    p_remind.set_defaults(func=cmd_remind)

    p_gui = sub.add_parser(
        "gui",
        help="Startet das PySide6-basierte Tray-Frontend",
    )
    p_gui.set_defaults(func=cmd_gui)

    p_web = sub.add_parser(
        "web",
        help="Startet den lokalen Flask-Web-Prototyp",
    )
    p_web.add_argument("--host", default="127.0.0.1", help="Bind-Adresse")
    p_web.add_argument("--port", type=int, default=5000, help="Port fuer den Webserver")
    p_web.add_argument("--db", default=None, help="Optionaler Pfad zur SQLite-Datenbank")
    p_web.add_argument(
        "--debug",
        action="store_true",
        help="Flask-Debug-Modus aktivieren (nur lokal)",
    )
    p_web.set_defaults(func=cmd_web)

    p_sources = sub.add_parser(
        "sources",
        help="Uebersicht der geladenen Regelwerke (Stand, Eintragszahl, Quelle)",
    )
    p_sources.add_argument(
        "--verbose", "-v", action="store_true",
        help="Detaillierte Ausgabe (URL, Methode, Lizenz)",
    )
    p_sources.add_argument(
        "--json", action="store_true", help="Ausgabe als JSON",
    )
    p_sources.set_defaults(func=cmd_sources)

    # Alias: `status` -> identisch zu `sources`
    p_status = sub.add_parser(
        "status",
        help="Alias fuer `sources`: Regelwerksuebersicht",
    )
    p_status.add_argument("--verbose", "-v", action="store_true")
    p_status.add_argument("--json", action="store_true")
    p_status.set_defaults(func=cmd_sources)

    p_rules = sub.add_parser(
        "rules",
        help="Listet geladene AM-RL-Regeln einer Anlage",
    )
    p_rules.add_argument(
        "--anlage", required=True,
        help="Anlage: III, V, VI_A, VI_B, VI (=A+B), alle",
    )
    p_rules.add_argument(
        "--atc", default=None,
        help="ATC-Praefix-Filter (z.B. A10 oder A10%% / A10*)",
    )
    p_rules.add_argument(
        "--ampel", default=None, choices=["rot", "gelb", "gruen", "ROT", "GELB", "GRUEN"],
        help="Nur Regeln mit gegebener Ampel-Farbe",
    )
    p_rules.add_argument(
        "--output", default="table", choices=["table", "json", "csv"],
        help="Ausgabeformat",
    )
    p_rules.add_argument(
        "--verbose", "-v", action="store_true",
        help="Zusaetzlich Begruendungstext mit ausgeben",
    )
    p_rules.set_defaults(func=cmd_rules)

    p_coverage = sub.add_parser(
        "coverage",
        help="Berechnet Regelwerksabdeckung C(S) fuer JSON-Falllisten",
    )
    p_coverage.add_argument(
        "--cases",
        required=True,
        help="JSON-Datei: Liste von {id?, icd, atc, alter?} oder {'cases': [...]}",
    )
    p_coverage.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    p_coverage.set_defaults(func=cmd_coverage)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
