# -*- coding:utf-8 -*-
# @Time     : 2020/1/19 11:13
# @Author   : zhouliang02
# @description  :
from pymouse import PyMouse

from videos_producer.main import ClickProducer, OpenCVProducer
from videos_transponder.main import BaiDuYunTransponder


def test_parse_operation_file():
    a = ClickProducer.parse_operation_file("../data/click_path.txt")
    for item in a:
        print(item.to_json())


def test_main():

    m = PyMouse()
    print(m.position())
    test_click = ClickProducer(".", "../data/click_path.txt")
    test_click.run()


def test_opencv():
    profucer = OpenCVProducer("/Users/zhouliang/local_documents/tmp", 60)
    profucer.run()


def test_tranport():
    t = BaiDuYunTransponder("23.2bb6eaa567b75beb28fd8368c19c3794.2592000.1582039002.3513857307-238347")
    t.push_file("/Users/zhouliang/local_documents/tmp/test.py")


if __name__ == "__main__":
    # test_parse_operation_file()
    # test_main()
    test_opencv()
    # test_tranport()
