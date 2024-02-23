@echo off
setlocal enabledelayedexpansion

set "env_path_found="

for /f "tokens=1,* delims= " %%a in ('"%localappdata%\NVIDIA\MiniConda\Scripts\conda.exe" env list') do (
    set "env_name=%%a"
    set "env_path=%%b"
    if "!env_path!"=="" (
        set "env_path=!env_name!"
    )
    echo !env_path! | findstr /C:"env_trt_llama2" > nul
    if !errorlevel! equ 0 (
        set "env_path_found=!env_path!"
        goto :endfor
    )
)

:endfor
if not "%env_path_found%"=="" (
    echo Environment path found: %env_path_found%
    call "%localappdata%\NVIDIA\MiniConda\Scripts\activate.bat" %env_path_found%
    
    REM Check the Python version in the activated environment
    echo Checking Python version in the activated environment...
    python --version

    REM Check and install specific packages if not installed
    pip list | findstr Flask > nul || pip install Flask==2.2.5
    pip list | findstr flask-marshmallow > nul || pip install flask-marshmallow==0.15.0
    pip list | findstr Flask-Migrate > nul || pip install Flask-Migrate==4.0.4
    pip list | findstr numpy > nul || pip install numpy==1.24.0
    pip list | findstr pydantic > nul || pip install pydantic==2.3.0
    pip list | findstr pydantic-core > nul || pip install pydantic-core==2.6.3
    pip list | findstr pydantic-settings > nul || pip install pydantic-settings==2.0.3
    pip list | findstr transformers > nul || pip install transformers==4.34.0
    
    python verify_install.py
    python app.py
    pause
) else (
    echo Environment with 'env_trt_llama2' not found.
    pause
)

endlocal
