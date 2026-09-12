from pathlib import Path
import json

DATA = Path(__file__).parent / "todo.json"

def load():
    if not DATA.exists():          # 第一次运行，文件还不存在
        return []
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:   # 文件被写坏了，不要崩
        print("数据文件损坏，先按空列表处理")
        return []

def save(tasks):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)