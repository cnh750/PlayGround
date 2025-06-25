@echo off
if "%VENV_PATH%"=="" (
    echo Error: VENV_PATH environment variable not set.
    pause
    exit /b
)

if exist "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
    echo Virtual environment activated.
) else (
    echo Error: venv not found at "%VENV_PATH%".
    pause
)