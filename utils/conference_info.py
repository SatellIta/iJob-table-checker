from dataclasses import dataclass

'''
定义了conference类,读取数据并保存到类属性的方法暂时还在
read_docx.py 及 read_url.py 两个文件中
'''

@dataclass
class Conference:
    index: int
    title: str
    place: str
    date: str
    time: str
    detail: str
    