#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成占位符 WAV 文件的脚本
用于在没有真实音效的情况下测试项目
"""

import wave
import struct
import os
import sys

def generate_placeholder_wav(filename, duration=2, frequency=440):
    """
    生成占位符 WAV 文件（简单的正弦波）
    
    参数：
    - filename: 输出文件名
    - duration: 时长（秒）
    - frequency: 频率（Hz）
    """
    sample_rate = 44100  # 采样率
    num_samples = int(sample_rate * duration)
    
    try:
        # 创建 WAV 文件
        with wave.open(filename, 'wb') as wav_file:
            # 参数：通道数、采样宽度、采样率、帧数、压缩类型、压缩名
            wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
            
            # 生成简单的正弦波
            for i in range(num_samples):
                # 计算正弦波值
                sample = int(32767 * 0.3 * 
                           (((i / sample_rate) * frequency) % 1.0) * 2 - 1)
                # 写入采样值
                wav_file.writeframes(struct.pack('<h', sample))
        
        print(f"✅ 已生成: {filename}")
        return True
    except Exception as e:
        print(f"❌ 生成失败 {filename}: {e}")
        return False

def main():
    """主函数"""
    wav_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(wav_dir)
    
    print("🎵 生成占位符 WAV 文件...\n")
    
    # 需要生成的音效文件列表
    sound_files = {
        "熊家肚子饿饿的.wav": 880,          # 高音
        "今天心情超级好哒.wav": 523,        # 中高音
        "熊家有点难过.wav": 294,            # 低音
        "哼，熊家生气了.wav": 392,          # 中音
        "好吃！谢谢主人~熊家好满足！.wav": 440,
        "熊家洗香香啦~.wav": 523,
        "唱歌啊哒哒.wav": 587,
        "动起来，熊家要运动.wav": 659,
        "主人好，熊家想你了.wav": 523,
        "和主人玩真开心！熊家好幸福~.wav": 659,
        "熊家爱你哦~么么哒！.wav": 784,
        "布布最好了~熊家最喜欢布布！.wav": 698,
        "哼！布布坏！熊家要欺负你！.wav": 329,
    }
    
    print(f"📊 将生成 {len(sound_files)} 个音效文件\n")
    
    success_count = 0
    for filename, frequency in sound_files.items():
        if generate_placeholder_wav(filename, duration=2, frequency=frequency):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"✅ 完成: {success_count}/{len(sound_files)} 个文件")
    print(f"{'='*50}")
    
    if success_count == len(sound_files):
        print("\n🎉 所有占位符音效已生成！")
        print("💡 你现在可以运行项目了，音效会正常播放（但使用的是占位符音）")
        print("📝 要更换成真实音效，请参考 README.md")
        return True
    else:
        print(f"\n⚠️  有 {len(sound_files) - success_count} 个文件生成失败")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
