@echo off
color 0B
title Mithila Foods - Supplier Tracker System
echo.
echo ============================================================
echo           MITHILA FOODS SUPPLIER TRACKER SYSTEM
echo                    Starting Application...
echo ============================================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run "setup.bat" first to initialize the application.
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please run "setup.bat" to fix this issue.
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo [2/3] Checking database status...
python manage.py showmigrations --plan >nul 2>&1
if errorlevel 1 (
    echo ERROR: Database not properly configured
    echo Please run "setup.bat" to fix this issue.
    pause
    exit /b 1
)
echo ✓ Database is ready

echo.
echo [3/3] Starting Django development server...
echo.
echo ============================================================
echo                   APPLICATION STARTING
echo ============================================================
echo.
echo 🌐 Your application will be available at:
echo    ► http://localhost:8000/        (Main Application)
echo    ► http://localhost:8000/admin/  (Admin Panel)
echo.
echo 📋 Features Available:
echo    ► Item Master Management
echo    ► Add/Edit/Delete Items  
echo    ► Category-wise Listing
echo    ► Search & Filtering
echo    ► Dashboard Analytics
echo    ► Bulk Operations
echo.
echo 🔧 Controls:
echo    ► Press Ctrl+C to stop the server
echo    ► Close this window to stop the application
echo.
echo ============================================================
echo                  SERVER STARTING...
echo ============================================================
echo.

:: Start the Django server
python manage.py runserver
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the server
    echo This might be due to:
    echo 1. Port 8000 is already in use
    echo 2. Database issues
    echo 3. Missing dependencies
    echo.
    echo Try running "setup.bat" to fix these issues.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo              APPLICATION STOPPED
echo ============================================================
echo.
echo The server has been stopped.
echo To restart, double-click this file again or run:
echo python manage.py runserver
echo.
pause
