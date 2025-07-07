@echo off
echo Practical OnlyFans Link Scraper
echo ===============================
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install requests beautifulsoup4 python-dotenv

echo.
echo Starting the practical scraper...
echo This will keep searching until it finds 100 valid OnlyFans links.
echo The process will continue until the target is reached.
echo.

python practical_onlyfans_scraper.py

echo.
echo Scraping completed! Check the output files:
echo - practical_onlyfans_links.txt
echo - practical_onlyfans_links.json
echo.
pause 