@echo off
echo Validated OnlyFans Link Scraper
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
echo Starting the validated scraper...
echo This will validate each OnlyFans profile to ensure they are real and active.
echo This process will take longer but will give you quality results.
echo.

python validated_onlyfans_scraper.py

echo.
echo Validation completed! Check the output files:
echo - validated_onlyfans_links.txt
echo - validated_onlyfans_links.json
echo.
pause 