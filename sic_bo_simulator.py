"""
骰寶 (Sic Bo) 模擬器

這個程式模擬骰寶遊戲，一次投擲三個骰子，並計算各種押注類型的獲勝機率和期望值。
"""

import random
from collections import defaultdict, Counter

class SicBoSimulator:
    def __init__(self):
        # 定義各種押注類型和賠率
        self.bet_types = {
            # 基本高低注區
            "高 (HI)": {"description": "點數總和為 12-18", "payout": 1},
            "低 (LO)": {"description": "點數總和為 3-10", "payout": 0.95},
            "11 HI-LO": {"description": "點數總和為 11", "payout": 5},
            
            # 點數盤/三軍/three forces
            "單骰點數": {"description": "指定骰子點數出現1,2或3次", "payout": {
                1: 1,  # 出現一次
                2: 2,  # 出現兩次
                3: 3   # 出現三次 (即三同)
            }},
            "單骰點數_隨機賠率": {"description": "指定骰子點數出現1,2或3次 (隨機賠率)", "payout": {
                1: 2,  # 出現一次 (固定2X)
                2: 4,  # 出現兩次 (固定2X)
                3: 6   # 出現三次 (固定2X)
            }},
            
            # 牌九式/兩個數字組合
            "雙骰組合": {"description": "指定的兩個骰子點數", "payout": 5},
            "雙骰組合_隨機賠率": {"description": "指定的兩個骰子點數 (隨機賠率)", "payout": 10},
            
            # 三骰/三顆骰子組合 (1,2,3) 或 (4,5,6)
            "三骰組合_出現兩個": {"description": "三顆骰子組合中出現兩個點數", "payout": 1},
            "三骰組合_出現兩個_隨機賠率": {"description": "三顆骰子組合中出現兩個點數 (隨機賠率)", "payout": 2},
            "三骰組合_全中": {"description": "三顆骰子組合中，三個點數全中", "payout": 5},
            "三骰組合_全中_隨機賠率": {"description": "三顆骰子組合中，三個點數全中 (隨機賠率)", "payout": 10},
            
            # 特定點數與高低組合
            "1_LO": {"description": "點數總和小於等於10點，且包含點數1", "payout": 1.8},
            "2_LO": {"description": "點數總和小於等於10點，且包含點數2", "payout": 2},
            "3_LO": {"description": "點數總和小於等於10點，且包含點數3", "payout": 3},
            "4_LO": {"description": "點數總和小於等於10點，且包含點數4", "payout": 4},
            "5_LO": {"description": "點數總和小於等於10點，且包含點數5", "payout": 5},
            "6_LO": {"description": "點數總和小於等於10點，且包含點數6", "payout": 7},
            
            "3_HI": {"description": "點數總和大於等於12點，且包含點數3", "payout": 4},
            "4_HI": {"description": "點數總和大於等於12點，且包含點數4", "payout": 4},
            "5_HI": {"description": "點數總和大於等於12點，且包含點數5", "payout": 3},
            "6_HI": {"description": "點數總和大於等於12點，且包含點數6", "payout": 2},
            
            # 隨機賠率 (高倍)
            "1_LO_隨機高倍": {"description": "點數總和小於等於10點，且包含點數1 (隨機高倍)", "payout": [1.8, 3, 5, 10, 15]},
            "2_LO_隨機高倍": {"description": "點數總和小於等於10點，且包含點數2 (隨機高倍)", "payout": [2, 4, 6, 10, 15]},
            "3_LO_隨機高倍": {"description": "點數總和小於等於10點，且包含點數3 (隨機高倍)", "payout": [3, 6, 9, 15, 24]},
            "4_LO_隨機高倍": {"description": "點數總和小於等於10點，且包含點數4 (隨機高倍)", "payout": [4, 8, 12, 20, 32]},
            "5_LO_隨機高倍": {"description": "點數總和小於等於10點，且包含點數5 (隨機高倍)", "payout": [5, 10, 15, 25, 40]},
            "6_LO_隨機高倍": {"description": "點數總和小於等於10點，且包含點數6 (隨機高倍)", "payout": [7, 14, 21, 35, 56]},
            
            "3_HI_隨機高倍": {"description": "點數總和大於等於12點，且包含點數3 (隨機高倍)", "payout": [4, 8, 12, 20, 32]},
            "4_HI_隨機高倍": {"description": "點數總和大於等於12點，且包含點數4 (隨機高倍)", "payout": [4, 8, 12, 20, 32]},
            "5_HI_隨機高倍": {"description": "點數總和大於等於12點，且包含點數5 (隨機高倍)", "payout": [3, 6, 9, 15, 24]},
            "6_HI_隨機高倍": {"description": "點數總和大於等於12點，且包含點數6 (隨機高倍)", "payout": [2, 4, 6, 10, 15]},
            
            # 單骰點數隨機高倍
            "單骰點數_隨機高倍": {"description": "指定骰子點數出現1,2或3次 (隨機高倍)", "payout": {
                1: [1, 2, 3],      # 出現一次
                2: [2, 4, 6],      # 出現兩次
                3: [3, 6, 9]       # 出現三次
            }},
            
            # 雙骰組合隨機高倍
            "雙骰組合_隨機高倍": {"description": "指定的兩個骰子點數 (隨機高倍)", "payout": [5, 10, 15, 25, 40]},
            
            # 三骰組合隨機高倍
            "三骰組合_出現兩個_隨機高倍": {"description": "三顆骰子組合中出現兩個點數 (隨機高倍)", "payout": [1, 2, 3, 5, 8]},
            "三骰組合_全中_隨機高倍": {"description": "三顆骰子組合中，三個點數全中 (隨機高倍)", "payout": [5, 10, 15, 25, 40]},
        }
        self.results_history = []

    def roll_dice(self):
        """模擬投擲三個骰子"""
        return [random.randint(1, 6) for _ in range(3)]

    def get_total_points(self, dice):
        """計算骰子總點數"""
        return sum(dice)
    
    def is_triple(self, dice):
        """檢查是否為三同點"""
        return len(set(dice)) == 1
    
    def is_hi(self, dice):
        """檢查是否為'高 (HI)'：總點數 12-18"""
        total = self.get_total_points(dice)
        return 12 <= total <= 18
    
    def is_lo(self, dice):
        """檢查是否為'低 (LO)'：總點數 3-10"""
        total = self.get_total_points(dice)
        return 3 <= total <= 10
    
    def is_hi_lo_11(self, dice):
        """檢查是否為'11 HI-LO'：總點數等於11"""
        return self.get_total_points(dice) == 11
    
    def count_specific_number(self, dice, number):
        """計算特定點數出現的次數"""
        return dice.count(number)
    
    def check_pair(self, dice, num1, num2):
        """檢查是否有特定的一對骰子點數"""
        counter = Counter(dice)
        return counter[num1] >= 1 and counter[num2] >= 1
        
    def check_x_lo(self, dice, x):
        """檢查是否為'X_LO'：總點數小於等於10點且包含點數X"""
        total = self.get_total_points(dice)
        return total <= 10 and x in dice
    
    def check_x_hi(self, dice, x):
        """檢查是否為'X_HI'：總點數大於等於12點且包含點數X"""
        total = self.get_total_points(dice)
        return total >= 12 and x in dice
        
    def check_three_dice_combo(self, dice, combo_type):
        """檢查三骰組合
        combo_type: 'low' 代表 (1,2,3), 'high' 代表 (4,5,6)
        """
        if combo_type == 'low':
            target_set = {1, 2, 3}
        else:  # high
            target_set = {4, 5, 6}
        
        dice_set = set(dice)
        common_elements = dice_set.intersection(target_set)
        
        # 返回匹配的數量: 0, 2, 或 3
        if len(common_elements) == len(target_set):
            return "全中"
        elif len(common_elements) >= 2:
            return "出現兩個"
        else:
            return "不符合"
    
    def simulate_single_roll(self):
        """模擬一次投擲並返回結果"""
        dice = self.roll_dice()
        total = self.get_total_points(dice)
        is_triple = self.is_triple(dice)
        
        # 計算各點數出現次數
        counts = {i: dice.count(i) for i in range(1, 7)}
        
        # 計算各種三骰組合結果
        low_combo_result = self.check_three_dice_combo(dice, 'low')
        high_combo_result = self.check_three_dice_combo(dice, 'high')
        
        # 計算各種點數與高低組合結果
        x_lo_results = {x: self.check_x_lo(dice, x) for x in range(1, 7)}
        x_hi_results = {x: self.check_x_hi(dice, x) for x in range(1, 7)}
        
        result = {
            "dice": dice,
            "total": total,
            "is_triple": is_triple,
            "is_hi": self.is_hi(dice),
            "is_lo": self.is_lo(dice),
            "is_hi_lo_11": self.is_hi_lo_11(dice),
            "counts": counts,
            "low_combo": low_combo_result,
            "high_combo": high_combo_result,
            "x_lo": x_lo_results,
            "x_hi": x_hi_results
        }
        
        self.results_history.append(result)
        return result
    
    def simulate_multiple_rolls(self, num_simulations=1000):
        """模擬多次投擲"""
        for _ in range(num_simulations):
            self.simulate_single_roll()
        return self.results_history
    
    def calculate_statistics(self):
        """計算統計資訊"""
        if not self.results_history:
            return "沒有模擬數據"
        
        total_rolls = len(self.results_history)
        stats = {
            "總模擬次數": total_rolls,
            "高 (HI)": sum(1 for r in self.results_history if r["is_hi"]) / total_rolls,
            "低 (LO)": sum(1 for r in self.results_history if r["is_lo"]) / total_rolls,
            "11 HI-LO": sum(1 for r in self.results_history if r["is_hi_lo_11"]) / total_rolls,
            "三同點": sum(1 for r in self.results_history if r["is_triple"]) / total_rolls,
            "點數總和": defaultdict(int),
            "點數出現次數": {i: defaultdict(int) for i in range(1, 7)},
            "三骰組合_低": {
                "出現兩個": sum(1 for r in self.results_history if r["low_combo"] == "出現兩個") / total_rolls,
                "全中": sum(1 for r in self.results_history if r["low_combo"] == "全中") / total_rolls
            },
            "三骰組合_高": {
                "出現兩個": sum(1 for r in self.results_history if r["high_combo"] == "出現兩個") / total_rolls,
                "全中": sum(1 for r in self.results_history if r["high_combo"] == "全中") / total_rolls
            },
            "X_LO": {x: sum(1 for r in self.results_history if r["x_lo"][x]) / total_rolls for x in range(1, 7)},
            "X_HI": {x: sum(1 for r in self.results_history if r["x_hi"][x]) / total_rolls for x in range(1, 7)}
        }
        
        # 計算總點數出現的頻率
        for result in self.results_history:
            stats["點數總和"][result["total"]] += 1
            
            # 計算各點數出現1,2,3次的頻率
            for num in range(1, 7):
                count = result["counts"][num]
                if count > 0:
                    stats["點數出現次數"][num][count] += 1
        
        # 轉換為百分比
        for total in stats["點數總和"]:
            stats["點數總和"][total] /= total_rolls
            
        for num in stats["點數出現次數"]:
            for count in stats["點數出現次數"][num]:
                stats["點數出現次數"][num][count] /= total_rolls
                
        # 計算雙骰組合出現的機率
        stats["雙骰組合"] = {}
        for i in range(1, 7):
            for j in range(i, 7):
                if i != j:  # 不同點數的組合
                    key = f"{i},{j}"
                    count = sum(1 for r in self.results_history if 
                                self.check_pair(r["dice"], i, j))
                    stats["雙骰組合"][key] = count / total_rolls
                    
        return stats
    
    def calculate_expected_value(self, bet_amount=100):
        """計算各種投注的期望值
        
        獲獎期望值算法:
        EV = Win Probability * (1 + Payout)
        以模擬的角度來說:
        EV = All Win / (Bet * 下注次數)
        """
        stats = self.calculate_statistics()
        if isinstance(stats, str):
            return "沒有模擬數據，無法計算期望值"
            
        ev = {}
        
        # 高低及11 HI-LO
        ev["高 (HI)"] = stats["高 (HI)"] * (1 + self.bet_types["高 (HI)"]["payout"])
        ev["低 (LO)"] = stats["低 (LO)"] * (1 + self.bet_types["低 (LO)"]["payout"])
        ev["11 HI-LO"] = stats["11 HI-LO"] * (1 + self.bet_types["11 HI-LO"]["payout"])
        
        # 單骰點數 (點數盤/三軍)
        ev["單骰點數"] = {}
        for num in range(1, 7):
            ev["單骰點數"][num] = {}
            for count in range(1, 4):
                win_prob = stats["點數出現次數"][num].get(count, 0)
                payout = self.bet_types["單骰點數"]["payout"].get(count, 0)
                ev["單骰點數"][num][count] = win_prob * (1 + payout)
        
        # 單骰點數 (隨機賠率固定2X)
        ev["單骰點數_隨機賠率"] = {}
        for num in range(1, 7):
            ev["單骰點數_隨機賠率"][num] = {}
            for count in range(1, 4):
                win_prob = stats["點數出現次數"][num].get(count, 0)
                payout = self.bet_types["單骰點數_隨機賠率"]["payout"].get(count, 0)
                ev["單骰點數_隨機賠率"][num][count] = win_prob * (1 + payout)
        
        # 雙骰組合 (牌九式)
        ev["雙骰組合"] = {}
        for combo, win_prob in stats["雙骰組合"].items():
            payout = self.bet_types["雙骰組合"]["payout"]
            ev["雙骰組合"][combo] = win_prob * (1 + payout)
            
        # 雙骰組合 (隨機賠率)
        ev["雙骰組合_隨機賠率"] = {}
        for combo, win_prob in stats["雙骰組合"].items():
            payout = self.bet_types["雙骰組合_隨機賠率"]["payout"]
            ev["雙骰組合_隨機賠率"][combo] = win_prob * (1 + payout)
        
        # 三骰組合
        ev["三骰組合_低"] = {}
        ev["三骰組合_高"] = {}
        
        # 低組合(1,2,3)
        ev["三骰組合_低"]["出現兩個"] = stats["三骰組合_低"]["出現兩個"] * (1 + self.bet_types["三骰組合_出現兩個"]["payout"])
        ev["三骰組合_低"]["全中"] = stats["三骰組合_低"]["全中"] * (1 + self.bet_types["三骰組合_全中"]["payout"])
        
        # 高組合(4,5,6)
        ev["三骰組合_高"]["出現兩個"] = stats["三骰組合_高"]["出現兩個"] * (1 + self.bet_types["三骰組合_出現兩個"]["payout"])
        ev["三骰組合_高"]["全中"] = stats["三骰組合_高"]["全中"] * (1 + self.bet_types["三骰組合_全中"]["payout"])
        
        # X_LO和X_HI投注
        ev["X_LO"] = {}
        for x in range(1, 7):
            win_prob = stats["X_LO"][x]
            if f"{x}_LO" in self.bet_types:
                payout = self.bet_types[f"{x}_LO"]["payout"]
                ev["X_LO"][x] = win_prob * (1 + payout)
            
        ev["X_HI"] = {}
        for x in range(3, 7):  # 只有3, 4, 5, 6有HI投注
            win_prob = stats["X_HI"][x]
            if f"{x}_HI" in self.bet_types:
                payout = self.bet_types[f"{x}_HI"]["payout"]
                ev["X_HI"][x] = win_prob * (1 + payout)
            
        return ev
    
    def visualize_results(self):
        """視覺化模擬結果 - 已停用圖表生成"""
        if not self.results_history:
            return "沒有模擬數據可視覺化"
        
        stats = self.calculate_statistics()
        
        # 圖表生成功能已停用
        return "圖表生成已停用，請查看文字統計結果"

    def print_results(self):
        """打印模擬結果和統計資訊"""
        stats = self.calculate_statistics()
        if isinstance(stats, str):
            print(stats)
            return
            
        print(f"總模擬次數: {stats['總模擬次數']}")
        print("\n基本結果概率:")
        print(f"高 (HI): {stats['高 (HI)']:.4f}")
        print(f"低 (LO): {stats['低 (LO)']:.4f}")
        print(f"11 HI-LO: {stats['11 HI-LO']:.4f}")
        print(f"三同點: {stats['三同點']:.4f}")
        
        print("\n總點數概率:")
        for total in sorted(stats['點數總和'].keys()):
            print(f"總點數 {total}: {stats['點數總和'][total]:.4f}")
            
        print("\n各點數出現次數概率:")
        for num in range(1, 7):
            print(f"點數 {num}:")
            for count in range(1, 4):
                prob = stats['點數出現次數'][num].get(count, 0)
                print(f"  出現 {count} 次: {prob:.4f}")
                
        print("\n三骰組合概率:")
        print("低組合(1,2,3):")
        print(f"  出現兩個: {stats['三骰組合_低']['出現兩個']:.4f}")
        print(f"  全中: {stats['三骰組合_低']['全中']:.4f}")
        print("高組合(4,5,6):")
        print(f"  出現兩個: {stats['三骰組合_高']['出現兩個']:.4f}")
        print(f"  全中: {stats['三骰組合_高']['全中']:.4f}")
        
        print("\nX_LO與X_HI概率:")
        print("X_LO (點數總和小於等於10點，且包含點數X):")
        for x in range(1, 7):
            print(f"  {x}_LO: {stats['X_LO'][x]:.4f}")
        print("X_HI (點數總和大於等於12點，且包含點數X):")
        for x in range(1, 7):
            print(f"  {x}_HI: {stats['X_HI'][x]:.4f}")
        
        print("\n雙骰組合概率:")
        for combo, prob in stats['雙骰組合'].items():
            print(f"  {combo}: {prob:.4f}")
                
        print("\n期望值 (投注額: 100):")
        ev = self.calculate_expected_value()
        if isinstance(ev, str):
            print(ev)
            return
            
        print("基本投注:")
        print(f"高 (HI): {ev['高 (HI)']:.2f}")
        print(f"低 (LO): {ev['低 (LO)']:.2f}")
        print(f"11 HI-LO: {ev['11 HI-LO']:.2f}")
        
        print("\n單骰點數投注 (點數盤/三軍):")
        for num in range(1, 7):
            print(f"點數 {num}:")
            for count in range(1, 4):
                expected_value = ev['單骰點數'][num][count]
                print(f"  出現 {count} 次: {expected_value:.2f}")
                
        print("\n單骰點數投注 (隨機賠率固定2X):")
        for num in range(1, 7):
            print(f"點數 {num}:")
            for count in range(1, 4):
                expected_value = ev['單骰點數_隨機賠率'][num][count]
                print(f"  出現 {count} 次: {expected_value:.2f}")
                
        print("\n雙骰組合投注 (牌九式):")
        for combo, expected_value in ev['雙骰組合'].items():
            print(f"  {combo}: {expected_value:.2f}")
            
        print("\n雙骰組合投注 (隨機賠率):")
        for combo, expected_value in ev['雙骰組合_隨機賠率'].items():
            print(f"  {combo}: {expected_value:.2f}")
            
        print("\n三骰組合投注:")
        print("低組合(1,2,3):")
        print(f"  出現兩個: {ev['三骰組合_低']['出現兩個']:.2f}")
        print(f"  全中: {ev['三骰組合_低']['全中']:.2f}")
        print("高組合(4,5,6):")
        print(f"  出現兩個: {ev['三骰組合_高']['出現兩個']:.2f}")
        print(f"  全中: {ev['三骰組合_高']['全中']:.2f}")
        
        print("\nX_LO與X_HI投注:")
        print("X_LO (點數總和小於等於10點，且包含點數X):")
        for x in range(1, 7):
            if x in ev['X_LO']:
                print(f"  {x}_LO: {ev['X_LO'][x]:.2f}")
        print("X_HI (點數總和大於等於12點，且包含點數X):")
        for x in range(3, 7):
            if x in ev['X_HI']:
                print(f"  {x}_HI: {ev['X_HI'][x]:.2f}")
