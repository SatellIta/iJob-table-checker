import difflib
def compare_text(text1, text2):
    # 将文本按行分割
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    print(lines1)
    clear_lines1 = []
    clear_lines2 = []
    for line in lines1:
        clear_lines1.append(line.strip())
    print(clear_lines1)

    for line in lines2:
        clear_lines2.append(line.strip())

    # 使用ndiff比较并获取差异
    diff = list(difflib.ndiff(clear_lines1, clear_lines2))
    
    # 过滤出有差异的行
    differences = [line for line in diff if line.startswith('+ ') or line.startswith('- ') or line.startswith('? ')]
    
    return differences

text1 = "这是第行\n 这是第二行"


text2 = "这是第一行\n 第二行"

differences = compare_text(text1, text2)
if not differences:
    print("haha\n")
for d in differences:
    print(d)

print(differences)

list_ = []
list1 = ['- 这是第行', '+ 这是第一行', '?    +\n', '- 这是第二行', '? --\n', '+ 第二行']
list_.append("详情不同")
list_.append(list1)

list2 = []
for dif in list_:
    for item in dif:
        if isinstance(item, list):
            for subitem in item:
                list2.append(subitem)
        else:
            list2.append(item)

print(list_)
print(list2)