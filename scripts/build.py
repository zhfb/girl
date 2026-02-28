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


def build_portable_exe():
    print("\n" + "=" * 50)
    print("正在打包便携版（单文件 exe）...")
    print("=" * 50)
    run_command("pyinstaller scripts/build_portable.spec", cwd="..")


def build_installer_exe():
    print("\n" + "=" * 50)
    print("正在打包安装版（文件夹形式）...")
    print("=" * 50)
    run_command("pyinstaller scripts/build.spec", cwd="..")


def build_installer():
    print("\n" + "=" * 50)
    print("正在使用NSIS制作安装程序...")
    print("=" * 50)
    if not os.path.exists("../release"):
        os.makedirs("../release")
    run_command("makensis scripts/installer.nsi", cwd="..")


def create_portable_zip():
    print("\n" + "=" * 50)
    print("正在创建便携版压缩包...")
    print("=" * 50)
    zip_name = f"{APP_NAME}_v{VERSION}_便携版.zip"
    release_dir = Path("../release")
    portable_exe = Path("../dist/AIGirlfriend.exe")
    readme_file = Path("../docs/使用说明.txt")

    if not portable_exe.exists():
        print(f"错误: 找不到便携版 exe {portable_exe}")
        return

    temp_dir = release_dir / "temp_portable"
    temp_dir.mkdir(exist_ok=True)

    shutil.copy(portable_exe, temp_dir)
    (temp_dir / "portable.txt").write_text("便携版模式\n数据存储在 data/ 目录下", encoding="utf-8")
    if readme_file.exists():
        shutil.copy(readme_file, temp_dir / "使用说明.txt")

    zip_path = release_dir / zip_name
    shutil.make_archive(str(zip_path).replace(".zip", ""), "zip", temp_dir)

    shutil.rmtree(temp_dir)
    print(f"便携版压缩包已创建: {zip_path}")


def create_installer_zip():
    print("\n" + "=" * 50)
    print("正在创建安装版压缩包...")
    print("=" * 50)
    zip_name = f"{APP_NAME}_v{VERSION}_安装版.zip"
    release_dir = Path("../release")
    installer_file = release_dir / f"{APP_NAME}_v{VERSION}_安装程序.exe"
    readme_file = Path("../docs/使用说明.txt")

    if not installer_file.exists():
        print(f"错误: 找不到安装程序 {installer_file}")
        return

    temp_dir = release_dir / "temp_installer"
    temp_dir.mkdir(exist_ok=True)

    shutil.copy(installer_file, temp_dir)
    if readme_file.exists():
        shutil.copy(readme_file, temp_dir / "使用说明.txt")

    zip_path = release_dir / zip_name
    shutil.make_archive(str(zip_path).replace(".zip", ""), "zip", temp_dir)

    shutil.rmtree(temp_dir)
    print(f"安装版压缩包已创建: {zip_path}")


def main():
    os.chdir(Path(__file__).parent)

    print("=" * 50)
    print(f"{APP_NAME} 自动打包脚本 v{VERSION}")
    print("=" * 50)
    print("\n本脚本将生成两个版本：")
    print("1. 便携版 - 解压后直接运行 exe，数据存储在程序目录")
    print("2. 安装版 - 使用 NSIS 安装程序")
    print("=" * 50)

    clean_build()
    build_portable_exe()
    build_installer_exe()
    build_installer()
    create_portable_zip()
    create_installer_zip()

    print("\n" + "=" * 50)
    print("打包完成！")
    print(f"发布文件位于: {Path('../release').absolute()}")
    print("\n生成的文件：")
    print(f"  - {APP_NAME}_v{VERSION}_便携版.zip")
    print(f"  - {APP_NAME}_v{VERSION}_安装版.zip")
    print("=" * 50)


if __name__ == "__main__":
    main()
