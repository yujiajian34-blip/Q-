# -*- coding: utf-8 -*-
"""
心里话管理系统
用户可以记录自己的想法和心事
"""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict


class InnerThought:
    """单条心里话"""
    
    def __init__(self, content: str, mood: str = "普通", date: str = None):
        self.content = content
        self.mood = mood  # 心情标签：开心、普通、难过、感慨、感谢、甜蜜等
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "mood": self.mood,
            "date": self.date,
            "timestamp": self.timestamp
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'InnerThought':
        thought = InnerThought(
            content=data.get("content", ""),
            mood=data.get("mood", "普通"),
            date=data.get("date", "")
        )
        thought.timestamp = data.get("timestamp", thought.timestamp)
        return thought


class InnerThoughtsManager:
    """心里话管理器"""
    
    THOUGHTS_FILE = "inner_thoughts.json"
    
    # 心情标签
    MOOD_TAGS = ["开心", "普通", "难过", "感慨", "感谢", "甜蜜", "期待", "伤心"]
    
    def __init__(self):
        self.thoughts: List[InnerThought] = []
        self.today_thoughts: List[InnerThought] = []
        self.load_thoughts()
        self.load_today_thoughts()
    
    def load_thoughts(self):
        """加载所有心里话"""
        if os.path.exists(self.THOUGHTS_FILE):
            try:
                with open(self.THOUGHTS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.thoughts = [InnerThought.from_dict(item) for item in data.get('thoughts', [])]
            except Exception as e:
                print(f"加载心里话失败: {e}")
                self.thoughts = []
    
    def save_thoughts(self):
        """保存所有心里话"""
        try:
            data = {
                'thoughts': [thought.to_dict() for thought in self.thoughts],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.THOUGHTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存心里话失败: {e}")
    
    def add_thought(self, content: str, mood: str = "普通") -> InnerThought:
        """添加新心里话"""
        thought = InnerThought(content, mood)
        self.thoughts.append(thought)
        self.today_thoughts.append(thought)
        self.save_thoughts()
        return thought
    
    def load_today_thoughts(self):
        """加载今天的心里话"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.today_thoughts = [
            t for t in self.thoughts 
            if t.date.startswith(today)
        ]
    
    def get_today_thoughts(self) -> List[InnerThought]:
        """获取今天的心里话"""
        self.load_today_thoughts()
        return self.today_thoughts
    
    def get_thoughts_by_date(self, date_str: str) -> List[InnerThought]:
        """获取特定日期的心里话"""
        return [
            t for t in self.thoughts 
            if t.date.startswith(date_str)
        ]
    
    def get_all_thoughts(self) -> List[InnerThought]:
        """获取所有心里话"""
        return self.thoughts
    
    def get_recent_thoughts(self, days: int = 7) -> List[InnerThought]:
        """获取最近N天的心里话"""
        from datetime import timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return [t for t in self.thoughts if t.date >= cutoff_date]
    
    def delete_thought(self, index: int):
        """删除指定心里话"""
        if 0 <= index < len(self.thoughts):
            self.thoughts.pop(index)
            self.save_thoughts()
            return True
        return False
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        self.load_today_thoughts()
        today_count = len(self.today_thoughts)
        total_count = len(self.thoughts)
        
        # 统计心情分布
        mood_dist = {}
        for mood in self.MOOD_TAGS:
            mood_dist[mood] = len([t for t in self.thoughts if t.mood == mood])
        
        return {
            'today_count': today_count,
            'total_count': total_count,
            'mood_distribution': mood_dist
        }
    
    def get_thoughts_summary(self, max_length: int = 500) -> str:
        """获取最近心里话的总结（用于日记生成）"""
        recent = self.get_recent_thoughts(days=3)
        if not recent:
            return ""
        
        # 获取最多3条最近的心里话
        summary_thoughts = recent[-3:] if len(recent) >= 3 else recent
        
        summary = "最近的心里话:\n"
        for i, thought in enumerate(summary_thoughts, 1):
            # 心里话过长则截断
            content = thought.content[:100] + "..." if len(thought.content) > 100 else thought.content
            summary += f"{i}. ({thought.mood}): {content}\n"
        
        return summary[:max_length]
