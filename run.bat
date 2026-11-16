@echo off
cd /d "%~dp0"
python -m src.assembler tests\program.yaml program.bin --test
pause