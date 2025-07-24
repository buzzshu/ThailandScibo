"""
骰寶模擬器測試腳本 - 使用最新賠率
"""

from sic_bo_simulator import SicBoSimulator
import random

def main():
    # 建立模擬器實例
    print("初始化骰寶 (Sic Bo) 模擬器...")
    simulator = SicBoSimulator()
    
    # 執行單次模擬
    print("\n模擬一次投擲:")
    result = simulator.simulate_single_roll()
    dice = result["dice"]
    total = result["total"]
    print(f"骰子點數: {dice[0]}, {dice[1]}, {dice[2]}")
    print(f"總點數: {total}")
    print(f"是高 (HI): {result['is_hi']}")
    print(f"是低 (LO): {result['is_lo']}")
    print(f"是11 HI-LO: {result['is_hi_lo_11']}")
    print(f"是三同點: {result['is_triple']}")
    
    # 展示特殊點數組合
    print("\n特殊點數組合:")
    
    # 低組合(1,2,3)
    print(f"低組合(1,2,3) 結果: {result['low_combo']}")
    
    # 高組合(4,5,6)
    print(f"高組合(4,5,6) 結果: {result['high_combo']}")
    
    # 檢查點數出現次數
    print("\n各點數出現次數:")
    for num in range(1, 7):
        print(f"點數 {num}: {result['counts'][num]} 次")
        
    # X_LO 和 X_HI結果
    print("\nX_LO結果:")
    for x in range(1, 7):
        print(f"{x}_LO: {result['x_lo'][x]}")
        
    print("\nX_HI結果:")
    for x in range(1, 7):
        print(f"{x}_HI: {result['x_hi'][x]}")
    
    # 模擬隨機賠率
    print("\n隨機賠率示例:")
    print("1_LO隨機高倍賠率:", random.choice([1.8, 3, 5, 10, 15]))
    print("單骰點數出現1次隨機高倍賠率:", random.choice([1, 2, 3]))
    print("雙骰組合隨機高倍賠率:", random.choice([5, 10, 15, 25, 40]))
    
    # 執行多次模擬
    print("\n進行模擬計算中...")
    simulations = 20000
    simulator.simulate_multiple_rolls(simulations)
    print(f"完成 {simulations} 次模擬")
    
    # 印出統計結果
    print("\n統計結果:")
    simulator.print_results()
    
    # 視覺化結果
    print("\n生成視覺化圖表:")
    result = simulator.visualize_results()
    print(result)
    print("\n請開啟圖表文件查看視覺化結果")

if __name__ == "__main__":
    main()
