@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

python --version >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Python wurde nicht gefunden. Bitte Python 3.10+ installieren.
    pause
    exit /b 1
)

echo [INFO] Installiere/aktualisiere Packaging-Abhaengigkeiten...
python -m pip install -e ".[gui]" pyinstaller
if errorlevel 1 (
    echo [FEHLER] Abhaengigkeiten fuer den Build konnten nicht installiert werden.
    pause
    exit /b 1
)

echo [INFO] Bereinige alte Build-Artefakte...
powershell -NoProfile -Command "Get-ChildItem -LiteralPath 'build','dist' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force"

echo [INFO] Baue VerordnungsAmpel als PySide6-Desktop-Bundle...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --windowed ^
  --name VerordnungsAmpel ^
  --specpath build ^
  --icon "%cd%\src\verordnungsampel\gui\icons\ampel.ico" ^
  --paths src ^
  --add-data "%cd%\data\seed;data\seed" ^
  --add-data "%cd%\src\verordnungsampel\gui\icons;verordnungsampel\gui\icons" ^
  verordnungsampel_gui.py

if errorlevel 1 (
    echo [FEHLER] PyInstaller-Build fehlgeschlagen.
    pause
    exit /b 1
)

echo.
echo [OK] Build fertig: dist\VerordnungsAmpel\VerordnungsAmpel.exe
