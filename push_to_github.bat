@echo off
chcp 65001 > nul
title Upload to GitHub - Leang-Huoy
echo ======================================================================
echo   🚀 UPLOAD / PUSH គម្រោង AUTO POST ទៅកាន់ GITHUB (Leang-Huoy)
echo ======================================================================
echo.
echo   Git User: Leang-Huoy (loanghuoy12@gmail.com)
echo.
echo   ----------------------------------------------------------------------
echo   👉 ប្រសិនបើអ្នកបានបង្កើត Repo នៅលើ GitHub រួចហើយ 
echo      សូមចម្លង Link (ឧទាហរណ៍: https://github.com/Leang-Huoy/auto-posts.git)
echo   ----------------------------------------------------------------------
echo.
set /p REPO_URL="👉 សូម Paste Link GitHub Repository នៅទីនេះ: "

if "%REPO_URL%"=="" (
    echo.
    echo   ❌ អ្នកមិនបានបញ្ចូល Link ទេ។ សូមសាកល្បងម្ដងទៀត!
    goto end
)

echo.
echo   [1/3] កំពុងកំណត់ Remote Origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo   [2/3] កំណត់ Default Branch ទៅ main...
git branch -M main

echo   [3/3] កំពុង Push កូដឡើងទៅ GitHub...
echo   (ចំណាំ៖ ប្រសិនបើមានផ្ទាំង Browser ឬ Terminal សួរ Login សូមចុច Sign In)
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo   🎉 ជោគជ័យ! កូដរបស់អ្នកត្រូវបានបង្ហោះឡើងទៅកាន់ GitHub រួចរាល់ហើយ!
    echo ======================================================================
) else (
    echo.
    echo   ⚠️ ការ Push មិនទាន់ជោគជ័យ។ សូមពិនិត្យមើលសិទ្ធិ ឬលេខសម្ងាត់/Token ឡើងវិញ។
)

:end
echo.
pause
