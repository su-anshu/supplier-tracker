@echo off
color 0A
title Mithila Foods - Supplier Tracker Setup
echo.
echo ============================================================
echo           MITHILA FOODS SUPPLIER TRACKER SYSTEM
echo                    INITIAL SETUP
echo ============================================================
echo.

echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python is installed

echo.
echo [2/8] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo [3/8] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo [4/8] Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo ✓ All packages installed successfully

echo.
echo [5/8] Setting up database...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)
echo ✓ Migrations created

python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to apply migrations
    pause
    exit /b 1
)
echo ✓ Database setup complete

echo.
echo [6/8] Loading sample data...
python manage.py load_sample_data
if errorlevel 1 (
    echo WARNING: Failed to load sample data (this is optional)
) else (
    echo ✓ Sample data loaded successfully
)

echo.
echo [7/8] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo WARNING: Failed to collect static files (may not be critical)
) else (
    echo ✓ Static files collected
)

echo.
echo [8/8] Running system check...
python manage.py check
if errorlevel 1 (
    echo ERROR: System check failed
    pause
    exit /b 1
)
echo ✓ System check passed

echo.
echo ============================================================
echo                    SETUP COMPLETE! 
echo ============================================================
echo.
echo Your Supplier Tracker System is now ready to use!
echo.
echo TO START THE APPLICATION:
echo 1. Double-click "run_app.bat" 
echo 2. Or run: python manage.py runserver
echo 3. Then visit: http://localhost:8000
echo.
echo ADMIN ACCESS (Optional):
echo - To create admin user, run: python manage.py createsuperuser
echo - Then visit: http://localhost:8000/admin
echo.
echo FEATURES READY:
echo ✓ Item Master with 8 sample items
echo ✓ Add/Edit/Delete items
echo ✓ Category-wise item listing  
echo ✓ Search and filtering
echo ✓ Dashboard with analytics
echo ✓ Bulk operations
echo ✓ Mobile responsive design
echo.
echo ============================================================
echo.
set /p "answer=Do you want to start the application now? (Y/N): "
if /i "%answer%"=="Y" (
    echo.
    echo Starting application...
    python manage.py runserver
) else (
    echo.
    echo Setup complete. Use "run_app.bat" to start the application anytime.
    pause
)
