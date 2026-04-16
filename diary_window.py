from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QComboBox, QCalendarWidget, QListWidget,
                            QListWidgetItem, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QFont, QColor
from diary_manager import DiaryManager
from datetime import datetime

class DiaryWindow(QWidget):
    """日记窗口"""
    def __init__(self, diary_manager: DiaryManager, parent=None):
        super().__init__(parent)
        self.diary_manager = diary_manager
        self.current_date = None
        
        # 设置窗口属性
        self.setWindowTitle("🐱 布布的日记")
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        
        self.init_ui()
        self.load_today()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🐱 布布的日记")
        self.setGeometry(100, 100, 900, 650)
        
        # 设置窗口在屏幕中央
        screen = self.screen().availableGeometry()
        x = (screen.width() - 900) // 2
        y = (screen.height() - 650) // 2
        self.move(screen.left() + x, screen.top() + y)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QListWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 5px;
            }
            QCalendarWidget {
                background-color: white;
                border: 2px solid #ddd;
            }
        """)
        
        # 主布局
        main_layout = QHBoxLayout()
        
        # 左侧：日历和日记列表
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # 日历
        calendar_label = QLabel("📅 日期选择")
        calendar_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        left_layout.addWidget(calendar_label)
        
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.clicked.connect(self.on_calendar_date_clicked)
        left_layout.addWidget(self.calendar)
        
        # 日记列表
        list_label = QLabel("📝 日记列表（最近30天）")
        list_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        left_layout.addWidget(list_label)
        
        self.diary_list = QListWidget()
        self.diary_list.itemClicked.connect(self.on_diary_item_clicked)
        left_layout.addWidget(self.diary_list)
        
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(350)
        
        # 右侧：日记编辑
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        # 标题
        title_layout = QHBoxLayout()
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_layout.addWidget(self.date_label)
        title_layout.addStretch()
        right_layout.addLayout(title_layout)
        
        # 心情选择
        mood_layout = QHBoxLayout()
        mood_label = QLabel("今天的心情:")
        mood_label.setFont(QFont("Microsoft YaHei", 11))
        self.mood_combo = QComboBox()
        self.mood_combo.addItems(["开心 😊", "普通 😐", "难过 😢", "生气 😠"])
        self.mood_combo.setMaximumWidth(150)
        mood_layout.addWidget(mood_label)
        mood_layout.addWidget(self.mood_combo)
        mood_layout.addStretch()
        right_layout.addLayout(mood_layout)
        
        # 事件记录
        events_label = QLabel("✨ 今天的事件:")
        events_label.setFont(QFont("Microsoft YaHei", 11))
        right_layout.addWidget(events_label)
        
        self.events_list = QListWidget()
        self.events_list.setMaximumHeight(100)
        right_layout.addWidget(self.events_list)
        
        # 日记内容
        content_label = QLabel("📖 日记内容:")
        content_label.setFont(QFont("Microsoft YaHei", 11))
        right_layout.addWidget(content_label)
        
        self.diary_text = QTextEdit()
        self.diary_text.setPlaceholderText("记录今天与布布的点点滴滴...\n\n今天天气很好，布布很开心...\n和布布一起玩耍，很有趣...")
        right_layout.addWidget(self.diary_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("💾 保存日记")
        self.save_button.clicked.connect(self.save_diary)
        button_layout.addWidget(self.save_button)
        
        self.delete_button = QPushButton("🗑️ 删除日记")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.delete_button.clicked.connect(self.delete_diary)
        button_layout.addWidget(self.delete_button)
        
        self.close_button = QPushButton("❌ 关闭")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #999;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        right_layout.addLayout(button_layout)
        
        right_widget.setLayout(right_layout)
        
        # 添加左右布局
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget, 1)
        
        self.setLayout(main_layout)
    
    def load_today(self):
        """加载今天的日记"""
        today = self.diary_manager.get_today_date()
        self.current_date = today
        self.load_diaries_list()
        self.load_diary_content(today)
    
    def load_diaries_list(self):
        """加载日记列表"""
        self.diary_list.clear()
        diaries = self.diary_manager.get_recent_diaries(30)
        
        for diary in diaries:
            mood_emoji = self.get_mood_emoji(diary.mood)
            text = f"{mood_emoji} {diary.date} - {diary.mood}"
            item = QListWidgetItem(text)
            
            # 不同心情用不同颜色标记
            if diary.mood == "开心":
                item.setForeground(QColor("#FFD700"))
            elif diary.mood == "难过":
                item.setForeground(QColor("#87CEEB"))
            elif diary.mood == "生气":
                item.setForeground(QColor("#FF6B6B"))
            else:
                item.setForeground(QColor("#333"))
            
            item.setData(Qt.UserRole, diary.date)
            self.diary_list.addItem(item)
    
    def load_diary_content(self, date: str):
        """加载指定日期的日记内容"""
        diary = self.diary_manager.get_diary_by_date(date)
        self.current_date = date
        
        # 更新日期标签
        self.date_label.setText(f"📅 {date}")
        
        if diary:
            # 设置心情
            mood_index = ["开心", "普通", "难过", "生气"].index(diary.mood)
            self.mood_combo.setCurrentIndex(mood_index)
            
            # 设置事件列表
            self.events_list.clear()
            for event in diary.events:
                self.events_list.addItem(event)
            
            # 设置日记内容
            self.diary_text.setPlainText(diary.content)
        else:
            # 新日记
            self.mood_combo.setCurrentIndex(1)  # 普通
            self.events_list.clear()
            self.diary_text.setPlainText("")
    
    def on_calendar_date_clicked(self, date: QDate):
        """日历日期点击"""
        selected_date = date.toString("yyyy-MM-dd")
        self.load_diary_content(selected_date)
    
    def on_diary_item_clicked(self, item: QListWidgetItem):
        """日记列表项点击"""
        date = item.data(Qt.UserRole)
        self.load_diary_content(date)
        
        # 更新日历选择
        date_parts = date.split('-')
        q_date = QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
        self.calendar.setSelectedDate(q_date)
    
    def save_diary(self):
        """保存日记"""
        try:
            if not self.current_date:
                QMessageBox.warning(self, "警告", "请选择日期")
                return
            
            content = self.diary_text.toPlainText()
            mood_text = self.mood_combo.currentText().split()[0]  # 去掉emoji
            
            if not content.strip():
                QMessageBox.warning(self, "警告", "请输入日记内容")
                return
            
            self.diary_manager.update_diary(self.current_date, content, mood_text)
            QMessageBox.information(self, "成功", "日记已保存 ✨")
            self.load_diaries_list()
        except Exception as e:
            print(f"❌ 保存日记出错: {e}")
            QMessageBox.warning(self, "错误", f"保存日记失败: {str(e)}")
    
    def delete_diary(self):
        """删除日记"""
        if not self.current_date:
            return
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除 {self.current_date} 的日记吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.diary_manager.delete_diary(self.current_date)
            QMessageBox.information(self, "成功", "日记已删除")
            self.load_diaries_list()
            self.load_today()
    
    @staticmethod
    def get_mood_emoji(mood: str) -> str:
        """获取心情对应的emoji"""
        mood_map = {
            "开心": "😊",
            "普通": "😐",
            "难过": "😢",
            "生气": "😠"
        }
        return mood_map.get(mood, "😐")
