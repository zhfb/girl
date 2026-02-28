import asyncio
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCursor


class ChatMessageWidget(QFrame):
    def __init__(self, role: str, content: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.content = content
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        avatar_label = QLabel("👤" if self.role == "user" else "💬")
        avatar_label.setFixedSize(40, 40)
        avatar_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background-color: #f0f0f0;
                border-radius: 20px;
                qproperty-alignment: AlignCenter;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        name_label = QLabel("你" if self.role == "user" else "小萌")
        name_label.setStyleSheet("font-weight: bold; color: #666;")
        
        text_label = QLabel(self.content)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("""
            QLabel {
                background-color: %s;
                padding: 10px;
                border-radius: 10px;
                color: #333;
            }
        """ % ("#e3f2fd" if self.role == "user" else "#f5f5f5"))
        
        content_layout.addWidget(name_label)
        content_layout.addWidget(text_label)
        
        if self.role == "user":
            layout.addStretch()
            layout.addWidget(content_widget)
            layout.addWidget(avatar_label)
        else:
            layout.addWidget(avatar_label)
            layout.addWidget(content_widget)
            layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("""
            ChatMessageWidget {
                background-color: transparent;
            }
        """)


class ChatWorker(QThread):
    message_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, chat_manager, user_message: str):
        super().__init__()
        self.chat_manager = chat_manager
        self.user_message = user_message

    async def _run_async(self):
        try:
            async for chunk in self.chat_manager.send_message(self.user_message, stream=True):
                self.message_received.emit(chunk)
        except Exception as e:
            self.message_received.emit(f"错误: {str(e)}")
        finally:
            self.finished.emit()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_async())
        loop.close()


class TTSWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, chat_manager, text: str):
        super().__init__()
        self.chat_manager = chat_manager
        self.text = text

    async def _run_async(self):
        try:
            audio_path = await self.chat_manager.synthesize_voice(self.text)
            self.finished.emit(audio_path if audio_path else "")
        except Exception:
            self.finished.emit("")

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_async())
        loop.close()


class ChatWidget(QWidget):
    def __init__(self, chat_manager, parent=None):
        super().__init__(parent)
        self.chat_manager = chat_manager
        self.current_assistant_message = ""
        self.current_message_widget = None
        self.init_ui()
        self.load_history()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        header = QLabel("💖 AI女友聊天")
        header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                background-color: #ffcdd2;
                color: #c62828;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.addStretch()
        self.messages_layout.setSpacing(5)
        
        self.scroll_area.setWidget(self.messages_container)
        layout.addWidget(self.scroll_area)
        
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #ff8a80;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("发送")
        self.send_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background-color: #ff8a80;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        self.setLayout(layout)

    def load_history(self):
        messages = self.chat_manager.short_term_memory.get_full_messages()
        for msg in messages:
            self.add_message(msg.role, msg.content, animate=False)

    def add_message(self, role: str, content: str, animate: bool = True):
        if not content.strip():
            return
            
        message_widget = ChatMessageWidget(role, content)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_widget)
        
        if animate:
            QTimer.singleShot(100, lambda: self.scroll_to_bottom())

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        user_message = self.input_field.text().strip()
        if not user_message:
            return
            
        self.input_field.clear()
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        
        self.add_message("user", user_message)
        
        self.current_assistant_message = ""
        self.current_message_widget = None
        
        self.worker = ChatWorker(self.chat_manager, user_message)
        self.worker.message_received.connect(self.on_message_chunk)
        self.worker.finished.connect(self.on_chat_finished)
        self.worker.start()

    def on_message_chunk(self, chunk: str):
        self.current_assistant_message += chunk
        
        if self.current_message_widget is None:
            self.current_message_widget = ChatMessageWidget("assistant", self.current_assistant_message)
            self.messages_layout.insertWidget(self.messages_layout.count() - 1, self.current_message_widget)
        else:
            self.current_message_widget.content = self.current_assistant_message
            for child in self.current_message_widget.findChildren(QLabel):
                if child.text() not in ["👤", "💬", "你", "小萌"]:
                    child.setText(self.current_assistant_message)
                    break
            self.current_message_widget.update()
        
        self.scroll_to_bottom()

    def on_chat_finished(self):
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()
        
        if self.current_assistant_message:
            self.play_voice(self.current_assistant_message)

    def play_voice(self, text: str):
        self.tts_worker = TTSWorker(self.chat_manager, text)
        self.tts_worker.finished.connect(self.on_voice_finished)
        self.tts_worker.start()

    def on_voice_finished(self, audio_path: str):
        if audio_path:
            pass
