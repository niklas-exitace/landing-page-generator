@echo off
echo.
echo ========================================
echo    PUSH TO GITHUB - EASY SETUP
echo ========================================
echo.
echo IMPORTANT: First create a repository on GitHub:
echo 1. Go to https://github.com/new
echo 2. Name it: landing-page-generator
echo 3. Make it Public
echo 4. DON'T initialize with README
echo 5. Click Create repository
echo.
pause

echo.
echo Now I'll push your code to GitHub...
echo.

cd /d C:\Users\Niklas\PycharmProjects\Crawler\LandingPageGenerator

git init
git add .
git commit -m "Initial commit - Landing Page Generator with Claude Opus 4"

echo.
echo ========================================
echo IMPORTANT: Enter your GitHub username when prompted
echo ========================================
echo.
set /p username="Enter your GitHub username: "

git remote add origin https://github.com/%username%/landing-page-generator.git
git push -u origin main

echo.
echo ========================================
echo.
echo If you see an error about 'main', run this command manually:
echo git push -u origin master
echo.
echo Otherwise, your code is now on GitHub!
echo.
echo Next: Go to https://share.streamlit.io/ to deploy
echo.
pause