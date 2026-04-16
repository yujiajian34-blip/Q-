import json
import os
from datetime import datetime
from typing import List, Optional, Dict
from data_manager import Mood

class DiaryEntry:
    """日记条目类"""
    def __init__(self, date: str, mood: str, content: str, events: List[str] = None):
        self.date = date  # 格式: YYYY-MM-DD
        self.mood = mood  # 心情：开心、普通、难过、生气
        self.content = content  # 日记内容
        self.events = events or []  # 当天发生的事件（喂食、互动等）
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "mood": self.mood,
            "content": self.content,
            "events": self.events,
            "timestamp": self.timestamp
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'DiaryEntry':
        entry = DiaryEntry(
            date=data.get("date", ""),
            mood=data.get("mood", "普通"),
            content=data.get("content", ""),
            events=data.get("events", [])
        )
        entry.timestamp = data.get("timestamp", entry.timestamp)
        return entry


class DiaryManager:
    """日记管理器"""
    DIARY_FILE = "pet_diary.json"
    
    def __init__(self):
        self.diaries: Dict[str, DiaryEntry] = {}
        self.load_diaries()
    
    def get_today_date(self) -> str:
        """获取今天的日期"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def add_event(self, event: str):
        """添加当天事件"""
        today = self.get_today_date()
        if today not in self.diaries:
            self.diaries[today] = DiaryEntry(
                date=today,
                mood="普通",
                content="",
                events=[]
            )
        
        if event not in self.diaries[today].events:
            self.diaries[today].events.append(event)
        self.save_diaries()
    
    def get_or_create_today(self) -> DiaryEntry:
        """获取或创建今天的日记"""
        today = self.get_today_date()
        if today not in self.diaries:
            self.diaries[today] = DiaryEntry(
                date=today,
                mood="普通",
                content="",
                events=[]
            )
        return self.diaries[today]
    
    def update_today_diary(self, content: str, mood: str = None):
        """更新今天的日记"""
        entry = self.get_or_create_today()
        entry.content = content
        if mood:
            entry.mood = mood
        self.save_diaries()
    
    def update_diary(self, date: str, content: str, mood: str = None):
        """更新指定日期的日记"""
        if date not in self.diaries:
            self.diaries[date] = DiaryEntry(
                date=date,
                mood=mood or "普通",
                content=content,
                events=[]
            )
        else:
            self.diaries[date].content = content
            if mood:
                self.diaries[date].mood = mood
        self.save_diaries()
    
    def get_diary_by_date(self, date: str) -> Optional[DiaryEntry]:
        """获取指定日期的日记"""
        return self.diaries.get(date)
    
    def get_all_diaries(self) -> List[DiaryEntry]:
        """获取所有日记（按日期倒序）"""
        return sorted(
            self.diaries.values(),
            key=lambda x: x.date,
            reverse=True
        )
    
    def get_recent_diaries(self, days: int = 30) -> List[DiaryEntry]:
        """获取最近N天的日记"""
        all_diaries = self.get_all_diaries()
        return all_diaries[:days]
    
    def delete_diary(self, date: str) -> bool:
        """删除指定日期的日记"""
        if date in self.diaries:
            del self.diaries[date]
            self.save_diaries()
            return True
        return False
    
    def save_diaries(self):
        """保存日记到文件"""
        data = {date: entry.to_dict() for date, entry in self.diaries.items()}
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.DIARY_FILE)
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存日记失败: {e}")
    
    def load_diaries(self):
        """从文件加载日记"""
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.DIARY_FILE)
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 支持新格式：{"diaries": []}
                    if isinstance(data, dict) and "diaries" in data:
                        diaries_list = data.get("diaries", [])
                        self.diaries = {}
                        for entry_data in diaries_list:
                            if isinstance(entry_data, dict):
                                date = entry_data.get("date", "")
                                if date:
                                    self.diaries[date] = DiaryEntry.from_dict(entry_data)
                    else:
                        # 支持旧格式：{date: {...}, ...}
                        self.diaries = {
                            date: DiaryEntry.from_dict(entry_data)
                            for date, entry_data in data.items()
                        }
            except Exception as e:
                print(f"加载日记失败: {e}")
                self.diaries = {}
    
    def get_statistics(self) -> dict:
        """获取日记统计信息"""
        stats = {
            "total": len(self.diaries),
            "mood_count": {
                "开心": 0,
                "普通": 0,
                "难过": 0,
                "生气": 0
            },
            "total_events": 0
        }
        
        for entry in self.diaries.values():
            stats["mood_count"][entry.mood] = stats["mood_count"].get(entry.mood, 0) + 1
            stats["total_events"] += len(entry.events)
        
        return stats
