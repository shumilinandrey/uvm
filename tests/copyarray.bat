@echo off
chcp 65001 >nul
cd /d "%~dp0.."

python -m src.assembler tests/copyarray.yaml copyarray.bin
if errorlevel 1 goto error

python -m src.interpreter copyarray.bin dump.xml 50 55
if errorlevel 1 goto error

type dump.xml

echo.
echo COMPLETED
goto end

:error
echo.
echo FAILED

:end
pause