@echo off
echo.
echo ========================================
echo   CHECKPOINT ROLLBACK UTILITY
echo ========================================
echo.
echo Available Checkpoints:
git tag
echo.
echo Current Status:
git log --oneline -3
echo.
echo ========================================
echo   ROLLBACK OPTIONS
echo ========================================
echo.
echo 1. Soft Rollback  (Keep current changes)
echo 2. Hard Rollback  (Discard all changes)  
echo 3. Create Recovery Branch
echo 4. Show Checkpoint Details
echo 5. Cancel
echo.
set /p choice="Choose option (1-5): "

if "%choice%"=="1" goto soft_rollback
if "%choice%"=="2" goto hard_rollback  
if "%choice%"=="3" goto recovery_branch
if "%choice%"=="4" goto show_details
if "%choice%"=="5" goto cancel
goto invalid

:soft_rollback
echo.
echo Available checkpoints:
git tag
set /p checkpoint="Enter checkpoint name (e.g., checkpoint-1): "
echo.
echo Performing soft rollback to %checkpoint%...
git reset --soft %checkpoint%
echo.
echo ✅ Soft rollback completed!
echo Your changes are preserved but uncommitted.
goto end

:hard_rollback
echo.
echo ⚠️  WARNING: This will permanently delete all changes!
echo Available checkpoints:
git tag
set /p checkpoint="Enter checkpoint name (e.g., checkpoint-1): "
echo.
set /p confirm="Are you sure? Type 'YES' to confirm: "
if not "%confirm%"=="YES" goto cancel
echo.
echo Performing hard rollback to %checkpoint%...
git reset --hard %checkpoint%
echo.
echo ✅ Hard rollback completed!
echo All changes after %checkpoint% have been discarded.
goto end

:recovery_branch
echo.
echo Available checkpoints:
git tag
set /p checkpoint="Enter checkpoint name (e.g., checkpoint-1): "
set /p branchname="Enter new branch name (e.g., emergency-restore): "
echo.
echo Creating recovery branch '%branchname%' from %checkpoint%...
git checkout -b %branchname% %checkpoint%
echo.
echo ✅ Recovery branch created!
echo You are now on branch '%branchname%' at %checkpoint%
goto end

:show_details
echo.
echo Available checkpoints:
git tag
set /p checkpoint="Enter checkpoint name to view details: "
echo.
echo Checkpoint Details:
echo ==================
git show %checkpoint%
goto end

:invalid
echo.
echo ❌ Invalid choice. Please try again.
pause
goto start

:cancel
echo.
echo Operation cancelled.
goto end

:end
echo.
echo Current git status:
git status --short
echo.
pause
