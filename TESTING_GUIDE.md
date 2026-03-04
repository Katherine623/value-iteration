"""
測試指南 (Testing Guide)

使用以下步驟測試應用功能
"""

# 測試步驟 1: 驗證 Flask 伺服器運行
# 打開瀏覽器訪問: http://127.0.0.1:5000/

# 測試步驟 2: 基本功能測試

## 2.1 測試 HW1-1 (網格地圖開發)
steps_hw1_1 = """
1. 在上方輸入框輸入數字 7
2. 點擊 "Generate Square" 按鈕
3. 應該看到 7x7 的網格
4. 點擊第一個格子 -> 應該變成綠色（起點）
5. 點擊一個遠離起點的格子 -> 應該變成紅色（終點）
6. 點擊其他 5 個格子（7-2=5）-> 應該變成灰色（障礙物）
7. 看到提示 "Setup complete! You can now calculate policy and value."
"""

## 2.2 測試 HW1-2 (隨機策略 + 策略評估)
steps_hw1_2 = """
1. 完成 HW1-1 的設置
2. 在下拉菜單選擇 "HW1-2: Random Policy + Policy Evaluation"
3. 點擊 "Calculate Policy & Value" 按鈕
4. 等待計算完成（約 1-2 秒）
5. 應該看到兩個矩陣：
   - 左邊：Policy Matrix（包含 ↑ ↓ ← → 符號）
   - 右邊：Value Matrix（包含數字，通常為負數）
6. 每次運行應該得到不同的隨機策略
"""

## 2.3 測試 HW1-3 (價值迭代 - 最優策略)
steps_hw1_3 = """
1. 完成 HW1-1 的設置（相同的格子設置）
2. 在下拉菜單選擇 "HW1-3: Value Iteration (Optimal Policy)"
3. 點擊 "Calculate Policy & Value" 按鈕
4. 等待計算完成
5. 應該看到兩個矩陣：
   - 左邊：Policy Matrix（最優策略，箭頭指向目標）
   - 右邊：Value Matrix（相同的起點應該看到相同或類似的值）
6. 比較 HW1-2 和 HW1-3 的結果：
   - HW1-3 的箭頭應該形成一條指向目標的路徑
   - HW1-3 的數值應該比 HW1-2 更一致
"""

## 2.4 API 直接測試（可選）
curl_test = """
使用 curl 或 Postman 測試 API:

curl -X POST http://127.0.0.1:5000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "n": 5,
    "start": [0, 0],
    "end": [4, 4],
    "obstacles": [[1, 1], [2, 2], [3, 3]],
    "algorithm": "value_iter"
  }'

應該得到 JSON 回應，包含 value_matrix 和 policy_matrix
"""

# 關鍵測試點
key_tests = [
    "✓ 網格生成正確尺寸",
    "✓ 起點為綠色",
    "✓ 終點為紅色",
    "✓ 障礙物為灰色",
    "✓ 障礙物數量正確 (n-2)",
    "✓ 隨機策略每次不同",
    "✓ 價值迭代結果確定性相同",
    "✓ 最優策略指向目標",
    "✓ 價值矩陣數值合理",
    "✓ 邊界檢查正確"
]

# 預期結果
expected_results = {
    "hw1_1": "能夠成功設置 n×n 網格，選擇起點、終點和障礙物",
    "hw1_2": "隨機策略顯示箭頭，價值為負數，多次運行得到不同結果",
    "hw1_3": "最優策略箭頭形成指向目標的路徑，多次運行得到相同結果",
    "api": "返回有效的 JSON 格式響應"
}

print("=" * 60)
print("HW1-1, HW1-2, HW1-3 測試指南")
print("=" * 60)
print()
print("HW1-1: 網格地圖開發")
print(steps_hw1_1)
print()
print("HW1-2: 隨機策略 + 策略評估")
print(steps_hw1_2)
print()
print("HW1-3: 價值迭代（最優策略）")
print(steps_hw1_3)
print()
print("API 測試")
print(curl_test)
print()
print("關鍵測試點:")
for test in key_tests:
    print(f"  {test}")
