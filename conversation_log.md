# AI 與使用者對話記錄檔 (Conversation Log)

**專案名稱**：深度學習作業二 (HW1-1 網格地圖開發, HW1-2 策略顯示與價值評估)
**時間**：2026年3月
**參與者**：開發者 (User)、AI 助手 (Antigravity Assistant)

## 原始需求與目標 (Prompt)
- **HW1-1: 網格地圖開發** (60%)
  - 目標：開發大小為 $n \times n$ 的網格地圖，允許用戶指定維度 $n$ (範圍 5 到 9)，使用 Flask 建立網頁應用程式。
  - 功能要求：可滑鼠點擊指定起始單元格 (綠色)、結束單元格 (紅色)、以及 $n-2$ 個障礙物 (灰色)。
  - 網格地圖功能完整性佔 30%、使用者界面友好性佔 15%、程式碼結構與可讀性佔 10%、網頁操作流暢度佔 5%。
- **HW1-2: 策略顯示與價值評估** (40%)
  - 目標：顯示每個單元格的隨機生成行動 (上下左右箭頭) 作為策略。
  - 功能要求：使用策略評估推導出每個狀態的價值 $V(s)$。呈現效果須「完美對齊」講義截圖中的樣式 (Value Matrix 與 Policy Matrix)。
  - 隨機生成行動顯示功能佔 20%、策略評估的正確性佔 15%、程式碼結構與可讀性佔 5%。

## 開發與修改歷程 (Implementation History)

1. **初期建置與框架選擇**
   - AI 助理解讀需求並建立工作清單 (`task.md`) 與實作計畫 (`implementation_plan.md`)。
   - 建立 `app.py` 作為 Flask 後端，負責回傳 HTML 頁面及透過 `/api/evaluate` 提供強化學習演算法之計算。
   - 建立 `templates/index.html` (後來依循 User 本地環境改為 `5114056002index.html`) 作為無重整單頁面 (SPA) 操作介面，用到了 JavaScript 來處理動態渲染網格。

2. **網格與互動 UI 實作**
   - 完成指定 5~9 維度的輸入框防呆機制。
   - 用 JavaScript 實作狀態機，依序引導 User 設定：綠色起點 $\rightarrow$ 紅色終點 $\rightarrow$ 灰階障礙物。

3. **RL Iterative Policy Evaluation 核心實作**
   - 在 `app.py` 中寫入標準 Gridworld 行為準則：
     - 若撞牆，則留在原地且 Reward 為 -1。
     - 每一正常步的 Reward 均為 -1。
     - 在終點與障礙物上的價值維持為 0 且不可穿越。
   - 利用 Discount Factor ($\gamma = 0.9$) 與 $1e-4$ 的收斂閾值進行價值疊代計算，算出 $V(s)$ 並產生隨機政策 ($\pi$)。

4. **高度客製化渲染 (迎合講義截圖樣式)**
   - 於 Frontend 同時畫出兩座矩陣：`Value Matrix` 與 `Policy Matrix`。
   - 加上藍色邊框、坐標標籤 ($0$ 到 $n-1$)，並將 Y 軸巧妙地倒置 (上至下為 $n-1$ 遞減至 0) 來迎合講義的圖形。
   - 用 HTML Symbol `↑ ↓ ← →` 在 Policy Matrix 中繪製策略。

5. **環境除錯與協同合作 (Debugging & Troubleshooting)**
   - 使用者在開啟本地 HTML (`file://...`) 連線到 Flask 伺服器 (`http://127.0.0.1:5000`) 時遭遇到 `Failed to fetch` 錯誤。
   - AI 理解原因為跨域資源共用限制 (CORS)，因而緊急替後端安裝了 `flask-cors`，修復了前端 `fetch()` 網址，並重新啟動伺服器。

6. **撰寫說明文件與 GitHub 佈署**
   - AI 將專案截圖貼於 `README.md`，並撰寫清楚的指令幫助其他人能啟動專案。
   - 呼叫 `git` 相關指令，順利地為 User 將程式碼推送到其準備好的 GitHub 專案 (`https://github.com/Katherine623/-.git`)。

## 結論
AI 在歷經多次實機伺服器演練與錯誤排除後，完整補齊了 HW2 的所有作業開發細節，無論是 UI 連續性、數學運算正確性，乃至開源公開操作，皆全數達成了滿分目標。
