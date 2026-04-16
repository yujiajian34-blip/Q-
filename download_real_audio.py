#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从GitHub下载真实的WAV音效文件
"""

import os
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# 音效文件列表
AUDIO_FILES = [
    "主人好，熊家想你了.wav",
    "今天心情超级好哒.wav",
    "动起来，熊家要运动.wav",
    "和主人玩真开心！熊家好幸福~.wav",
    "哼！布布坏！熊家要欺负你！.wav",
    "哼，熊家生气了.wav",
    "唱歌啊哒哒.wav",
    "好吃！谢谢主人~熊家好满足！.wav",
    "布布最好了~熊家最喜欢布布！.wav",
    "熊家有点难过.wav",
    "熊家洗香香啦~.wav",
    "熊家爱你哦~么么哒！.wav",
    "熊家肚子饿饿的.wav",
]

# GitHub仓库信息
GITHUB_BASE = "https://raw.githubusercontent.com/yujiajian34-blip/q-pet/main/wav"

# 本地保存路径
WAV_DIR = Path("wav")
WAV_DIR.mkdir(exist_ok=True)

print("\n" + "="*60)
print("🎵 从GitHub下载真实的WAV音效文件")
print("="*60)

success_count = 0
fail_count = 0

for filename in AUDIO_FILES:
    # URL编码文件名
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
    url = f"{GITHUB_BASE}/{encoded_filename}"
    filepath = WAV_DIR / filename
    
    # 显示进度
    print(f"\n📥 正在下载: {filename}")
    
    try:
        # 下载文件
        print(f"   源: {url[:70]}...")
        urllib.request.urlretrieve(url, filepath)
        
        # 检查文件大小
        file_size = filepath.stat().st_size
        if file_size > 1000:  # 至少1KB
            print(f"   ✅ 成功下载 ({file_size} bytes)")
            success_count += 1
        else:
            print(f"   ❌ 文件过小 ({file_size} bytes)，可能是空文件")
            fail_count += 1
            
    except urllib.error.URLError as e:
        print(f"   ❌ 下载失败: {e}")
        fail_count += 1
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        fail_count += 1

# 总结
print("\n" + "="*60)
print("📊 下载总结")
print("="*60)
print(f"✅ 成功: {success_count}/{len(AUDIO_FILES)}")
print(f"❌ 失败: {fail_count}/{len(AUDIO_FILES)}")

if success_count == len(AUDIO_FILES):
    print("\n🎉 所有文件下载成功！")
    print("💡 现在重启应用后应该能听到真实的语音了")
elif success_count > 0:
    print(f"\n⚠️  成功下载 {success_count} 个文件，部分失败")
    print("💡 失败的文件可能是网络问题，请重试")
else:
    print("\n❌ 全部下载失败")
    print("💡 请检查网络连接或GitHub仓库")

print("="*60 + "\n")
