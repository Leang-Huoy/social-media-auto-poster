@echo off
chcp 65001 > nul
title Social Media Auto Poster Pro - Online Cloud Hosting
echo ======================================================================
echo   🌐 កំពុងបើកដំណើរការ HOSTING អនឡាញ (CLOUDFLARE SECURE TUNNEL)...
echo ======================================================================
echo.
echo   [1/2] ពិនិត្យមើល Local Server (Port 5000)...
netstat -ano | findstr ":5000" > nul
if %errorlevel% neq 0 (
    echo   កំពុងបើកដំណើរការ Server...
    start /b python app.py 2>nul || start /b AutoPosterUI.exe
    timeout /t 3 /nobreak > nul
) else (
    echo   ✅ Server កំពុងដំណើរការរួចរាល់ហើយ!
)

echo.
echo   [2/2] កំពុងបង្កើតតំណភ្ជាប់ HTTPS សាធារណៈសម្រាប់ប្រើលើទូរស័ព្ទ...
echo   ----------------------------------------------------------------------
echo   👉 សូមរង់ចាំមើលតំណភ្ជាប់ 'https://....trycloudflare.com' ខាងក្រោម៖
echo   ----------------------------------------------------------------------
cloudflared.exe tunnel --url http://127.0.0.1:5000
pause

