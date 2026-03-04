# 部署指南 (Deployment Guide)

## 🚀 快速部署到 Render.com（推荐）

### 方法 1: 使用 Render Dashboard（最简单）

1. **访问 Render**: https://render.com
2. **注册/登录** 账号（可以用 GitHub 账号登录）
3. **点击 "New +"** → 选择 **"Web Service"**
4. **连接 GitHub 仓库**:
   - 点击 "Connect account" 连接你的 GitHub
   - 选择仓库: `Katherine623/-`
5. **配置设置**:
   - **Name**: `gridworld-value-iteration`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: 选择 **Free**
6. **点击 "Create Web Service"**
7. **等待部署** (约 2-5 分钟)
8. **访问你的应用**: Render 会提供一个 URL，如 `https://gridworld-value-iteration.onrender.com`

### 方法 2: 使用 Render Blueprint (自动配置)

1. 访问 Render Dashboard
2. 点击 "New +" → **"Blueprint"**
3. 连接你的 GitHub 仓库
4. Render 会自动读取 `render.yaml` 配置
5. 点击 "Apply" 开始部署

---

## 🌐 其他部署选项

### Railway.app（也很简单）

1. 访问 https://railway.app
2. 用 GitHub 登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 会自动检测 Flask 应用并部署
6. 获取部署 URL

### Heroku（需要信用卡验证）

1. 安装 Heroku CLI
2. 在项目目录运行:
```bash
heroku login
heroku create gridworld-app
git push heroku master
heroku open
```

---

## 📝 部署后的 URL 示例

部署成功后，你会得到一个公开访问的 URL：
- Render: `https://gridworld-value-iteration.onrender.com`
- Railway: `https://gridworld-app.up.railway.app`
- Heroku: `https://gridworld-app.herokuapp.com`

---

## 🔧 本地测试部署配置

在推送到 GitHub 之前，可以本地测试：

```bash
# 安装 gunicorn
pip install gunicorn

# 运行生产模式
gunicorn app:app

# 或指定端口
gunicorn app:app --bind 0.0.0.0:8000
```

---

## ⚠️ 注意事项

1. **免费套餐限制**:
   - Render Free: 应用闲置 15 分钟后会休眠，首次访问需要等待启动
   - Railway: 每月 500 小时免费使用

2. **环境变量**:
   - `FLASK_ENV=production` (已在 render.yaml 配置)
   - `PORT` (自动设置)

3. **CORS 配置**:
   - 已启用 Flask-CORS，支持跨域访问

4. **静态文件**:
   - HTML 文件在项目根目录，Flask 会自动提供

---

## 📊 在 GitHub 中显示 Deployments

部署成功后，GitHub 会自动在仓库页面显示 Deployments 状态：

1. Render/Railway 会自动创建 GitHub Deployment
2. 在仓库页面可以看到 "Deployments" 部分
3. 显示部署状态和访问链接

---

## 🎯 推荐工作流

```
本地开发 → 推送到 GitHub → 自动部署到 Render → 在线访问
```

每次推送到 `master` 分支，Render 会自动重新部署！
