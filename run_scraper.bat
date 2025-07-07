@echo off
echo OnlyFans Link Scraper
echo ===================
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
pip install -r requirements.txt

echo.
echo Starting the scraper...
echo This may take several minutes depending on your internet connection.
echo.

python onlyfans_scraper.py

echo.
echo Scraping completed! Check the output files:
echo - onlyfans_links.txt
echo - onlyfans_links.json
echo.
pause 