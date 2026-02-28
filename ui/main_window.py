from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from .chat_widget import ChatWidget
from .settings import SettingsWidget
from core import ChatManager
from utils import ConfigManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.chat_manager = ChatManager(self.config_manager)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("💖 AI女友")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 10, 10, 10)
        
        self.chat_button = QPushButton("💬 聊天")
        self.chat_button.setCheckable(True)
        self.chat_button.setChecked(True)
        self.chat_button.clicked.connect(lambda: self.switch_page(0))
        
        self.settings_button = QPushButton("⚙️ 设置")
        self.settings_button.setCheckable(True)
        self.settings_button.clicked.connect(lambda: self.switch_page(1))
        
        for btn in [self.chat_button, self.settings_button]:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    background-color: #f5f5f5;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #ff8a80;
                    color: white;
                }
                QPushButton:hover:!checked {
                    background-color: #e0e0e0;
                }
            """)
        
        nav_layout.addWidget(self.chat_button)
        nav_layout.addWidget(self.settings_button)
        nav_layout.addStretch()
        
        main_layout.addLayout(nav_layout)
        
        self.page_stack = QStackedWidget()
        
        self.chat_widget = ChatWidget(self.chat_manager)
        self.settings_widget = SettingsWidget(self.config_manager)
        
        self.page_stack.addWidget(self.chat_widget)
        self.page_stack.addWidget(self.settings_widget)
        
        main_layout.addWidget(self.page_stack)
        central_widget.setLayout(main_layout)

    def switch_page(self, index: int):
        self.chat_button.setChecked(index == 0)
        self.settings_button.setChecked(index == 1)
        self.page_stack.setCurrentIndex(index)
        
        if index == 0:
            self.chat_manager.reload_config()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "确认退出", "确定要退出吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
