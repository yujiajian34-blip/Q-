# -*- coding: utf-8 -*-
"""
思维气泡管理系统 (Thinking Bubble System)
管理熊家的各种想法气泡及其显示逻辑
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class BubbleTheme(Enum):
    """气泡主题"""
    FOOD = "food"           # 关于吃的
    SLEEP = "sleep"         # 关于睡觉
    BUBU = "bubu"           # 关于布布
    OWNER = "owner"         # 关于主人
    FANTASY = "fantasy"     # 自我幻想
    PHILOSOPHY = "philosophy"  # 哲学思考
    TIMELY = "timely"       # 特殊时段限定
    DAILY = "daily"         # 日常碎碎念

class BubbleManager:
    """思维气泡管理器"""
    
    def __init__(self):
        self.last_bubble_time = None
        self.shown_bubbles = []  # 记录最近显示过的气泡，避免短期重复
        self.bubble_pool = self._init_bubble_pool()
        self.min_interval = 45  # 两次气泡间隔（秒）
        self.repeat_limit_hours = 2  # 同一条气泡 2 小时内不重复
        
    def _init_bubble_pool(self) -> Dict[BubbleTheme, List[str]]:
        """初始化气泡内容池"""
        return {
            BubbleTheme.FOOD: [
                "主人今天给熊家吃什么好呢…",
                "好想吃西瓜啊～甜甜的那种 🍉",
                "布布偷偷藏了零食！熊家看到了！",
                "奶茶…奶茶…脑子里全是奶茶 🧋",
                "如果熊家会做饭就好了…算了还是等主人",
                "拉面还是米饭呢…好难选",
                "熊家的肚子在唱歌了～",
                "今天要吃三碗饭！不…五碗！",
                "主人不会又忘给熊家买零食吧",
                "冰淇淋…夏天好想吃冰淇淋",
                "布布说减肥…熊家才不要减呢",
                "世界上最好吃的东西是什么？是主人做的！",
                "好奇怪…明明刚吃完为什么又饿了",
                "熊家决定了！今天要当一只快乐的馋猫",
                "如果能住在蛋糕里就好了～",
            ],
            BubbleTheme.SLEEP: [
                "好困…再趴五分钟…就五分钟…",
                "熊家的床是不是在召唤我",
                "昨晚梦到在云朵上跳来跳去 ☁️",
                "打个哈欠～啊～～～",
                "布布睡觉打呼噜！超大声的！",
                "如果可以冬眠就好了…熊家要睡一整个冬天",
                "主人还在忙吗…熊家先眯一会儿",
                "趴着好舒服啊…不想动了",
                "为什么人要睡觉呢…不睡觉多玩一会儿不好吗",
                "熊家发明了新睡姿！趴着睡！",
                "伸个懒腰～咔嚓～舒服",
                "好想抱着布布睡觉…虽然它不让我抱",
            ],
            BubbleTheme.BUBU: [
                "布布今天又装可爱…明明没有熊家可爱",
                "哼！布布不理熊家，熊家也不理布布！",
                "布布的屁股好软…嘿嘿 🤭",
                "熊家是布布最好的朋友！布布也是！…大概吧",
                "今天要欺负布布几次呢…三次？五次？",
                "布布今天穿新衣服了…熊家也要！",
                "偷偷跟在布布后面…嘿嘿嘿",
                "布布在干嘛呢…好想偷看",
                "熊家和布布谁更可爱？当然是熊家啦！",
                "布布今天好像不太开心…要不要安慰一下呢",
                "算了…还是不欺负布布了（才怪）",
                "布布说熊家胖…熊家那叫圆润！",
                "如果布布不在…熊家会觉得无聊的吧",
                "今天和布布和好了！熊家很大度的",
                "布布的毛摸起来好舒服啊～",
            ],
            BubbleTheme.OWNER: [
                "主人今天看起来很开心呢～",
                "主人又在忙了…熊家乖乖不打扰",
                "主人什么时候陪熊家玩呀",
                "熊家最喜欢主人了！（小声）",
                "主人的屏幕好大…熊家能在上面走来走去",
                "主人今天喝水了吗？要记得喝水哦！",
                "好想贴贴主人…",
                "主人打的字好快…熊家一个都看不懂",
                "主人是不是在玩游戏？熊家也想玩！",
                "有主人在的地方就是熊家的家",
                "主人今天笑了几次呢…熊家都数着呢",
                "主人的手好暖…",
                "熊家会一直陪着主人的！",
                "主人加班好辛苦…熊家给你加油！",
                "如果主人是全世界最好的主人…那熊家就是全世界最好的熊",
            ],
            BubbleTheme.FANTASY: [
                "熊家是全世界最可爱的！不接受反驳！",
                "如果熊家会飞就好了…嗖～",
                "熊家觉得今天特别帅",
                "总有一天熊家要成为大明星！",
                "熊家的歌声一定很好听…吧？",
                "如果能变成人类…熊家要吃遍全世界",
                "熊家是仙女！仙女不需要理由！🧚",
                "熊家的梦想是…每天都能开开心心的",
                "熊家觉得自己的尾巴特别好看",
                "今天也是元气满满的熊家！",
            ],
            BubbleTheme.PHILOSOPHY: [
                "屏幕外面是什么世界呢…",
                "时间过得好快啊…",
                "熊家在想…1+1等于几来着",
                "为什么猫有九条命…熊家想要十条",
                "今天星期几来着…",
                "风是从哪里来的呢…",
                "熊家在想一个很重要的问题…午饭吃什么",
                "如果世界是圆的…熊家走到头会不会掉下去",
                "云朵是不是棉花糖做的…",
                "为什么打哈欠会传染呢…啊～",
                "熊家数了数…今天一共发了三次呆",
                "主人的电脑里面是不是住着很多人",
                "好无聊啊…有没有什么好玩的",
            ],
            BubbleTheme.TIMELY: [
                "早上好呀世界！今天也要加油！",
                "好困…为什么早上要起这么早",
                "午饭时间到了！熊家的肚子已经准备好了",
                "下午茶时间！奶茶在哪里！",
                "主人快下班了吧…熊家等好久了",
                "终于晚上了！熊家的活跃时间到了！",
                "好困…但是还想再玩一会儿…",
                "主人还不睡吗…熊家先睡了哦",
                "周末了！可以赖床了！",
                "新的一周开始啦！熊家要加油！",
            ],
            BubbleTheme.DAILY: [
                "熊家今天又活力满满的！",
                "安安静静思考人生…",
                "嘿嘿，有点小开心呢",
                "感觉今天会很特别！",
                "不知道哪里来的小期待…",
                "熊家就是这么可爱 😊",
                "咦，有人在看熊家吗？",
                "时间你走慢点好不好…",
                "这一刻很完美呢～",
                "熊家要更加努力哦！",
            ],
        }
    
    def get_bubble(self, theme: Optional[BubbleTheme] = None) -> Optional[str]:
        """
        获取气泡内容
        
        Args:
            theme: 优先选择的主题，为 None 时随机选择
            
        Returns:
            气泡内容或 None（如果触发间隔限制）
        """
        # 检查时间间隔限制（仅在已显示过气泡时检查）
        if self.last_bubble_time:
            time_diff = (datetime.now() - self.last_bubble_time).total_seconds()
            if time_diff < self.min_interval:
                return None
        
        # 选择主题
        if theme is None:
            theme = random.choice(list(BubbleTheme))
        elif isinstance(theme, str):
            theme = BubbleTheme[theme.upper()]
        
        # 根据时间自动调整主题
        current_hour = datetime.now().hour
        if current_hour < 10 or (22 <= current_hour <= 23):
            # 早上或深夜提高 SLEEP 主题概率
            if random.random() < 0.4:
                theme = BubbleTheme.SLEEP
        
        # 获取该主题的气泡池
        pool = self.bubble_pool.get(theme, [])
        if not pool:
            # 如果该主题没有内容，用其他主题
            theme = random.choice([t for t in BubbleTheme if t != theme])
            pool = self.bubble_pool.get(theme, [])
        
        if not pool:
            return None
        
        # 获取近期未重复出现的气泡
        candidate = self._get_non_repeated_bubble(pool)
        
        # 更新记录
        self.last_bubble_time = datetime.now()
        self.shown_bubbles.append({
            'text': candidate,
            'time': datetime.now(),
        })
        
        # 只保留最近 10 条记录
        if len(self.shown_bubbles) > 10:
            self.shown_bubbles.pop(0)
        
        return candidate
    
    def _get_non_repeated_bubble(self, pool: List[str]) -> str:
        """获取不重复的气泡"""
        # 计算 2 小时内被过滤的气泡
        cutoff_time = datetime.now() - timedelta(hours=self.repeat_limit_hours)
        recent_bubbles = [
            b['text'] for b in self.shown_bubbles 
            if b['time'] > cutoff_time
        ]
        
        # 尝试找一个没在最近出现过的气泡
        candidates = [b for b in pool if b not in recent_bubbles]
        
        if candidates:
            return random.choice(candidates)
        else:
            # 如果全部最近都出现过，就随机取一个
            return random.choice(pool)
    
    def get_bubble_duration(self, text: str) -> int:
        """
        根据文字长度计算气泡持续时间（毫秒）
        
        Args:
            text: 气泡文本
            
        Returns:
            持续时间（毫秒）
        """
        length = len(text)
        # 基础时间 2000ms + 每 5 个字 500ms
        return 2000 + (length // 5) * 500
    
    def get_contextual_bubble(self, action: str) -> Optional[str]:
        """
        根据用户行为获取相关的气泡
        
        Args:
            action: 行为类型 (feed/play/emotion/touch/drag)
            
        Returns:
            气泡内容or None
        """
        action_theme_map = {
            'feed': BubbleTheme.FOOD,
            'play': BubbleTheme.BUBU,
            'emotion': BubbleTheme.FANTASY,
            'touch': BubbleTheme.OWNER,
            'drag': BubbleTheme.OWNER,
            'sleep': BubbleTheme.SLEEP,
        }
        
        # 20% 概率触发相关气泡
        if random.random() < 0.2:
            theme = action_theme_map.get(action)
            if theme:
                return self.get_bubble(theme)
        
        return None
    
    def clear_history(self):
        """清除气泡历史记录（每天凌晨调用）"""
        self.shown_bubbles.clear()
        self.last_bubble_time = None
