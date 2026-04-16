#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试音效播放
"""

import sys
import time
from pathlib import Path
from audio_manager import get_audio_manager, play_sound

print("\n🎵 测试音效播放系统\n")

# 初始化管理器
manager = get_audio_manager()

# 检查可用音效
available = manager.list_available_sounds()
print(f"✅ 找到 {len(available)} 个音效文件")
print("\n应用中集成的音效映射:")
for key, filename in sorted(manager.AUDIO_FILES.items()):
    status = "✅" if key in available else "❌"
    print(f"  {status} {key:15} -> {filename}")

# 尝试播放第一个音效
if available:
    print(f"\n🔊 测试播放...")
    first_key = list(sorted(available.keys()))[0]
    print(f"正在播放: {first_key}")
    
    try:
        result = play_sound(first_key)
        if result:
            print(f"✅ 已启动播放({first_key})")
            print("   (异步模式 - 不阻塞)")
            # 等待一下让音效播放
            time.sleep(3)
        else:
            print(f"❌ 播放失败")
    except Exception as e:
        print(f"❌ 错误: {e}")
else:
    print("\n❌ 没有找到任何音效文件")

print("\n✅ 测试完成！")
print("\n💡 提示:")
print("   • 如果没有声音，可能是:")
print("     - PyAudio 未安装（会自动使用 Windows winsound）")
print("     - 系统音量设置为静音")
print("     - 音效文件格式不兼容")
