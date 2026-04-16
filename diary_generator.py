# -*- coding: utf-8 -*-
"""
便签日记生成系统
基于模板和随机元素自动生成每日便签
"""

import random
from datetime import datetime
from typing import Dict, List, Optional
import json
import os

class DiaryGenerator:
    """便签日记生成器"""
    
    def __init__(self):
        self.today_diary = None
        self.diary_file = "pet_diary.json"
        self.history_cache = []  # 缓存最近的日记用于去重
        self.load_history()
        
    def load_history(self):
        """加载历史日记用于去重"""
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    diaries = data.get('diaries', [])
                    # 只保存最近 10 篇用于对比
                    self.history_cache = diaries[-10:] if diaries else []
            except:
                pass
    
    def generate_daily_diary(self, stats: Dict) -> str:
        """
        生成每日便签日记
        
        Args:
            stats: 包含以下字段的字典
                - clicks: 点击次数
                - drags: 拖拽次数
                - throws: 甩飞次数
                - mood: 心情值 (0-100)
                - day_count: 使用天数
                - behaviors_played: 播放的行为种类
                
        Returns:
            生成的日记文本
        """
        now = datetime.now()
        
        # 生成日记组件
        header = self._generate_header(now, stats)
        body = self._generate_body(now, stats)
        footer = self._generate_footer(now, stats)
        
        # 组合日记
        diary = f"{header}\n\n{body}\n\n{footer}"
        
        # 保存日记
        self._save_diary(now, diary, stats)
        
        self.today_diary = diary
        return diary
    
    def _generate_header(self, now: datetime, stats: Dict) -> str:
        """生成日记开头"""
        emojis = ["🌻", "🌈", "☀️", "🌙", "🌧️", "⛅"]
        emoji = random.choice(emojis)
        
        day_name = self._get_day_name(now)
        weather = random.choice(["晴天", "多云", "阴天", "小雨", "大风", "下雪"])
        
        headers = [
            f"{emoji} {now.strftime('%m')}月{now.strftime('%d')}日 {day_name} {weather}",
            f"{emoji} {day_name}的早晨，熊家又来写日记啦！",
            f"{emoji} 第 {stats.get('day_count', 1)} 天，熊家的日记本！",
            f"📖 {now.strftime('%m/%d')} - 熊家的小日记",
        ]
        
        # 根据互动次数选择开头
        interactions = stats.get('clicks', 0) + stats.get('drags', 0)
        if interactions > 15:
            headers.append("🎉 今天好忙啊！熊家有好多事要写！")
        elif interactions < 3:
            headers.append("😴 今天好安静…熊家在想主人在干嘛")
        
        return random.choice(headers)
    
    def _generate_body(self, now: datetime, stats: Dict) -> str:
        """生成日记正文"""
        body_parts = []
        
        # 互动部分
        clicks = stats.get('clicks', 0)
        drags = stats.get('drags', 0)
        throws = stats.get('throws', 0)
        
        if clicks > 0:
            if clicks > 10:
                body_parts.append(f"今天主人戳了熊家 {clicks} 次！熊家好开心！虽然有时候被甩飞，但熊家都习惯了。")
            elif clicks > 5:
                body_parts.append(f"主人今天点了熊家 {clicks} 次，每次熊家都特别开心 😊")
            else:
                body_parts.append(f"虽然主人只点了 {clicks} 次，但熊家都记在心里了。")
        
        if drags > 0:
            body_parts.append(f"被主人拖来拖去了 {drags} 次！熊家都快晕了！")
        
        if throws > 0:
            body_parts.append(f"啊…又被甩飞了 {throws} 次…虽然有点疼，但这证明主人很喜欢熊家呢！")
        
        # 心情部分
        mood = stats.get('mood', 70)
        if mood > 80:
            body_parts.append("今天熊家的心情超级好！好想整天都开心 ✨")
        elif mood < 40:
            body_parts.append("虽然今天心情有点低落，但看到主人就好多了 💕")
        
        # 行为部分
        behaviors = stats.get('behaviors_played', 0)
        if behaviors > 5:
            body_parts.append(f"今天表演了 {behaviors} 种不同的动作！熊家真的太专业了！")
        
        # 时间相关
        hour = now.hour
        if 7 <= hour < 12:
            body_parts.append("早上的熊家特别精神！又蹦又跳的~")
        elif 12 <= hour < 14:
            body_parts.append("午饭时间！熊家的肚子在唱歌…")
        elif 14 <= hour < 17:
            body_parts.append("下午已经有点懒散了…想在温暖的地方眯一会")
        elif hour >= 21:
            body_parts.append("晚上是熊家的活动时间！精力充沛！")
        
        # 随机感想
        thoughts = [
            "希望主人今天工作顺利！",
            "布布也是熊家很重要的朋友呢～",
            "熊家会一直陪着主人的！",
            "明天也要开开心心的！",
            "又是充实的一天～",
        ]
        body_parts.append(random.choice(thoughts))
        
        return "\n".join(body_parts)
    
    def _generate_footer(self, now: datetime, stats: Dict) -> str:
        """生成日记结尾"""
        footers = [
            "好了，今天的日记就到这里！明天见！✨",
            "熊家有点困了…晚安世界…晚安主人～",
            "今天也是充实的一天呢！明天加油！💪",
            "日记写完啦！熊家要去休息咯~",
            "希望明天也能见到开心的主人！😊",
            "又是值得纪念的一天～记下来了！",
        ]
        return random.choice(footers)
    
    def _get_day_name(self, date: datetime) -> str:
        """获取星期名称"""
        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return days[date.weekday()]
    
    def _save_diary(self, date: datetime, content: str, stats: Dict):
        """保存日记到文件"""
        diary_data = {
            "date": date.strftime("%Y-%m-%d"),
            "content": content,
            "stats": stats,
            "created_at": datetime.now().isoformat(),
        }
        
        # 加载现有数据
        diaries = []
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    diaries = data.get('diaries', [])
            except:
                pass
        
        # 检查今天的日记是否已存在，存在则替换
        today_str = date.strftime("%Y-%m-%d")
        existing_idx = next(
            (i for i, d in enumerate(diaries) if d['date'] == today_str),
            -1
        )
        
        if existing_idx >= 0:
            diaries[existing_idx] = diary_data
        else:
            diaries.append(diary_data)
        
        # 保存到文件
        try:
            with open(self.diary_file, 'w', encoding='utf-8') as f:
                json.dump({"diaries": diaries}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存日记失败: {e}")
    
    def get_diary_by_date(self, date: datetime) -> Optional[Dict]:
        """获取指定日期的日记"""
        if not os.path.exists(self.diary_file):
            return None
        
        try:
            with open(self.diary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                diaries = data.get('diaries', [])
                
                date_str = date.strftime("%Y-%m-%d")
                for diary in diaries:
                    if diary['date'] == date_str:
                        return diary
        except:
            pass
        
        return None
    
    def get_all_diaries(self) -> List[Dict]:
        """获取所有日记"""
        if not os.path.exists(self.diary_file):
            return []
        
        try:
            with open(self.diary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('diaries', [])
        except:
            return []
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        diaries = self.get_all_diaries()
        
        return {
            "total_diaries": len(diaries),
            "first_date": diaries[0]["date"] if diaries else None,
            "latest_date": diaries[-1]["date"] if diaries else None,
            "total_interactions": sum(
                d["stats"].get("clicks", 0) + d["stats"].get("drags", 0)
                for d in diaries
            ),
        }
