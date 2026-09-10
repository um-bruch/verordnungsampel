"""VerordnungsAmpel — Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren.

Dieses Paket exponiert das Kern-API:
- :func:`verordnungsampel.engine.evaluator.evaluate` fuer Ampel-Pruefungen
- :class:`verordnungsampel.audit.compliance_log.ComplianceLog` fuer den Audit-Trail
- :func:`verordnungsampel.db.connection.open_database` fuer die Datenbank
- :mod:`verordnungsampel.exchange` fuer standardisierte JSON-Austauschformate

Lizenz: GPL-3.0-or-later
"""

__version__ = "0.1.0"

from verordnungsampel.exchange import (
    CASEBUNDLE_SCHEMA_VERSION,
    RULESET_SCHEMA_VERSION,
    export_casebundle,
    export_casebundle_from_log,
    export_casebundle_json,
    export_ruleset,
    export_ruleset_json,
    import_casebundle,
    import_ruleset,
    validate_casebundle,
    validate_ruleset,
)
__all__ = [
    "__version__",
    "CASEBUNDLE_SCHEMA_VERSION",
    "RULESET_SCHEMA_VERSION",
    "export_casebundle",
    "export_casebundle_from_log",
    "export_casebundle_json",
    "export_ruleset",
    "export_ruleset_json",
    "import_casebundle",
    "import_ruleset",
    "validate_casebundle",
    "validate_ruleset",
]
