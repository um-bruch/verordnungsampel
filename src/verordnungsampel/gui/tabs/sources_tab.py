"""Tab 'Regelwerke': Uebersicht ueber geladene Seed-Daten (Stand, Eintraege, Quelle).

Spiegelt die Ausgabe des CLI-Befehls `sources`. Zusaetzlich:
    * Button 'Aktualisierungs-Check' — zeigt derzeit nur einen Hinweis,
      dass der Check manuell via `scripts/update_amrl.py` angestossen
      werden muss.
    * Button 'Neu laden' — liest die Metadaten frisch aus der DB ein.
"""

from __future__ import annotations

from typing import Dict, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from verordnungsampel.db.connection import open_database


class SourcesTab(QWidget):
    """Zeigt geladene Regelwerke + Stand-Datum, identisch zu `cli sources`."""

    def __init__(self) -> None:
        super().__init__()
        self._build()
        self.refresh()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        header = QLabel(
            "<b>Regelwerke in der aktuellen Installation</b><br/>"
            "<span style='color:#666'>"
            "AM-RL-Anlagen und weitere Quellen mit Stand-Datum und Eintragszahl."
            "</span>"
        )
        header.setTextFormat(Qt.RichText)
        header.setWordWrap(True)
        root.addWidget(header)

        # Scrollbarer Inhalt
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._inner = QWidget()
        self._inner_layout = QVBoxLayout(self._inner)
        self._inner_layout.setAlignment(Qt.AlignTop)
        self._scroll.setWidget(self._inner)
        root.addWidget(self._scroll, 1)

        # Buttons
        btn_row = QHBoxLayout()
        self._btn_refresh = QPushButton("Neu laden")
        self._btn_refresh.clicked.connect(self.refresh)
        btn_row.addWidget(self._btn_refresh)

        self._btn_update = QPushButton("Aktualisierungs-Check...")
        self._btn_update.clicked.connect(self._on_update_check)
        btn_row.addWidget(self._btn_update)
        btn_row.addStretch(1)
        root.addLayout(btn_row)

    def _on_update_check(self) -> None:
        QMessageBox.information(
            self,
            "Aktualisierungs-Check",
            "Der Aktualisierungs-Check gegen die offiziellen G-BA-PDFs "
            "muss derzeit manuell vom Maintainer angestossen werden.\n\n"
            "Befehl:\n"
            "    python scripts/update_amrl.py diff --anlage III --url <G-BA-PDF-URL>\n\n"
            "Details: siehe data/seed/UPDATE_METHODE.md",
        )

    def _load_data(self) -> Dict[str, Any]:
        """Liest Seed-Meta + Zaehler aus der DB."""
        conn, db_path = open_database()
        try:
            row = conn.execute(
                "SELECT value FROM settings WHERE key='seed_meta_json'"
            ).fetchone()
            import json as _json
            meta_map: Dict[str, Dict[str, Any]] = {}
            if row and row[0]:
                try:
                    loaded = _json.loads(row[0])
                    if isinstance(loaded, dict):
                        meta_map = loaded
                except _json.JSONDecodeError:
                    pass

            anlage_counts: Dict[str, int] = {}
            for r in conn.execute(
                "SELECT anlage, COUNT(*) FROM amrl_anlage GROUP BY anlage"
            ).fetchall():
                anlage_counts[str(r[0])] = int(r[1])

            pb_count = conn.execute("SELECT COUNT(*) FROM praxisbesonderheit").fetchone()[0]
            regel_count = conn.execute("SELECT COUNT(*) FROM regel").fetchone()[0]
            quellen = conn.execute(
                "SELECT kuerzel, titel, stand FROM quelle "
                "WHERE kuerzel NOT LIKE 'AMRL_%' ORDER BY kuerzel"
            ).fetchall()
            last_init_row = conn.execute(
                "SELECT value FROM settings WHERE key='last_init'"
            ).fetchone()
            last_init = last_init_row[0] if last_init_row else "(unbekannt)"
        finally:
            conn.close()
        return {
            "meta_map": meta_map,
            "anlage_counts": anlage_counts,
            "pb_count": pb_count,
            "regel_count": regel_count,
            "quellen": quellen,
            "db_path": str(db_path),
            "last_init": last_init,
        }

    def refresh(self) -> None:
        """Leert den Inhalt und baut ihn neu aus der DB auf."""
        # Kinder entfernen
        while self._inner_layout.count():
            item = self._inner_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        try:
            data = self._load_data()
        except Exception as exc:  # pragma: no cover - UI-Fehlerpfad
            lbl = QLabel(f"<span style='color:#a00'>Fehler beim Laden: {exc}</span>")
            lbl.setTextFormat(Qt.RichText)
            self._inner_layout.addWidget(lbl)
            return

        meta_map = data["meta_map"]
        order = [
            ("amrl_anlage_III.json", "AM-RL Anlage III"),
            ("amrl_anlage_V.json", "AM-RL Anlage V"),
            ("amrl_anlage_VI_A.json", "AM-RL Anlage VI-A (Off-Label, anerkannt)"),
            ("amrl_anlage_VI_B.json", "AM-RL Anlage VI-B (Off-Label, nicht anerkannt)"),
        ]
        for fname, label in order:
            meta = meta_map.get(fname, {})
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet("QFrame { background: #f7f7f8; border-radius: 4px; }")
            lay = QVBoxLayout(frame)
            lay.setContentsMargins(8, 6, 8, 6)
            stand = meta.get("stand", "?")
            json_n = meta.get("eintraege_anzahl", "?")
            db_n = data["anlage_counts"].get(str(meta.get("anlage", "")), 0)
            extr = meta.get("extraktion_datum", "?")
            title = QLabel(
                f"<b>{label}</b><br/>"
                f"<span style='color:#333'>"
                f"Stand: <b>{stand}</b> &nbsp; | &nbsp; "
                f"Eintraege in DB: <b>{db_n}</b> (JSON: {json_n}) &nbsp; | &nbsp; "
                f"Extrahiert: {extr}"
                f"</span>"
            )
            title.setTextFormat(Qt.RichText)
            title.setWordWrap(True)
            lay.addWidget(title)
            url = meta.get("quelle_url")
            if url:
                url_lbl = QLabel(
                    f"<span style='color:#666;font-size:10px'>Quelle: "
                    f"<a href='{url}'>{url}</a></span>"
                )
                url_lbl.setTextFormat(Qt.RichText)
                url_lbl.setOpenExternalLinks(True)
                url_lbl.setWordWrap(True)
                lay.addWidget(url_lbl)
            self._inner_layout.addWidget(frame)

        # Weitere Quellen
        weitere_title = QLabel(
            "<br/><b>Weitere Quellen</b> (PRISCUS, GKV-SV, BSG-Urteile):"
        )
        weitere_title.setTextFormat(Qt.RichText)
        self._inner_layout.addWidget(weitere_title)

        for kuerzel, titel, stand in data["quellen"]:
            lbl = QLabel(
                f"&bull; <b>{kuerzel}</b> (Stand {stand or '?'}) "
                f"<span style='color:#666'>{titel or ''}</span>"
            )
            lbl.setTextFormat(Qt.RichText)
            lbl.setWordWrap(True)
            self._inner_layout.addWidget(lbl)

        # Footer
        footer = QLabel(
            f"<br/><span style='color:#666;font-size:10px'>"
            f"Datenbank: {data['db_path']}<br/>"
            f"Letzte init: {data['last_init']}<br/>"
            f"PRISCUS/Container-Regeln: {data['regel_count']} &nbsp; | &nbsp; "
            f"Praxisbesonderheiten: {data['pb_count']}"
            f"</span>"
        )
        footer.setTextFormat(Qt.RichText)
        footer.setWordWrap(True)
        self._inner_layout.addWidget(footer)
        self._inner_layout.addStretch(1)


__all__ = ["SourcesTab"]
