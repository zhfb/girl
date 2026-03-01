# 💖 AI女友 - Web版本

基于Web的智能AI女友应用程序，用户启动服务后通过浏览器访问 localhost 使用。支持多种语言模型，具有强大的记忆能力和高度个性化定制功能。

## 功能特点

- 🤖 **多模型支持**：DeepSeek、OpenAI 等多种语言模型
- 🧠 **记忆系统**：短期记忆，不会忘记最近对话内容
- ✏️ **自定义提示词**：灵活的角色设定和配置
- 🎨 **精美界面**：现代化的 Web 聊天界面
- 🌐 **跨平台**：通过浏览器访问，支持 Windows、Mac、Linux

## 快速开始

### 运行程序

1. 克隆或下载项目
2. 安装依赖：`pip install -r requirements.txt`
3. 启动服务：`python start.py`
4. 服务启动后会自动打开浏览器访问 http://localhost:8000

### 使用说明

1. 首次使用时，点击右上角的 ⚙️ 设置按钮
2. 选择要使用的模型（DeepSeek 或 OpenAI）
3. 输入你的 API Key
4. 保存设置
5. 返回聊天界面开始对话！

## 获取 API Key

- **DeepSeek（推荐）**：https://platform.deepseek.com/
- **OpenAI**：https://platform.openai.com/

## 项目结构

```
ai-girlfriend/
├── config/              # 配置文件
├── core/                # 核心逻辑
│   ├── model/           # 模型适配器
│   ├── memory/          # 记忆系统
│   ├── chat/            # 对话管理
│   └── prompt/          # 提示词系统
├── backend/             # Web 后端（FastAPI）
│   ├── main.py          # 后端主入口
│   └── api/             # API 路由
├── frontend/            # Web 前端
│   ├── index.html       # 主页面
│   ├── css/
│   │   └── style.css    # 样式文件
│   └── js/
│       └── app.js       # 前端逻辑
├── utils/               # 工具函数
├── docs/                # 文档
├── start.py             # 启动脚本（自动打开浏览器）
└── requirements.txt     # 依赖列表
```

## 技术架构

- **后端**：FastAPI（高性能异步 Web 框架）
- **前端**：原生 HTML/CSS/JavaScript（无需构建工具）
- **实时通信**：WebSocket（流式对话输出）
- **数据存储**：本地 JSON 配置文件

## 停止服务

在终端按 `Ctrl+C` 即可停止服务。

## 许可证

本项目仅供学习和研究使用。
