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
echo DE-JURIST AI установлен.
echo Перед запуском задайте OPENAI_API_KEY в переменных среды Windows.
echo Затем запустите run.bat
pause
