# Security Policy

## Supported Versions

Pre-Alpha (0.x). Security fixes are applied to the current development branch only.

## Reporting a Vulnerability

If you find a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue**
2. **Use GitHub's [private vulnerability reporting](../../security/advisories/new)**
3. Include: description, steps to reproduce, potential impact

### How to Report

1. Go to: Repository → Security → Advisories → New
2. Fill out the form (title, description, severity, affected versions)
3. Submit privately (not visible to public until disclosed)

We will respond as soon as possible.

## Scope

Relevant attack surfaces in VerordnungsAmpel:

- **SQLite database** (`regelwerk.db` in `%APPDATA%\VerordnungsAmpel\`) — local data integrity, injection via input fields
- **Compliance-Log Hash-Chain** (`audit/compliance_log.py`) — tampering with chain integrity, hash collision risks
- **Seed data loader** (`db/seed.py`) — malicious JSON files in `data/seed/`
- **CLI input handling** — command injection via ICD/ATC/patient fields
- **GUI input handling** (PySide6) — input sanitization, file-dialog paths

Out of scope:

- Attacks that require local OS-level access to the user's machine
- Social engineering against clinicians
- Physical security of the practice hardware

## Response

As a small volunteer-driven project, response times may vary. Critical issues will be
prioritized. Please allow reasonable time (30 days for most issues, 90 days for complex
fixes) before public disclosure.

## Data Privacy

This tool does **not** process patient personal data by design. If you encounter any code
path that leaks, persists, or transmits patient-identifiable information, treat it as a
critical issue and report it via private advisory.
