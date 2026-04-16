#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
思维气泡 + 日记系统 测试脚本
"""

import os
import sys
from datetime import datetime, timedelta

# 测试 1: 思维气泡管理器
print("=" * 70)
print("测试 1: 思维气泡管理器")
print("=" * 70)

try:
    from bubble_manager import BubbleManager, BubbleTheme
    
    manager = BubbleManager()
    print(f"✅ BubbleManager 初始化成功")
    print(f"   共有 {sum(len(v) for v in manager.bubble_pool.values())} 条气泡内容")
    print(f"   主题数量: {len(BubbleTheme)}")
    
    # 测试获取气泡
    for theme in list(BubbleTheme)[:3]:
        bubble = manager.get_bubble(theme)
        duration = manager.get_bubble_duration(bubble) if bubble else 0
        print(f"   • {theme.name:12s}: '{bubble[:20]}...' ({duration}ms)")
    
    # 测试关联气泡
    contextual = manager.get_contextual_bubble('feed')
    print(f"   • 行为关联(feed): '{contextual[:20]}...' " if contextual else "   • 行为关联(feed): None")
    
except Exception as e:
    print(f"❌ BubbleManager 测试失败: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试 2: 日记生成器
print("=" * 70)
print("测试 2: 日记生成器")
print("=" * 70)

try:
    from diary_generator import DiaryGenerator
    
    gen = DiaryGenerator()
    print(f"✅ DiaryGenerator 初始化成功")
    
    # 清除测试日期的日记（防止重复）
    test_date = datetime.now()
    test_stats = {
        'clicks': 8,
        'drags': 2,
        'throws': 1,
        'mood': 75,
        'day_count': 5,
        'behaviors_played': 6,
    }
    
    diary = gen.generate_daily_diary(test_stats)
    print(f"   • 生成日记长度: {len(diary)} 字")
    print(f"   • 日记开头: {diary[:30]}...")
    print(f"   • 日记结尾: ...{diary[-30:]}")
    
    # 测试读取日记
    retrieved = gen.get_diary_by_date(test_date)
    if retrieved:
        print(f"   ✅ 日记已保存并可读取")
    
    # 统计信息
    stats = gen.get_statistics()
    print(f"   • 总日记数: {stats['total_diaries']}")
    print(f"   • 总互动数: {stats['total_interactions']}")
    
except Exception as e:
    print(f"❌ DiaryGenerator 测试失败: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试 3: 集成检查
print("=" * 70)
print("测试 3: 模块集成检查")
print("=" * 70)

try:
    # 检查所有必需的类和方法都能导入
    from pet_widget import PetWidget
    from bubble_manager import BubbleManager
    from diary_generator import DiaryGenerator
    from diary_notebook_window import DiaryNotebookWindow
    
    print("✅ 所有模块导入成功！")
    print("   • PetWidget")
    print("   • BubbleManager")
    print("   • DiaryGenerator")
    print("   • DiaryNotebookWindow")
    
    # 检查 pet_widget 中的新方法
    import inspect
    members = inspect.getmembers(PetWidget, predicate=inspect.isfunction)
    method_names = [name for name, _ in members]
    
    required_methods = ['show_thinking_bubble', 'show_diary_notebook']
    for method in required_methods:
        if method in method_names:
            print(f"   ✅ 方法 {method} 已添加")
        else:
            print(f"   ❌ 方法 {method} 缺失")
    
except Exception as e:
    print(f"❌ 集成检查失败: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试 4: JSON 文件检查
print("=" * 70)
print("测试 4: 数据文件检查")
print("=" * 70)

try:
    import json
    
    if os.path.exists('pet_diary.json'):
        with open('pet_diary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            diaries = data.get('diaries', [])
            print(f"✅ 日记文件存在并有效")
            print(f"   • 包含 {len(diaries)} 篇日记")
            if diaries:
                latest = diaries[-1]
                print(f"   • 最新日记: {latest['date']}")
    else:
        print(f"⚠️  日记文件不存在（首次运行会自动创建）")
        
except Exception as e:
    print(f"❌ 文件检查失败: {e}")

print()

# 测试总结
print("=" * 70)
print("✨ 所有测试完成！")
print("=" * 70)
print()
print("接下来你可以：")
print("1. 运行 python main.py 启动程序")
print("2. 右键点击熊家 → '📖 查看熊家的日记本'查看新日记窗口")
print("3. 等待 90-240 秒观看思维气泡随机出现")
print("4. 与熊家互动，每天都会生成新的日记！")
print()
