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
