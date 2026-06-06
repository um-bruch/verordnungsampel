"""Lokaler Flask-Prototyp fuer die Browser-/PWA-Linie.

Der Prototyp fuehrt bewusst keine zweite Fachlogik ein, sondern nutzt
dieselben Evaluations- und Praxisbesonderheitsfunktionen wie CLI und GUI.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from flask import Flask, Response, jsonify, render_template_string, request

from verordnungsampel import __version__
from verordnungsampel.db.connection import open_database
from verordnungsampel.db.seed import ensure_seed_data
from verordnungsampel.engine.evaluator import evaluate
from verordnungsampel.engine.praxisbesonderheit import find_matching

MANIFEST = {
    "name": "VerordnungsAmpel",
    "short_name": "VA-Check",
    "description": "Lokaler Ampel-Check für Verordnungsrisiken aus öffentlichen Regelwerken.",
    "start_url": "/",
    "id": "/",
    "scope": "/",
    "display": "standalone",
    "background_color": "#f5f1e8",
    "theme_color": "#355f3d",
    "lang": "de-DE",
    "icons": [
        {"src": "/static/icons/Icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/static/icons/Icon-512.png", "sizes": "512x512", "type": "image/png"},
        {
            "src": "/static/icons/Icon-maskable-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable",
        },
        {
            "src": "/static/icons/Icon-maskable-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable",
        },
    ],
}

SW_JS = """\
const CACHE_NAME = "verordnungsampel-v1";
const STATIC_ASSETS = [
  "/manifest.webmanifest",
  "/offline.html",
  "/static/icons/Icon-192.png",
  "/static/icons/Icon-512.png",
  "/static/icons/Icon-maskable-192.png",
  "/static/icons/Icon-maskable-512.png",
];
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((c) => c.addAll(STATIC_ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request).catch(() => caches.match("/offline.html"))
    );
    return;
  }
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
"""

DISCLAIMER_TEXT = (
    "Informationswerk, nicht klinisch validiert, kein Medizinprodukt. "
    "Die VerordnungsAmpel ersetzt nicht die ärztliche Prüfung im Einzelfall."
)

AMPel_LABELS = {
    "gruen": "Grün",
    "gelb": "Gelb",
    "rot": "Rot",
}

HTML_TEMPLATE = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VerordnungsAmpel Web-Prototyp</title>
  <link rel="manifest" href="/manifest.webmanifest">
  <style>
    :root {
      --bg: linear-gradient(180deg, #f5f1e8 0%, #eef3e4 100%);
      --panel: rgba(255, 255, 255, 0.9);
      --border: rgba(38, 55, 43, 0.12);
      --text: #1e2a20;
      --muted: #526154;
      --green: #2f7d32;
      --yellow: #b98900;
      --red: #b53a2d;
      --shadow: 0 18px 40px rgba(34, 52, 39, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
      color: var(--text);
      background: var(--bg);
      min-height: 100vh;
    }
    main {
      width: min(980px, calc(100% - 2rem));
      margin: 2rem auto 3rem;
    }
    .hero, .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(8px);
    }
    .hero {
      padding: 1.75rem;
      margin-bottom: 1rem;
    }
    .hero h1 {
      margin: 0 0 0.5rem;
      font-size: clamp(2rem, 4vw, 3rem);
      line-height: 1;
    }
    .hero p, .hero li, .card p, .card li {
      color: var(--muted);
      line-height: 1.5;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1rem;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.45rem 0.8rem;
      border-radius: 999px;
      background: rgba(47, 125, 50, 0.08);
      color: var(--text);
      font-size: 0.95rem;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }
    .card {
      padding: 1.25rem;
    }
    label {
      display: block;
      font-weight: 600;
      margin-bottom: 0.35rem;
    }
    input {
      width: 100%;
      border: 1px solid rgba(34, 52, 39, 0.16);
      border-radius: 14px;
      padding: 0.85rem 1rem;
      font: inherit;
      background: rgba(255, 255, 255, 0.96);
      color: var(--text);
    }
    input:focus {
      outline: 2px solid rgba(47, 125, 50, 0.25);
      border-color: rgba(47, 125, 50, 0.4);
    }
    .button-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1rem;
    }
    button {
      border: 0;
      border-radius: 14px;
      padding: 0.9rem 1.1rem;
      font: inherit;
      font-weight: 700;
      color: white;
      background: linear-gradient(135deg, #355f3d, #4a7b52);
      cursor: pointer;
    }
    .hint {
      margin-top: 0.75rem;
      font-size: 0.95rem;
    }
    .alert {
      padding: 0.9rem 1rem;
      border-radius: 16px;
      margin-top: 1rem;
      font-weight: 600;
    }
    .alert.error {
      background: rgba(181, 58, 45, 0.12);
      color: #7f261e;
    }
    .result-head {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      align-items: center;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }
    .status-badge {
      font-size: 1rem;
      font-weight: 700;
      padding: 0.55rem 0.95rem;
      border-radius: 999px;
      color: white;
    }
    .status-badge.gruen { background: var(--green); }
    .status-badge.gelb { background: var(--yellow); }
    .status-badge.rot { background: var(--red); }
    .rule-list, .pb-list {
      display: grid;
      gap: 0.8rem;
      margin-top: 1rem;
    }
    .rule {
      border: 1px solid var(--border);
      border-left: 6px solid var(--green);
      border-radius: 18px;
      padding: 0.9rem 1rem;
      background: rgba(255, 255, 255, 0.82);
    }
    .rule.gelb { border-left-color: var(--yellow); }
    .rule.rot { border-left-color: var(--red); }
    .rule h3 {
      margin: 0 0 0.45rem;
      font-size: 1rem;
    }
    .rule p {
      margin: 0.2rem 0;
    }
    .footer-note {
      margin-top: 1rem;
      font-size: 0.95rem;
      color: var(--muted);
    }
    code {
      font-family: "Cascadia Code", "Consolas", monospace;
      font-size: 0.95em;
    }
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>VerordnungsAmpel</h1>
      <p>Lokaler Browser-Prototyp für die geplante Web/PWA-Linie. Die bestehende Ampel-Engine, die Praxisbesonderheiten und die Seed-Daten werden direkt aus dem Python-Kern genutzt.</p>
      <div class="meta">
        <span class="pill">Version {{ version }}</span>
        <span class="pill">Nur lokal</span>
        <span class="pill">Kein Persistenz-Workflow im Browser</span>
      </div>
    </section>

    <section class="card">
      <form method="post" novalidate>
        <div class="grid">
          <div>
            <label for="icd">ICD-10-GM</label>
            <input id="icd" name="icd" value="{{ form_data.icd }}" placeholder="z. B. I10" required>
          </div>
          <div>
            <label for="atc">ATC</label>
            <input id="atc" name="atc" value="{{ form_data.atc }}" placeholder="z. B. C09AA02" required>
          </div>
          <div>
            <label for="alter">Alter (optional)</label>
            <input id="alter" name="alter" value="{{ form_data.alter }}" placeholder="z. B. 72" inputmode="numeric">
          </div>
        </div>
        <div class="button-row">
          <button type="submit">Prüfung ausführen</button>
        </div>
        <p class="hint">{{ disclaimer }}</p>
      </form>

      {% if error %}
        <div class="alert error">{{ error }}</div>
      {% endif %}
    </section>

    {% if result %}
      <section class="card" style="margin-top: 1rem;">
        <div class="result-head">
          <div>
            <h2 style="margin: 0 0 0.35rem;">Prüfergebnis</h2>
            <p style="margin: 0;">ICD <code>{{ result.icd }}</code> · ATC <code>{{ result.atc }}</code>{% if result.alter is not none %} · Alter {{ result.alter }}{% endif %}</p>
          </div>
          <span class="status-badge {{ result.gesamt }}">{{ ampel_labels[result.gesamt] }}</span>
        </div>

        {% if result.container_hinweise %}
          <p><strong>Container-Hinweise:</strong> {{ result.container_hinweise | join(", ") }}</p>
        {% endif %}

        <div class="rule-list">
          {% for treffer in result.treffer %}
            <article class="rule {{ treffer.ampel }}">
              <h3>{{ ampel_labels[treffer.ampel] }} · {{ treffer.regel }}</h3>
              <p>{{ treffer.begruendung }}</p>
              {% if treffer.quelle %}
                <p><strong>Quelle:</strong> {{ treffer.quelle.kuerzel }} — {{ treffer.quelle.titel }}{% if treffer.quelle.stand %} (Stand {{ treffer.quelle.stand }}){% endif %}</p>
              {% endif %}
              {% if treffer.container %}
                <p><strong>Container:</strong> {{ treffer.container }}</p>
              {% endif %}
            </article>
          {% endfor %}
        </div>

        {% if result.praxisbesonderheiten %}
          <h2 style="margin-top: 1.35rem;">Praxisbesonderheiten</h2>
          <div class="pb-list">
            {% for pb in result.praxisbesonderheiten %}
              <article class="rule gruen">
                <h3>{{ pb.bezeichnung }}</h3>
                <p>ATC-Muster: <code>{{ pb.atc_pattern }}</code>{% if pb.icd_pattern %} · ICD-Muster: <code>{{ pb.icd_pattern }}</code>{% endif %}</p>
                {% if pb.quelle %}
                  <p><strong>Quelle:</strong> {{ pb.quelle.kuerzel }} — {{ pb.quelle.titel }}</p>
                {% endif %}
              </article>
            {% endfor %}
          </div>
        {% endif %}

        <p class="footer-note">API-Pendant für spätere PWA-Schichten: <code>POST /api/check</code></p>
      </section>
    {% endif %}
  </main>
  <script>
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js");
    }
  </script>
</body>
</html>
"""


def _parse_alter(raw_value: Any) -> int | None:
    """Parst das optionale Alter aus Formular- oder JSON-Daten."""
    if raw_value in (None, ""):
        return None
    try:
        alter = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Alter muss eine ganze Zahl sein.") from exc
    if alter < 0:
        raise ValueError("Alter darf nicht negativ sein.")
    return alter


def _ensure_seed_data(conn: sqlite3.Connection) -> None:
    """Laedt Seed-Daten beim ersten Web-Zugriff automatisch nach."""
    ensure_seed_data(conn)


def _run_check(
    icd: str | None,
    atc: str | None,
    alter: Any = None,
    *,
    db_path: str | None = None,
) -> dict[str, Any]:
    """Fuehrt eine Browser-Pruefung gegen die bestehende Fachlogik aus."""
    icd_norm = (icd or "").strip().upper()
    atc_norm = (atc or "").strip().upper()
    if not icd_norm:
        raise ValueError("ICD-10-GM-Code fehlt.")
    if not atc_norm:
        raise ValueError("ATC-Code fehlt.")

    alter_value = _parse_alter(alter)
    conn, _ = open_database(db_path)
    try:
        _ensure_seed_data(conn)
        ergebnis = evaluate(icd_norm, atc_norm, alter=alter_value, conn=conn)
        praxisbesonderheiten = find_matching(icd_norm, atc_norm, conn=conn)
    finally:
        conn.close()

    payload = ergebnis.to_dict()
    payload["container_hinweise"] = ergebnis.container_hinweise
    payload["praxisbesonderheiten"] = [pb.to_dict() for pb in praxisbesonderheiten]
    return payload


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Erstellt die Flask-Anwendung fuer lokalen Browser-Zugriff."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=None,
        DISCLAIMER=DISCLAIMER_TEXT,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    @app.get("/health")
    def health() -> Any:
        return jsonify(
            {
                "status": "ok",
                "service": "verordnungsampel-web",
                "version": __version__,
            }
        )

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
        result = None
        error = None
        form_data = {
            "icd": request.form.get("icd", ""),
            "atc": request.form.get("atc", ""),
            "alter": request.form.get("alter", ""),
        }
        if request.method == "POST":
            try:
                result = _run_check(
                    form_data["icd"],
                    form_data["atc"],
                    form_data["alter"],
                    db_path=app.config.get("DATABASE"),
                )
            except ValueError as exc:
                error = str(exc)
        return render_template_string(
            HTML_TEMPLATE,
            ampel_labels=AMPel_LABELS,
            disclaimer=app.config["DISCLAIMER"],
            error=error,
            form_data=form_data,
            result=result,
            version=__version__,
        )

    @app.post("/api/check")
    def api_check() -> Any:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "error": "JSON-Objekt erwartet."}), 400
        try:
            result = _run_check(
                payload.get("icd"),
                payload.get("atc"),
                payload.get("alter"),
                db_path=app.config.get("DATABASE"),
            )
        except ValueError as exc:
            return jsonify({"status": "error", "error": str(exc)}), 400
        return jsonify(
            {
                "status": "ok",
                "version": __version__,
                "disclaimer": app.config["DISCLAIMER"],
                "result": result,
            }
        )

    @app.get("/manifest.webmanifest")
    def manifest() -> Any:
        return Response(json.dumps(MANIFEST, ensure_ascii=False), mimetype="application/manifest+json")

    @app.get("/sw.js")
    def service_worker() -> Any:
        return Response(SW_JS, mimetype="application/javascript",
                        headers={"Service-Worker-Allowed": "/"})

    @app.get("/offline.html")
    def offline() -> Any:
        return (
            "<html><body><h1>Lokal nicht erreichbar</h1>"
            "<p>Starten Sie den Python-Server neu.</p></body></html>",
            200,
        )

    return app
