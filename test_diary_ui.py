#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日记窗口测试脚本 - 独立测试
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from diary_manager import DiaryManager
from diary_window import DiaryWindow

def test_diary_window_ui():
    """测试日记窗口UI"""
    print("🧪 测试日记窗口UI...")
    
    try:
        # 创建 QApplication
        app = QApplication(sys.argv)
        print("  ✅ QApplication 创建成功")
        
        # 创建 DiaryManager
        diary_manager = DiaryManager()
        print("  ✅ DiaryManager 创建成功")
        
        # 创建日记窗口
        diary_window = DiaryWindow(diary_manager)
        print("  ✅ DiaryWindow 创建成功")
        
        # 显示窗口
        diary_window.show()
        print("  ✅ DiaryWindow 显示成功")
        
        # 获取窗口信息
        print(f"\n  📊 窗口信息：")
        print(f"     标题: {diary_window.windowTitle()}")
        print(f"     大小: {diary_window.width()}x{diary_window.height()}")
        print(f"     位置: ({diary_window.x()}, {diary_window.y()})")
        
        # 运行应用（可选，按 Ctrl+C 退出）
        print("\n  💡 窗口已打开，按 Ctrl+C 关闭...")
        print("  💡 或者关闭窗口以自动退出\n")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_diary_window_ui()
    sys.exit(0 if success else 1)
