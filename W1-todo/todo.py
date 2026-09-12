"""todo-cli v1 — 第 1 周产出物（对应手册 W1 的 A / B / C 三块）

知识点：
  B 变量与控制流 / 函数与模块 / 异常处理 / 列表与字典
  C 数据持久化（open + json + encoding + pathlib）
  A 命令行程序入口 + 版本控制

用法：
    python todo.py add "背单词"
    python todo.py list
    python todo.py done 1
    python todo.py del 1
"""

import json
import sys
from pathlib import Path

# ============================================================
# C 块：数据持久化
# Path(__file__).parent = 本文件所在的目录。
# 用它拼出来的路径，无论你在哪个目录执行 python todo.py，
# 找到的都是同一个数据文件——这就是"数据不丢"的第一步。
# ============================================================
DATA_FILE = Path(__file__).parent / "todo.json"


def load_tasks() -> list[dict]:
    """从磁盘读出任务列表。

    三种情况都要能扛住：
      1. 文件还不存在（第一次运行）
      2. 文件内容被写坏（JSON 解析失败）
      3. 文件存在但没有读取权限
    """
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("[警告] todo.json 内容损坏，已按空列表处理")
        return []
    except OSError as error:
        print(f"[错误] 读取失败：{error}")
        return []


def save_tasks(tasks: list[dict]) -> None:
    """把任务列表写回磁盘。

    注意：'w' 模式一打开就会清空文件。
    所以流程永远是 先 load 全部 -> 在内存里改 -> 再 save 回去，
    绝不能在中间把 tasks 重置成空列表，否则旧数据就没了。
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # ensure_ascii=False：中文按中文写入，不写成 \u80cc\u5355\u8bcd
        # indent=2：文件格式化，方便你手动打开检查
        json.dump(tasks, f, ensure_ascii=False, indent=2)


# ============================================================
# B 块：函数、列表、字典、异常
# ============================================================
def next_id(tasks: list[dict]) -> int:
    """生成下一个编号：当前最大 id + 1。删掉的任务编号不复用。"""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(title: str) -> None:
    """新增一条任务。空内容属于非法输入。"""
    title = title.strip()
    if not title:
        print("[错误] 任务内容不能为空")
        return

    tasks = load_tasks()
    tasks.append({"id": next_id(tasks), "title": title, "done": False})
    save_tasks(tasks)
    print(f"[完成] 已添加：{title}")


def list_tasks() -> None:
    """查看全部任务。"""
    tasks = load_tasks()
    if not tasks:
        print("（还没有任务，先用 add 添加一条）")
        return

    print(f"共 {len(tasks)} 条任务：")
    for task in tasks:
        mark = "[x]" if task["done"] else "[ ]"
        print(f"  {mark} {task['id']}. {task['title']}")


def mark_done(task_id: int) -> None:
    """把指定编号的任务标记为完成。"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"[提示] 第 {task_id} 条已经是完成状态")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"[完成] 已标记完成：{task['title']}")
            return
    print(f"[错误] 没有编号为 {task_id} 的任务")


def delete_task(task_id: int) -> None:
    """删除指定编号的任务，其余任务必须原样保留。"""
    tasks = load_tasks()
    kept = [task for task in tasks if task["id"] != task_id]
    if len(kept) == len(tasks):          # 数量没变 = 编号不存在
        print(f"[错误] 没有编号为 {task_id} 的任务")
        return
    save_tasks(kept)
    print(f"[完成] 已删除第 {task_id} 条任务")


# ============================================================
# A 块：命令行入口
# ============================================================
USAGE = """用法：
  python todo.py add "任务内容"
  python todo.py list
  python todo.py done <编号>
  python todo.py del <编号>"""


def to_int(text: str) -> int | None:
    """把命令行参数转成整数；不是数字就返回 None，而不是让程序崩溃。"""
    try:
        return int(text)
    except ValueError:
        return None


def main() -> None:
    argv = sys.argv[1:]                  # sys.argv[0] 是脚本名，参数从 [1:] 开始

    if not argv:
        print(USAGE)
        return

    command = argv[0]

    if command == "add":
        if len(argv) < 2:
            print('[错误] add 后面要跟任务内容，例如：python todo.py add "背单词"')
        else:
            # 用 join 拼起来，这样不加引号写多个词也能用：
            #   python todo.py add 背单词 明天
            add_task(" ".join(argv[1:]))

    elif command == "list":
        list_tasks()

    elif command in ("done", "del"):
        if len(argv) < 2:
            print(f"[错误] {command} 后面要跟一个编号")
            return
        task_id = to_int(argv[1])
        if task_id is None:
            print(f"[错误] 编号必须是数字，你输入的是：{argv[1]}")
            return
        if command == "done":
            mark_done(task_id)
        else:
            delete_task(task_id)

    else:
        print(f"[错误] 未知命令：{command}")
        print(USAGE)


if __name__ == "__main__":               # 只有直接运行本文件时才执行
    main()
