"""Tests fuer den lokalen Flask-Web-Prototyp."""

from verordnungsampel.web.app import create_app


def _make_client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "web-prototype.db"),
        }
    )
    return app.test_client()


def test_health_endpoint_reports_ok(tmp_path):
    client = _make_client(tmp_path)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["service"] == "verordnungsampel-web"


def test_api_check_returns_structured_result(tmp_path):
    client = _make_client(tmp_path)

    response = client.post(
        "/api/check",
        json={"icd": "I10", "atc": "C09AA02"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["result"]["icd"] == "I10"
    assert payload["result"]["atc"] == "C09AA02"
    assert payload["result"]["gesamt"] in {"gruen", "gelb", "rot"}
    assert isinstance(payload["result"]["treffer"], list)
    assert "disclaimer" in payload


def test_api_check_validates_required_fields(tmp_path):
    client = _make_client(tmp_path)

    response = client.post("/api/check", json={"icd": "", "atc": ""})

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["status"] == "error"
    assert "ICD" in payload["error"]


def test_html_form_renders_result(tmp_path):
    client = _make_client(tmp_path)

    response = client.post(
        "/",
        data={"icd": "F41", "atc": "N05BA01", "alter": "72"},
    )

    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Prüfergebnis" in page
    assert "N05BA01" in page


def test_manifest_endpoint_returns_manifest_json(tmp_path):
    client = _make_client(tmp_path)

    response = client.get("/manifest.webmanifest")

    assert response.status_code == 200
    assert "application/manifest+json" in response.content_type


def test_manifest_has_pwa_required_fields(tmp_path):
    client = _make_client(tmp_path)

    response = client.get("/manifest.webmanifest")

    data = response.get_json(force=True)
    assert data["display"] == "standalone"
    assert "id" in data
    assert "scope" in data
    assert data["start_url"]


def test_sw_endpoint_returns_javascript(tmp_path):
    client = _make_client(tmp_path)

    response = client.get("/sw.js")

    assert response.status_code == 200
    assert "javascript" in response.content_type
    assert b"verordnungsampel-v1" in response.data


def test_offline_fallback_endpoint(tmp_path):
    client = _make_client(tmp_path)

    response = client.get("/offline.html")

    assert response.status_code == 200
    assert b"erreichbar" in response.data


def test_index_html_references_manifest_and_sw(tmp_path):
    client = _make_client(tmp_path)

    response = client.get("/")

    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "manifest.webmanifest" in page
    assert "sw.js" in page
