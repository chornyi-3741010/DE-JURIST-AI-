# DE-JURIST AI Desktop

DE-JURIST AI — Windows Desktop Assistent für deutsche Rechts- und Verwaltungsangelegenheiten.

## Wichtige Änderungen in diesem Branch

- Produktionstaugliche Architektur (app/ package).
- Lokale SQLite‑Datenbank für Fälle, Dokumente, Fristen und Nachrichten.
- Lokale Dokumentenverarbeitung (PDF/DOCX/TXT/PNG/JPG) mit optionaler OCR.
- Upload an OpenAI nur nach explizitem Opt‑in und Bestätigung.


## Что уже есть
- отдельное окно Windows;
- юридическая системная инструкция;
- чат;
- загрузка нескольких PDF/DOCX/изображений и других файлов;
- автоматическая передача вложений модели;
- режим проверки актуального права через web search;
- быстрые действия: анализ, сроки, ошибки, правовая основа, Widerspruch, ответ ведомству, перевод;
- локальная история диалога;
- архитектура для дальнейших модулей.

## Установка
1. Установите Python 3.10+.
2. Запустите `install.bat`.
3. Создайте/настройте переменную среды Windows `OPENAI_API_KEY`.
4. Запустите `run.bat`.

## Сборка EXE
После проверки работы запустите `build_exe.bat`. Файл будет в `dist\DE-JURIST-AI.exe`.

## Важно
Юридический AI не заменяет адвоката. Перед реальной отправкой юридически значимых документов проверяйте факты, сроки и актуальность права.
