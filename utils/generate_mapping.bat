@echo off
REM ========================================
REM اسکریپت تولید خودکار mapping.txt
REM برای استفاده در ویندوز
REM ========================================

echo.
echo ========================================
echo    ابزار تولید خودکار Mapping File
echo ========================================
echo.

REM چک کردن وجود پایتون
python --version >nul 2>&1
if errorlevel 1 (
    echo [خطا] پایتون نصب نیست!
    echo لطفا پایتون را از python.org نصب کنید
    pause
    exit /b 1
)

REM اجرای اسکریپت
echo در حال تولید فایل mapping...
echo.

python "%~dp0mapping_generator.py" %*

if errorlevel 1 (
    echo.
    echo [خطا] مشکلی در اجرا پیش آمد!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   عملیات با موفقیت انجام شد!
echo ========================================
echo.
echo فایل mapping.txt آماده ارسال به بات است.
echo.
pause
