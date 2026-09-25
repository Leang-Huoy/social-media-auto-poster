@echo off
chcp 65001 > nul
title Upload to GitHub - Leang-Huoy
echo ======================================================================
echo   🚀 UPLOAD / PUSH គម្រោង AUTO POST ទៅកាន់ GITHUB
echo ======================================================================
echo.
echo   Repository: https://github.com/Leang-Huoy/social-media-auto-poster.git
echo   User: Leang-Huoy (loanghuoy12@gmail.com)
echo.
echo   ----------------------------------------------------------------------
echo   👉 កំពុងធ្វើការ Push កូដឡើងទៅកាន់ GitHub...
echo   (ប្រសិនបើមានផ្ទាំងតូច ឬ Browser លោតចេញមក សូមចុច "Sign in with your browser")
echo   ----------------------------------------------------------------------
echo.

git remote remove origin 2>nul
git remote add origin https://github.com/Leang-Huoy/social-media-auto-poster.git
git branch -M main

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo   🎉 ជោគជ័យ ១០០%! កូដត្រូវបានបង្ហោះឡើងទៅកាន់ GitHub រួចរាល់ហើយ!
    echo   🌐 ពិនិត្យមើលកូដ៖ https://github.com/Leang-Huoy/social-media-auto-poster
    echo ======================================================================
) else (
    echo.
    echo   ----------------------------------------------------------------------
    echo   💡 បើមិនទាន់ជោគជ័យ អ្នកអាចប្រើ GitHub Personal Access Token (PAT)៖
    echo   ----------------------------------------------------------------------
    echo.
    set /p GH_TOKEN="សូម Paste GitHub Token (បើមាន) ឬចុច Enter ដើម្បីចាកចេញ: "
    if not "%GH_TOKEN%"=="" (
        git remote set-url origin https://%GH_TOKEN%@github.com/Leang-Huoy/social-media-auto-poster.git
        git push -u origin main
        if %errorlevel% equ 0 (
            echo.
            echo   🎉 ជោគជ័យ! បាន Push តាមរយៈ Token រួចរាល់!
        )
    )
)

echo.
pause
