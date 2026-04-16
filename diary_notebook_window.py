# -*- coding: utf-8 -*-
"""
熊家日记本窗口（便签风格）
日历 + 便签内容查看
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCalendarWidget, QTextEdit, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QDate, QSize, QTimer
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from datetime import datetime, timedelta
from diary_generator import DiaryGenerator

class DiaryNotebookWindow(QWidget):
    """熊家的日记本（便签风格）"""
    
    def __init__(self, diary_generator: DiaryGenerator, parent=None):
        super().__init__(parent)
        self.diary_generator = diary_generator
        self.current_date = QDate.currentDate()
        
        self.setWindowTitle("📖 熊家的日记本")
        self.setGeometry(100, 100, 800, 600)
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QWidget {
                background-color: #fff8f3;
                font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            }
            QCalendarWidget {
                background-color: white;
                border: 2px solid #f0e6d2;
                border-radius: 8px;
                padding: 10px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #ffcc99;
                color: #333;
            }
            QTextEdit {
                background-color: white;
                border: 3px solid #ffcc99;
                border-radius: 12px;
                padding: 15px;
                font-size: 13px;
                color: #333;
                line-height: 1.6;
            }
            QPushButton {
                background-color: #ffaa66;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff9944;
            }
            QLabel {
                color: #333;
            }
        """)
        
        self.init_ui()
        self.load_diary()
        
        # 每5秒更新一次，检查是否需要刷新
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.check_date_change)
        self.refresh_timer.start(5000)
    
    def init_ui(self):
        """初始化 UI"""
        main_layout = QHBoxLayout()
        
        # 左侧：日历
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("📅 选择日期"))
        
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(self.current_date)
        self.calendar.clicked.connect(self.on_date_selected)
        left_layout.addWidget(self.calendar)
        
        # 统计信息
        stats_group = QLabel()
        stats = self.diary_generator.get_statistics()
        stats_text = f"""
📊 日记统计
━━━━━━━━━━
总日记数: {stats['total_diaries']}
总互动数: {stats['total_interactions']}
"""
        stats_group.setText(stats_text)
        stats_group.setStyleSheet("background-color: #fff0e6; padding: 10px; border-radius: 8px;")
        left_layout.addWidget(stats_group)
        
        # 右侧：日记内容
        right_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("💭 熊家的小日记")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        right_layout.addWidget(title_label)
        
        # 日记内容
        self.diary_text = QTextEdit()
        self.diary_text.setReadOnly(True)
        self.diary_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 3px dashed #ffcc99;
                border-radius: 12px;
                padding: 15px;
                font-size: 13px;
                color: #333;
            }
        """)
        right_layout.addWidget(self.diary_text)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        prev_btn = QPushButton("⬅ 前一天")
        prev_btn.clicked.connect(self.show_prev_day)
        button_layout.addWidget(prev_btn)
        
        today_btn = QPushButton("📌 今天")
        today_btn.clicked.connect(self.show_today)
        button_layout.addWidget(today_btn)
        
        next_btn = QPushButton("后一天 ➡")
        next_btn.clicked.connect(self.show_next_day)
        button_layout.addWidget(next_btn)
        
        right_layout.addLayout(button_layout)
        
        # 日期显示
        self.date_label = QLabel()
        self.update_date_label()
        right_layout.addWidget(self.date_label)
        
        # 合并左右
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        self.setLayout(main_layout)
    
    def update_date_label(self):
        """更新日期标签"""
        date_str = self.current_date.toString("yyyy-MM-dd dddd")
        data_cn = self._get_cn_date(self.current_date)
        self.date_label.setText(f"📅 {data_cn}")
        self.date_label.setStyleSheet(
            "color: #ff9944; font-size: 12px; padding: 5px;"
        )
    
    def _get_cn_date(self, qdate: QDate) -> str:
        """转换为中文日期"""
        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return f"{qdate.year()}年{qdate.month()}月{qdate.day()}日 {days[qdate.dayOfWeek()-1]}"
    
    def on_date_selected(self, qdate: QDate):
        """选择日期"""
        self.current_date = qdate
        self.update_date_label()
        self.load_diary()
    
    def load_diary(self):
        """加载日记"""
        dt = datetime(
            self.current_date.year(),
            self.current_date.month(),
            self.current_date.day()
        )
        
        diary = self.diary_generator.get_diary_by_date(dt)
        
        if diary:
            content = diary['content']
            
            # 添加装饰
            decorated_content = f"""
{content}

━━━━━━━━━━━━━━━━━
"""
            
            # 添加统计信息
            stats = diary.get('stats', {})
            if stats:
                decorated_content += f"""
📊 今日数据：
  💬 点击: {stats.get('clicks', 0)} 次
  📍 拖拽: {stats.get('drags', 0)} 次
  😊 心情: {stats.get('mood', 70)}/100
"""
            
            self.diary_text.setText(decorated_content)
        else:
            self.diary_text.setText(
                "这一天还没有日记呢...\n\n"
                "熊家正在努力写日记中！📝\n\n"
                "赶快来和熊家互动，就会产生新的日记哦！ 💕"
            )
    
    def show_prev_day(self):
        """显示前一天"""
        self.current_date = self.current_date.addDays(-1)
        self.calendar.setSelectedDate(self.current_date)
        self.update_date_label()
        self.load_diary()
    
    def show_next_day(self):
        """显示后一天"""
        self.current_date = self.current_date.addDays(1)
        self.calendar.setSelectedDate(self.current_date)
        self.update_date_label()
        self.load_diary()
    
    def show_today(self):
        """显示今天"""
        self.current_date = QDate.currentDate()
        self.calendar.setSelectedDate(self.current_date)
        self.update_date_label()
        self.load_diary()
    
    def check_date_change(self):
        """检查日期是否改变"""
        if QDate.currentDate() != self.current_date:
            # 如果还在今天的日记，自动刷新
            if QDate.currentDate().daysTo(self.current_date) == 0:
                self.load_diary()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.refresh_timer.stop()
        super().closeEvent(event)
