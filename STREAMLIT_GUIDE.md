# Streamlit 部署指南

## 本地執行

### 1. 安裝依賴
```bash
pip install -r streamlit_requirements.txt
```

### 2. 執行應用
```bash
streamlit run streamlit_app.py
```

應用會自動在 `http://localhost:8501` 打開

## 部署到 Streamlit Cloud

### 1. 準備預備
- 確保 `streamlit_app.py` 和 `streamlit_requirements.txt` 已推送到 GitHub
- GitHub 帳號已連接到 Streamlit Cloud

### 2. 部署步驟

#### 方式 A: Streamlit Cloud (推薦，完全免費)
1. 訪問 https://streamlit.io/cloud
2. 用 GitHub 帳號登入
3. 點擊 "New app"
4. 選擇：
   - Repository: `Katherine623/value-iteration`
   - Branch: `master`
   - File path: `streamlit_app.py`
5. 點擊 Deploy

應用將在 `https://[你的應用名稱].streamlit.app` 上線

#### 方式 B: Render.com (需自訂 Procfile)
1. 如果使用 Render，需要更新 Procfile：
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. 在 Render 中設定環境變數：
   - 建立 `.streamlit/config.toml` 檔案以保存 Streamlit 配置

#### 方式 C: Heroku
```bash
# 更新 Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 部署
git add .
git commit -m "Deploy Streamlit app to Heroku"
git push heroku master
```

## 比較：Flask vs Streamlit

| 項目 | Flask | Streamlit |
|------|-------|-----------|
| 部署便利性 | 需要自訂前後端 | 一行指令即可運行 |
| 開發速度 | 較慢 | 非常快 |
| 前端設計 | 需要 HTML/CSS/JS | 內建 UI 元件 |
| 互動性 | 手動管理 | session_state 自動管理 |
| 免費部署 | 需要付費服務 | Streamlit Cloud 完全免費 |
| 適合用途 | 生產環境應用 | 原型開發和演示 |

## 功能說明

### 互動式網格設置
- 點擊網格按鈕選擇起始點（綠色）、終點（紅色）、障礙物（灰色）
- 使用側邊欄調整網格大小 (3-10)
- 重置按鈕清除所有設置

### 計算與結果
- 自動執行 Value Iteration 演算法
- 顯示 Policy Matrix（最優策略）
- 顯示 Value Function（狀態價值）
- 視覺化最優路徑

## 參數配置

在 `streamlit_app.py` 中調整演算法參數：

```python
gamma = 0.9  # 折扣因子
theta = 1e-4  # 收斂閾值
```

## 故障排除

### 問題：應用無法部署到 Streamlit Cloud
**解決：** 確保 `streamlit_requirements.txt` 中列出所有依賴

### 問題：互動元素無反應
**解決：** Streamlit Cloud 可能需要 1-2 分鐘首次部署，重新整理頁面

### 問題：計算很慢
**解決：** 大型網格 (10×10) 會增加計算時間，考慮減少網格或優化算法

## 下一步

- 移除或備檔 `app.py` 和 `5114056002index.html`（如果只用 Streamlit）
- 更新 GitHub README.md 指向 Streamlit Cloud URL
- 可選：保留 Flask 版本供生產環境使用
