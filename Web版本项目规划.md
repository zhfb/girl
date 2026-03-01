# AI女友 Web版本项目规划

## 项目概述
基于Web的智能AI女友应用程序，用户启动服务后通过浏览器访问 localhost 使用。支持多种语言模型和语音模型，具有强大的记忆能力和高度个性化定制功能。

**发布目标**：用户运行启动脚本后，自动打开浏览器访问本地Web界面。

## 技术架构

### 后端：FastAPI + Python
- **Web框架**: FastAPI（高性能、异步支持）
- **后端逻辑**: 复用现有的核心模块
- **API通信**: RESTful API + WebSocket（用于流式对话）
- **数据存储**: SQLite + JSON

### 前端：纯HTML/CSS/JavaScript
- **UI框架**: 原生JavaScript + CSS3（无需额外构建工具）
- **实时通信**: WebSocket（流式输出）
- **样式**: 现代化、响应式设计

## 项目结构
```
ai-girlfriend/
├── config/                  # 配置文件
│   └── models.json          # 模型配置
├── core/                    # 核心逻辑（复用）
│   ├── model/               # 模型适配器
│   ├── memory/              # 记忆系统
│   ├── chat/                # 对话管理
│   └── prompt/              # 提示词系统
├── backend/                 # Web后端
│   ├── __init__.py
│   ├── main.py              # FastAPI主入口
│   ├── api/                 # API路由
│   │   ├── chat.py          # 对话API
│   │   ├── config.py        # 配置API
│   │   └── models.py        # 模型API
│   └── websocket/           # WebSocket处理
│       └── chat_stream.py   # 流式对话
├── frontend/                # Web前端
│   ├── index.html           # 主页面
│   ├── css/
│   │   └── style.css        # 样式文件
│   └── js/
│       └── app.js           # 前端逻辑
├── utils/                   # 工具函数
│   └── config.py            # 配置管理
├── docs/                    # 文档
├── requirements.txt         # Python依赖
└── start.py                 # 启动脚本（自动打开浏览器）
```

## 核心功能

### 1. 多模型支持系统
- **语言模型**: DeepSeek、OpenAI等
- **语音模型**: Edge-TTS等
- **模型配置管理**: Web界面配置API密钥

### 2. 智能对话系统
- **实时聊天**: WebSocket流式输出，打字机效果
- **记忆能力**: 短期/长期记忆
- **对话历史**: 保存和查看历史对话

### 3. 提示词系统
- **角色设定**: Web界面自定义角色
- **提示词模板**: 预设模板选择

### 4. 设置界面
- **模型配置**: API密钥、参数设置
- **角色设定**: 名字、性格、背景故事

## API设计

### RESTful API
- `GET /api/config` - 获取配置
- `POST /api/config` - 保存配置
- `GET /api/models` - 获取可用模型列表
- `GET /api/chat/history` - 获取对话历史
- `POST /api/chat/clear` - 清空对话历史

### WebSocket
- `WS /ws/chat` - 流式对话接口

## 部署方式

### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务（自动打开浏览器）
python start.py
```

启动后自动打开浏览器访问 `http://localhost:8000`

## 开发计划

### 第一阶段：基础框架
- 创建FastAPI后端
- 创建基础前端界面
- 集成现有核心模块
- 实现基础对话功能

### 第二阶段：功能完善
- 添加设置界面
- 实现对话历史保存
- 添加角色设定功能
- 美化UI界面

### 第三阶段：优化和发布
- 性能优化
- Bug修复
- 用户体验优化
