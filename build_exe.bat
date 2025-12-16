@echo off
echo ========================================
echo  JK's Boutique - Executable Builder
echo ========================================
echo.
echo Installing required packages...
pip install reportlab pyinstaller
echo.
echo Building executable...
echo This may take a few minutes...
echo.
pyinstaller --onefile --windowed --name "JK_Boutique" --add-data "boutique.db;." main.py
echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Your executable is located at:
echo dist\JK_Boutique.exe
echo.
echo You can run it by double-clicking the .exe file
echo or copy it to any Windows computer!
echo.
pause
