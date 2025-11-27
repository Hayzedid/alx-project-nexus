@echo off
echo ========================================
echo   Social Media Feed - Quick Start
echo ========================================
echo.
echo Starting React + TypeScript Frontend...
echo.
cd social-media-frontend
start cmd /k "npm run dev"
echo.
echo Frontend is starting on http://localhost:3000
echo.
echo Make sure the backend is running on http://localhost:8000
echo If not, run: python manage.py runserver
echo.
echo ========================================
pause
