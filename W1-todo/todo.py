"""todo-cli v1 — 第 1 周产出物（对应手册 W1 的 A / B / C 三块）

知识点：
  B 变量与控制流 / 函数与模块 / 异常处理 / 列表与字典
  C 数据持久化（open + json + encoding + pathlib）
  A 命令行程序入口 + 版本控制 + 退出码

用法：
    python todo.py add "背单词"
    python todo.py list
    python todo.py done 1
    python todo.py del 1

退出码（终端和脚本靠它判断"成功还是失败"）：
    0 = 成功
    1 = 用法错误 / 参数非法 / 编号不存在 / 数据文件不可读
可以自己验证：
    python todo.py list ; echo $LASTEXITCODE        # PowerShell: $LASTEXITCODE
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# C 块：数据持久化
# Path(__file__).parent = 本文件所在的目录。
# 用它拼出来的路径，无论你在哪个目录执行 python todo.py，
# 找到的都是同一个数据文件——这就是"数据不丢"的第一步。
# ============================================================
DATA_FILE = Path(__file__).parent / "todo.json"


def decode_text(raw: bytes) -> str | None:
    """字节 -> 文本。

    "utf-8-sig" 比 "utf-8" 多一个本事：能自动吃掉 Windows 记事本
    可能加在文件开头的 BOM。带 BOM 的 JSON 用 "utf-8" 读会解析失败。
    UTF-8 读不了（比如文件是记事本按 ANSI/GBK 存的）就再试 GBK。
    两种都不行才返回 None。
    """
    for encoding in ("utf-8-sig", "gbk"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def is_task_list(data: object) -> bool:
    """检查读出来的东西是不是我们期望的形状。

    期望：一个列表，每一项都是带 id/title/done 三个键的字典。
    光靠 json.loads 只能保证"是合法 JSON"，保证不了形状——
    文件里写个 {} 或 [{"title": "x"}] 也是合法 JSON，但后面会崩。
    """
    if not isinstance(data, list):
        return False
    return all(
        isinstance(task, dict)
        and isinstance(task.get("id"), int)
        and isinstance(task.get("title"), str)
        and isinstance(task.get("done"), bool)
        for task in data
    )


def broken_file(reason: str) -> list[dict]:
    """数据文件读不出来时的统一出口：先备份原文件，再返回空列表。

    为什么必须备份？因为 save_tasks 用的是 'w' 模式，一打开就清空文件。
    如果读失败时直接返回 []，那么下一次 add 就会把旧数据整片抹掉。
    这是"从别处拷来的 todo.json 编码不对"最容易踩的数据丢失坑。
    """
    stamp = f"{datetime.now():%Y%m%d-%H%M%S}"
    backup = DATA_FILE.parent / f"{DATA_FILE.name}.bad-{stamp}"
    index = 1
    while backup.exists():          # 同一秒里坏两次，也不要让备份互相覆盖
        backup = DATA_FILE.parent / f"{DATA_FILE.name}.bad-{stamp}-{index}"
        index += 1
    print(f"[警告] {DATA_FILE.name} 无法读取：{reason}")
    try:
        DATA_FILE.replace(backup)
        print(f"[警告] 原文件已备份为 {backup.name}，不会被覆盖；本次按空列表处理")
    except OSError as error:
        print(f"[错误] 备份失败（{error}），请先手动备份 {DATA_FILE.name} 再继续")
    return []


def load_tasks() -> list[dict]:
    """从磁盘读出任务列表。

    四种情况都要能扛住：
      1. 文件还不存在（第一次运行）——返回空列表，这是正常的
      2. 文件不是 UTF-8（从别的电脑或编辑器搬过来的，常见是 ANSI/GBK 或带 BOM）
      3. 内容不是合法 JSON，或结构不对（顶层不是任务列表）——备份后按空列表处理
      4. 文件存在但没有读取权限、或被别的程序锁着——报错并尽量备份，绝不静默覆盖
    """
    if not DATA_FILE.exists():
        return []

    try:
        raw = DATA_FILE.read_bytes()          # 先按字节读，编码问题才好处理
    except OSError as error:
        return broken_file(f"读取失败：{error}")

    text = decode_text(raw)
    if text is None:
        return broken_file("既不是 UTF-8 也不是 GBK 编码的文本")

    try:
        data = json.loads(text)               # 文本 -> Python 数据
    except json.JSONDecodeError as error:
        return broken_file(f"不是合法 JSON（第 {error.lineno} 行：{error.msg}）")

    if not is_task_list(data):
        return broken_file("结构不对：顶层应是任务列表，每项要有 id/title/done")

    return data


def save_tasks(tasks: list[dict]) -> bool:
    """把任务列表写回磁盘。成功 True，失败 False（不抛异常、不崩溃）。

    两条铁律：
      1. 流程永远是 先 load 全部 -> 在内存里改 -> 再 save 回去。
         绝不能在中间把 tasks 重置成空列表，否则旧数据就没了。
      2. 先写临时文件 todo.json.tmp，再整体替换正式文件（原子替换）。
         这样即使写到一半断电、磁盘满、文件被占用，
         外人看到的 todo.json 要么是完整旧版，要么是完整新版，不会是半截废文件。
    写入一律用不带 BOM 的 UTF-8，保证文件干净、跨平台可读。
    """
    tmp = DATA_FILE.with_name(DATA_FILE.name + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            # ensure_ascii=False：中文按中文写入，不写成 \u80cc\u5355\u8bcd
            # indent=2：文件格式化，方便你手动打开检查
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        tmp.replace(DATA_FILE)
        return True
    except OSError as error:
        print(f"[错误] 保存失败：{error}")
        print(f"[错误] {DATA_FILE.name} 可能只读、被别的程序占用或磁盘已满；本次修改没有写入")
        try:
            tmp.unlink(missing_ok=True)      # 清掉可能残留的半截临时文件
        except OSError:
            pass
        return False


# ============================================================
# B 块：函数、列表、字典、异常
# 下面每个"动作函数"都返回 bool：
#   True  = 干成了   False = 没干成（内容为空 / 编号不存在）
# main() 再把 bool 翻译成终端的退出码。
# ============================================================
def next_id(tasks: list[dict]) -> int:
    """生成下一个编号：当前最大 id + 1。删掉的任务编号不复用。"""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(title: str) -> bool:
    """新增一条任务。空内容属于非法输入。"""
    title = title.strip()
    if not title:
        print("[错误] 任务内容不能为空")
        return False

    tasks = load_tasks()
    tasks.append({"id": next_id(tasks), "title": title, "done": False})
    if not save_tasks(tasks):
        return False
    print(f"[完成] 已添加：{title}")
    return True


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


def mark_done(task_id: int) -> bool:
    """把指定编号的任务标记为完成。"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"[提示] 第 {task_id} 条已经是完成状态")
            else:
                task["done"] = True
                if not save_tasks(tasks):
                    return False
                print(f"[完成] 已标记完成：{task['title']}")
            return True
    print(f"[错误] 没有编号为 {task_id} 的任务")
    return False


def delete_task(task_id: int) -> bool:
    """删除指定编号的任务，其余任务必须原样保留。"""
    tasks = load_tasks()
    kept = [task for task in tasks if task["id"] != task_id]
    if len(kept) == len(tasks):          # 数量没变 = 编号不存在
        print(f"[错误] 没有编号为 {task_id} 的任务")
        return False
    if not save_tasks(kept):
        return False
    print(f"[完成] 已删除第 {task_id} 条任务")
    return True


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


def main() -> int:
    argv = sys.argv[1:]                  # sys.argv[0] 是脚本名，参数从 [1:] 开始

    if not argv:
        print(USAGE)
        return 1                         # 没给命令 = 用法错误

    command = argv[0]

    if command == "add":
        if len(argv) < 2:
            print('[错误] add 后面要跟任务内容，例如：python todo.py add "背单词"')
            return 1
        # 用 join 拼起来，这样不加引号写多个词也能用：
        #   python todo.py add 背单词 明天
        return 0 if add_task(" ".join(argv[1:])) else 1

    if command == "list":
        list_tasks()
        return 0

    if command in ("done", "del"):
        if len(argv) < 2:
            print(f"[错误] {command} 后面要跟一个编号")
            return 1
        task_id = to_int(argv[1])
        if task_id is None:
            print(f"[错误] 编号必须是数字，你输入的是：{argv[1]}")
            return 1
        if command == "done":
            return 0 if mark_done(task_id) else 1
        return 0 if delete_task(task_id) else 1

    print(f"[错误] 未知命令：{command}")
    print(USAGE)
    return 1


if __name__ == "__main__":               # 只有直接运行本文件时才执行
    sys.exit(main())                     # 把返回值变成退出码交给终端
