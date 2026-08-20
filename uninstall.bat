@echo off
chcp 65001 >nul
setlocal

echo ========================================
echo      Nepali Language Uninstaller
echo ========================================
echo.

set "NEP_HOME=%~dp0"
set "NEP_HOME=%NEP_HOME:~0,-1%"

echo Nepali Language path:
echo %NEP_HOME%
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$nepPath = '%NEP_HOME%';" ^
    "$current = [Environment]::GetEnvironmentVariable('Path','User');" ^
    "$paths = @($current -split ';' | Where-Object { $_ -ne '' -and $_ -ne $nepPath });" ^
    "$newPath = ($paths -join ';');" ^
    "[Environment]::SetEnvironmentVariable('Path',$newPath,'User');" ^
    "Write-Host 'Nepali Language PATH बाट हटाइयो।'"

if errorlevel 1 (
    echo.
    echo ERROR: PATH बाट हटाउन सकिएन।
    pause
    exit /b 1
)

echo.
echo ========================================
echo Uninstall सफल भयो।
echo ========================================
echo.
echo Project files delete गरिएको छैन।
echo PATH बाट मात्र Nepali Language हटाइएको छ।
echo.
echo परिवर्तन लागू गर्न नयाँ Terminal खोल्नुहोस्।
echo.
pause