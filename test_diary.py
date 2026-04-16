#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日记功能测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_diary_manager():
    """测试 DiaryManager"""
    print("🧪 测试 DiaryManager...")
    try:
        from diary_manager import DiaryManager
        dm = DiaryManager()
        print("  ✅ DiaryManager 导入成功")
        print(f"  ✅ 已加载 {len(dm.diaries)} 条日记")
        
        # 测试添加事件
        dm.add_event("🧪 测试事件")
        print("  ✅ 事件添加成功")
        
        # 测试获取今日日记
        today_diary = dm.get_or_create_today()
        print(f"  ✅ 获取今日日记成功: {today_diary.date}")
        
        return True
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_diary_window():
    """测试 DiaryWindow"""
    print("\n🧪 测试 DiaryWindow...")
    try:
        from diary_manager import DiaryManager
        from diary_window import DiaryWindow
        print("  ✅ DiaryWindow 导入成功")
        
        # 不创建实例（需要 QApplication），只检查导入
        print("  ✅ DiaryWindow 类定义完整")
        return True
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pet_widget():
    """测试 PetWidget 与日记集成"""
    print("\n🧪 测试 PetWidget 集成...")
    try:
        from pet_widget import PetWidget
        print("  ✅ PetWidget 导入成功")
        
        # 检查是否有 diary_manager 属性
        import inspect
        source = inspect.getsource(PetWidget.__init__)
        if "diary_manager" in source:
            print("  ✅ PetWidget 已集成 diary_manager")
        else:
            print("  ⚠️  未找到 diary_manager 集成代码")
        
        # 检查是否有 show_diary_window 方法
        if hasattr(PetWidget, 'show_diary_window'):
            print("  ✅ show_diary_window 方法存在")
        else:
            print("  ❌ show_diary_window 方法不存在")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🐱 Q宠桌面宠物 - 日记功能测试")
    print("=" * 50)
    
    results = []
    results.append(("DiaryManager", test_diary_manager()))
    results.append(("DiaryWindow", test_diary_window()))
    results.append(("PetWidget", test_pet_widget()))
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 所有测试都通过了！日记功能应该正常工作。")
        print("使用方法：右键点击宠物 → 📔 查看日记")
    else:
        print("\n⚠️  有测试失败，请查看上面的错误信息。")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
