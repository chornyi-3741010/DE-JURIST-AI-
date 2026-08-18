@echo off
chcp 65001 >nul
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name DE-JURIST-AI main.ru --add-data "resources\system_prompt.txt;resources" --distpath "releases\DE-JURIST-AI-1.0.0\dist" --workpath "releases\DE-JURIST-AI-1.0.0\build" --specpath "releases\DE-JURIST-AI-1.0.0\specs" --clean
if errorlevel 1 (
  echo Ошибка сборки.
  pause
  exit /b 1
)
echo.
echo Готово. EXE находится в папке dist\DE-JURIST-AI.exe
pause
