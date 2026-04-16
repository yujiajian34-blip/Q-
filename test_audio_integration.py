#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音效集成和应用功能
"""

import os
import sys
import json
from pathlib import Path

# 测试1: 检查wav文件夹
def test_wav_files():
    print("\n" + "="*50)
    print("🎵 测试1: 检查音效文件")
    print("="*50)
    
    wav_dir = Path("c:\\Users\\yujj\\Desktop\\Q12\\Q-\\wav")
    if not wav_dir.exists():
        print("❌ wav文件夹不存在")
        return False
    
    wav_files = list(wav_dir.glob("*.wav"))
    print(f"✅ 找到 {len(wav_files)} 个WAV文件")
    
    for wav_file in sorted(wav_files):
        file_size = wav_file.stat().st_size
        print(f"   📄 {wav_file.name} ({file_size} bytes)")
    
    return len(wav_files) == 13

# 测试2: 检查日记数据
def test_diary_data():
    print("\n" + "="*50)
    print("📔 测试2: 检查日记数据")
    print("="*50)
    
    diary_file = Path("c:\\Users\\yujj\\Desktop\\Q12\\Q-\\pet_diary.json")
    if not diary_file.exists():
        print("⚠️  日记文件不存在（首次运行）")
        return True
    
    try:
        with open(diary_file, 'r', encoding='utf-8') as f:
            diary_data = json.load(f)
        
        print(f"✅ 日记文件有效，包含 {len(diary_data)} 条记录")
        
        # 显示最近的日记
        for date in list(diary_data.keys())[-3:]:
            entry = diary_data[date]
            mood = entry.get('mood', '未记录')
            events = entry.get('events', [])
            print(f"   📅 {date}: 心情={mood}, 事件={len(events)}件")
            if events:
                for event in events[-2:]:
                    print(f"      - {event}")
        
        return True
    except Exception as e:
        print(f"❌ 日记文件错误: {e}")
        return False

# 测试3: 检查应用配置
def test_app_config():
    print("\n" + "="*50)
    print("⚙️  测试3: 检查应用配置文件")
    print("="*50)
    
    pet_save = Path("c:\\Users\\yujj\\Desktop\\Q12\\Q-\\pet_save.json")
    if not pet_save.exists():
        print("⚠️  宠物存档不存在（首次运行）")
        return True
    
    try:
        with open(pet_save, 'r', encoding='utf-8') as f:
            pet_data = json.load(f)
        
        print(f"✅ 宠物存档有效")
        print(f"   🐻 饥饿值: {pet_data.get('hunger', 'N/A')}")
        print(f"   😊 心情值: {pet_data.get('mood', 'N/A')}")
        print(f"   💪 精力值: {pet_data.get('energy', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ 宠物存档错误: {e}")
        return False

# 测试4: 检查必要的Python模块
def test_modules():
    print("\n" + "="*50)
    print("📦 测试4: 检查Python依赖模块")
    print("="*50)
    
    required_modules = {
        'PyQt5': 'PyQt5.QtWidgets',
        'wave': 'wave',
        'struct': 'struct',
        'json': 'json',
    }
    
    all_ok = True
    for name, module in required_modules.items():
        try:
            __import__(module)
            print(f"✅ {name} 已安装")
        except ImportError:
            print(f"❌ {name} 未安装")
            all_ok = False
    
    return all_ok

# 测试5: 检查音效播放能力
def test_audio_playback():
    print("\n" + "="*50)
    print("🔊 测试5: 检查音效播放能力")
    print("="*50)
    
    try:
        import wave
        
        # 测试读取一个音效文件
        test_file = Path("c:\\Users\\yujj\\Desktop\\Q12\\Q-\\wav\\熊家肚子饿饿的.wav")
        if not test_file.exists():
            print("❌ 测试音效文件不存在")
            return False
        
        with wave.open(str(test_file), 'rb') as wav:
            n_frames = wav.getnframes()
            frame_rate = wav.getframerate()
            duration = n_frames / frame_rate
            
            print(f"✅ 音效文件可读")
            print(f"   采样率: {frame_rate} Hz")
            print(f"   帧数: {n_frames}")
            print(f"   时长: {duration:.2f} 秒")
        
        return True
    except Exception as e:
        print(f"❌ 音效读取失败: {e}")
        return False

# 主测试函数
def main():
    print("\n╔" + "="*48 + "╗")
    print("║" + " 🎮 Q宠桌面宠物 - 集成测试报告 ".center(48) + "║")
    print("╚" + "="*48 + "╝")
    
    results = {
        "音效文件": test_wav_files(),
        "日记数据": test_diary_data(),
        "应用配置": test_app_config(),
        "Python模块": test_modules(),
        "音效播放": test_audio_playback(),
    }
    
    print("\n" + "="*50)
    print("📊 测试总结")
    print("="*50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ 全部测试通过！应用已准备好使用")
        print("\n📝 使用说明:")
        print("   1. 右键点击宠物可以进行互动")
        print("   2. 点击菜单可以查看日记")
        print("   3. 所有操作都会自动记录到日记中")
        print("   4. 支持以下操作音效:")
        print("      - 🍖 喂食")
        print("      - 🛁 洗澡")
        print("      - 🎵 唱歌")
        print("      - 🏃 运动")
        print("      - 🤗 玩耍")
    else:
        print("⚠️  部分测试未通过，请检查上方错误信息")
    print("="*50 + "\n")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
