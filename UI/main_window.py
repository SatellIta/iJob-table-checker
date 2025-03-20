from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from .open_file_dialog import OpenFileDialog
from utils.read_docx import open_document, read_document, storage_info
from utils.conference_info import Conference

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("IJob")
        self.resize(800, 600)
        title_icon = QIcon("./UI/poop-smiley.png")
        self.setWindowIcon(title_icon)
        
        # 创建主菜单
        self.create_menu()
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 创建两个文本框
        self.text_box1 = QLineEdit()
        self.text_box2 = QLineEdit()
        
        # 添加标签和文本框到布局
        layout.addWidget(QLabel("文本框 1:"))
        layout.addWidget(self.text_box1)
        layout.addWidget(QLabel("文本框 2:"))
        layout.addWidget(self.text_box2)
        
        # 添加一些空白空间
        layout.addStretch()
    
    def create_menu(self):
        # 创建菜单栏
        menu_bar = self.menuBar()
        
        # 创建文件菜单
        file_menu = menu_bar.addMenu("文件(&F)")
        
        # 添加文件菜单项
        open_action = QAction("打开(&O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.show_open_dialog)
        file_menu.addAction(open_action)
        
        save_action = QAction("保存(&S)", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 创建编辑菜单
        edit_menu = menu_bar.addMenu("编辑(&E)")
        
        # 添加编辑菜单项
        clear_action = QAction("清除文本框", self)
        clear_action.triggered.connect(self.clear_text_boxes)
        edit_menu.addAction(clear_action)
    
    def clear_text_boxes(self):
        self.text_box1.clear()
        self.text_box2.clear()

    # 点击打开文件后触发
    def show_open_dialog(self):
        dialog = OpenFileDialog(self)
        if dialog.exec() == QDialog.Accepted:
            file_path = dialog.path_input.text()
        # 打开选择的docx
        doc = open_document(file_path)
        conferences = storage_info(doc)

        print(f"选择的文件路径: {file_path}")