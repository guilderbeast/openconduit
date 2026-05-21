@echo off
TITLE Conduit Core: Zero-Touch Deployment Engine
color 0F
echo ===================================================
echo    OPEN CONDUIT FOUNDATION: NODE INSTALLER V4
echo ===================================================
echo.

:: ---------------------------------------------------------
:: PHASE 1: THE BOUNCER (Hardware Verification)
:: ---------------------------------------------------------
echo [1/4] Verifying System Architecture...

:: OS EDITION CHECK
powershell -Command "$os = (Get-CimInstance Win32_OperatingSystem).Caption; if ($os -match 'Home') { exit 1 } else { exit 0 }"
if %errorlevel% equ 1 (
    color 0C
    echo [FATAL ERROR] Windows Home Edition detected. Windows Pro is mandatory for network routing.
    pause
    exit
)

:: RAM CHECK (16GB Minimum)
powershell -Command "$ram = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory; if ($ram -lt 15000000000) { exit 1 } else { exit 0 }"
if %errorlevel% equ 1 (
    color 0C
    echo [FATAL ERROR] Insufficient memory. 16GB RAM required to run local AI and render environments.
    pause
    exit
)

:: GPU CHECK (Discrete Hardware)
powershell -Command "$gpu = (Get-CimInstance Win32_VideoController).Name; if ($gpu -match 'RTX|GTX|Radeon RX') { exit 0 } else { exit 1 }"
if %errorlevel% equ 1 (
    color 0C
    echo [FATAL ERROR] No dedicated rendering GPU detected (GTX/RTX/Radeon RX required).
    pause
    exit
)
echo  - Hardware parameters verified. Proceeding to construct environment...

:: ---------------------------------------------------------
:: PHASE 2: THE ARCHITECT (Path Parity & Z: Drive)
:: ---------------------------------------------------------
echo.
echo [2/4] Constructing Local Environment...
set "REPO_PATH=%~dp0"
:: Strip trailing backslash
set "REPO_PATH=%REPO_PATH:~0,-1%"

:: Map Z: Drive persistently to the current installation folder
echo Mapping Z:\ drive to %REPO_PATH%...
subst Z: /D >nul 2>&1
subst Z: "%REPO_PATH%"
echo  - Z:\ Drive parity established.

:: ---------------------------------------------------------
:: PHASE 3: THE LOCKSMITH (Overwrite Protection & Git Shielding)
:: ---------------------------------------------------------
echo.
echo [3/4] Securing Configuration Files...

:: Apply Overwrite Lock to YAML
if exist "Z:\flamenco-3.9-windows-amd64\flamenco-manager.yaml" (
    attrib +r "Z:\flamenco-3.9-windows-amd64\flamenco-manager.yaml"
    echo  - YAML configuration locked to Port 80.
) else (
    echo  [WARNING] flamenco-manager.yaml not found. Lock failed.
)

:: Secure the .gitignore from Ghost Worker DBs
echo. >> "Z:\.gitignore"
echo # Local Flamenco Databases (Do Not Track) >> "Z:\.gitignore"
echo flamenco-manager.sqlite* >> "Z:\.gitignore"
echo  - SQLite database added to local .gitignore shield.

:: ---------------------------------------------------------
:: PHASE 4: THE HANDOFF (Ghost Launchers)
:: ---------------------------------------------------------
echo.
echo [4/4] Deploying Desktop Interfaces...

:: Create Ghost Worker Launcher
set "DESKTOP=%USERPROFILE%\Desktop"
echo Set WshShell = CreateObject("WScript.Shell") > "%DESKTOP%\Start-Conduit-Worker.vbs"
echo WshShell.Run """Z:\Start-Worker.bat""", 0 >> "%DESKTOP%\Start-Conduit-Worker.vbs"
echo Set WshShell = Nothing >> "%DESKTOP%\Start-Conduit-Worker.vbs"

:: Create Master Kill Switch
echo @echo off > "%DESKTOP%\Kill-Conduit-Farm.bat"
echo TITLE Conduit Core: Kill Switch >> "%DESKTOP%\Kill-Conduit-Farm.bat"
echo taskkill /F /IM flamenco-manager.exe /T ^>nul 2^>^&1 >> "%DESKTOP%\Kill-Conduit-Farm.bat"
echo taskkill /F /IM flamenco-worker.exe /T ^>nul 2^>^&1 >> "%DESKTOP%\Kill-Conduit-Farm.bat"
echo timeout /t 2 ^>nul >> "%DESKTOP%\Kill-Conduit-Farm.bat"

echo  - Ghost interface deployed to desktop.
echo.
color 0A
echo ===================================================
echo [SUCCESS] NODE DEPLOYMENT COMPLETE
echo ===================================================
echo The Open Conduit infrastructure is locked and ready.
echo Use the shortcuts on your desktop to operate the farm.
pause >nul