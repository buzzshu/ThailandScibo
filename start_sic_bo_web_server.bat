@echo off
echo 正在啟動骰寶模擬器網頁服務...

echo 您的IP地址是:
ipconfig | findstr /i "IPv4"

echo.
echo 其他電腦可以通過訪問 http://[您的IP地址]:5000 使用骰寶模擬器
echo.
echo 按任意鍵繼續啟動網頁服務...
pause > nul

python sic_bo_web_simulator.py
pause
