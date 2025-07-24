@echo off
echo 正在啟動骰寶模擬器網頁工具...
echo.
echo 如果Python或Flask未安裝，將會顯示錯誤信息。
echo.

python sic_bo_web_simulator.py

echo.
if %errorlevel% neq 0 (
  echo 出現錯誤！請確保已安裝必要的Python套件:
  echo pip install flask matplotlib
  echo.
  pause
) else (
  echo 伺服器已關閉。
  echo.
  pause
)
