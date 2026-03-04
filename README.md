# Grid World Value Iteration

Flask 網頁應用：完整實作 HW1-1、HW1-2、HW1-3

## 功能特點

- ✅ HW1-1：可設定 n×n 網格（n 範圍 5~9）
- ✅ 滑鼠點擊設定起點（綠色）與終點（紅色）
- ✅ 依規範設定障礙物數量為 n-2（灰色）
- ✅ HW1-2：隨機策略（↑↓←→）與策略評估 V(s)
- ✅ HW1-3：價值迭代求最佳政策與最佳價值函數 V*(s)
- ✅ 最優路徑黃色高亮顯示
- ✅ 價值函數顏色漸變可視化（綠→藍→紅）
- ✅ Flask 後端 + HTML/CSS/JS 前端

## 線上演示

🚀 **實時演示**：https://value-iteration.onrender.com/

已部署在 Render.com

## 本地執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行應用
python app.py

# 訪問
http://localhost:5000
```

## 部署到 Render.com

1. Fork 此儲存庫
2. 在 [Render.com](https://render.com) 註冊帳號
3. 建立 New Web Service
4. 連接你的 GitHub 儲存庫
5. 使用以下設置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. 點擊 Deploy

## 使用說明

1. 輸入網格大小（5-9）
2. 點擊 "Generate Grid"
3. 設置起始點（點擊一次，綠色）
4. 設置終點（點擊一次，紅色）
5. 設置障礙物（點擊多次，灰色，總數為 n-2）
6. 點擊「計算 HW1-2 策略評估與 HW1-3 最佳策略」
7. 查看結果：
   - HW1-2：Random Policy + Value Function V(s)
   - HW1-3：Optimal Policy + Optimal Value Function V*(s)

## 技術棧

- Python 3.12
- Flask 3.0
- HTML5 / CSS3 / JavaScript
- Value Iteration Algorithm

## 作者

學號: 5114056002
