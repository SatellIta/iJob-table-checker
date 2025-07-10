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

# 提示文件打开成功，没有使用
class SuccessMessage(QMessageBox):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("文件打开成功")
        self.setFixedSize(200, 120)

        layout = QVBoxLayout(self)
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        button.accepted.connect(self.accept)
        layout.addWidget(button)

        self.setLayout(layout)

# 提示文件打开失败，返回错误原因
class FailFileMessage(QMessageBox):
    def __init__(self, parent = None, filename="", error_message=None):
        super().__init__(parent)

        self.setWindowTitle("文件打开失败")
        self.setIcon(QMessageBox.Critical)
        self.setText(f"无法打开文件: {filename}")

        if error_message:
            self.setInformativeText(f"错误原因: {error_message}")

        self.setStandardButtons(QMessageBox.Ok)

# 提示网络连接问题，返回错误原因
class FailWebMessage(QMessageBox):
    def __init__(self, parent=None, error_message=None):
        super().__init__(parent)

        self.setWindowTitle("连接出错")
        self.setIcon(QMessageBox.Critical)
        self.setText(f"可能是以下问题: ")

        if error_message:
            self.setInformativeText(f"{error_message}")

        self.setStandardButtons(QMessageBox.Ok)

# 显示比较结果的窗口
class CompareResultDialog(QDialog):
    def __init__(self, parent=None, compare_result=None):
        super().__init__(parent)

        self.setWindowTitle("比较结果")
        self.resize(800, 600)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation)) 
        
        # 创建窗口布局，上面部分是比较结果，如果有不一致，将会显示在info_area中
        # 如无不一致，则不会显示info_area
        main_area = QVBoxLayout()
        title_label = QLabel()

        if compare_result:
            title_label.setText(f"发现如下{len(compare_result)}处不一致: \n")
        else:
            title_label.setText("没有发现错误！")

        main_area.addWidget(title_label)

        # 初始化info_area
        info_area = QHBoxLayout()
        info = QTextEdit()
        info.setReadOnly(True)
        if compare_result:
            info.clear()

            # 将不同处按格式排布在info区域内
            for idx, differences in compare_result.items():
                info.append(f"{idx}: \n")

                # 展平嵌套列表
                for dif in differences:

                    for item in dif:

                        if isinstance(item, list):
                            for subitem in item:
                                info.append(subitem)

                        else:
                            info.append(item)
                    
            info_area.addWidget(info)
            main_area.addLayout(info_area)
        
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        button.accepted.connect(self.accept)
        main_area.addWidget(button)
        self.setLayout(main_area)