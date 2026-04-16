#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日记窗口快速测试 - 无阻塞版本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 开始测试日记窗口...")

try:
    print("  1️⃣ 测试模块导入...")
    from diary_manager import DiaryManager
    print("     ✅ diary_manager 导入成功")
    
    from diary_window import DiaryWindow
    print("     ✅ diary_window 导入成功")
    
    print("\n  2️⃣ 创建 DiaryManager...")
    dm = DiaryManager()
    print(f"     ✅ 创建成功，已加载 {len(dm.diaries)} 条日记")
    
    print("\n  3️⃣ 尝试创建 DiaryWindow（不需要 QApplication）...")
    print("     警告：这将失败，因为需要 QApplication")
    print("     但我们可以检查类定义是否完整")
    
    # 检查 DiaryWindow 的方法
    methods = [m for m in dir(DiaryWindow) if not m.startswith('_')]
    print(f"\n     DiaryWindow 有 {len(methods)} 个public方法:")
    
    important_methods = [
        'init_ui',
        'load_today',
        'load_diaries_list',
        'load_diary_content',
        'save_diary',
        'delete_diary',
        'show_diary_window'
    ]
    
    for method in important_methods:
        if hasattr(DiaryWindow, method):
            print(f"     ✅ {method}")
        else:
            print(f"     ❌ {method} 缺失！")
    
    print("\n✅ 所有模块检查完成！")
    print("\n💡 要打开日记窗口，需要:")
    print("   1. 运行主程序: python main.py")
    print("   2. 右键点击宠物")
    print("   3. 选择 '📔 查看日记'")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
