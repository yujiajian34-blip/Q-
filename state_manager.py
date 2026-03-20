from enum import Enum, auto
from typing import Optional, Callable
import random
from data_manager import Mood

class PetState(Enum):
    IDLE = auto()
    IDLE_ACTION = auto()
    DRAGGING = auto()
    FEED = auto()
    BATH = auto()
    SING = auto()
    EXERCISE = auto()
    GREETING = auto()
    INTERACT = auto()
    EXPRESSION = auto()
    EMOTION = auto()
    PLAY_WITH_BUBU = auto()
    BULLY_BUBU = auto()
    DOUBLE_CLICK = auto()

class StateManager:
    IDLE_ANIMATION = "开心的趴着.webp"
    
    IDLE_ACTIONS = [
        "抠脚丫.webp",
        "晕乎乎.webp",
        "爬一爬.webp",
        "伸懒腰.webp",
        "满地打滚.webp",
        "装傻.webp",
        "馋猫.webp"
    ]
    
    IDLE_ACTIONS_HAPPY = [
        "开心的趴着.webp",
        "爬一爬.webp",
        "满地打滚.webp",
        "馋猫.webp"
    ]
    
    IDLE_ACTIONS_SAD = [
        "晕乎乎.webp",
        "抠脚丫.webp",
        "装傻.webp"
    ]
    
    DRAGGING_ANIMATION = "骑着小猪.webp"
    
    DOUBLE_CLICK_ANIMATIONS = [
        "跳一跳.webp",
        "大喊.webp",
        "突然出现.webp",
        "耍帅.webp",
        "恶龙咆哮.webp"
    ]
    
    DOUBLE_CLICK_HAPPY = [
        "跳一跳.webp",
        "耍帅.webp",
        "恶龙咆哮.webp"
    ]
    
    DOUBLE_CLICK_SAD = [
        "大喊.webp",
        "突然出现.webp"
    ]
    
    DOUBLE_CLICK_ANGRY = [
        "恶龙咆哮.webp",
        "大喊.webp"
    ]
    
    FEED_ANIMATIONS = [
        "吃西瓜.webp",
        "吃拉面.webp",
        "喝奶茶.webp"
    ]
    
    EXERCISE_ANIMATIONS = [
        "兔子舞.webp",
        "小鹿跳舞.webp",
        "奶牛跳舞.webp"
    ]
    
    GREETING_ANIMATIONS = [
        "早上好.webp",
        "下班了.webp"
    ]
    
    INTERACT_ANIMATIONS = [
        "和我玩.webp",
        "贴屏幕喊主人.webp"
    ]
    
    EXPRESSION_ANIMATIONS = [
        "爱你哦.webp",
        "给飞吻.webp",
        "仙女下凡.webp"
    ]
    
    EXPRESSION_SAD = [
        "哭唧唧.webp"
    ]
    
    EMOTION_ANIMATIONS = [
        "哭唧唧.webp",
        "生气.webp"
    ]
    
    PLAY_WITH_BUBU_ANIMATIONS = [
        "喊布布捶背.webp",
        "想布布.webp"
    ]
    
    BULLY_BUBU_ANIMATIONS = [
        "打布布.webp",
        "偷布布.webp",
        "掐布布屁股.webp",
        "推到布布.webp"
    ]
    
    def __init__(self):
        self.current_state = PetState.IDLE
        self.state_changed_callback: Optional[Callable] = None
        self.current_mood = Mood.NORMAL
    
    def set_state(self, state: PetState):
        self.current_state = state
        if self.state_changed_callback:
            self.state_changed_callback(state)
    
    def set_mood(self, mood: Mood):
        self.current_mood = mood
    
    def get_random_idle_action(self) -> str:
        if self.current_mood == Mood.HAPPY:
            return random.choice(self.IDLE_ACTIONS_HAPPY)
        elif self.current_mood == Mood.SAD:
            return random.choice(self.IDLE_ACTIONS_SAD)
        else:
            return random.choice(self.IDLE_ACTIONS)
    
    def get_random_double_click_animation(self) -> str:
        if self.current_mood == Mood.HAPPY:
            return random.choice(self.DOUBLE_CLICK_HAPPY)
        elif self.current_mood == Mood.SAD:
            return random.choice(self.DOUBLE_CLICK_SAD)
        elif self.current_mood == Mood.ANGRY:
            return random.choice(self.DOUBLE_CLICK_ANGRY)
        else:
            return random.choice(self.DOUBLE_CLICK_ANIMATIONS)
    
    def get_random_feed_animation(self) -> str:
        return random.choice(self.FEED_ANIMATIONS)
    
    def get_random_exercise_animation(self) -> str:
        return random.choice(self.EXERCISE_ANIMATIONS)
    
    def get_random_greeting(self) -> str:
        return random.choice(self.GREETING_ANIMATIONS)
    
    def get_random_interact_animation(self) -> str:
        return random.choice(self.INTERACT_ANIMATIONS)
    
    def get_random_expression_animation(self) -> str:
        if self.current_mood == Mood.SAD or self.current_mood == Mood.ANGRY:
            return random.choice(self.EXPRESSION_SAD)
        return random.choice(self.EXPRESSION_ANIMATIONS)
    
    def get_random_emotion_animation(self) -> str:
        return random.choice(self.EMOTION_ANIMATIONS)
    
    def get_random_play_with_bubu_animation(self) -> str:
        return random.choice(self.PLAY_WITH_BUBU_ANIMATIONS)
    
    def get_random_bully_bubu_animation(self) -> str:
        return random.choice(self.BULLY_BUBU_ANIMATIONS)
    
    def get_next_state_after_animation(self) -> PetState:
        return PetState.IDLE
    
    def get_random_idle_interval(self) -> int:
        if self.current_mood == Mood.HAPPY:
            return random.randint(30000, 60000)
        elif self.current_mood == Mood.SAD or self.current_mood == Mood.ANGRY:
            return random.randint(90000, 180000)
        else:
            return random.randint(60000, 120000)
