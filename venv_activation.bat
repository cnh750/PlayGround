@echo off

REM Check if argument is given
if "%~1"=="" (
    REM No argument, check if "venv" folder exists in current directory
    if exist ".\venv\VENV\Scripts\activate.bat" (
        set VENV_PATH=%cd%\venv\VENV
    ) else (
        echo Error: No argument given and no "venv" folder found in current directory.
        echo Usage: venv_activation.bat [path\to\venv]
        pause
        exit /b
    )
) else (
    REM Use the given argument as venv path
    set VENV_PATH=%~1
)

REM Activate venv if it exists
if exist "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
    echo Virtual environment activated from "%VENV_PATH%".
) else (
    echo Error: venv not found at "%VENV_PATH%".
    pause
)
