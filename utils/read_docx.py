from docx import Document
from PySide6.QtWidgets import QMessageBox
from conference_info import Conference
import os, re

def open_document(file_path):
    '''
    读取word文件,并返回文档对象

    args:
        file_path: word文档的路径
    '''
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        # 检查文件扩展名
        if not file_path.lower().endswith('.docx'):
            raise ValueError("不是有效的Word文档(.docx)文件")
            
        # 尝试打开文档
        doc = Document(file_path)
        return doc
        
    except Exception as e:
        oops = QMessageBox()
        oops.setWindowTitle(" ")
        oops.setText(f"无法打开文件: {os.path.basename(file_path)}")
        oops.setInformativeText(f"错误原因: {str(e)}")
        oops.setStandardButtons(QMessageBox.Ok)
        oops.setIcon(QMessageBox.Warning)
        oops.exec()
        return None

# 读取所有宣讲会的信息函数
def read_document(doc):
    row_data = []
    for line in doc.paragraphs:
        if line.text.strip():
            row_data.append(line)
        else:
            continue

    return row_data

# 传入doc文件,创建并返回所有包含所有宣讲会的列表
def storage_info(doc):
    row_data = read_document(doc)
    conferences = []
    current_conference = None
    conference_data = []
    pattern = re.compile(r'No\.\s*(\d+)')  # 匹配"No.数字"模式
    
    for i, paragraph in enumerate(row_data):
        text = paragraph.text.strip()
        match = pattern.search(text)
        
        if match:
            # 找到新的会议编号，如果已有会议信息则先保存
            if current_conference is not None and conference_data:
                # 创建会议对象并添加到列表
                conf = create_conference(current_conference, conference_data)
                if conf:
                    conferences.append(conf)
                # 清空当前会议数据
                conference_data = []
            
            # 提取会议编号
            current_conference = int(match.group(1))
            # 保存当前行，可能包含会议标题
            conference_data.append(text)
        elif current_conference is not None:
            # 继续收集当前会议的信息
            conference_data.append(text)
    
    # 处理最后一个会议
    if current_conference is not None and conference_data:
        conf = create_conference(current_conference, conference_data)
        if conf:
            conferences.append(conf)
    
    return conferences

def create_conference(index, data_lines):
    """
    从收集的文本行创建Conference对象
    
    参数:
        index: 会议编号
        data_lines: 会议相关的文本行列表
    """
    if not data_lines:
        return None
    
    # 基本处理逻辑 - 根据实际文档格式调整
    title = data_lines[0]  # 假设第一行包含标题
    
    # 尝试解析地点、日期和时间
    place = ""
    date = ""
    time = ""
    detail = ""
    
    # 寻找含有地点的行
    place_pattern = re.compile(r'地\s*点[:：]\s*(.*)', re.IGNORECASE)
    # 寻找含有日期的行
    date_pattern = re.compile(r'日\s*期[:：]\s*(.*)', re.IGNORECASE)
    # 寻找含有时间的行
    time_pattern = re.compile(r'时\s*间[:：]\s*(.*)', re.IGNORECASE)
    
    for line in data_lines[1:]:  # 跳过标题行
        # 检查地点
        place_match = place_pattern.search(line)
        if place_match:
            place = place_match.group(1).strip()
            continue
            
        # 检查日期
        date_match = date_pattern.search(line)
        if date_match:
            date = date_match.group(1).strip()
            continue
            
        # 检查时间
        time_match = time_pattern.search(line)
        if time_match:
            time = time_match.group(1).strip()
            continue
            
        # 其他行作为详情
        if detail:
            detail += "\n" + line
        else:
            detail = line
    
    # 创建并返回Conference对象
    return Conference(
        index=index,
        title=title.replace(f"No.{index}", "").strip(),  # 移除标题中的编号
        place=place,
        date=date,
        time=time,
        detail=detail
    )
        