@echo off
chcp 65001 >nul
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Ошибка установки зависимостей.
  pause
  exit /b 1
)
echo.
echo DE-JURIST AI installiert.
echo Bitte setzen Sie OPENAI_API_KEY als Umgebungsvariable, wenn Online-Funktionen genutzt werden sollen.
echo Then run run.bat
pause
