import difflib    # 用于比较文本的标准库
import re
from .conference_info import Conference

# 比对宣讲会信息的不同，有不同返回字典，无不同返回None
def compare_doc_web(conferences_from_doc, conferences_from_web):
    compare_result = {}
    # 标记错误的索引
    idx = 1          
    for conf_doc in conferences_from_doc:
        # 用于检查是否找到一致标题的宣讲会
        checked = False     

        for conf_web in conferences_from_web:
            if conf_doc.title == conf_web.title:
                checked = True
                break
        
        # 匹配则开始对比每一项内容
        if checked:
            res = compare_conf(conf_doc, conf_web)
            if res:
                compare_result[idx] = []
                compare_result[idx].append(res)
            else:
                idx += 1
                continue
        # 没有匹配则计入未匹配错误
        else:
            res = f"没有找到宣讲会: {conf_doc.title}"
            compare_result[idx] = []
            compare_result[idx].append(res)
            idx += 1
            continue
    
    if compare_result:
        return compare_result
    else:
        return None

# 比较两个宣讲会信息，返回不一致的列表
def compare_conf(conf_1: Conference, conf_2: Conference):
    """
    conf_2 的detail属性中包含长于conf_1 的detail属性中的字符串
    应该先将conf_2.detail截断成conf_1.detail大致的长度
    """
    differences = []

    # 比较日期
    if conf_1.date != conf_2.date:
        diff = difference(conf_1.date, conf_2.date)
        differences.append(f"日期不同:\n")
        differences.append(diff)

    # 比较时间
    if conf_1.time != conf_2.time:
        diff = difference(conf_1.time, conf_2.time)
        differences.append(f"时间不同:\n")
        differences.append(diff)

    # 比较地点
    if conf_1.place != conf_2.place:
        diff = difference(conf_1.place, conf_2.place)
        differences.append(f"地点不同:\n")
        differences.append(diff)

    # 比较内容
    # 先截断conf_2.detail，找到共同的开头
    start_idx = conf_2.detail.find(conf_1.detail[:len("三个字")])
    text2 = conf_2.detail[start_idx: ]
    #end_idx = min(len(conf_1.detail) + 100, len(text2))
    #text2 = conf_2.detail[start_idx:end_idx]
    if conf_1.detail != text2:
        # 先把没有\n的文段截成按段排列的
        text1 = truncate(conf_1.detail)
        text2 = truncate(text2)

        # 统计text1的段数，以此为依据再次截取text2
        num = 0
        for char in text1:
            if char == '\n':
                num += 1

        for idx, char in enumerate(text2):
            if char == '\n':
                num -= 1
            if num == 0:
                idx += 1
                text2 = text2[:idx]

        diff = difference(text1, text2)
        differences.append(f"详情不同:\n")
        #diff = diff[:-3]  # conf2中的detail比conf1中的长，所以不要最后的不同部分
        differences.append(diff)
    
    return differences

# 输入两个字符串，利用difflib.ndiff比较并获取差异
def difference(str1: str, str2: str):
    lines1 = str1.splitlines()
    lines2 = str2.splitlines()
    clear_lines1 = []
    clear_lines2 = []
    # 清除多余的空白符
    for line in lines1:
        if line.strip():  # 确保没有空行
            clear_lines1.append(line.strip())
    for line in lines2:
        if line.strip():
            clear_lines2.append(line.strip())

    diff = list(difflib.ndiff(clear_lines1, clear_lines2))

    # 过滤出有差异的行
    diffs = [line for line in diff if line.startswith('+ ') or line.startswith('- ') or line.startswith('? ')]

    return diffs

# 按照标点来分段
def truncate(text: str):
    for punct in "，。？！,?!":  # AI给的算法总是出乎意料地简单
        text = text.replace(punct, punct + '\n')

    return text