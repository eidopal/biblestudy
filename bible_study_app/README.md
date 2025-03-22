# 每日圣经学习应用

这是一个帮助用户进行圣经学习的Web应用程序，提供每日阅读计划和经文背诵功能。

## 主要功能

- **每日阅读计划**：显示当天需要阅读的圣经章节
- **经文背诵**：显示当天需要背诵的经文
- **自定义内容**：管理员可以手动输入经文内容，特别是当API无法获取内容时
- **用户认证**：包含基本的用户登录系统，区分普通用户和管理员
- **响应式设计**：适配手机、平板和电脑等不同设备

## 开发技术

- 后端：Flask (Python)
- 前端：Bootstrap 5、JavaScript
- 认证：Flask-Login
- 数据存储：JSON文件

## 本地运行

1. 克隆仓库：
```bash
git clone <仓库地址>
cd bible_study_app
```

2. 创建并激活虚拟环境：
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行应用：
```bash
python web_app.py
```

5. 访问应用：http://localhost:5000

## 部署到Vercel

1. 注册 [Vercel](https://vercel.com/) 账号并连接到您的GitHub仓库

2. 在Vercel控制台中点击"New Project"，选择此仓库

3. 在构建设置中选择：
   - Framework Preset: Other
   - Build Command: 留空
   - Output Directory: 留空
   - Install Command: `pip install -r requirements.txt`

4. 点击"Deploy"

5. 部署完成后，您可以使用Vercel提供的URL访问您的应用

## 使用说明

### 初次使用

- 默认管理员账号: `admin`
- 默认密码: `admin`
- **重要**: 首次登录后请创建新的管理员账号并更改默认密码

### 管理员功能

- 设置阅读计划
- 添加/编辑背诵经文
- 手动输入经文内容
- 管理用户账号

### 普通用户功能

- 查看每日阅读计划
- 查看每日背诵经文

## 许可证

MIT 