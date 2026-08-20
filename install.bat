@echo off
chcp 65001 >nul
setlocal

echo ========================================
echo       Nepali Language Installer
echo ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python भेटिएन।
    echo पहिले Python install गर्नुहोस्।
    echo.
    pause
    exit /b 1
)

echo Python भेटियो:
python --version
echo.

set "NEP_HOME=%~dp0"
set "NEP_HOME=%NEP_HOME:~0,-1%"

echo Nepali Language path:
echo %NEP_HOME%
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$nepPath = '%NEP_HOME%';" ^
    "$current = [Environment]::GetEnvironmentVariable('Path','User');" ^
    "$paths = @($current -split ';' | Where-Object { $_ -ne '' });" ^
    "if ($paths -notcontains $nepPath) {" ^
    "  $newPath = (($paths + $nepPath) -join ';');" ^
    "  [Environment]::SetEnvironmentVariable('Path',$newPath,'User');" ^
    "  Write-Host 'PATH मा Nepali Language थपियो।';" ^
    "} else {" ^
    "  Write-Host 'Nepali Language PATH मा पहिल्यै छ।';" ^
    "}"

if errorlevel 1 (
    echo.
    echo ERROR: PATH update गर्न सकिएन।
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation सफल भयो।
echo ========================================
echo.
echo नयाँ PowerShell वा Terminal खोल्नुहोस्।
echo त्यसपछि चलाउनुहोस्:
echo.
echo     nep version
echo.
pause