#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Q宠 打包脚本 - 使用 PyInstaller 生成独立 exe
"""

import PyInstaller.__main__
import os
import sys

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(project_root, "main.py")
wav_folder = os.path.join(project_root, "wav")

print("=" * 70)
print("Q宠 exe 打包程序")
print("=" * 70)
print(f"项目路径: {project_root}")
print()

# PyInstaller 打包配置
args = [
    main_script,
    '--onefile',                           # 生成单个 exe 文件
    '--windowed',                          # 无控制台窗口
    '--name=Q宠',                          # exe 文件名
    f'--distpath={project_root}\\dist',    # 输出目录
    f'--workpath={project_root}\\build',   # 工作目录
    f'--specpath={project_root}',          # spec 文件目录
    '--hidden-import=audio_manager',
    '--hidden-import=data_manager',
    '--hidden-import=state_manager',
    '--hidden-import=diary_manager',
    '--hidden-import=diary_window',
    '--hidden-import=pet_widget',
]

# 添加资源文件夹（包含所有 webp 和 wav 文件）
# 使用相对路径确保打包后 exe 能找到资源
if os.path.exists(wav_folder):
    args.append(f'--add-data={wav_folder}{os.pathsep}wav')
    print(f"✓ 包含音频文件夹: {wav_folder}")

# 添加 webp 动画文件
webp_count = 0
for file in os.listdir(project_root):
    if file.endswith('.webp'):
        webp_path = os.path.join(project_root, file)
        args.append(f'--add-data={webp_path}{os.pathsep}.')
        webp_count += 1

print(f"✓ 包含 {webp_count} 个动画文件")
print()
print("开始打包...(这可能需要几分钟)")
print()

try:
    PyInstaller.__main__.run(args)
    print()
    print("=" * 70)
    print("✅ 打包成功！")
    print("=" * 70)
    exe_path = os.path.join(project_root, "dist", "Q宠.exe")
    print(f"\n📦 exe 文件位置:")
    print(f"   {exe_path}")
    print(f"\n💡 使用方法:")
    print(f"   1. 直接双击 Q宠.exe 运行")
    print(f"   2. 或在 Windows Explorer 中打开 dist 文件夹")
    print()
except Exception as e:
    print()
    print("=" * 70)
    print(f"❌ 打包失败")
    print("=" * 70)
    print(f"错误: {e}")
    print()
    sys.exit(1)
