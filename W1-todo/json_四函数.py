"""json 模块的四个函数 —— 跑一遍就懂

    读：load(文件对象)          loads(字符串)
    写：dump(数据, 文件对象)     dumps(数据) -> 字符串

记忆法：名字带 s 的是 string（处理字符串），不带 s 的是 file（处理文件）。
方向：load 是「文本 -> Python」，dump 是「Python -> 文本」，别记反。
"""

import json

task = {"id": 1, "title": "背单词", "done": False}
tasks = [task]


print("=== 1. dumps：Python 数据 -> 字符串 ===")
text = json.dumps(tasks, ensure_ascii=False, indent=2)
print("返回类型：", type(text))
print(text)

# print()
# print("=== 2. loads：字符串 -> Python 数据 ===")
# back = json.loads(text)
# print("返回类型：", type(back))
# print("取第一条的标题：", back[0]["title"])
#
# print()
# print("=== 3. dump：Python 数据 -> 写入文件 ===")
# with open("demo.json", "w", encoding="utf-8") as f:
#     json.dump(tasks, f, ensure_ascii=False, indent=2)
# print("已写入 demo.json")
#
# print()
# print("=== 4. load：文件 -> Python 数据 ===")
# with open("demo.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
# print("返回类型：", type(data))
# print("内容：", data)
#
# print()
# print("=== 对比：ensure_ascii 开与关 ===")
# print("默认(True) ：", json.dumps(task))
# print("False      ：", json.dumps(task, ensure_ascii=False))
#
# print()
# print("=== 类型对应关系 ===")
# print(json.dumps({"none": None, "bool": True, "tuple": (1, 2), "float": 3.5}))
# print("注意：元组 (1,2) 存进去会变成列表 [1, 2]")
