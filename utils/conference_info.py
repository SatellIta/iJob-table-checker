from dataclasses import dataclass

@dataclass
class Conference:
    index: int
    title: str
    place: str
    date: str
    time: str
    detail: str

    @classmethod
    def from_row(cls, row_data):
        '''
        从没有表格只有段落的数据创建Conference对象
        其中段落数据是根据ijob宣讲信息定制的
        '''
        

        return cls(
            index = 
            title = 
            place = 
            date = 
            time = 
            detail = 
        )