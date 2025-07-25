@echo off
color 0C
title Mithila Foods - Troubleshooting & Maintenance
echo.
echo ============================================================
echo           MITHILA FOODS SUPPLIER TRACKER SYSTEM
echo                TROUBLESHOOTING & MAINTENANCE
echo ============================================================
echo.

:menu
echo Choose an option:
echo.
echo [1] Check System Status
echo [2] Reset Database (WARNING: Deletes all data)
echo [3] Reinstall Dependencies  
echo [4] Clear Cache Files
echo [5] Run on Different Port
echo [6] Check Logs
echo [7] Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto check_status
if "%choice%"=="2" goto reset_database
if "%choice%"=="3" goto reinstall_deps
if "%choice%"=="4" goto clear_cache
if "%choice%"=="5" goto different_port
if "%choice%"=="6" goto check_logs
if "%choice%"=="7" goto exit
goto menu

:check_status
echo.
echo ============================================================
echo                    SYSTEM STATUS CHECK
echo ============================================================
echo.

echo Checking Python...
python --version
echo.

echo Checking virtual environment...
if exist "venv" (
    echo ✓ Virtual environment exists
    call venv\Scripts\activate
    echo ✓ Virtual environment activated
) else (
    echo ✗ Virtual environment missing
    echo Run "setup.bat" to create it
    pause
    goto menu
)

echo.
echo Checking Django installation...
python -c "import django; print('Django version:', django.get_version())"
echo.

echo Checking database...
python manage.py check --database default
echo.

echo Checking migrations...
python manage.py showmigrations
echo.

pause
goto menu

:reset_database
echo.
echo ============================================================
echo                     RESET DATABASE
echo ============================================================
echo.
echo WARNING: This will delete ALL your data!
echo This includes all items, suppliers, and user accounts.
echo.
set /p confirm="Are you sure? Type YES to continue: "
if not "%confirm%"=="YES" (
    echo Operation cancelled.
    pause
    goto menu
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo Deleting database...
if exist "db.sqlite3" del db.sqlite3
echo ✓ Database deleted

echo Running fresh migrations...
python manage.py migrate
echo ✓ Database recreated

echo Loading sample data...
python manage.py load_sample_data
echo ✓ Sample data loaded

echo.
echo Database has been reset successfully!
echo You may need to create a new admin user with "create_admin.bat"
pause
goto menu

:reinstall_deps
echo.
echo ============================================================
echo                  REINSTALL DEPENDENCIES
echo ============================================================
echo.

call venv\Scripts\activate
echo Upgrading pip...
python -m pip install --upgrade pip

echo Reinstalling requirements...
pip install -r requirements.txt --upgrade

echo.
echo Dependencies reinstalled successfully!
pause
goto menu

:clear_cache
echo.
echo ============================================================
echo                    CLEAR CACHE FILES
echo ============================================================
echo.

echo Clearing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo ✓ Python cache cleared

echo Clearing migration files (keeping __init__.py)...
for /r %%f in (items\migrations\*.py) do @if not "%%~nxf"=="__init__.py" del "%%f"
echo ✓ Migration files cleared

echo.
echo Cache files cleared! You may need to run migrations again.
pause
goto menu

:different_port
echo.
echo ============================================================
echo                   RUN ON DIFFERENT PORT
echo ============================================================
echo.

call venv\Scripts\activate
set /p port="Enter port number (e.g., 8080): "
echo.
echo Starting server on port %port%...
echo Visit: http://localhost:%port%/
echo.
python manage.py runserver %port%
pause
goto menu

:check_logs
echo.
echo ============================================================
echo                      CHECK LOGS
echo ============================================================
echo.

if exist "logs\django.log" (
    echo Showing last 20 lines of django.log:
    echo.
    powershell "Get-Content 'logs\django.log' -Tail 20"
) else (
    echo No log files found.
    echo Logs will be created when you run the application.
)

echo.
pause
goto menu

:exit
echo.
echo Goodbye!
timeout /t 2 /nobreak >nul
exit
