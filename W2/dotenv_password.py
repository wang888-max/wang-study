# import os
#
#
# from dotenv import load_dotenv
#
# load_dotenv()
#
# user_name = os.getenv("MY_USERNAME")
# password = os.getenv("PASSWORD")
#
# print(user_name)
# print(password)


import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).with_name(".env")


def main() -> None:
    if not load_dotenv(ENV_FILE):
        raise SystemExit(f"没能加载配置文件：{ENV_FILE}")

    try:
        # 不叫 USERNAME：那是 Windows 的系统变量，会静默抢占 .env 的值
        user_name = os.environ["MY_USERNAME"]
        password = os.environ["PASSWORD"]
    except KeyError as missing:
        raise SystemExit(f"缺少环境变量：{missing.args[0]}") from None

    print(f"用户名：{user_name}")
    print(f"密码长度：{len(password)}")   # 密钥不落地到日志


if __name__ == "__main__":
    main()