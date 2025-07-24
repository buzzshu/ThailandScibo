# Render 部署指南

本文件提供將骰寶模擬器部署到 Render 雲平台的詳細步驟。

## 前置準備

確保您已經將以下文件添加到您的代碼庫中：

1. `requirements.txt` - 列出所有依賴項
2. `render_build.sh` - 構建腳本
3. `Procfile` - 告訴 Render 如何啟動應用
4. `.gitignore` - 排除不必要的文件

## 部署步驟

1. **創建 Render 帳戶**：
   - 訪問 [https://render.com](https://render.com) 並註冊一個帳戶
   - 登錄您的帳戶

2. **連接您的 GitHub 倉庫**：
   - 點擊右上角的 "New +"
   - 選擇 "Web Service"
   - 點擊 "Connect" 按鈕連接到您的 GitHub 帳戶
   - 找到並選擇包含骰寶模擬器的倉庫
   - 如果您的倉庫沒有顯示，您可能需要在 GitHub 上授予 Render 訪問權限

3. **配置 Web 服務**：
   - **Name**：為您的服務命名，例如 `sic-bo-simulator`
   - **環境**：選擇 `Python 3`
   - **區域**：選擇離您的目標用戶最近的區域
   - **分支**：選擇您希望部署的 Git 分支，通常是 `main` 或 `master`
   - **構建命令**：輸入 `sh render_build.sh`
   - **啟動命令**：輸入 `gunicorn sic_bo_web_simulator:app`

4. **高級設置**（可選）：
   - 您可以添加環境變量 `RENDER=true` 來標記生產環境
   - 對於免費帳戶，保留默認的自動休眠設置

5. **點擊 "Create Web Service"**：
   - Render 將開始構建和部署您的應用
   - 這可能需要幾分鐘時間

6. **訪問您的應用**：
   - 部署成功後，Render 會提供一個 URL（通常是 `https://your-service-name.onrender.com`）
   - 點擊此 URL 或在瀏覽器中打開它即可使用您的骰寶模擬器

## 常見問題解決

如果您遇到部署問題，這裡有一些常見解決方法：

1. **構建失敗**：
   - 檢查日誌，找出具體錯誤
   - 確認 `requirements.txt` 中的依賴兼容
   - 嘗試在本地安裝所有依賴以驗證它們是否兼容

2. **應用無法啟動**：
   - 檢查 `Procfile` 中的命令是否正確
   - 確認應用主文件名稱是否與 `Procfile` 中的一致
   - 檢查日誌中的錯誤信息

3. **應用運行但有錯誤**：
   - 在 Render 儀表板中查看日誌
   - 檢查是否所有必要的文件都已上傳到 GitHub
   - 確認所有路徑使用是否正確（本地文件路徑 vs. 服務器路徑）

## 後續維護

1. **更新應用**：
   - 推送更改到 GitHub 上的同一分支
   - Render 將自動重新部署您的應用

2. **監控**：
   - 在 Render 儀表板上監控應用性能和日誌
   - 檢查錯誤和警告信息

3. **擴展**（如需要）：
   - 如果您需要更多資源，可以升級到 Render 的付費計劃
