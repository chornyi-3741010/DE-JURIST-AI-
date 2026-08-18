# DE-JURIST AI Desktop

DE-JURIST AI — Windows Desktop Assistent für deutsche Rechts- und Verwaltungsangelegenheiten.

Version: 1.0.0

## Kurzüberblick
- Produktionstaugliche Struktur unter `app/`.
- Lokale SQLite‑Datenbank für Fälle, Dokumente, Fristen und Nachrichten.
- Lokale Dokumentverarbeitung (PDF/DOCX/TXT/PNG/JPG) mit optionaler OCR (Tesseract).
- Keine automatische Übertragung von Dokumenten an externe APIs — Uploads nur nach explizitem Opt‑In.
- **Benutzeroberfläche: 100% Russisch**
- **Mehrsprachige juristische Funktionen: Deutsch ↔ Russisch ↔ Ukrainisch**

## Installation & Verwendung

### Option A: Fertige Windows-EXE (empfohlen für Endbenutzer)
1. Laden Sie die fertig kompilierte EXE herunter: `releases/DE-JURIST-AI-1.0.0/dist/DE-JURIST-AI.exe`
2. Kopieren Sie die EXE auf Ihren Windows-PC (keine Python-Installation erforderlich).
3. Starten Sie die EXE direkt.
4. **Optional:** Für OCR-Funktionalität installieren Sie zusätzlich Tesseract (siehe unten).

### Option B: Installation von Quellcode (Entwicklung)
1. Python 3.11+ installieren.
2. Repository klonen und in das Projektverzeichnis wechseln.
3. `install.bat` ausführen (installiert Abhängigkeiten aus requirements.txt).

## Erster Start (lokal)
1. Setzen Sie optional die Umgebungsvariable `OPENAI_API_KEY` (nur für Online-Analyse).
2. Starten Sie die Anwendung mit `run.bat` oder aus dem Projekt: `python main.ru`.
3. Beim ersten Start wird ein App‑Datenverzeichnis unter `%APPDATA%\DE-JURIST-AI` angelegt und die SQLite‑DB (`database.sqlite`) erstellt.

## Benutzeroberfläche
- **Sprache: Russisch**
  Alle UI-Elemente sind auf Russisch:
  - Fenster-Titel: "DE-JURIST AI — юридический агент Германии"
  - Module: Чат, Анализ документа, Мои дела, Письма, Сроки, Шаблоны, Настройки
  - Schnellaktionen: Проанализировать документ, Перевести на русский, Перевести на украинский, etc.

## Unterstützte Sprachen & Übersetzungen
Der juristischen Assistent unterstützt folgende Arbeitssprachen:
- **Deutsch (deu)** - Deutsche Behörden- und Rechtsdokumente
- **Russisch (rus)** - Russischsprachige Benutzer
- **Ukrainisch (ukr)** - Ukrainischsprachige Benutzer

Alle Übersetzungsrichtungen sind möglich:
- Deutsch ↔ Russisch
- Deutsch ↔ Ukrainisch
- Russisch ↔ Ukrainisch

Nutzen Sie die Schnellaktionen "Перевести на русский" oder "Перевести на украинский" für Übersetzungen.

## OCR (Tesseract)
Wenn Sie Bild‑ oder gescannte PDF‑OCR nutzen möchten, installieren Sie Tesseract:
- Windows: https://github.com/tesseract-ocr/tesseract/releases ➜ Installer herunterladen und installieren.
- Wählen Sie **mindestens** diese Sprachdaten aus: Deutsch (deu), Russisch (rus), Ukrainisch (ukr)
- Fügen Sie den Installationspfad (z. B. `C:\Program Files\Tesseract-OCR`) zur PATH-Umgebungsvariablen hinzu.

Nach Installation erkennt die App automatisch OCR; falls nicht, prüfen Sie `tesseract --version` in der Eingabeaufforderung.

## Build: Windows EXE (Release)
1. Stelle sicher, dass `main.ru` die Eingangsdatei ist (nicht `main.py`).
2. `build_exe.bat` ausführen (PyInstaller). Das Ergebnis wird unter `releases/DE-JURIST-AI-1.0.0/dist/DE-JURIST-AI.exe` erstellt.
3. Die EXE ist als Einzeldatei gepackt (35.3 MB) und benötigt auf Ziel‑Windows kein installiertes Python.

### Rebuild durchführen:
```bash
build_exe.bat
```

Test auf sauberem Windows (empfohlen):
- Kopieren Sie die erzeugte EXE auf einen Windows‑PC ohne Python.
- Starten Sie die EXE: GUI sollte in Russisch erscheinen.
- Erstellen Sie einen neuen Fall, fügen Sie ein PDF hinzu und starten Sie die Dokumentanalyse.

## Datenschutz & Speicherung
- Nutzerdaten werden standardmäßig unter `%APPDATA%\DE-JURIST-AI` gespeichert, nicht im Installationsverzeichnis.
- Dokumente und Datenbank enthalten potenziell sensible PII. Vor produktivem Einsatz ist Verschlüsselung/Redaction empfehlenswert.
- Opt-in für externe Verarbeitung: Dokumente werden standardmäßig lokal verarbeitet. Externe API-Aufrufe nur mit explizitem Opt-In.

## CI / Automatisierter Build
Es gibt eine GitHub Actions Workflow-Datei `.github/workflows/windows-build.yml`, die auf `windows-latest` den Build und Tests ausführt und die EXE als Artefakt bereitstellen kann.

## Eingangsdatei
- **Einstiegspunkt:** `main.ru` (nicht `main.py`)
- Dies ist korrekt benannt und erlaubt Verwendung des `.ru`-Dateityps.
- Alle Build-Tools (run.bat, build_exe.bat, GitHub Actions) verwenden `main.ru`.

## Build- und Release-Hinweise
- Backup: Sichern Sie `%APPDATA%\DE-JURIST-AI` vor Updates.
- Release-Version: DE-JURIST-AI 1.0.0
- Signing: Für Produktion empfehlen wir Code-Signing des EXE.
- **EXE-Größe:** 35.3 MB (alle Python-Dependencies gebündelt)
- **Abhängigkeiten auf Zielcomputer:** Nur Tesseract (für OCR) + Sprachdaten (optional)

## Haftungsausschluss
Diese Software ist kein Ersatz für Rechtsberatung. Bei rechtsverbindlichen Entscheidungen unbedingt qualifizierte Rechtsberatung einholen.
