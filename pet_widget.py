import os
import random
import sys
import winreg
from PyQt5.QtWidgets import QWidget, QMenu, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QMovie, QPainter, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer, QSize, QPropertyAnimation, QRect, QEasingCurve
from state_manager import StateManager, PetState
from data_manager import DataManager, Mood, FOODS

class SpeechBubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.label = QLabel(self)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 230);
                color: #333333;
                border: 2px solid #cccccc;
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 14px;
                font-family: "Microsoft YaHei", sans-serif;
            }
        """)
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(200)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(500)
        
        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self.start_fade_out)
        
        self.setFixedSize(220, 80)
    
    def show_bubble(self, text: str, duration: int = 3000):
        self.label.setText(text)
        self.label.adjustSize()
        self.setFixedSize(self.label.size() + QSize(24, 16))
        
        self.opacity_effect.setOpacity(1.0)
        self.show()
        
        self.hide_timer.start(duration)
    
    def start_fade_out(self):
        self.hide_timer.stop()
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()
    
    def update_position(self, parent_pos: QPoint, parent_size: QSize):
        x = parent_pos.x() + (parent_size.width() - self.width()) // 2
        y = parent_pos.y() - self.height() - 10
        self.move(x, y)

class PetWidget(QWidget):
    SCALE_FACTOR = 0.5
    EDGE_MARGIN = 10
    REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "Q宠桌面宠物"
    
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.state_manager = StateManager()
        self.movie = None
        self.current_animation = None
        self.dragging = False
        self.drag_position = QPoint()
        self.stay_on_top = True
        self.original_size = QSize()
        self.is_hungry = False
        
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.on_idle_timer)
        
        self.decay_timer = QTimer(self)
        self.decay_timer.timeout.connect(self.on_decay_timer)
        self.decay_timer.start(600000)
        
        self.speech_timer = QTimer(self)
        self.speech_timer.timeout.connect(self.show_random_speech)
        self.speech_timer.start(random.randint(30000, 60000))
        
        self.animation_queue = []
        
        self.speech_bubble = SpeechBubble()
        
        self.init_ui()
        self.setup_callbacks()
        self.update_mood()
        self.check_hunger_state()
        self.start_idle()
    
    def init_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.show()
    
    def setup_callbacks(self):
        self.state_manager.state_changed_callback = self.on_state_changed
    
    def get_asset_path(self, filename: str) -> str:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, filename)
    
    def get_exe_path(self) -> str:
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            return os.path.abspath(__file__)
    
    def is_autostart_enabled(self) -> bool:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_KEY, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, self.APP_NAME)
            winreg.CloseKey(key)
            return True
        except:
            return False
    
    def enable_autostart(self) -> bool:
        try:
            exe_path = self.get_exe_path()
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_KEY, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, self.APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"设置开机启动失败: {e}")
            return False
    
    def disable_autostart(self) -> bool:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_KEY, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, self.APP_NAME)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"取消开机启动失败: {e}")
            return False
    
    def update_mood(self):
        mood = self.data_manager.get_mood()
        self.state_manager.set_mood(mood)
    
    def check_hunger_state(self):
        if self.data_manager.hunger < 30:
            if not self.is_hungry:
                self.is_hungry = True
                self.show_bubble("主人，我饿了...想吃东西...")
        else:
            self.is_hungry = False
    
    def on_decay_timer(self):
        self.data_manager.hunger = max(0, self.data_manager.hunger - 5)
        self.data_manager.mood_value = max(0, self.data_manager.mood_value - 2)
        
        if self.data_manager.hunger < 30:
            self.data_manager.mood_value = max(0, self.data_manager.mood_value - 3)
        
        self.update_mood()
        self.check_hunger_state()
        self.data_manager.save_data()
    
    def show_bubble(self, text: str, duration: int = 3000):
        self.speech_bubble.show_bubble(text, duration)
        self.update_bubble_position()
    
    def update_bubble_position(self):
        self.speech_bubble.update_position(self.pos(), self.size())
    
    def show_random_speech(self):
        self.speech_timer.stop()
        
        if self.is_hungry:
            texts = [
                "肚子好饿啊...",
                "主人，有吃的吗？",
                "我想吃东西...",
                "馋猫模式启动！"
            ]
        else:
            mood = self.data_manager.get_mood()
            if mood == Mood.HAPPY:
                texts = [
                    "今天心情真好！",
                    "主人最好了！",
                    "嘿嘿嘿~",
                    "好开心呀！",
                    "想出去玩！"
                ]
            elif mood == Mood.SAD:
                texts = [
                    "有点难过...",
                    "主人不理我了吗？",
                    "呜呜呜...",
                    "想布布了..."
                ]
            elif mood == Mood.ANGRY:
                texts = [
                    "哼！生气了！",
                    "不要理我！",
                    "走开走开！"
                ]
            else:
                texts = [
                    "主人好呀~",
                    "今天天气不错呢",
                    "想干嘛呢？",
                    "陪我玩嘛~",
                    "嘿嘿~",
                    "你在看什么？"
                ]
        
        text = random.choice(texts)
        self.show_bubble(text)
        
        self.speech_timer.start(random.randint(30000, 60000))
    
    def load_animation(self, filename: str, loop: bool = True):
        filepath = self.get_asset_path(filename)
        
        if self.movie:
            self.movie.stop()
            self.movie.frameChanged.disconnect()
            try:
                self.movie.finished.disconnect()
            except:
                pass
            self.movie.deleteLater()
            self.movie = None
        
        self.movie = QMovie(filepath)
        self.is_loop_animation = loop
        self.current_filename = filename
        
        if self.movie.isValid():
            self.movie.frameChanged.connect(self.on_frame_changed)
            self.movie.start()
            
            size = self.movie.currentPixmap().size()
            if size.isEmpty():
                size = self.movie.frameRect().size()
            if size.isEmpty():
                self.movie.jumpToFrame(0)
                size = self.movie.currentPixmap().size()
            
            scaled_size = QSize(int(size.width() * self.SCALE_FACTOR), int(size.height() * self.SCALE_FACTOR))
            self.setFixedSize(scaled_size)
            self.original_size = size
            self.current_animation = filename
            
            if not loop:
                self.check_animation_finished()
        else:
            self.load_static_image(filepath)
    
    def check_animation_finished(self):
        if not self.movie or self.is_loop_animation:
            return
        
        frame_count = self.movie.frameCount()
        if frame_count > 0 and self.movie.currentFrameNumber() >= frame_count - 1:
            self.on_animation_finished()
        else:
            QTimer.singleShot(50, self.check_animation_finished)
    
    def load_static_image(self, filepath: str):
        pixmap = QPixmap(filepath)
        if not pixmap.isNull():
            self.original_size = pixmap.size()
            scaled_pixmap = pixmap.scaled(
                int(pixmap.width() * self.SCALE_FACTOR),
                int(pixmap.height() * self.SCALE_FACTOR),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setFixedSize(scaled_pixmap.size())
            self.static_pixmap = scaled_pixmap
            self.current_animation = filepath
        self.update()
    
    def on_frame_changed(self):
        self.update()
    
    def on_animation_finished(self):
        if self.animation_queue:
            next_animation = self.animation_queue.pop(0)
            self.load_animation(next_animation, loop=False)
        else:
            next_state = self.state_manager.get_next_state_after_animation()
            self.state_manager.set_state(next_state)
            self.play_state_animation()
    
    def play_state_animation(self):
        if self.is_hungry and self.state_manager.current_state == PetState.IDLE:
            self.load_animation("馋猫.webp", loop=True)
            self.start_idle_timer()
            return
        
        state = self.state_manager.current_state
        
        if state == PetState.IDLE:
            self.load_animation(self.state_manager.IDLE_ANIMATION, loop=True)
            self.start_idle_timer()
        elif state == PetState.IDLE_ACTION:
            animation = self.state_manager.get_random_idle_action()
            self.load_animation(animation, loop=False)
        elif state == PetState.DRAGGING:
            self.load_animation(self.state_manager.DRAGGING_ANIMATION, loop=True)
        elif state == PetState.FEED:
            animation = self.state_manager.get_random_feed_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.BATH:
            self.load_animation("洗澡.webp", loop=False)
        elif state == PetState.SING:
            self.load_animation("唱歌.webp", loop=False)
        elif state == PetState.EXERCISE:
            animation = self.state_manager.get_random_exercise_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.GREETING:
            animation = self.state_manager.get_random_greeting()
            self.load_animation(animation, loop=False)
        elif state == PetState.INTERACT:
            animation = self.state_manager.get_random_interact_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.EXPRESSION:
            animation = self.state_manager.get_random_expression_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.EMOTION:
            animation = self.state_manager.get_random_emotion_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.PLAY_WITH_BUBU:
            animation = self.state_manager.get_random_play_with_bubu_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.BULLY_BUBU:
            animation = self.state_manager.get_random_bully_bubu_animation()
            self.load_animation(animation, loop=False)
        elif state == PetState.DOUBLE_CLICK:
            animation = self.state_manager.get_random_double_click_animation()
            self.load_animation(animation, loop=False)
    
    def on_state_changed(self, state: PetState):
        if state != PetState.IDLE:
            self.idle_timer.stop()
    
    def start_idle(self):
        self.state_manager.set_state(PetState.IDLE)
        self.play_state_animation()
    
    def start_idle_timer(self):
        interval = self.state_manager.get_random_idle_interval()
        self.idle_timer.start(interval)
    
    def on_idle_timer(self):
        self.idle_timer.stop()
        if self.state_manager.current_state == PetState.IDLE:
            self.state_manager.set_state(PetState.IDLE_ACTION)
            self.play_state_animation()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        if self.movie and self.movie.isValid():
            current_frame = self.movie.currentPixmap()
            if not current_frame.isNull():
                scaled_pixmap = current_frame.scaled(
                    self.width(), self.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                painter.drawPixmap(0, 0, scaled_pixmap)
        elif hasattr(self, 'static_pixmap') and self.static_pixmap:
            scaled_pixmap = self.static_pixmap.scaled(
                self.width(), self.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_pixmap)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            
            if self.state_manager.current_state != PetState.DRAGGING:
                self.idle_timer.stop()
                self.state_manager.set_state(PetState.DRAGGING)
                self.play_state_animation()
            
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            self.update_bubble_position()
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.snap_to_edge()
            self.start_idle()
            event.accept()
    
    def snap_to_edge(self):
        screen = self.screen().availableGeometry()
        pet_rect = self.geometry()
        
        left_distance = pet_rect.left() - screen.left()
        right_distance = screen.right() - pet_rect.right()
        top_distance = pet_rect.top() - screen.top()
        bottom_distance = screen.bottom() - pet_rect.bottom()
        
        min_distance = min(left_distance, right_distance, top_distance, bottom_distance)
        
        if min_distance <= self.EDGE_MARGIN:
            new_pos = pet_rect.topLeft()
            
            if min_distance == left_distance:
                new_pos.setX(screen.left())
            elif min_distance == right_distance:
                new_pos.setX(screen.right() - pet_rect.width())
            elif min_distance == top_distance:
                new_pos.setY(screen.top())
            elif min_distance == bottom_distance:
                new_pos.setY(screen.bottom() - pet_rect.height())
            
            self.animate_move(new_pos)
    
    def animate_move(self, new_pos: QPoint):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(QRect(new_pos, self.size()))
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.idle_timer.stop()
            self.state_manager.set_state(PetState.DOUBLE_CLICK)
            self.play_state_animation()
            self.show_bubble("主人点我啦~")
            event.accept()
    
    def moveEvent(self, event):
        super().moveEvent(event)
        self.update_bubble_position()
    
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(255, 255, 255, 230);
                border: 1px solid rgba(200, 200, 200, 150);
                border-radius: 10px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 6px;
                margin: 2px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: rgba(100, 150, 255, 100);
            }
            QMenu::item:disabled {
                color: #666666;
                background-color: transparent;
            }
            QMenu::separator {
                height: 1px;
                background: rgba(200, 200, 200, 150);
                margin: 5px 10px;
            }
        """)
        
        mood = self.data_manager.get_mood()
        mood_emoji = {Mood.HAPPY: "😊", Mood.NORMAL: "😐", Mood.SAD: "😢", Mood.ANGRY: "😠"}
        status_text = f"❤️ {self.data_manager.intimacy}  |  {mood_emoji[mood]} {self.data_manager.mood_value}  |  🍖 {self.data_manager.hunger}"
        status_action = menu.addAction(status_text)
        status_action.setEnabled(False)
        menu.addSeparator()
        
        feed_menu = menu.addMenu("🍴 喂食")
        feed_menu.setStyleSheet(menu.styleSheet())
        for food_key, food in FOODS.items():
            food_action = feed_menu.addAction(f"{food.display_name} (亲密度+{food.intimacy})")
            food_action.triggered.connect(lambda checked, f=food_key: self.do_feed_specific(f))
        
        bath_action = menu.addAction("🛁 洗澡")
        sing_action = menu.addAction("🎵 唱歌")
        exercise_action = menu.addAction("💃 运动")
        greet_action = menu.addAction("🌞 问候")
        interact_action = menu.addAction("🤝 互动")
        expression_action = menu.addAction("💕 表情")
        emotion_action = menu.addAction("😢 情绪")
        bubu_action = menu.addAction("🐻 和布布玩")
        bully_action = menu.addAction("👊 欺负布布")
        menu.addSeparator()
        
        autostart_text = "🚀 取消开机启动" if self.is_autostart_enabled() else "🚀 开机自动启动"
        autostart_action = menu.addAction(autostart_text)
        
        top_text = "📌 取消置顶" if self.stay_on_top else "📌 置顶显示"
        top_action = menu.addAction(top_text)
        menu.addSeparator()
        
        quit_action = menu.addAction("❌ 退出")
        
        action = menu.exec_(event.globalPos())
        
        if action == bath_action:
            self.do_bath()
        elif action == sing_action:
            self.do_sing()
        elif action == exercise_action:
            self.do_exercise()
        elif action == greet_action:
            self.do_greeting()
        elif action == interact_action:
            self.do_interact()
        elif action == expression_action:
            self.do_expression()
        elif action == emotion_action:
            self.do_emotion()
        elif action == bubu_action:
            self.do_play_with_bubu()
        elif action == bully_action:
            self.do_bully_bubu()
        elif action == autostart_action:
            self.toggle_autostart()
        elif action == top_action:
            self.toggle_stay_on_top()
        elif action == quit_action:
            self.data_manager.save_data()
            self.speech_bubble.close()
            self.close()
    
    def toggle_autostart(self):
        if self.is_autostart_enabled():
            if self.disable_autostart():
                self.show_bubble("已取消开机启动~", 2000)
            else:
                self.show_bubble("取消失败...", 2000)
        else:
            if self.enable_autostart():
                self.show_bubble("开机就会见到我啦~", 2000)
            else:
                self.show_bubble("设置失败...", 2000)
    
    def do_feed_specific(self, food_key: str):
        food = FOODS.get(food_key)
        if food:
            self.idle_timer.stop()
            self.data_manager.feed(food)
            self.update_mood()
            self.check_hunger_state()
            self.data_manager.save_data()
            self.state_manager.set_state(PetState.FEED)
            self.load_animation(food_key, loop=False)
            self.show_bubble(f"好吃！谢谢主人~", 2000)
    
    def do_bath(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(10)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.BATH)
        self.play_state_animation()
        self.show_bubble("洗香香~", 2000)
    
    def do_sing(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(5)
        self.data_manager.add_intimacy(3)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.SING)
        self.play_state_animation()
        self.show_bubble("啦啦啦~", 2000)
    
    def do_exercise(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(8)
        self.data_manager.add_intimacy(2)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.EXERCISE)
        self.play_state_animation()
        self.show_bubble("动起来！", 2000)
    
    def do_greeting(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(5)
        self.data_manager.add_intimacy(5)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.GREETING)
        self.play_state_animation()
        self.show_bubble("主人好呀~", 2000)
    
    def do_interact(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(10)
        self.data_manager.add_intimacy(8)
        self.data_manager.total_play_count += 1
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.INTERACT)
        self.play_state_animation()
        self.show_bubble("和主人玩真开心！", 2000)
    
    def do_expression(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(5)
        self.data_manager.add_intimacy(5)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.EXPRESSION)
        self.play_state_animation()
        self.show_bubble("爱你哦~", 2000)
    
    def do_emotion(self):
        self.idle_timer.stop()
        self.state_manager.set_state(PetState.EMOTION)
        self.play_state_animation()
        self.show_bubble("呜呜呜...", 2000)
    
    def do_play_with_bubu(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(8)
        self.data_manager.add_intimacy(6)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.PLAY_WITH_BUBU)
        self.play_state_animation()
        self.show_bubble("布布最好了~", 2000)
    
    def do_bully_bubu(self):
        self.idle_timer.stop()
        self.data_manager.add_mood(-5)
        self.data_manager.add_intimacy(-3)
        self.update_mood()
        self.data_manager.save_data()
        self.state_manager.set_state(PetState.BULLY_BUBU)
        self.play_state_animation()
        self.show_bubble("哼！布布坏！", 2000)
    
    def toggle_stay_on_top(self):
        self.stay_on_top = not self.stay_on_top
        if self.stay_on_top:
            self.setWindowFlags(
                Qt.FramelessWindowHint |
                Qt.WindowStaysOnTopHint |
                Qt.Tool
            )
        else:
            self.setWindowFlags(
                Qt.FramelessWindowHint |
                Qt.Tool
            )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()
    
    def closeEvent(self, event):
        self.data_manager.save_data()
        self.speech_bubble.close()
        super().closeEvent(event)
