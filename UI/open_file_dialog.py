from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# 当用户点击打开文件选项的时候，会弹出新窗口
class OpenFileDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("选择文件")
        self.setFixedSize(450, 120)

        # 启用拖放功能
        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)

        # 添加文件选择框和浏览按钮
        path_layout = QHBoxLayout()
        self.path_label = QLabel("输入文件路径: ")
        self.path_input = QLineEdit(self)

        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_file)

        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)

        layout.addWidget(self.path_label)
        layout.addLayout(path_layout)

        # 添加确定和取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            self.path_input.setText(file_path)
            