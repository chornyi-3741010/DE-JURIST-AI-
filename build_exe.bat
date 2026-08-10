@echo off
chcp 65001 >nul
python -m pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name DE-JURIST-AI main.py
if errorlevel 1 (
  echo Ошибка сборки.
  pause
  exit /b 1
)
echo.
echo Готово. EXE находится в папке dist\DE-JURIST-AI.exe
pause
