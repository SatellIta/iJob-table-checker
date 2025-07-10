from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os, re, json

class SettingMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("设置")
        self.setMinimumSize(500, 400)

        # 设置config文件路径
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
        self.config_file = os.path.join(self.config_dir, "setting.json")

        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # 默认配置
        self.default_settings = {
            "general": {
                "auto_check": False,   # 读取完后是否自动对比内容
                "days_ahead": 1,   # 预告的日期与当前日期的差值
                "theme": "system",
            },
            "network": {
                "timeout": 5,
                
            },
            "files": {
                "default_save_path": os.path.join(os.path.dirname(self.config_dir), "saves"),
                "auto_save": False,
            }
        }

        # 加载配置
        self.settings = self.load_settings()

        # 创建设置菜单UI
        self.init_ui()

    # 从配置文件读取设置，失败则返回默认配置
    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                QMessageBox.warning(self, "加载配置文件错误", f"无法加载设置：{str(e)}\n将使用默认设置！")

        
