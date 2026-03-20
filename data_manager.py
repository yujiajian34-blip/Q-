import json
import os
from enum import Enum
from typing import Optional
from datetime import datetime

class Mood(Enum):
    HAPPY = "开心"
    NORMAL = "普通"
    SAD = "难过"
    ANGRY = "生气"

class Food:
    def __init__(self, name: str, display_name: str, intimacy: int, mood: int, hunger: int):
        self.name = name
        self.display_name = display_name
        self.intimacy = intimacy
        self.mood = mood
        self.hunger = hunger

FOODS = {
    "吃西瓜.webp": Food("吃西瓜.webp", "🍉 西瓜", intimacy=5, mood=3, hunger=10),
    "吃拉面.webp": Food("吃拉面.webp", "🍜 拉面", intimacy=8, mood=5, hunger=20),
    "喝奶茶.webp": Food("喝奶茶.webp", "🧋 奶茶", intimacy=10, mood=8, hunger=5),
}

class DataManager:
    SAVE_FILE = "pet_save.json"
    
    def __init__(self):
        self.intimacy = 50
        self.mood_value = 70
        self.hunger = 50
        self.last_feed_time = datetime.now()
        self.last_interact_time = datetime.now()
        self.total_feed_count = 0
        self.total_play_count = 0
        
        self.load_data()
    
    def get_mood(self) -> Mood:
        if self.mood_value >= 80 and self.intimacy >= 60:
            return Mood.HAPPY
        elif self.mood_value <= 30 or self.intimacy <= 20:
            return Mood.SAD
        elif self.mood_value <= 20:
            return Mood.ANGRY
        else:
            return Mood.NORMAL
    
    def add_mood(self, value: int):
        self.mood_value = max(0, min(100, self.mood_value + value))
    
    def add_intimacy(self, value: int):
        self.intimacy = max(0, min(100, self.intimacy + value))
    
    def decay_stats(self):
        self.mood_value = max(0, self.mood_value - 1)
        self.hunger = max(0, self.hunger - 2)
        if self.hunger < 20:
            self.mood_value = max(0, self.mood_value - 2)
    
    def feed(self, food: Food):
        self.intimacy = min(100, self.intimacy + food.intimacy)
        self.mood_value = min(100, self.mood_value + food.mood)
        self.hunger = min(100, self.hunger + food.hunger)
        self.last_feed_time = datetime.now()
        self.total_feed_count += 1
    
    def save_data(self):
        data = {
            "intimacy": self.intimacy,
            "mood_value": self.mood_value,
            "hunger": self.hunger,
            "last_feed_time": self.last_feed_time.isoformat(),
            "last_interact_time": self.last_interact_time.isoformat(),
            "total_feed_count": self.total_feed_count,
            "total_play_count": self.total_play_count
        }
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.SAVE_FILE)
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_data(self):
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.SAVE_FILE)
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.intimacy = data.get("intimacy", 50)
                self.mood_value = data.get("mood_value", 70)
                self.hunger = data.get("hunger", 50)
                self.total_feed_count = data.get("total_feed_count", 0)
                self.total_play_count = data.get("total_play_count", 0)
            except:
                pass
