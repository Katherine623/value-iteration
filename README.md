# Grid World Value Iteration

HW1-3: 使用价值迭代算法实现网格世界最优策略求解

## 功能特点

- ✅ 价值迭代算法实现
- ✅ 最优路径黄色高亮显示
- ✅ 价值函数颜色渐变可视化（绿→蓝→红）
- ✅ 交互式网格设置（3×3 到 10×10）
- ✅ Flask 后端 + HTML/CSS/JS 前端

## 在线演示

部署在：[Render.com](https://value-iteration.onrender.com) 或 [Railway](https://value-iteration.up.railway.app)

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问
http://localhost:5000
```

## 部署到 Render.com

1. Fork 此仓库
2. 在 [Render.com](https://render.com) 注册账号
3. 创建 New Web Service
4. 连接你的 GitHub 仓库
5. 使用以下设置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. 点击 Deploy

## 使用说明

1. 输入网格大小（3-10）
2. 点击 "Generate Grid"
3. 设置起始点（点击一次，绿色）
4. 设置终点（点击一次，红色）
5. 设置障碍物（点击多次，灰色）
6. 点击 "Calculate Optimal Policy & Value"
7. 查看结果：
   - Policy Matrix：显示最优策略，黄色为最优路径
   - Value Function：显示状态价值，颜色渐变

## 技术栈

- Python 3.12
- Flask 3.0
- HTML5 / CSS3 / JavaScript
- Value Iteration Algorithm

## 作者

学号: 5114056002
