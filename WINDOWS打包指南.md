# AI女友 - Windows打包指南

## 前置准备（在Windows电脑上）

### 1. 安装Python 3.9+
从 https://www.python.org/downloads/ 下载安装

### 2. 安装NSIS
从 https://nsis.sourceforge.io/Download 下载最新版并安装

### 3. 克隆或下载项目代码到Windows电脑

## 打包步骤

### 第一步：安装依赖
```cmd
cd 项目目录
pip install -r requirements.txt
```

### 第二步：使用PyInstaller打包（文件夹模式）
```cmd
pyinstaller scripts/build.spec
```

完成后，会在 `dist/AIGirlfriend/` 目录下看到：
- `AIGirlfriend.exe` - 主程序
- 所有依赖的库文件
- `config/` - 配置文件
- `docs/` - 文档

### 第三步：使用NSIS制作安装程序
```cmd
cd scripts
makensis installer.nsi
```

完成后，会在 `release/` 目录下生成：
- `AI女友_v1.0.0_安装程序.exe`

## 生成的文件

打包完成后，您将获得：
1. `dist/AIGirlfriend/` - 完整的程序文件夹（可直接运行）
2. `release/AI女友_v1.0.0_安装程序.exe` - 类似百度网盘的安装程序

## 安装程序特点

- 类似百度网盘的安装向导界面
- 需要管理员权限运行
- 默认安装到 `C:\Program Files\AI女友\`
- 创建桌面快捷方式和开始菜单项
- 用户数据存储在 `%APPDATA%\AIGirlfriend\`
- 卸载时保留用户数据

## 便携版打包（可选）

如果您也需要便携版，可以运行：
```cmd
pyinstaller scripts/build_portable.spec
```

这会生成单个exe文件，数据存储在程序目录的data/文件夹下。
