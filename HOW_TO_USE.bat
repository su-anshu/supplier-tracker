@echo off
color 0F
title Mithila Foods - How to Use
echo.
echo ============================================================
echo           MITHILA FOODS SUPPLIER TRACKER SYSTEM
echo                    HOW TO USE GUIDE
echo ============================================================
echo.
echo BATCH FILES AVAILABLE:
echo.
echo 🔧 SETUP.BAT
echo    ► First-time setup (run this first!)
echo    ► Installs all dependencies
echo    ► Sets up database
echo    ► Loads sample data
echo    ► One-time setup only
echo.
echo 🚀 RUN_APP.BAT  
echo    ► Daily use - starts the application
echo    ► Double-click to run
echo    ► Opens at http://localhost:8000
echo    ► Use this every time you want to run the app
echo.
echo 👤 CREATE_ADMIN.BAT
echo    ► Creates admin user for advanced features
echo    ► Optional but recommended
echo    ► Access admin at http://localhost:8000/admin
echo.
echo 🔍 TROUBLESHOOT.BAT
echo    ► Fix common problems
echo    ► Reset database if needed
echo    ► System diagnostics
echo    ► Run on different port
echo.
echo ============================================================
echo                    QUICK START GUIDE
echo ============================================================
echo.
echo FOR FIRST TIME USERS:
echo 1. Double-click "setup.bat" (wait for completion)
echo 2. Double-click "create_admin.bat" (optional)
echo 3. Double-click "run_app.bat" 
echo 4. Open browser to http://localhost:8000
echo.
echo FOR DAILY USE:
echo 1. Double-click "run_app.bat"
echo 2. Use the application
echo 3. Press Ctrl+C to stop when done
echo.
echo ============================================================
echo                      FEATURES AVAILABLE
echo ============================================================
echo.
echo ✅ Item Master Management
echo    ► Add new items with detailed information
echo    ► Edit existing items
echo    ► Delete items with confirmation
echo    ► Category-wise organization
echo.
echo ✅ Advanced Search & Filtering
echo    ► Search by name, ID, or HSN code
echo    ► Filter by category, status, classification
echo    ► Expandable category view
echo.
echo ✅ Dashboard Analytics
echo    ► Visual charts and statistics
echo    ► Category breakdown
echo    ► Recent items tracking
echo    ► Items needing attention alerts
echo.
echo ✅ Bulk Operations
echo    ► Select multiple items
echo    ► Mass activate/deactivate
echo    ► Bulk status changes
echo.
echo ✅ Professional Interface
echo    ► Mobile responsive design
echo    ► Bootstrap 5 styling
echo    ► Intuitive navigation
echo    ► Real-time validation
echo.
echo ============================================================
echo                    SAMPLE DATA INCLUDED
echo ============================================================
echo.
echo The system comes with 8 sample items:
echo ► Raw Materials: Basmati Rice, Turmeric, Red Chili
echo ► Packaging: Cardboard Boxes, Plastic Pouches
echo ► Stationery: Office Paper A4
echo ► Infrastructure: Industrial Weighing Scale
echo ► Others: Cleaning Detergent
echo.
echo ============================================================
echo                       NEED HELP?
echo ============================================================
echo.
echo 🆘 Problems? Run "troubleshoot.bat"
echo 📧 Technical Issues? Check the README.md file
echo 🔄 Need to reset? Use troubleshoot menu option 2
echo 🌐 Can't access? Try different port in troubleshoot menu
echo.
echo ============================================================
echo.
set /p "start=Ready to start? Press Enter to run setup.bat or type 'exit' to close: "
if /i "%start%"=="exit" (
    exit
) else (
    call setup.bat
)
