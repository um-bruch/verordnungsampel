"""VerordnungsAmpel — Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren.

Dieses Paket exponiert das Kern-API:
- :func:`verordnungsampel.engine.evaluator.evaluate` fuer Ampel-Pruefungen
- :class:`verordnungsampel.audit.compliance_log.ComplianceLog` fuer den Audit-Trail
- :func:`verordnungsampel.db.connection.open_database` fuer die Datenbank

Lizenz: GPL-3.0-or-later
"""

__version__ = "0.1.0"
__all__ = ["__version__"]
