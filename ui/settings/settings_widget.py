from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QFormLayout, QLineEdit, QComboBox, QSpinBox, 
    QDoubleSpinBox, QPushButton, QLabel, QGroupBox,
    QTextEdit, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from utils import ConfigManager


class SettingsWidget(QWidget):
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        tabs.addTab(self.create_model_tab(), "模型设置")
        tabs.addTab(self.create_character_tab(), "角色设定")
        tabs.addTab(self.create_voice_tab(), "语音设置")
        tabs.addTab(self.create_memory_tab(), "记忆设置")
        
        layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("保存设置")
        save_button.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        reset_button = QPushButton("重置默认")
        reset_button.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_model_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        llm_group = QGroupBox("语言模型设置")
        llm_layout = QFormLayout()
        
        self.active_llm_combo = QComboBox()
        self.active_llm_combo.addItems(["deepseek", "openai"])
        self.active_llm_combo.setCurrentText(self.config.get("active_llm", "deepseek"))
        llm_layout.addRow("当前使用模型:", self.active_llm_combo)
        
        self.deepseek_api_key = QLineEdit(self.config.get("llm_models.deepseek.api_key", ""))
        self.deepseek_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        llm_layout.addRow("DeepSeek API Key:", self.deepseek_api_key)
        
        self.deepseek_api_base = QLineEdit(self.config.get("llm_models.deepseek.api_base", "https://api.deepseek.com"))
        llm_layout.addRow("DeepSeek API Base:", self.deepseek_api_base)
        
        self.deepseek_model = QLineEdit(self.config.get("llm_models.deepseek.model", "deepseek-chat"))
        llm_layout.addRow("DeepSeek 模型:", self.deepseek_model)
        
        self.openai_api_key = QLineEdit(self.config.get("llm_models.openai.api_key", ""))
        self.openai_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        llm_layout.addRow("OpenAI API Key:", self.openai_api_key)
        
        self.openai_api_base = QLineEdit(self.config.get("llm_models.openai.api_base", "https://api.openai.com/v1"))
        llm_layout.addRow("OpenAI API Base:", self.openai_api_base)
        
        self.openai_model = QLineEdit(self.config.get("llm_models.openai.model", "gpt-3.5-turbo"))
        llm_layout.addRow("OpenAI 模型:", self.openai_model)
        
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(self.config.get("llm_models.deepseek.temperature", 0.7))
        llm_layout.addRow("温度 (Temperature):", self.temperature_spin)
        
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 8000)
        self.max_tokens_spin.setSingleStep(100)
        self.max_tokens_spin.setValue(self.config.get("llm_models.deepseek.max_tokens", 2000))
        llm_layout.addRow("最大 Token 数:", self.max_tokens_spin)
        
        llm_group.setLayout(llm_layout)
        layout.addWidget(llm_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_character_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        char_group = QGroupBox("角色设定")
        char_layout = QFormLayout()
        
        self.char_name = QLineEdit(self.config.get("character.name", "小萌"))
        char_layout.addRow("名字:", self.char_name)
        
        self.char_nickname = QLineEdit(self.config.get("character.nickname", "萌萌"))
        char_layout.addRow("昵称:", self.char_nickname)
        
        self.char_personality = QLineEdit("、".join(self.config.get("character.personality", ["温柔", "可爱", "体贴"])))
        char_layout.addRow("性格 (用顿号分隔):", self.char_personality)
        
        self.char_avatar = QLineEdit(self.config.get("character.avatar", "default"))
        char_layout.addRow("头像:", self.char_avatar)
        
        self.char_background = QTextEdit(self.config.get("character.background_story", ""))
        self.char_background.setMaximumHeight(100)
        char_layout.addRow("背景故事:", self.char_background)
        
        char_group.setLayout(char_layout)
        layout.addWidget(char_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_voice_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        voice_group = QGroupBox("语音设置")
        voice_layout = QFormLayout()
        
        self.active_tts_combo = QComboBox()
        self.active_tts_combo.addItems(["edge-tts"])
        self.active_tts_combo.setCurrentText(self.config.get("active_tts", "edge-tts"))
        voice_layout.addRow("语音引擎:", self.active_tts_combo)
        
        self.tts_voice = QLineEdit(self.config.get("tts_models.edge-tts.voice", "zh-CN-XiaoxiaoNeural"))
        voice_layout.addRow("音色:", self.tts_voice)
        
        self.tts_rate = QLineEdit(self.config.get("tts_models.edge-tts.rate", "+0%"))
        voice_layout.addRow("语速:", self.tts_rate)
        
        self.tts_pitch = QLineEdit(self.config.get("tts_models.edge-tts.pitch", "+0Hz"))
        voice_layout.addRow("音调:", self.tts_pitch)
        
        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_memory_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        memory_group = QGroupBox("记忆设置")
        memory_layout = QFormLayout()
        
        self.short_term_max = QSpinBox()
        self.short_term_max.setRange(5, 100)
        self.short_term_max.setValue(self.config.get("memory.short_term_max", 20))
        memory_layout.addRow("短期记忆最大消息数:", self.short_term_max)
        
        self.long_term_enabled = QComboBox()
        self.long_term_enabled.addItems(["启用", "禁用"])
        self.long_term_enabled.setCurrentText("启用" if self.config.get("memory.long_term_enabled", True) else "禁用")
        memory_layout.addRow("长期记忆:", self.long_term_enabled)
        
        self.auto_summarize = QComboBox()
        self.auto_summarize.addItems(["启用", "禁用"])
        self.auto_summarize.setCurrentText("启用" if self.config.get("memory.auto_summarize", True) else "禁用")
        memory_layout.addRow("自动总结:", self.auto_summarize)
        
        memory_group.setLayout(memory_layout)
        layout.addWidget(memory_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def save_settings(self):
        self.config.set("active_llm", self.active_llm_combo.currentText())
        self.config.set("llm_models.deepseek.api_key", self.deepseek_api_key.text())
        self.config.set("llm_models.deepseek.api_base", self.deepseek_api_base.text())
        self.config.set("llm_models.deepseek.model", self.deepseek_model.text())
        self.config.set("llm_models.deepseek.temperature", self.temperature_spin.value())
        self.config.set("llm_models.deepseek.max_tokens", self.max_tokens_spin.value())
        
        self.config.set("llm_models.openai.api_key", self.openai_api_key.text())
        self.config.set("llm_models.openai.api_base", self.openai_api_base.text())
        self.config.set("llm_models.openai.model", self.openai_model.text())
        self.config.set("llm_models.openai.temperature", self.temperature_spin.value())
        
        self.config.set("character.name", self.char_name.text())
        self.config.set("character.nickname", self.char_nickname.text())
        self.config.set("character.personality", [p.strip() for p in self.char_personality.text().split("、") if p.strip()])
        self.config.set("character.avatar", self.char_avatar.text())
        self.config.set("character.background_story", self.char_background.toPlainText())
        
        self.config.set("active_tts", self.active_tts_combo.currentText())
        self.config.set("tts_models.edge-tts.voice", self.tts_voice.text())
        self.config.set("tts_models.edge-tts.rate", self.tts_rate.text())
        self.config.set("tts_models.edge-tts.pitch", self.tts_pitch.text())
        
        self.config.set("memory.short_term_max", self.short_term_max.value())
        self.config.set("memory.long_term_enabled", self.long_term_enabled.currentText() == "启用")
        self.config.set("memory.auto_summarize", self.auto_summarize.currentText() == "启用")
        
        QMessageBox.information(self, "成功", "设置已保存！")

    def reset_settings(self):
        reply = QMessageBox.question(
            self, "确认", "确定要重置为默认设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config.config = self.config.get_default_config()
            self.config.save_config()
            self.reload_settings()
            QMessageBox.information(self, "成功", "已重置为默认设置！")

    def reload_settings(self):
        self.active_llm_combo.setCurrentText(self.config.get("active_llm", "deepseek"))
        self.deepseek_api_key.setText(self.config.get("llm_models.deepseek.api_key", ""))
        self.deepseek_api_base.setText(self.config.get("llm_models.deepseek.api_base", "https://api.deepseek.com"))
        self.deepseek_model.setText(self.config.get("llm_models.deepseek.model", "deepseek-chat"))
        self.openai_api_key.setText(self.config.get("llm_models.openai.api_key", ""))
        self.openai_api_base.setText(self.config.get("llm_models.openai.api_base", "https://api.openai.com/v1"))
        self.openai_model.setText(self.config.get("llm_models.openai.model", "gpt-3.5-turbo"))
        self.temperature_spin.setValue(self.config.get("llm_models.deepseek.temperature", 0.7))
        self.max_tokens_spin.setValue(self.config.get("llm_models.deepseek.max_tokens", 2000))
        
        self.char_name.setText(self.config.get("character.name", "小萌"))
        self.char_nickname.setText(self.config.get("character.nickname", "萌萌"))
        self.char_personality.setText("、".join(self.config.get("character.personality", ["温柔", "可爱", "体贴"])))
        self.char_avatar.setText(self.config.get("character.avatar", "default"))
        self.char_background.setPlainText(self.config.get("character.background_story", ""))
        
        self.active_tts_combo.setCurrentText(self.config.get("active_tts", "edge-tts"))
        self.tts_voice.setText(self.config.get("tts_models.edge-tts.voice", "zh-CN-XiaoxiaoNeural"))
        self.tts_rate.setText(self.config.get("tts_models.edge-tts.rate", "+0%"))
        self.tts_pitch.setText(self.config.get("tts_models.edge-tts.pitch", "+0Hz"))
        
        self.short_term_max.setValue(self.config.get("memory.short_term_max", 20))
        self.long_term_enabled.setCurrentText("启用" if self.config.get("memory.long_term_enabled", True) else "禁用")
        self.auto_summarize.setCurrentText("启用" if self.config.get("memory.auto_summarize", True) else "禁用")
