@echo off
setlocal enabledelayedexpansion

set "ENV_NAME=rtx_data_app1"
set "PYTHON_VERSION=3.10.13"

REM Check if the environment exists
call "%localappdata%\NVIDIA\MiniConda\Scripts\conda.exe" info --envs | findstr /C:"%ENV_NAME%" > nul
if errorlevel 1 (
    echo Environment %ENV_NAME% not found. Creating...
    call "%localappdata%\NVIDIA\MiniConda\Scripts\conda.exe" create --name %ENV_NAME% python=%PYTHON_VERSION% --yes
    if errorlevel 1 (
        echo Failed to create environment %ENV_NAME%.
        exit /b 1
    )
)

REM Activate the environment
echo Activating environment %ENV_NAME%...
call "%localappdata%\NVIDIA\MiniConda\Scripts\activate.bat" %ENV_NAME%

REM Optionally, install requirements from a file if specified
if exist requirements.txt (
    echo Installing requirements from requirements.txt...
    pip install -r requirements.txt
)

REM Check the Python version in the activated environment
echo Checking Python version...
python --version

REM Start your app
python app.py
pause

endlocal
