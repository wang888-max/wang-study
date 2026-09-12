# todo-cli v1

第 1 周的产出物。一个能记住数据的命令行待办工具。

## 1. 如何安装

需要 Python 3.10 以上（本机是 3.12）。本项目只用标准库，**不需要 pip 安装任何东西**。

```bash
python --version    # 确认能打印出 Python 3.12.x
```

## 2. 如何运行

在**本项目目录下**打开终端：

```bash
python todo.py add "背单词"
python todo.py list
python todo.py done 1
python todo.py del 1
```

任务数据保存在同目录的 `todo.json` 里，关掉程序再打开依然在。

## 3. 当前功能

- [x] add：新增任务
- [x] list：查看全部任务（含完成状态）
- [x] done：按编号标记完成
- [x] del：按编号删除
- [x] 数据持久化到 JSON，程序重启不丢
- [x] 非法输入（空内容、非数字编号、不存在的编号）有友好提示，不崩溃
- [x] 数据文件损坏时给出警告并按空列表处理，不崩溃

## 4. 下周计划（W2）

- 把存储从 JSON 换成 SQLite，学会建表与基础 SQL
- 新增一个调用公开 API 的命令行工具
- 学会用 `.env` 管理密钥（为 W3 调用大模型做准备）
