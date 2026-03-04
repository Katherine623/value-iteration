# Grid World Value Iteration

HW1-3: 使用價值迭代演算法實現網格世界最優策略求解

## 功能特點

- ✅ 價值迭代演算法實現
- ✅ 最優路徑黃色高亮顯示
- ✅ 價值函數顏色漸變可視化（綠→藍→紅）
- ✅ 互動式網格設置（3×3 到 10×10）
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

1. 輸入網格大小（3-10）
2. 點擊 "Generate Grid"
3. 設置起始點（點擊一次，綠色）
4. 設置終點（點擊一次，紅色）
5. 設置障礙物（點擊多次，灰色）
6. 點擊 "Calculate Optimal Policy & Value"
7. 查看結果：
   - Policy Matrix：顯示最優策略，黃色為最優路徑
   - Value Function：顯示狀態價值，顏色漸變

## 技術棧

- Python 3.12
- Flask 3.0
- HTML5 / CSS3 / JavaScript
- Value Iteration Algorithm

## 作者

學號: 5114056002
