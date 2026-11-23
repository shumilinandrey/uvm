@echo off
cd /d "%~dp0.."

python -m src.assembler tests/vector1.yaml vector1.bin
python -m src.interpreter vector1.bin vector1.xml 600 608
type vector1.xml

echo.
python -m src.assembler tests/vector2.yaml vector2.bin
python -m src.interpreter vector2.bin vector2.xml 600 608
type vector2.xml

echo.
python -m src.assembler tests/vector3.yaml vector3.bin
python -m src.interpreter vector3.bin vector3.xml 600 608
type vector3.xml

pause