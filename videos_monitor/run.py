# -*- coding:utf-8 -*-
# @Time     : 2020/1/19 11:05
# @Author   : zhouliang02
# @description  :
import os
import time

from videos_producer.main import OpenCVProducer
from videos_transponder.main import ServerTransponder


def main():
    product = OpenCVProducer("/tmp", 10)
    # transponder = ServerTransponder()
    server_ip = os.environ.get("server_ip", "127.0.0.1")

    server_base_dir = os.environ.get("server_base_dir", "/tmp/")
    server_account = os.environ.get("server_account", "root")
    for photo_path in product.run():
        if not photo_path:
            continue
        dir_path = time.strftime("%Y-%m-%d/%H", time.localtime(time.time()))
        ServerTransponder(server_ip, server_account, f"{server_base_dir}{dir_path}").push_file(photo_path)


if __name__ == "__main__":
    main()
    pass

