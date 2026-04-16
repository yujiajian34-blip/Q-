#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音效管理模块 - 处理音效播放
"""

import os
import sys
import wave
import threading
from pathlib import Path
from typing import Optional

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


class AudioManager:
    """音效播放管理器"""
    
    # 音效文件映射
    AUDIO_FILES = {
        'feed': '熊家肚子饿饿的.wav',
        'feed_satisfied': '好吃！谢谢主人~熊家好满足！.wav',
        'bath': '熊家洗香香啦~.wav',
        'sing': '唱歌啊哒哒.wav',
        'exercise': '动起来，熊家要运动.wav',
        'play': '和主人玩真开心！熊家好幸福~.wav',
        'tease': '哼！布布坏！熊家要欺负你！.wav',
        'happy': '今天心情超级好哒.wav',
        'sad': '熊家有点难过.wav',
        'angry': '哼，熊家生气了.wav',
        'praise': '布布最好了~熊家最喜欢布布！.wav',
        'love': '熊家爱你哦~么么哒！.wav',
        'greet': '主人好，熊家想你了.wav',
    }
    
    def __init__(self, audio_dir: str = None):
        """
        初始化音效管理器
        
        Args:
            audio_dir: 音效文件所在目录
        """
        if audio_dir is None:
            # 默认使用应用目录下的 wav 文件夹
            app_dir = os.path.dirname(os.path.abspath(__file__))
            audio_dir = os.path.join(app_dir, 'wav')
        
        self.audio_dir = Path(audio_dir)
        self.is_playing = False
        self.current_thread = None
        
        # 检查音效目录
        if not self.audio_dir.exists():
            print(f"⚠️  音效目录不存在: {self.audio_dir}")
    
    def get_audio_path(self, audio_key: str) -> Optional[Path]:
        """获取音效文件路径"""
        if audio_key not in self.AUDIO_FILES:
            print(f"❌ 未知的音效: {audio_key}")
            return None
        
        audio_file = self.audio_dir / self.AUDIO_FILES[audio_key]
        if not audio_file.exists():
            print(f"⚠️  音效文件不存在: {audio_file}")
            return None
        
        return audio_file
    
    def play_audio(self, audio_key: str, async_mode: bool = True) -> bool:
        """
        播放音效
        
        Args:
            audio_key: 音效键值（见 AUDIO_FILES）
            async_mode: 是否异步播放（不阻塞）
        
        Returns:
            是否成功启动播放
        """
        audio_path = self.get_audio_path(audio_key)
        if not audio_path:
            return False
        
        if async_mode:
            # 异步播放，不阻塞
            thread = threading.Thread(
                target=self._play_wav_file,
                args=(audio_path,),
                daemon=True
            )
            thread.start()
            self.current_thread = thread
            return True
        else:
            # 同步播放
            return self._play_wav_file(audio_path)
    
    def _play_wav_file(self, file_path: Path) -> bool:
        """
        使用 PyAudio 播放 WAV 文件
        
        Args:
            file_path: WAV 文件路径
        
        Returns:
            是否成功
        """
        if not PYAUDIO_AVAILABLE:
            print("⚠️  PyAudio 未安装，尝试使用 Windows 音效 API")
            return self._play_with_windows_api(file_path)
        
        try:
            self.is_playing = True
            
            with wave.open(str(file_path), 'rb') as wav_file:
                # 获取音频参数
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                
                # 创建 PyAudio 实例
                pa = pyaudio.PyAudio()
                
                # 打开流
                stream = pa.open(
                    format=pa.get_format_from_width(sample_width),
                    channels=n_channels,
                    rate=frame_rate,
                    output=True,
                    frames_per_buffer=2048
                )
                
                # 读取并播放音频
                chunk_size = 2048
                while True:
                    data = wav_file.readframes(chunk_size)
                    if not data:
                        break
                    stream.write(data)
                
                # 清理资源
                stream.stop_stream()
                stream.close()
                pa.terminate()
            
            self.is_playing = False
            return True
        
        except Exception as e:
            print(f"❌ 播放失败: {e}")
            self.is_playing = False
            return False
    
    def _play_with_windows_api(self, file_path: Path) -> bool:
        """使用 Windows API 播放音效"""
        try:
            import winsound
            winsound.PlaySound(str(file_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            return True
        except Exception as e:
            print(f"⚠️  Windows 音效 API 失败: {e}")
            return False
    
    def stop_audio(self):
        """停止播放"""
        self.is_playing = False
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=1)
    
    def list_available_sounds(self) -> dict:
        """列出可用的音效"""
        available = {}
        for key, filename in self.AUDIO_FILES.items():
            path = self.audio_dir / filename
            if path.exists():
                available[key] = filename
        return available


# 全局实例
_audio_manager: Optional[AudioManager] = None


def get_audio_manager() -> AudioManager:
    """获取全局音效管理器实例"""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager


def play_sound(audio_key: str) -> bool:
    """便捷函数：播放音效"""
    manager = get_audio_manager()
    return manager.play_audio(audio_key, async_mode=True)


if __name__ == '__main__':
    # 测试音效播放
    print("🎵 音效播放测试\n")
    
    manager = AudioManager()
    
    print("📋 可用的音效:")
    available = manager.list_available_sounds()
    for key, filename in sorted(available.items()):
        print(f"  • {key:15} -> {filename}")
    
    if available:
        print("\n🎧 测试播放第一个音效...")
        first_key = list(available.keys())[0]
        print(f"播放: {first_key}")
        manager.play_audio(first_key, async_mode=False)
        print("✅ 播放完成")
