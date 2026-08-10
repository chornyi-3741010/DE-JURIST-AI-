@echo off
chcp 65001 >nul
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name DE-JURIST-AI app\main.py --add-data "resources\system_prompt.txt;resources" --add-data "data;data"
if errorlevel 1 (
  echo Ошибка сборки.
  pause
  exit /b 1
)
echo.
echo Готово. EXE находится в папке dist\DE-JURIST-AI.exe
pause
