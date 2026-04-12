"""Zentrale deutsche Strings für die GUI.

Vorbereitet für spätere i18n (derzeit nur Deutsch). Alle Klartexte der
GUI sollen hier leben, damit Übersetzungen später problemlos möglich sind.
"""

from __future__ import annotations


APP_TITLE = "VerordnungsAmpel"
APP_TAGLINE = "Companion-Tool für Vertragsärzte zur Regress-Prävention"

# Tray-Tooltip / Menüs
TRAY_TOOLTIP = "VerordnungsAmpel — Regress-Prävention"
TRAY_SHOW = "Fenster anzeigen"
TRAY_HIDE = "Fenster verbergen"
TRAY_QUIT = "Beenden"

# Menüs
MENU_FILE = "&Datei"
MENU_QUIT = "Be&enden"
MENU_VIEW = "&Ansicht"
MENU_ALWAYS_ON_TOP = "Immer im Vordergrund"
MENU_MINIMAL_MODE = "Minimal-Modus"
MENU_TRANSPARENCY = "Leicht transparent"
MENU_HELP = "&Hilfe"
MENU_ABOUT = "Über VerordnungsAmpel"

# Tabs
TAB_CHECK = "Check"
TAB_JUSTIFY = "Begründen"
TAB_WORKFLOW = "Workflow"
TAB_LOG = "Compliance-Log"
TAB_REMINDER = "Reminder"
TAB_SOURCES = "Regelwerke"

# Check-Tab
CHECK_ICD_LABEL = "ICD-10-GM:"
CHECK_ATC_LABEL = "ATC-Code:"
CHECK_AGE_LABEL = "Alter (optional):"
CHECK_BUTTON = "Prüfen"
CHECK_NO_LOG = "Ergebnis NICHT im Compliance-Log speichern"
CHECK_RESULT_LABEL = "Ergebnis:"
CHECK_SOURCES_LABEL = "Quellen / Begründungen:"
CHECK_PB_LABEL = "Praxisbesonderheit(en):"
CHECK_HINT_EMPTY = "ICD- und ATC-Code eingeben, dann 'Prüfen'."
CHECK_HINT_UNKNOWN = (
    "Kein Treffer — die Kombination ist nicht in unserem Regelwerk. "
    "Bei Unsicherheit: manuelle Prüfung gegen die AM-RL nötig."
)
CHECK_ERROR_MISSING = "ICD- und ATC-Code sind Pflicht."
CHECK_ERROR_GENERIC = "Fehler bei der Prüfung: {msg}"

# Ampel-Farben / Labels
AMPEL_GRUEN = "GRÜN"
AMPEL_GELB = "GELB"
AMPEL_ROT = "ROT"
AMPEL_NONE = "—"

# Justify-Tab
JUSTIFY_NO_DATA = (
    "Erst einen Check im Reiter 'Check' ausführen. "
    "Die strukturierte Begründungspflicht wird nur bei GELB oder ROT aktiv."
)
JUSTIFY_GRUEN_HINT = (
    "Ampel ist GRÜN — keine strukturierte Begründungspflicht. "
    "Du kannst trotzdem freiwillig dokumentieren."
)
JUSTIFY_INTRO = (
    "Die folgenden Felder müssen im Moment der Verordnung ausgefüllt werden "
    "(SG Marburg 14.02.2024; BSG B 6 KA 26/13). Nachträgliche Dokumentation reicht NICHT."
)
JUSTIFY_CONFIRM = "Ich bestätige, dass die Angaben im Moment der Verordnung zutreffen."
JUSTIFY_SUBMIT = "Begründung versiegeln & im Log speichern"
JUSTIFY_SUCCESS = "Begründung erfolgreich im Compliance-Log versiegelt."
JUSTIFY_ERROR_HEAD = "Begründung unvollständig:"

# Workflow-Tab
WORKFLOW_INTRO = (
    "Generiere einen Vorab-Klärungs-Workflow (Antrag / Hinweis / Stellungnahme) "
    "für Container-Marker aus der Ampel."
)
WORKFLOW_PRAXIS = "Praxisname:"
WORKFLOW_PRAXIS_ADRESSE = "Praxisadresse:"
WORKFLOW_ARZT = "Arzt:"
WORKFLOW_BSNR = "BSNR:"
WORKFLOW_LANR = "LANR:"
WORKFLOW_KK = "Krankenkasse:"
WORKFLOW_PATIENT = "Patienten-Kürzel:"
WORKFLOW_GENERATE = "Text generieren"
WORKFLOW_COPY = "In Zwischenablage"
WORKFLOW_SAVE = "Als TXT speichern…"
WORKFLOW_NO_DATA = (
    "Erst einen Check im Reiter 'Check' ausführen. "
    "Der Workflow wird aus dem Ampel-Ergebnis abgeleitet."
)
WORKFLOW_KEINE_AKTION = (
    "Für diese Verordnung ist kein Vorab-Klärungs-Schritt erforderlich."
)
WORKFLOW_COPIED = "Text wurde in die Zwischenablage kopiert."
WORKFLOW_SAVED = "Text wurde gespeichert: {path}"

# Log-Tab
LOG_REFRESH = "Aktualisieren"
LOG_VERIFY = "Hash-Chain prüfen"
LOG_EMPTY = "Compliance-Log ist leer."
LOG_VERIFY_OK = "Hash-Chain intakt ({n} Eintrag/Einträge)."
LOG_VERIFY_FAIL = "ACHTUNG: Hash-Chain ist GEBROCHEN!"

# Reminder-Tab
REMINDER_QUARTAL = "Quartal (YYYY-Qn):"
REMINDER_GENERATE = "Reminder erzeugen"
REMINDER_ERROR = "Ungültiges Quartalsformat. Beispiel: 2026-Q2"
REMINDER_EMPTY = "Keine Verordnungen mit Praxisbesonderheit in diesem Quartal."

# Allgemein
BTN_OK = "OK"
BTN_CANCEL = "Abbrechen"
BTN_CLOSE = "Schließen"
STATUS_READY = "Bereit"
ABOUT_TEXT = (
    "VerordnungsAmpel — Prototyp v{version}\n"
    "Companion-Tool für Vertragsärzte zur Regress-Prävention.\n"
    "Kein Medical Device. Ersetzt keine ärztliche Prüfung.\n"
    "Lizenz: GPL-3.0-or-later"
)

# Hinweise
HINT_NOT_MEDICAL_DEVICE = (
    "Hinweis: Dies ist ein Informationswerk, kein Medical Device. "
    "Es ersetzt NICHT die ärztliche Prüfung im Einzelfall."
)

# Dauerhafte Statuszeile (unter MainWindow, Haftungsgutachten 10.3)
STATUS_PERMANENT_DISCLAIMER = (
    "Pre-Alpha — nicht klinisch validiert — keine Gewährleistung"
)

# Disclaimer-Dialog (Erststart-Acknowledgement, Haftungsgutachten 10.2)
DISCLAIMER_DIALOG_TITLE = (
    "VerordnungsAmpel — Nutzungsbedingungen zur Kenntnis nehmen"
)
DISCLAIMER_DIALOG_HEADLINE = (
    "Bevor Sie das Tool benutzen, bestätigen Sie bitte die folgenden Punkte:"
)
DISCLAIMER_CHECK_NOT_VALIDATED = (
    "Ich habe verstanden, dass dieses Tool nicht klinisch validiert ist."
)
DISCLAIMER_CHECK_NOT_CERTIFIED = (
    "Ich habe verstanden, dass es kein Medizinprodukt und nicht zertifiziert ist."
)
DISCLAIMER_CHECK_DOCTOR_RESPONSIBILITY = (
    "Ich bestätige, dass die ärztliche Verantwortung für jede Verordnung "
    "unverändert bei mir liegt."
)
DISCLAIMER_CHECK_OWN_RISK = (
    "Ich nutze das Tool auf eigenes Risiko (Haftung auf Vorsatz und grobe "
    "Fahrlässigkeit beschränkt, § 521 BGB)."
)
DISCLAIMER_BTN_ACCEPT = "Akzeptieren"
DISCLAIMER_BTN_REJECT = "Ablehnen"
DISCLAIMER_INFO_BUTTONS = (
    "Der Akzeptieren-Knopf wird erst aktiv, wenn alle vier Punkte angehakt sind. "
    "Bei Ablehnung wird die Anwendung beendet."
)
