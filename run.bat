@echo off
set "PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"

echo Installing requirements...
"%PYTHON_PATH%" -m pip install -r requirements.txt

echo Starting Bot...
"%PYTHON_PATH%" main.py
pause
