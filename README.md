# 骰寶 (Sic Bo) 模擬器

這個專案模擬骰寶遊戲，計算各種押注方式的獲勝機率和期望值。現在包含了一個網頁版模擬器，可以通過瀏覽器訪問並計算 RTP (Return to Player)。

## 骰寶規則說明

骰寶是一種賭博遊戲，使用三個骰子，玩家押注骰子點數的各種組合。本模擬器實現以下押注類型：

1. **高 (HI)**: 點數總和為 12-18，賠率 1:1
2. **低 (LO)**: 點數總和為 3-10，賠率 0.95:1
3. **11 HI-LO**: 點數總和為 11，賠率 5:1
4. **點數盤/三軍 (Three Forces)**:
   - 單骰 (出現1個相同數字)，賠率 1:1
   - 雙骰 (出現2個相同數字)，賠率 2:1
   - 三骰 (出現3個相同數字)，賠率 3:1
   - 隨機賠率模式 (固定2X): 2:1, 4:1, 6:1
   - 隨機賠率模式 (高倍): 1/2/3, 2/4/6, 3/6/9
5. **牌九式/兩個數字組合 (Two Dice Combination)**:
   - 出現兩個指定點數組合 (如1,2或4,5等)，賠率 5:1
   - 隨機賠率模式 (固定2X): 10:1
   - 隨機賠率模式 (高倍): 5/10/15/25/40
6. **三骰/三顆骰子組合 (1,2,3) 或 (4,5,6)**:
   - 出現兩個點數，賠率 1:1
   - 三個點數全中，賠率 5:1
   - 隨機賠率模式 (固定2X): 2:1, 10:1
   - 隨機賠率模式 (高倍): 1/2/3/5/8, 5/10/15/25/40
7. **特殊 X_LO 和 X_HI 組合**:
   - **X_LO**: 點數總和小於10點，且包含點數X
     - 1_LO: 賠率 1.8:1 (隨機高倍: 1.8/3/5/10/15)
     - 2_LO: 賠率 2:1 (隨機高倍: 2/4/6/10/15)
     - 3_LO: 賠率 3:1 (隨機高倍: 3/6/9/15/24)
     - 4_LO: 賠率 4:1 (隨機高倍: 4/8/12/20/32)
     - 5_LO: 賠率 5:1 (隨機高倍: 5/10/15/25/40)
     - 6_LO: 賠率 7:1 (隨機高倍: 7/14/21/35/56)
   - **X_HI**: 點數總和大於12點，且包含點數X
     - 3_HI: 賠率 4:1 (隨機高倍: 4/8/12/20/32)
     - 4_HI: 賠率 4:1 (隨機高倍: 4/8/12/20/32)
     - 5_HI: 賠率 3:1 (隨機高倍: 3/6/9/15/24)
     - 6_HI: 賠率 2:1 (隨機高倍: 2/4/6/10/15)

## 專案檔案

- `sic_bo_simulator.py`: 骰寶模擬器類別，包含各種計算方法
- `run_simulation.py`: 運行模擬的主程式
- `sic_bo_web_simulator.py`: 網頁版骰寶模擬器，使用 Flask 框架

## 使用方法

### 本地命令行模式

1. 確保已安裝必要的套件：
   ```
   pip install matplotlib numpy
   ```

2. 運行模擬程式：
   ```
   python run_simulation.py
   ```

### 本地網頁模式

1. 確保已安裝必要的套件：
   ```
   pip install flask numpy
   ```

2. 運行網頁模擬器：
   ```
   python sic_bo_web_simulator.py
   ```

3. 在瀏覽器中訪問：http://localhost:5000

### 在 Render 上部署網頁模式

1. 註冊或登入 [Render](https://render.com/)
2. 點擊 "New +" 按鈕，選擇 "Web Service"
3. 連接到您的 GitHub 賬號，選擇包含此模擬器代碼的倉庫
4. 配置以下選項：
   - **名稱**：可以自行設定，例如 "sic-bo-simulator"
   - **環境**：Python 3
   - **構建命令**：`sh render_build.sh`
   - **啟動命令**：`gunicorn sic_bo_web_simulator:app`
5. 點擊 "Create Web Service" 按鈕

部署完成後，您可以通過 Render 生成的網址訪問骰寶模擬器。

3. 程式會顯示：
   - 單次投擲結果
   - 基於多次投擲的統計結果
   - 各種押注的期望值
   - 生成視覺化圖表 (保存為 `sic_bo_simulation_results.png`)

## 自定義模擬

您可以修改 `run_simulation.py` 中的參數來自定義模擬：
- 增加模擬次數以獲得更準確的結果
- 修改投注金額來計算不同的期望值

## 視覺化結果說明

模擬結果會生成以下視覺化圖表：

### sic_bo_simulation_results.png：
1. **總點數分佈**: 顯示各總點數出現的次數
2. **基本投注結果比例**: 顯示高(HI)、低(LO)、11 HI-LO和三同點的出現比例
3. **各點數出現頻率**: 顯示各點數出現1次、2次或3次的比例
4. **基本投注期望值**: 顯示高(HI)、低(LO)和11 HI-LO的投注期望值
5. **X_LO投注期望值**: 顯示各X_LO投注的期望值
6. **X_HI投注期望值**: 顯示各X_HI投注的期望值

### sic_bo_dice_combo_results.png：
1. **點數盤投注期望值**: 顯示各點數出現1次、2次或3次的投注期望值
2. **三骰組合投注期望值**: 顯示低組合(1,2,3)和高組合(4,5,6)的投注期望值
