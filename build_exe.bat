@echo off
echo ========================================
echo Building Enterprise IDWMS v2
echo ========================================

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist app.spec del app.spec

pyinstaller ^
--name "Enterprise_IDWMS_v2" ^
--windowed ^
--onefile ^
--add-data "storage;storage" ^
--add-data "gui;gui" ^
--add-data "services;services" ^
app.py

echo.
echo ========================================
echo BUILD COMPLETE
echo ========================================
echo EXE location:
echo dist\Enterprise_IDWMS_v2.exe
pause
