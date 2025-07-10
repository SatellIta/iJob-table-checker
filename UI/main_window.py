from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from .some_dialog import OpenFileDialog, CompareResultDialog   # 自己定义的一些实用窗口
from utils.read_docx import open_document, read_document, storage_info   # 从文档中读取宣讲会信息
from utils.read_url import analyze_info   # 从网页获取宣讲会信息
from utils.conference_info import Conference   # 宣讲会类
from utils.compare import compare_doc_web   # 对比宣讲会信息
from .setting import SettingMenu   # 设置菜单
#from utils.read_url import open_url

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("IJob")
        self.resize(800, 600)
        title_icon = QIcon("./UI/poop-smiley.png")
        self.setWindowIcon(title_icon)
        
        # 创建菜单栏
        self.create_menu()

        # 创建状态栏
        self.create_status_bar()
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 添加文件路径显示区域
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("当前未选择文件")
        
        button_layout = QHBoxLayout()
        
        # 打开文件按钮
        self.open_file_btn = QPushButton("打开文件")
        self.open_file_btn.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.open_file_btn.clicked.connect(self.show_open_dialog)
        
        # 查找信息按钮
        self.search_btn = QPushButton("查找网页")
        self.search_btn.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.search_btn.clicked.connect(self.start_search)
        
        # 添加按钮到布局
        button_layout.addWidget(self.open_file_btn)
        button_layout.addWidget(self.search_btn)
        
        # 添加文件路径区域和按钮区域到主布局
        main_layout.addWidget(QLabel("文件路径:"))
        main_layout.addWidget(self.file_path_edit)
        main_layout.addLayout(button_layout)
        
        # 创建结果显示区域
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setPlaceholderText("查询结果将显示在这里...")

        self.search_area = QTextEdit()
        self.search_area.setReadOnly(True)
        self.search_area.setPlaceholderText("对比结果将显示在这里...")
        
        compare_layout = QHBoxLayout()
        compare_layout.addWidget(self.result_area)
        compare_layout.addWidget(self.search_area)

        main_layout.addWidget(QLabel("查询结果:"))
        main_layout.addLayout(compare_layout)
        
        self.conferences_from_docx = []
        self.conferences_from_web = []

        # 设置比较信息按钮，默认隐藏，触发显示按钮的函数放在show_open_dialog()和start_search()中
        self.compare_btn = QPushButton("开始比较！")
        self.compare_btn.setIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.compare_btn.clicked.connect(self.start_compare)
        self.compare_btn.setVisible(False)
        main_layout.addWidget(self.compare_btn)

        
    
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
        reset_result_action = QAction("清除当前文档", self)
        reset_result_action.triggered.connect(self.reset_result)
        edit_menu.addAction(reset_result_action)

        reset_compare_action = QAction("清除对比结果", self)
        reset_compare_action.triggered.connect(self.reset_compare)
        edit_menu.addAction(reset_compare_action)

        '''
        # 创建设置菜单
        options_action = QAction("设置(&O)", self)
        # options_action.setShortcut("O")  
        # 这个很有意思，只要添加到菜单栏的主栏里，pyside会自动根据(&{char})中的char，给这个action或者menu项设置快捷键alt+char
        options_action.triggered.connect(self.open_options_menu)
        menu_bar.addAction(options_action)
        '''
        

    # 设置状态栏，将查询进度实时显示出来
    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_icon = QLabel()
        icon = QPixmap("./UI/poop-smiley.png").scaled(16, 16)
        self.status_icon.setPixmap(icon)

        self.status_bar.addWidget(self.status_icon)

    # 点击打开文件后触发
    def show_open_dialog(self):
        dialog = OpenFileDialog(self)
        if dialog.exec() == QDialog.Accepted:
            file_path = dialog.path_input.text()
        # 打开选择的docx
        doc = open_document(file_path)
        if doc:    
            self.conferences_from_docx = storage_info(doc)

            if self.conferences_from_docx:
                self.result_area.clear()
                self.result_area.append(f"共找到{len(self.conferences_from_docx)}个宣讲会\n")
                self.result_area.append("基本信息预览: ")

                for conf in self.conferences_from_docx:
                    self.result_area.append(f"\n宣讲会{conf.index}: {conf.title}")
                    self.result_area.append(f"时间: {conf.date}\t{conf.time}")
                    self.result_area.append(f"地点: {conf.place}")

        print(f"选择的文件路径: {file_path}")

        # 如果网页信息已存在，显示compare_btn
        if self.conferences_from_web:
            self.compare_btn.setVisible(True)

    # 点击查找按钮后触发
    def start_search(self):
        conferences = analyze_info()
        if conferences:
            self.conferences_from_web = conferences
            self.search_area.clear()
            self.search_area.append(f"共找到{len(self.conferences_from_web)}个宣讲会\n")
            self.search_area.append("基本信息预览: ")

            for conf in self.conferences_from_web:
                self.search_area.append(f"\n宣讲会{conf.index}: {conf.title}")
                self.search_area.append(f"时间: {conf.date}\t{conf.time}")
                self.search_area.append(f"地点: {conf.place}")

        # 如果文件信息已存在，显示比较按钮
        if self.conferences_from_docx:
            self.compare_btn.setVisible(True)     
    
    def start_compare(self):
        # 比较两个的内容
        compare_result = compare_doc_web(self.conferences_from_docx, self.conferences_from_web)

        # 根据比较结果创建提示窗口，CompareResultDialog的初始化里面已经考虑了两种情况
        dialog = CompareResultDialog(self, compare_result=compare_result)
        dialog.exec()


    # 点击清除当前文档按钮后触发
    def reset_result(self):
        self.conferences_from_docx.clear()
        self.result_area.clear()

    # 点击清除结构
    def reset_compare(self):
        self.conferences_from_web.clear()
        self.search_area.clear()

    # 打开设置菜单
    def open_options_menu(self):
        message = CompareResultDialog()
        message.exec()