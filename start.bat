@echo off
REM ======================================================================
REM VerordnungsAmpel - Interaktives Demo-Menue
REM
REM Prototyp v0.1 - Companion-Tool fuer Vertragsaerzte zur
REM Regress-Praevention im Moment der Verordnung
REM
REM Direkt-Modus: start.bat check --icd I10 --atc C09AA02
REM Menue-Modus:  start.bat (ohne Argumente)
REM ======================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src;%PYTHONPATH%

python --version >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Python wurde nicht gefunden. Bitte Python 3.10+ installieren.
    pause
    exit /b 1
)

REM Direkt-Modus: alle Argumente an das CLI durchreichen
if not "%~1"=="" (
    python -m verordnungsampel.cli.main %*
    exit /b %errorlevel%
)

:menu
cls
echo ======================================================================
echo                  VerordnungsAmpel - Prototyp v0.1
echo ======================================================================
echo.
echo   Companion-Tool fuer Vertragsaerzte zur Regress-Praevention
echo   im Moment der Verordnung  (GPL-3.0, kein Medical Device)
echo.
echo ----------------------------------------------------------------------
echo   SETUP
echo     1. Datenbank initialisieren und Seed-Daten laden  (init)
echo.
echo   FUNKTION 1 - Ampel (Plausibilitaetspruefung)
echo     2. Beispiel GRUEN:  ACE-Hemmer bei Hypertonie     (I10 + C09AA02)
echo     3. Beispiel GELB:   PPI ohne Refluxdiagnose       (M54.5 + A02BC02)
echo     4. Beispiel ROT:    Benzodiazepin Patient 72 J.   (F41 + N05BA01)
echo.
echo   FUNKTION 2 - HSM (strukturierte Begruendungspflicht)
echo     5. Interaktive Begruendung (Beispiel-Fall ROT)
echo.
echo   FUNKTION 3 - Vorab-Klaerungs-Workflow
echo     6. Cannabis-Antrag                (pflicht_vorab)
echo     7. GLP-1 Stellungnahme            (stellungnahme)
echo     8. Paragraph 29 BMV-Ae Hinweis    (verboten_vorab)
echo.
echo   FUNKTION 4 - Praxisbesonderheiten + Quartalsreminder
echo     9. MS-Therapie erkennen           (G35 + L03AB07)
echo    10. Quartalsreminder 2026-Q2       (remind)
echo.
echo   FUNKTION 5 - Compliance-Log
echo    11. Log anzeigen                    (log)
echo    12. Hash-Chain pruefen              (verify)
echo.
echo   SONSTIGES
echo    13. CLI-Hilfe anzeigen              (--help)
echo    14. Tests ausfuehren                (pytest)
echo    15. GUI starten                     (PySide6 Tray-App)
echo     0. Beenden
echo ----------------------------------------------------------------------
echo.

set /p choice="Bitte Auswahl (0-15): "

if "%choice%"=="1"  goto do_init
if "%choice%"=="2"  goto do_gruen
if "%choice%"=="3"  goto do_gelb
if "%choice%"=="4"  goto do_rot
if "%choice%"=="5"  goto do_justify
if "%choice%"=="6"  goto do_cannabis
if "%choice%"=="7"  goto do_glp1
if "%choice%"=="8"  goto do_verboten
if "%choice%"=="9"  goto do_ms
if "%choice%"=="10" goto do_remind
if "%choice%"=="11" goto do_log
if "%choice%"=="12" goto do_verify
if "%choice%"=="13" goto do_help
if "%choice%"=="14" goto do_tests
if "%choice%"=="15" goto do_gui
if "%choice%"=="0"  goto end
goto menu

:do_init
echo.
python -m verordnungsampel.cli.main init
goto pause_return

:do_gruen
echo.
python -m verordnungsampel.cli.main check --icd I10 --atc C09AA02
goto pause_return

:do_gelb
echo.
python -m verordnungsampel.cli.main check --icd M54.5 --atc A02BC02
goto pause_return

:do_rot
echo.
python -m verordnungsampel.cli.main check --icd F41 --atc N05BA01 --alter 72
goto pause_return

:do_justify
echo.
echo Interaktive Begruendung fuer F41 + N05BA01 (PRISCUS ROT, Alter 72):
echo (Bei 'Bestaetigen? (j/N):' am Ende bitte 'j' eingeben.)
echo.
python -m verordnungsampel.cli.main justify --icd F41 --atc N05BA01 --alter 72
goto pause_return

:do_cannabis
echo.
python -m verordnungsampel.cli.main workflow --icd R52.1 --atc QV12 --kk "Musterkasse" --praxis "Musterpraxis" --arzt "Dr. med. Musterarzt" --patient P-4711
goto pause_return

:do_glp1
echo.
python -m verordnungsampel.cli.main workflow --icd E66.01 --atc A10BJ06 --kk "Musterkasse" --praxis "Musterpraxis" --arzt "Dr. med. Musterarzt" --patient P-0815
goto pause_return

:do_verboten
echo.
python -m verordnungsampel.cli.main workflow --icd I10 --atc C09AA02 --praxis "Musterpraxis" --arzt "Dr. med. Musterarzt"
goto pause_return

:do_ms
echo.
python -m verordnungsampel.cli.main check --icd G35 --atc L03AB07
goto pause_return

:do_remind
echo.
python -m verordnungsampel.cli.main remind --quartal 2026-Q2
goto pause_return

:do_log
echo.
python -m verordnungsampel.cli.main log --tail 20
goto pause_return

:do_verify
echo.
python -m verordnungsampel.cli.main verify
goto pause_return

:do_help
echo.
python -m verordnungsampel.cli.main --help
goto pause_return

:do_tests
echo.
python -m pytest tests/ -v
goto pause_return

:do_gui
echo.
echo Starte GUI (PySide6 Tray-App) -- Schliessen ueber Tray -^> Beenden.
python -m verordnungsampel.cli.main gui
goto pause_return

:pause_return
echo.
echo ----------------------------------------------------------------------
pause
goto menu

:end
echo.
echo Auf Wiedersehen.
endlocal
exit /b 0
