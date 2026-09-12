"""v0 最小版 —— 先读懂这个，再去看 todo.py

这个文件只有 20 行有效代码，但"数据不丢"的全部核心都在里面：
    读文件 -> 变成 Python 数据 -> 改 -> 写回文件

它故意不写函数、不写异常处理、不写命令行参数。
把它读懂、跑通、改坏、再修好，你就具备看 todo.py 的基础了。

跑法（在本目录下）：
    python v0_最小版.py
    python v0_最小版.py      # 再跑一次，看任务变成 2 条
"""

# import：把别人写好的工具箱拿进来用
#   json    负责「Python 数据 <-> 文本」的互相转换
#   pathlib 负责「找到文件到底在哪」
import json
from pathlib import Path

# Path(__file__)  这个 .py 文件自己
# .parent         它所在的文件夹
# / "todo.json"   拼成完整路径
# 变量名全大写是约定：表示"这是不会变的常量"
DATA_FILE = Path(__file__).parent / "todo.json"

# ---------- 第 1 步：把数据从磁盘读进内存 ----------
if DATA_FILE.exists():                                   # 文件存在吗？
    with open(DATA_FILE, "r", encoding="utf-8") as f:    # r = 只读模式
        tasks = json.load(f)                             # 文本 -> Python 的 list
else:
    tasks = []                                           # 第一次运行：内存里先放个空列表

# ---------- 第 2 步：在内存里修改 ----------
# {"title": ..., "done": ...} 是一个字典，表示一条任务
# tasks 是一个列表，里面装着若干这样的字典
# .append() 表示往列表末尾追加一个元素
tasks.append({"title": "背单词", "done": False})

# ---------- 第 3 步：写回磁盘 ----------
with open(DATA_FILE, "w", encoding="utf-8") as f:        # w = 覆盖写入
    # json.dump：把 Python 的 list/dict 变成文本写进文件
    # ensure_ascii=False：让中文还是中文，而不是 \u80cc 这种编码
    # indent=2：让文件带缩进，方便你用记事本打开检查
    json.dump(tasks, f, ensure_ascii=False, indent=2)

print("现在一共", len(tasks), "条任务")                  # len() 数列表里有几个元素
