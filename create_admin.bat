@echo off
color 0E
title Mithila Foods - Create Admin User
echo.
echo ============================================================
echo           MITHILA FOODS SUPPLIER TRACKER SYSTEM
echo                   CREATE ADMIN USER
echo ============================================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run "setup.bat" first to initialize the application.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo Creating admin user for Django admin panel...
echo.
echo You'll be asked to provide:
echo - Username (e.g., admin)
echo - Email address (e.g., admin@mithilafoods.com)
echo - Password (minimum 8 characters)
echo.
echo ============================================================
echo.

python manage.py createsuperuser

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create admin user
    pause
    exit /b 1
)

echo.
echo ============================================================
echo              ADMIN USER CREATED SUCCESSFULLY!
echo ============================================================
echo.
echo You can now access the admin panel at:
echo http://localhost:8000/admin/
echo.
echo Use the credentials you just created to login.
echo.
echo Admin Panel Features:
echo ✓ View all items in detailed tables
echo ✓ Bulk edit operations
echo ✓ Advanced filtering and search
echo ✓ Export data capabilities
echo ✓ User management (future)
echo ✓ System configuration
echo.
echo To start the application, run "run_app.bat"
echo.
pause
