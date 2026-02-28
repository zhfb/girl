# AI女友项目规划

## 项目概述
基于多模型API的智能AI女友应用程序，支持多种语言模型和语音模型，具有强大的记忆能力、丰富的交互体验和高度个性化定制功能。

**发布目标**：制作完整的安装包，用户下载压缩包后解压，运行安装程序即可使用。

## 核心功能

### 1. 多模型支持系统
- **语言模型支持**
  - DeepSeek系列（V3/R1等）
  - OpenAI GPT系列
  - Claude系列
  - 文心一言、通义千问等国产模型
  - 本地模型支持（Llama、Qwen等）
- **语音模型支持**
  - OpenAI Whisper（语音识别）
  - 火山引擎、阿里云等TTS
  - Edge-TTS（免费语音）
  - 本地语音模型
- **模型切换功能**：支持对话过程中动态切换模型
- **模型配置管理**：每个模型独立的API密钥、参数配置

### 2. 智能对话系统
- **实时对话聊天**
  - 流式输出，打字机效果
  - 支持打断和重新生成
  - 多轮对话上下文理解
- **强大记忆能力**
  - 短期记忆：最近对话上下文
  - 长期记忆：用户信息、重要事件、偏好设置
  - 记忆检索：基于向量相似度的记忆召回
  - 记忆管理：自动总结、重要性标记、遗忘机制
- **情感表达**
  - 情绪识别与回应
  - 多样化的语气风格
  - 表情包配合回复

### 3. 提示词系统
- **系统提示词自定义**
  - 角色设定模板
  - 自定义提示词编辑器
  - 提示词变量（{名字}、{性格}、{背景}等）
  - 提示词版本管理
- **预设提示词库**
  - 多种角色预设（御姐、萝莉、学姐、学妹、同事等）
  - 场景预设（日常聊天、约会、学习辅导等）
  - 用户可分享和导入提示词

### 4. 女友形象定制
- **基础设定**
  - 自定义名字、昵称
  - 年龄、身高、生日等个人信息
  - 性格标签选择（温柔、活泼、高冷、呆萌、腹黑等）
  - 兴趣爱好设定
- **背景故事**
  - 预设背景模板
  - 自定义背景编辑器
  - 时间线式背景故事
- **外观设定**
  - 头像选择/上传
  - 形象描述（用于AI生成回复参考）

### 5. 语音交互系统
- **语音输入（ASR）**
  - 实时语音转文字
  - 支持多种语言
  - 语音端点检测
  - 离线语音识别支持
- **语音输出（TTS）**
  - 文字转语音播放
  - 多种音色选择
  - 语速、音调、音量调节
  - 语音情感表达
  - 支持语音消息发送（保存为音频文件）
- **语音通话模式**
  - 实时语音对话
  - 打断和插话
  - 对话间歇检测

### 6. 视觉表现
- **头像系统**
  - 静态头像展示
  - 动态表情变化（根据对话内容切换表情）
  - 头像动画（眨眼、点头等）
- **2D立绘**
  - 简单Live2D效果
  - 姿势和表情变化
  - 服装切换
- **场景系统**
  - 多种场景背景（卧室、客厅、公园、咖啡厅等）
  - 时间相关场景变化（白天/夜晚）
  - 天气效果

### 7. 互动功能
- **日常互动**
  - 早安/晚安问候
  - 每日天气和新闻分享
  - 心情分享与倾听
  - 饮食、睡眠提醒
- **节日与纪念日**
  - 节日祝福
  - 重要日期提醒
  - 特殊场景互动
- **休闲娱乐**
  - 小游戏互动（猜谜、脑筋急转弯、成语接龙等）
  - 音乐推荐
  - 电影/书籍分享
- **实用功能**
  - 日程管理和提醒
  - 备忘录
  - 番茄钟专注模式
  - 学习陪伴

### 8. 数据管理
- **对话历史**
  - 本地对话保存
  - 对话搜索
  - 重要对话收藏
  - 对话导出（文本/JSON）
- **记忆管理**
  - 记忆查看和编辑
  - 重要性标记
  - 记忆导出/导入
- **配置管理**
  - 多账号支持
  - 配置备份和恢复
  - 数据加密存储

## 技术架构

### 推荐方案：Python + PyQt6
- **前端UI**: PyQt6 / PySide6
- **后端逻辑**: Python
- **API通信**: requests / aiohttp
- **向量数据库**: ChromaDB / FAISS（用于记忆检索）
- **语音处理**:
  - ASR: OpenAI Whisper / FunASR
  - TTS: edge-tts / pyttsx3 / 火山引擎
- **数据存储**: SQLite + JSON
- **打包发布**: PyInstaller + NSIS（制作安装包）

### 打包发布方案
- **PyInstaller**: 将Python代码和依赖打包成exe
- **NSIS (Nullsoft Scriptable Install System)**: 制作Windows安装程序
- **数据目录**: 用户数据存储在 `%APPDATA%/AIGirlfriend/` 下，确保升级不丢失数据
- **配置文件**: 首次运行自动生成默认配置，用户可在设置中修改
- **发布形式**: 压缩包（.zip）包含安装程序，用户解压后运行安装

### 备选方案：Electron + Vue3
- **前端**: Vue3 + Element Plus
- **后端**: Node.js
- **桌面框架**: Electron
- **向量数据库**: LanceDB / Weaviate
- **语音**: Web Speech API + 第三方TTS
- **打包**: electron-builder

## 核心模块设计

### 1. 模型适配器层
```
ModelAdapter (抽象基类)
├── LLMAdapter (语言模型适配器)
│   ├── DeepSeekAdapter
│   ├── OpenAIAdapter
│   ├── ClaudeAdapter
│   └── LocalModelAdapter
└── TTSAdapter (语音模型适配器)
    ├── EdgeTTSAdapter
    ├── VolcanoTTSAdapter
    └── OpenAITTSAdapter
```

### 2. 记忆系统架构
- **短期记忆**: 对话历史队列（最近N轮）
- **长期记忆**:
  - 用户档案（基本信息、偏好）
  - 事件记忆（重要对话摘要）
  - 知识记忆（用户分享的知识点）
- **记忆检索**: 向量相似度检索 + 时间权重
- **记忆总结**: 定期用LLM总结对话，提取重要信息

### 3. 提示词管理
- **模板引擎**: 支持变量替换
- **提示词组合**: 系统提示 + 角色设定 + 记忆摘要 + 当前对话
- **上下文构建**: 智能裁剪和优化提示词长度

## 项目结构
```
ai-girlfriend/
├── config/                  # 配置文件
│   ├── models.json          # 模型配置
│   ├── characters/          # 角色预设
│   └── prompts/             # 提示词模板
├── core/                    # 核心逻辑
│   ├── model/               # 模型适配器
│   │   ├── base.py
│   │   ├── llm/
│   │   └── tts/
│   ├── memory/              # 记忆系统
│   │   ├── short_term.py
│   │   ├── long_term.py
│   │   └── retriever.py
│   ├── chat/                # 对话管理
│   │   ├── manager.py
│   │   └── context.py
│   ├── prompt/              # 提示词系统
│   │   ├── template.py
│   │   └── builder.py
│   └── personality.py       # 性格系统
├── ui/                      # 界面组件
│   ├── main_window.py
│   ├── chat_widget.py
│   ├── settings/
│   └── components/
├── assets/                  # 资源文件
│   ├── images/
│   ├── avatars/
│   ├── backgrounds/
│   ├── voices/
│   └── icon.ico             # 程序图标
├── data/                    # 数据存储
│   ├── chat_history/
│   ├── memories/
│   └── user_data/
├── utils/                   # 工具函数
│   ├── audio.py
│   ├── vector_db.py
│   └── config.py
├── scripts/                 # 打包脚本
│   ├── build.py             # 自动化打包脚本
│   ├── build.spec           # PyInstaller配置
│   └── installer.nsi        # NSIS安装脚本
├── docs/                    # 文档
│   └── 使用说明.md
├── requirements.txt         # Python依赖
└── main.py                  # 主程序入口
```

## 发布包结构

### 最终发布压缩包
```
AI女友_v1.0.0.zip
├── AI女友_安装程序.exe    # NSIS安装程序
└── 使用说明.txt            # 简明使用说明
```

### 安装后目录结构
```
C:\Program Files\AI女友\
├── AIGirlfriend.exe        # 主程序
├── assets/                 # 资源文件
│   ├── images/
│   ├── avatars/
│   ├── backgrounds/
│   └── icon.ico
├── config/                 # 默认配置
│   ├── models.json
│   ├── characters/
│   └── prompts/
├── uninstall.exe           # 卸载程序
└── 使用说明.txt
```

### 用户数据目录
```
%APPDATA%\AIGirlfriend\
├── config.json             # 用户配置
├── chat_history/           # 对话历史
├── memories/               # 长期记忆
├── characters/             # 自定义角色
└── logs/                   # 日志文件
```

## 开发阶段

### 第一阶段：基础框架（MVP）
- 项目初始化和基础架构搭建
- 多LLM模型适配器（DeepSeek + OpenAI）
- 基础对话界面
- 简单提示词系统
- 基础对话历史保存

### 第二阶段：记忆系统
- 短期记忆实现
- 长期记忆存储
- 向量数据库集成
- 记忆检索和召回
- 记忆总结和管理界面

### 第三阶段：语音功能
- TTS语音输出
- 多音色选择
- 语音消息保存和发送
- ASR语音输入
- 基础语音对话

### 第四阶段：形象定制
- 角色设定界面
- 提示词模板系统
- 头像展示系统
- 预设角色库
- 用户自定义提示词编辑器

### 第五阶段：增强体验
- 动态表情和动画
- 场景切换
- 更多互动功能
- 界面美化
- 性能优化

### 第六阶段：打包发布
- PyInstaller打包配置
- NSIS安装程序制作
- 自动化打包脚本
- 完整功能测试
- Bug修复和优化
- 用户文档编写

## 配置文件示例

### config.json
```json
{
  "active_llm": "deepseek",
  "active_tts": "edge-tts",
  "llm_models": {
    "deepseek": {
      "api_key": "your-api-key",
      "api_base": "https://api.deepseek.com",
      "model": "deepseek-chat",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "openai": {
      "api_key": "your-api-key",
      "api_base": "https://api.openai.com/v1",
      "model": "gpt-4",
      "temperature": 0.7
    }
  },
  "tts_models": {
    "edge-tts": {
      "voice": "zh-CN-XiaoxiaoNeural",
      "rate": "+0%",
      "pitch": "+0Hz"
    }
  },
  "character": {
    "name": "小萌",
    "nickname": "萌萌",
    "personality": ["温柔", "可爱", "体贴"],
    "avatar": "default",
    "background_story": "你的大学学妹，性格温柔善良..."
  },
  "memory": {
    "short_term_max": 20,
    "long_term_enabled": true,
    "auto_summarize": true
  }
}
```

### 提示词模板示例
```
你是{名字}，{性格描述}。

{背景故事}

你的说话风格：{说话风格示例}

关于用户的重要信息：
{用户记忆摘要}

最近的对话历史：
{最近对话}

请以{名字}的身份回复用户，保持角色一致性。
```

## 打包与部署

### 开发环境配置
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行开发版本
python main.py
```

### requirements.txt
```
PyQt6>=6.6.0
requests>=2.31.0
aiohttp>=3.9.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
edge-tts>=6.1.0
openai>=1.0.0
pyinstaller>=6.0.0
```

### PyInstaller打包配置
创建 `scripts/build.spec` 文件：
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        ('../assets', 'assets'),
        ('../config', 'config'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'chromadb',
        'sentence_transformers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AIGirlfriend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AIGirlfriend',
    debug=False,
    bootloader_ignore_signals=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
```

### NSIS安装脚本
创建 `scripts/installer.nsi`：
```nsis
!define APPNAME "AI女友"
!define VERSION "1.0.0"
!define COMPANY "AIGirlfriend Team"
!define WEBSITE "https://github.com/your-repo"

!define APPNAME_SHORT "AIGirlfriend"
!define INSTALL_DIR "$PROGRAMFILES\${APPNAME}"
!define DATA_DIR "$APPDATA\${APPNAME_SHORT}"

Name "${APPNAME}"
OutFile "..\release\${APPNAME}_v${VERSION}_安装程序.exe"
InstallDir "${INSTALL_DIR}"
InstallDirRegKey HKLM "Software\${APPNAME}" "InstallPath"
RequestExecutionLevel admin
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "${APPNAME}"
VIAddVersionKey "CompanyName" "${COMPANY}"
VIAddVersionKey "LegalCopyright" "${COMPANY}"
VIAddVersionKey "FileDescription" "${APPNAME} Installation"
VIAddVersionKey "FileVersion" "${VERSION}"

!include "MUI2.nsh"

!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_WELCOMEPAGE_TITLE "欢迎使用 ${APPNAME} 安装向导"
!define MUI_WELCOMEPAGE_TEXT "本向导将指引你完成 ${APPNAME} 的安装。$\r$\n$\r$\n点击下一步继续。"
!define MUI_FINISHPAGE_TITLE "完成 ${APPNAME} 安装"
!define MUI_FINISHPAGE_TEXT "${APPNAME} 已成功安装到你的计算机。$\r$\n$\r$\n点击完成退出安装向导。"
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APPNAME_SHORT}.exe"
!define MUI_FINISHPAGE_RUN_TEXT "运行 ${APPNAME}"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\docs\使用说明.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

LangString DESC_SecMain ${LANG_ENGLISH} "主程序文件"
LangString DESC_SecDesktop ${LANG_ENGLISH} "创建桌面快捷方式"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "创建开始菜单项"

Section "${APPNAME} (必需)" SecMain
    SectionIn RO
    SetOutPath "$INSTDIR"

    File /r "..\dist\AIGirlfriend\*"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    WriteRegStr HKLM "Software\${APPNAME}" "InstallPath" "$INSTDIR"
    WriteRegStr HKLM "Software\${APPNAME}" "Version" "${VERSION}"

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANY}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
SectionEnd

Section "桌面快捷方式" SecDesktop
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APPNAME_SHORT}.exe"
SectionEnd

Section "开始菜单" SecStartMenu
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APPNAME_SHORT}.exe"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\卸载.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

Section "Post" SecPost
    SetShellVarContext all
    CreateDirectory "${DATA_DIR}"
SectionEnd

Section -AdditionalIcons
    WriteIniStr "$INSTDIR\${APPNAME}.url" "InternetShortcut" "URL" "${WEBSITE}"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\uninstall.exe"
    Delete "$INSTDIR\${APPNAME}.url"

    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\${APPNAME}\卸载.lnk"
    RMDir "$SMPROGRAMS\${APPNAME}"

    Delete "$DESKTOP\${APPNAME}.lnk"

    RMDir /r "$INSTDIR"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
    DeleteRegKey HKLM "Software\${APPNAME}"

    MessageBox MB_OK|MB_ICONINFORMATION "${APPNAME} 已成功卸载。$\n$\n注意：用户数据保留在 ${DATA_DIR}"
SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
```

### 自动化打包脚本
创建 `scripts/build.py`：
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
from pathlib import Path

VERSION = "1.0.0"
APP_NAME = "AI女友"

def run_command(cmd, cwd=None):
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"命令执行失败: {cmd}")
        sys.exit(1)

def clean_build():
    dirs_to_remove = ["build", "dist", "release"]
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"已删除: {d}")

def build_exe():
    print("正在使用PyInstaller打包...")
    run_command("pyinstaller scripts/build.spec", cwd="..")

def build_installer():
    print("正在使用NSIS制作安装程序...")
    if not os.path.exists("../release"):
        os.makedirs("../release")
    run_command("makensis scripts/installer.nsi", cwd="..")

def create_zip():
    print("正在创建发布压缩包...")
    zip_name = f"{APP_NAME}_v{VERSION}.zip"
    release_dir = Path("../release")
    installer_file = release_dir / f"{APP_NAME}_v{VERSION}_安装程序.exe"
    readme_file = Path("../docs/使用说明.txt")

    if not installer_file.exists():
        print(f"错误: 找不到安装程序 {installer_file}")
        sys.exit(1)

    temp_dir = release_dir / "temp_zip"
    temp_dir.mkdir(exist_ok=True)

    shutil.copy(installer_file, temp_dir)
    if readme_file.exists():
        shutil.copy(readme_file, temp_dir / "使用说明.txt")

    zip_path = release_dir / zip_name
    shutil.make_archive(str(zip_path).replace(".zip", ""), "zip", temp_dir)

    shutil.rmtree(temp_dir)
    print(f"压缩包已创建: {zip_path}")

def main():
    os.chdir(Path(__file__).parent)

    print("=" * 50)
    print(f"{APP_NAME} 自动打包脚本 v{VERSION}")
    print("=" * 50)

    clean_build()
    build_exe()
    build_installer()
    create_zip()

    print("\n" + "=" * 50)
    print("打包完成！")
    print(f"发布文件位于: {Path('../release').absolute()}")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

### 打包命令
```bash
# 方式一：使用自动化脚本（推荐）
cd scripts
python build.py

# 方式二：手动打包
# 1. 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 2. 使用PyInstaller打包
pyinstaller scripts/build.spec

# 3. 使用NSIS制作安装程序（需要先安装NSIS）
makensis scripts/installer.nsi

# 4. 手动创建压缩包
```

## 用户使用说明

### 简明使用步骤
1. 下载 `AI女友_v1.0.0.zip` 压缩包
2. 解压到任意位置
3. 双击运行 `AI女友_安装程序.exe`
4. 按照安装向导完成安装
5. 从桌面或开始菜单启动程序
6. 首次运行时在设置中配置API密钥
7. 开始使用！

### 首次配置
1. 启动程序后，点击设置按钮
2. 选择要使用的语言模型（如DeepSeek）
3. 输入你的API密钥
4. 保存配置
5. 返回聊天界面开始对话

### 注意事项
- 需要自行申请各模型的API密钥
- 对话数据保存在本地，不会上传到服务器
- 建议定期备份用户数据目录

## 注意事项
1. **API密钥安全**：加密存储API密钥，避免明文保存
2. **用户隐私保护**：对话数据本地存储，不上传服务器
3. **内容安全**：实现对话内容过滤，遵守相关法律法规
4. **记忆管理**：合理控制记忆数量，避免提示词过长
5. **模型成本**：提供使用统计和成本预估，避免超额消费
6. **多模型兼容性**：统一接口设计，方便扩展新模型
7. **语音质量**：提供多种语音选项，满足不同用户偏好
8. **打包体积优化**：排除不必要的依赖，减小安装包大小
9. **数据迁移**：升级时确保用户数据不丢失
10. **首次运行引导**：提供友好的首次使用向导
11. **安装体验**：NSIS安装程序提供专业的安装向导
12. **卸载友好**：卸载时保留用户数据，可选择性删除
