@echo off
echo ============================================================
echo Starting Social Media Platform
echo ============================================================
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd social-media-backend && python manage.py runserver 8000"
timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "python start_frontend.py"
timeout /t 2 /nobreak > nul

echo.
echo ============================================================
echo ✅ Servers Started!
echo ============================================================
echo.
echo Backend:  http://localhost:8000/graphql/
echo Frontend: http://localhost:3000
echo.
echo Press any key to open frontend in browser...
pause > nul

start http://localhost:3000

echo.
echo To stop servers, close the server windows
echo.
pause
