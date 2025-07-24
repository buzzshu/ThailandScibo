"""
骰寶網頁模擬器 - 計算玩家RTP (Return to Player)
"""

from sic_bo_simulator import SicBoSimulator
import random
import flask
from flask import Flask, render_template, request, jsonify
import threading
import numpy as np
import os

app = Flask(__name__, template_folder="templates")

# 模擬單個玩家的下注流程
def simulate_player(player_id, num_games, bet_amount, initial_capital, bet_type):
    simulator = SicBoSimulator()
    capital = initial_capital
    history = []
    total_bet = 0  # 總押注金額
    total_win = 0  # 總獲獎金額
    
    for game in range(num_games):
        if capital <= 0:  # 破產了
            break
            
        if capital < bet_amount:  # 資金不足以下注
            bet = capital
        else:
            bet = bet_amount
        
        total_bet += bet
            
        # 模擬一次骰子投擲
        result = simulator.simulate_single_roll()
        
        # 判斷是否贏了
        won = False
        if bet_type == "高 (HI)" and result["is_hi"]:
            won = True
            payout = simulator.bet_types["高 (HI)"]["payout"]
            winnings = bet * (1 + payout)
            total_win += winnings  # 記錄獲獎金額
        elif bet_type == "低 (LO)" and result["is_lo"]:
            won = True
            payout = simulator.bet_types["低 (LO)"]["payout"]
            winnings = bet * (1 + payout)
            total_win += winnings  # 記錄獲獎金額
        elif bet_type == "11 HI-LO" and result["is_hi_lo_11"]:
            won = True
            payout = simulator.bet_types["11 HI-LO"]["payout"]
            winnings = bet * (1 + payout)
            total_win += winnings  # 記錄獲獎金額
        else:
            winnings = 0
            
        # 更新資金
        capital = capital - bet + winnings
        
        # 記錄
        history.append({
            "game": game + 1,
            "dice": result["dice"],
            "total": result["total"],
            "bet_amount": bet,
            "won": won,
            "winnings": winnings,
            "capital": capital
        })
    
    # 計算正確的 RTP（總獲獎金額/總押注金額）
    player_rtp = total_win / total_bet if total_bet > 0 else 0
    
    return {
        "player_id": player_id,
        "initial_capital": initial_capital,
        "final_capital": capital,
        "games_played": len(history),
        "history": history,
        "total_bet": total_bet,
        "total_win": total_win,
        "rtp": player_rtp
    }

# 模擬多個玩家的下注流程
def simulate_multiple_players(num_players, num_games, bet_amount, initial_capital, bet_type):
    results = []
    
    for i in range(num_players):
        player_result = simulate_player(i+1, num_games, bet_amount, initial_capital, bet_type)
        results.append(player_result)
    
    # 計算整體RTP（所有玩家總獲獎金額/總押注金額）
    total_bet = sum(r["total_bet"] for r in results)
    total_win = sum(r["total_win"] for r in results)
    overall_rtp = total_win / total_bet if total_bet > 0 else 0
    
    return {
        "results": results,
        "overall_rtp": overall_rtp,
        "bet_type": bet_type,
        "num_players": num_players,
        "num_games": num_games,
        "bet_amount": bet_amount,
        "initial_capital": initial_capital
    }

# 創建 templates 資料夾如果不存在
os.makedirs("templates", exist_ok=True)

# 創建 HTML 模板
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>骰寶模擬器 - RTP計算</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .results {
            margin-top: 20px;
        }
        .loading {
            text-align: center;
            margin-top: 20px;
            display: none;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        }
        .chart-container {
            width: 100%;
            height: 400px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>骰寶模擬器 - RTP計算工具</h1>
        
        <div class="form-group">
            <label for="num_players">玩家數量:</label>
            <input type="number" id="num_players" value="10" min="1" max="1000">
        </div>
        
        <div class="form-group">
            <label for="num_games">每位玩家遊戲局數:</label>
            <input type="number" id="num_games" value="100" min="1" max="10000">
        </div>
        
        <div class="form-group">
            <label for="bet_amount">每局押注金額:</label>
            <input type="number" id="bet_amount" value="100" min="1">
        </div>
        
        <div class="form-group">
            <label for="initial_capital">起始資金:</label>
            <input type="number" id="initial_capital" value="10000" min="1">
        </div>
        
        <div class="form-group">
            <label for="bet_type">押注選項:</label>
            <select id="bet_type">
                <option value="高 (HI)">高 (HI)</option>
                <option value="低 (LO)">低 (LO)</option>
                <option value="11 HI-LO">11 HI-LO</option>
            </select>
        </div>
        
        <button onclick="runSimulation()">運行模擬</button>
        
        <div class="loading" id="loading">
            <p>模擬運行中，請稍候...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <!-- 結果將顯示在這裡 -->
        </div>
        
        <!-- 圖表功能已關閉
        <h2>資金變化圖表</h2>
        <div class="chart-container" id="capitalChart"></div>
        
        <h2>累計RTP與勝率圖表</h2>
        <div class="chart-container" id="rtpChart"></div>
        -->
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        let capitalChart = null;
        let rtpChart = null;
        
        function runSimulation() {
            const numPlayers = document.getElementById('num_players').value;
            const numGames = document.getElementById('num_games').value;
            const betAmount = document.getElementById('bet_amount').value;
            const initialCapital = document.getElementById('initial_capital').value;
            const betType = document.getElementById('bet_type').value;
            
            // 顯示載入中
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
            document.getElementById('error').innerHTML = '';
            
            // 圖表功能已關閉
            /*
            // 銷毀舊的圖表
            if (capitalChart) {
                capitalChart.destroy();
                capitalChart = null;
            }
            if (rtpChart) {
                rtpChart.destroy();
                rtpChart = null;
            }
            */
            
            // 發送API請求
            fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num_players: parseInt(numPlayers),
                    num_games: parseInt(numGames),
                    bet_amount: parseInt(betAmount),
                    initial_capital: parseInt(initialCapital),
                    bet_type: betType
                })
            })
            .then(response => response.json())
            .then(data => {
                // 隱藏載入中
                document.getElementById('loading').style.display = 'none';
                
                // 顯示結果
                displayResults(data);
            })
            .catch(error => {
                // 隱藏載入中
                document.getElementById('loading').style.display = 'none';
                
                // 顯示錯誤
                document.getElementById('error').innerHTML = '發生錯誤: ' + error.message;
                console.error('Error:', error);
            });
        }
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            
            // 整體RTP卡片
            const overallRtpCard = document.createElement('div');
            overallRtpCard.className = 'card';
            overallRtpCard.innerHTML = `
                <h2>整體模擬結果</h2>
                <p><strong>押注選項:</strong> ${data.bet_type}</p>
                <p><strong>玩家數量:</strong> ${data.num_players}</p>
                <p><strong>每位玩家遊戲局數:</strong> ${data.num_games}</p>
                <p><strong>每局押注金額:</strong> ${data.bet_amount}</p>
                <p><strong>起始資金:</strong> ${data.initial_capital}</p>
                <p><strong>整體RTP (Return to Player):</strong> ${(data.overall_rtp * 100).toFixed(2)}%</p>
            `;
            resultsDiv.appendChild(overallRtpCard);
            
            // 創建綜合圖表數據
            const chartLabels = Array.from({length: data.num_games}, (_, i) => i + 1);
            
            // 計算每局的平均資金和RTP
            const avgCapitalByGame = Array(data.num_games).fill(0);
            const rtpByGame = Array(data.num_games).fill(0);
            const winRateByGame = Array(data.num_games).fill(0);
            let activePlayers = Array(data.num_games).fill(0);
            
            // 用於累積計算每局的總下注和總贏金
            const totalBetByGame = Array(data.num_games).fill(0);
            const totalWinByGame = Array(data.num_games).fill(0);
            
            // 對每個玩家的每局進行統計
            data.results.forEach(player => {
                player.history.forEach((game, index) => {
                    if (index < data.num_games) {
                        avgCapitalByGame[index] += game.capital;
                        totalBetByGame[index] += game.bet_amount;
                        totalWinByGame[index] += game.won ? game.winnings : 0;
                        winRateByGame[index] += game.won ? 1 : 0;
                        activePlayers[index] += 1;
                    }
                });
            });
            
            // 計算累積的RTP
            for (let i = 0; i < data.num_games; i++) {
                let cumTotalBet = 0;
                let cumTotalWin = 0;
                
                for (let j = 0; j <= i; j++) {
                    cumTotalBet += totalBetByGame[j];
                    cumTotalWin += totalWinByGame[j];
                }
                
                rtpByGame[i] = cumTotalBet > 0 ? cumTotalWin / cumTotalBet : 0;
            }
            
            // 計算平均值
            for (let i = 0; i < data.num_games; i++) {
                if (activePlayers[i] > 0) {
                    avgCapitalByGame[i] /= activePlayers[i];
                    rtpByGame[i] /= activePlayers[i];
                    winRateByGame[i] = (winRateByGame[i] / activePlayers[i]) * 100;
                }
            }
            
            // 圖表功能已關閉
            /*
            // 創建資金變化圖表
            const capitalCtx = document.createElement('canvas');
            document.getElementById('capitalChart').innerHTML = '';
            document.getElementById('capitalChart').appendChild(capitalCtx);
            
            capitalChart = new Chart(capitalCtx, {
                type: 'line',
                data: {
                    labels: chartLabels,
                    datasets: [{
                        label: '平均資金',
                        data: avgCapitalByGame,
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: '平均資金變化'
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: '局數'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: '平均資金'
                            }
                        }
                    }
                }
            });
            
            // 創建累計RTP和勝率圖表
            const rtpCtx = document.createElement('canvas');
            document.getElementById('rtpChart').innerHTML = '';
            document.getElementById('rtpChart').appendChild(rtpCtx);
            
            rtpChart = new Chart(rtpCtx, {
                type: 'line',
                data: {
                    labels: chartLabels,
                    datasets: [
                        {
                            label: '累計RTP (%)',
                            data: rtpByGame.map(v => v * 100),
                            borderColor: 'rgb(255, 99, 132)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            fill: false,
                            yAxisID: 'y'
                        },
                        {
                            label: '勝率 (%)',
                            data: winRateByGame,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            fill: false,
                            yAxisID: 'y'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: '累計RTP與勝率'
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: '局數'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: '百分比 (%)'
                            },
                            min: 0,
                            max: 120
                        }
                    }
                }
            });
            */
        }
        
        function getRandomColor(index) {
            const colors = [
                'rgb(255, 99, 132)', // 紅色
                'rgb(54, 162, 235)', // 藍色
                'rgb(255, 206, 86)', // 黃色
                'rgb(75, 192, 192)', // 青色
                'rgb(153, 102, 255)', // 紫色
                'rgb(255, 159, 64)', // 橙色
                'rgb(199, 199, 199)' // 灰色
            ];
            
            return colors[index % colors.length];
        }
    </script>
</body>
</html>
    """)

# Flask 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    
    num_players = int(data.get('num_players', 10))
    num_games = int(data.get('num_games', 100))
    bet_amount = int(data.get('bet_amount', 100))
    initial_capital = int(data.get('initial_capital', 10000))
    bet_type = data.get('bet_type', '高 (HI)')
    
    # 限制最大玩家數和局數
    num_players = min(num_players, 1000)
    num_games = min(num_games, 10000)
    
    # 運行模擬
    results = simulate_multiple_players(num_players, num_games, bet_amount, initial_capital, bet_type)
    
    return jsonify(results)

if __name__ == '__main__':
    # 檢查Flask是否已安裝
    try:
        import flask
    except ImportError:
        print("Flask 未安裝。請運行 'pip install flask' 安裝Flask。")
        exit(1)
    
    # 根據環境變量決定是在本地還是在 Render 上運行
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print(f"啟動網頁模擬器，請在瀏覽器中訪問 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
