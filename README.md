# DE-JURIST AI Desktop

DE-JURIST AI — Windows Desktop Assistent für deutsche Rechts- und Verwaltungsangelegenheiten.

Version: 1.0.0

## Kurzüberblick
- Produktionstaugliche Struktur unter `app/`.
- Lokale SQLite‑Datenbank für Fälle, Dokumente, Fristen und Nachrichten.
- Lokale Dokumentverarbeitung (PDF/DOCX/TXT/PNG/JPG) mit optionaler OCR (Tesseract).
- Keine automatische Übertragung von Dokumenten an externe APIs — Uploads nur nach explizitem Opt‑In.

## Installation (Entwickler)
1. Python 3.11+ installieren.
2. Repository klonen und in das Projektverzeichnis wechseln.
3. `install.bat` ausführen (installiert Abhängigkeiten aus requirements.txt).

Hinweis: Für OCR-Funktionalität installieren Sie zusätzlich Tesseract (siehe unten).

## Erster Start (lokal)
1. Setzen Sie optional die Umgebungsvariable `OPENAI_API_KEY` (nur für Online-Analyse).
2. Starten Sie die Anwendung mit `run.bat` oder aus dem Projekt: `python main.py`.
3. Beim ersten Start wird ein App‑Datenverzeichnis unter `%APPDATA%\DE-JURIST-AI` angelegt und die SQLite‑DB (`database.sqlite`) erstellt.

## OCR (Tesseract)
Wenn Sie Bild‑ oder gescannte PDF‑OCR nutzen möchten, installieren Sie Tesseract:
- Windows: https://github.com/tesseract-ocr/tesseract/releases ➜ Installer herunterladen und installieren.
- Fügen Sie den Installationspfad (z. B. `C:\Program Files\Tesseract-OCR`) zur PATH-Umgebungsvariablen hinzu.

Nach Installation erkennt die App automatisch OCR; falls nicht, prüfen Sie `tesseract --version` in der Eingabeaufforderung.

## Build: Windows EXE (Release)
1. `build_exe.bat` ausführen (PyInstaller). Das Ergebnis wird unter `releases/DE-JURIST-AI-1.0.0/dist/DE-JURIST-AI.exe` erstellt.
2. Die EXE ist als Einzeldatei gepackt und benötigt auf Ziel‑Windows kein installiertes Python.

Test auf sauberem Windows (empfohlen):
- Kopieren Sie die erzeugte EXE auf einen Windows‑PC ohne Python.
- Starten Sie die EXE: GUI sollte erscheinen.
- Erstellen Sie einen neuen Fall, fügen Sie ein PDF hinzu und starten Sie die Dokumentanalyse.

## Datenschutz & Speicherung
- Nutzerdaten werden standardmäßig unter `%APPDATA%\DE-JURIST-AI` gespeichert, nicht im Installationsverzeichnis.
- Dokumente und Datenbank enthalten potenziell sensible PII. Vor produktivem Einsatz ist Verschlüsselung/Redaction empfehlenswert.

## CI / Automatisierter Build
Es gibt eine GitHub Actions Workflow-Datei `.github/workflows/windows-build.yml`, die auf `windows-latest` den Build und Tests ausführt und die EXE als Artefakt bereitstellen kann.

## Build- und Release-Hinweise
- Backup: Sichern Sie `%APPDATA%\DE-JURIST-AI` vor Updates.
- Release-Version: DE-JURIST-AI 1.0.0
- Signing: Für Produktion empfehlen wir Code-Signing des EXE.

## Haftungsausschluss
Diese Software ist kein Ersatz für Rechtsberatung. Bei rechtsverbindlichen Entscheidungen unbedingt qualifizierte Rechtsberatung einholen.
