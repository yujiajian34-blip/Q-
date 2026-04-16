# -*- coding: utf-8 -*-
"""
心里话编辑窗口
用户可以在这里记录自己的想法和心事
支持历史记录查看功能
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
    QListWidget, QListWidgetItem, QComboBox, QMessageBox, QScrollArea,
    QCalendarWidget
)
from PyQt5.QtCore import Qt, QSize, QTimer, QDate
from PyQt5.QtGui import QFont, QColor
from datetime import datetime, timedelta
from inner_thoughts import InnerThoughtsManager, InnerThought


class InnerThoughtsWindow(QWidget):
    """心里话编辑窗口"""
    
    def __init__(self, inner_thoughts_manager: InnerThoughtsManager, parent=None):
        super().__init__(parent)
        self.inner_thoughts_manager = inner_thoughts_manager
        self.current_date = QDate.currentDate()  # 当前浏览的日期
        
        self.setWindowTitle("💭 说说心里话")
        self.setGeometry(100, 100, 900, 650)
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QWidget {
                background-color: #fff8f3;
                font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #ffcc99;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                color: #333;
            }
            QPushButton {
                background-color: #ffaa66;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff9944;
            }
            QPushButton:pressed {
                background-color: #ff8833;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #ffcc99;
                border-radius: 6px;
                padding: 5px;
                color: #333;
            }
            QListWidget {
                background-color: white;
                border: 2px solid #f0e6d2;
                border-radius: 8px;
                color: #333;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #ffe6cc;
            }
            QLabel {
                color: #333;
            }
        """)
        
        self.init_ui()
        self.load_today_thoughts()
    
    
    def init_ui(self):
        """初始化UI - 分为编辑区和历史记录区"""
        main_layout = QHBoxLayout()
        
        # ===== 左侧：编辑和今天记录 =====
        left_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("💭 把心里话记录下来吧")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        left_layout.addWidget(title_label)
        
        # 说明文字
        tip_label = QLabel("✨ 把想法和心事写下来，熊家会参考你的心事来写日记~")
        tip_label.setStyleSheet("color: #ff9944; font-size: 10px;")
        tip_label.setWordWrap(True)
        left_layout.addWidget(tip_label)
        
        # 编辑区域
        edit_label = QLabel("📝 今天的想法")
        edit_font = QFont()
        edit_font.setBold(True)
        edit_label.setFont(edit_font)
        left_layout.addWidget(edit_label)
        
        # 心情选择
        mood_layout = QHBoxLayout()
        mood_layout.addWidget(QLabel("心情:"))
        self.mood_combo = QComboBox()
        self.mood_combo.addItems(self.inner_thoughts_manager.MOOD_TAGS)
        self.mood_combo.setMaximumWidth(100)
        mood_layout.addWidget(self.mood_combo)
        mood_layout.addStretch()
        left_layout.addLayout(mood_layout)
        
        # 文本输入框
        self.thought_text = QTextEdit()
        self.thought_text.setPlaceholderText("写下你的想法…")
        self.thought_text.setMinimumHeight(80)
        self.thought_text.setMaximumHeight(120)
        left_layout.addWidget(self.thought_text)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存")
        save_btn.clicked.connect(self.save_thought)
        button_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.clicked.connect(self.clear_input)
        button_layout.addWidget(clear_btn)
        
        left_layout.addLayout(button_layout)
        
        # 今天的记录
        left_layout.addWidget(QLabel("📚 今天的心里话"))
        
        self.today_list = QListWidget()
        self.today_list.itemSelectionChanged.connect(self.on_today_thought_selected)
        left_layout.addWidget(self.today_list)
        
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.clicked.connect(self.delete_today_thought)
        left_layout.addWidget(delete_btn)
        
        # ===== 右侧：历史记录浏览 =====
        right_layout = QVBoxLayout()
        
        # 标题
        history_title = QLabel("📅 历史记录")
        history_font = QFont()
        history_font.setPointSize(14)
        history_font.setBold(True)
        history_title.setFont(history_font)
        right_layout.addWidget(history_title)
        
        # 日期导航按钮
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton("⬅ 前一天")
        prev_btn.clicked.connect(self.show_prev_day)
        nav_layout.addWidget(prev_btn)
        
        today_btn = QPushButton("📌 今天")
        today_btn.clicked.connect(self.show_today)
        nav_layout.addWidget(today_btn)
        
        next_btn = QPushButton("后一天 ➡")
        next_btn.clicked.connect(self.show_next_day)
        nav_layout.addWidget(next_btn)
        
        right_layout.addLayout(nav_layout)
        
        # 日期显示
        self.date_label = QLabel()
        self.update_date_label()
        right_layout.addWidget(self.date_label)
        
        # 日历
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(self.current_date)
        self.calendar.clicked.connect(self.on_calendar_date_selected)
        right_layout.addWidget(self.calendar)
        
        # 历史记录列表
        right_layout.addWidget(QLabel("该日期的心里话"))
        self.history_list = QListWidget()
        self.history_list.itemSelectionChanged.connect(self.on_history_thought_selected)
        right_layout.addWidget(self.history_list)
        
        # 统计信息
        self.stats_label = QLabel()
        self.update_stats()
        right_layout.addWidget(self.stats_label)
        
        # 合并左右布局
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)
        
        self.setLayout(main_layout)
        self.load_today_thoughts()
        self.load_history_thoughts()
    
    def save_thought(self):
        """保存心里话"""
        content = self.thought_text.toPlainText().strip()
        
        if not content:
            QMessageBox.warning(self, "提示", "请输入心里话呢~")
            return
        
        mood = self.mood_combo.currentText()
        self.inner_thoughts_manager.add_thought(content, mood)
        
        # 清空输入框
        self.thought_text.clear()
        
        # 刷新列表
        self.load_today_thoughts()
        self.load_history_thoughts()
        self.update_stats()
        
        QMessageBox.information(self, "保存成功", "✨ 熊家已经收到你的心里话了！")
    
    
    
    def load_today_thoughts(self):
        """加载今天的心里话"""
        self.today_list.clear()
        today_thoughts = self.inner_thoughts_manager.get_today_thoughts()
        
        if not today_thoughts:
            self.today_list.addItem("还没有记录呢，快来写一条吧 💭")
            return
        
        for i, thought in enumerate(today_thoughts):
            # 格式化显示
            time = thought.date.split(" ")[1] if " " in thought.date else ""
            preview = thought.content[:40] + "..." if len(thought.content) > 40 else thought.content
            
            text = f"[{thought.mood}] {time}\n{preview}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, i)
            
            # 根据心情标签设置颜色
            mood_colors = {
                "开心": "#FFE6CC",
                "普通": "#F0F0F0",
                "难过": "#E6F2FF",
                "感慨": "#FCE6FF",
                "感谢": "#E6FFE6",
                "甜蜜": "#FFE6F0",
                "期待": "#FFFFE6",
                "伤心": "#E6FFFF"
            }
            
            bg_color = mood_colors.get(thought.mood, "#FFFFFF")
            item.setBackground(QColor(bg_color))
            
            self.today_list.addItem(item)
    
    def load_history_thoughts(self):
        """加载指定日期的心里话"""
        self.history_list.clear()
        date_str = self.current_date.toString("yyyy-MM-dd")
        history_thoughts = self.inner_thoughts_manager.get_thoughts_by_date(date_str)
        
        if not history_thoughts:
            self.history_list.addItem("这一天还没有记录呢 📝")
            return
        
        for i, thought in enumerate(history_thoughts):
            time = thought.date.split(" ")[1] if " " in thought.date else ""
            preview = thought.content[:40] + "..." if len(thought.content) > 40 else thought.content
            
            text = f"[{thought.mood}] {time}\n{preview}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, i)
            item.setData(Qt.UserRole + 1, thought)  # 存储原对象
            
            mood_colors = {
                "开心": "#FFE6CC",
                "普通": "#F0F0F0",
                "难过": "#E6F2FF",
                "感慨": "#FCE6FF",
                "感谢": "#E6FFE6",
                "甜蜜": "#FFE6F0",
                "期待": "#FFFFE6",
                "伤心": "#E6FFFF"
            }
            
            bg_color = mood_colors.get(thought.mood, "#FFFFFF")
            item.setBackground(QColor(bg_color))
            
            self.history_list.addItem(item)
    
    def on_today_thought_selected(self):
        """选中今天的心里话"""
        current_item = self.today_list.currentItem()
        if not current_item:
            return
        
        index = current_item.data(Qt.UserRole)
        if index is not None:
            today_thoughts = self.inner_thoughts_manager.get_today_thoughts()
            if 0 <= index < len(today_thoughts):
                thought = today_thoughts[index]
                self.thought_text.setText(thought.content)
                self.mood_combo.setCurrentText(thought.mood)
    
    def on_history_thought_selected(self):
        """选中历史记录的心里话"""
        current_item = self.history_list.currentItem()
        if not current_item:
            return
        
        thought = current_item.data(Qt.UserRole + 1)
        if thought:
            self.thought_text.setText(thought.content)
            self.mood_combo.setCurrentText(thought.mood)
    
    def on_calendar_date_selected(self, qdate):
        """日历日期选中"""
        self.current_date = qdate
        self.update_date_label()
        self.load_history_thoughts()
    
    def update_date_label(self):
        """更新日期标签"""
        date_str = self.current_date.toString("yyyy-MM-dd")
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekdays[self.current_date.dayOfWeek() - 1]
        self.date_label.setText(f"📅 {date_str} {weekday}")
        self.date_label.setStyleSheet("color: #ff9944; font-weight: bold;")
    
    def show_prev_day(self):
        """显示前一天"""
        self.current_date = self.current_date.addDays(-1)
        self.calendar.setSelectedDate(self.current_date)
        self.update_date_label()
        self.load_history_thoughts()
    
    def show_next_day(self):
        """显示后一天"""
        self.current_date = self.current_date.addDays(1)
        self.calendar.setSelectedDate(self.current_date)
        self.update_date_label()
        self.load_history_thoughts()
    
    def show_today(self):
        """显示今天"""
        self.current_date = QDate.currentDate()
        self.calendar.setSelectedDate(self.current_date)
        self.update_date_label()
        self.load_history_thoughts()
    
    def delete_today_thought(self):
        """删除今天选中的心里话"""
        current_item = self.today_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择要删除的心里话")
            return
        
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这条心里话吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            index = current_item.data(Qt.UserRole)
            if index is not None:
                today_thoughts = self.inner_thoughts_manager.get_today_thoughts()
                if 0 <= index < len(today_thoughts):
                    thought_to_delete = today_thoughts[index]
                    for i, t in enumerate(self.inner_thoughts_manager.thoughts):
                        if t is thought_to_delete:
                            self.inner_thoughts_manager.delete_thought(i)
                            break
                    
                    self.load_today_thoughts()
                    self.load_history_thoughts()
                    self.update_stats()
                    self.clear_input()
                    QMessageBox.information(self, "删除成功", "✨ 已删除")
    
    def clear_input(self):
        """清空输入"""
        self.thought_text.clear()
        self.mood_combo.setCurrentIndex(1)  # 设回"普通"
    
    def update_stats(self):
        """更新统计信息"""
        stats = self.inner_thoughts_manager.get_statistics()
        today_count = stats['today_count']
        total_count = stats['total_count']
        stats_text = f"📊 今天: {today_count} 条  |  总计: {total_count} 条"
        self.stats_label.setText(stats_text)
        self.stats_label.setStyleSheet("color: #ff9944; font-size: 10px;")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        super().closeEvent(event)
