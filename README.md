# 💖 AI女友

基于多模型API的智能AI女友应用程序，支持多种语言模型和语音模型，具有强大的记忆能力、丰富的交互体验和高度个性化定制功能。

## 功能特点

- 🤖 **多模型支持**：DeepSeek、OpenAI 等多种语言模型
- 🗣️ **语音交互**：TTS 文字转语音，支持多种音色
- 🧠 **记忆系统**：短期和长期记忆，不会忘记对话内容
- ✏️ **自定义提示词**：灵活的角色设定和提示词系统
- 🎨 **精美界面**：PyQt6 打造的现代化用户界面
- 📦 **一键安装**：NSIS 安装程序，开箱即用

## 快速开始

### 开发者

1. 克隆或下载项目
2. 创建虚拟环境：`python -m venv venv`
3. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. 安装依赖：`pip install -r requirements.txt`
5. 运行程序：`python main.py`

### 用户

1. 下载发布压缩包 `AI女友_v1.0.0.zip`
2. 解压后运行安装程序
3. 按照向导完成安装
4. 启动程序后在设置中配置 API Key
5. 开始使用！

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
├── ui/                  # 界面组件
├── assets/              # 资源文件
├── data/                # 数据存储
├── utils/               # 工具函数
├── scripts/             # 打包脚本
├── docs/                # 文档
├── main.py              # 主程序入口
└── requirements.txt     # 依赖列表
```

## 打包发布

使用提供的自动化脚本进行打包：

```bash
cd scripts
python build.py
```

这将依次执行：
1. 清理旧的构建文件
2. 使用 PyInstaller 打包成 exe
3. 使用 NSIS 制作安装程序
4. 创建发布压缩包

## 许可证

本项目仅供学习和研究使用。
