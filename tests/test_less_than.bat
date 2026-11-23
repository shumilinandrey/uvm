@echo off
chcp 65001 >nul
cd /d "%~dp0.."

python -m src.assembler tests/lessthan.yaml lessthan.bin

if errorlevel 1 goto error

echo.
python -m src.interpreter lessthan.bin lessthan.xml 50 52

if errorlevel 1 goto error

echo.
type lessthan.xml

echo.
echo memory[50] = 1
echo memory[51] = 0
echo memory[52] = 0

echo.
pause
exit /b 0

:error
echo.
pause
exit /b 1