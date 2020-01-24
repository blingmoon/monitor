# -*- coding:utf-8 -*-
# @Time     : 2020/1/19 11:12
# @Author   : zhouliang02
# @description  :
import os
import re
import time

from videos_producer.po import OperationElement


class ProducerBase(object):
    def __init__(self, save_dir_path):
        if not save_dir_path.endswith("/"):
            save_dir_path = f"{save_dir_path}/"
        self.save_dir = save_dir_path

    def run(self):
        """

        :return: **path**  product videos path
        """
        raise Exception(f"{type(self)} is not method run")


class ClickProducer(ProducerBase):
    """
        控制按键来录制视频,视频名也要和videos_name保持一致,写在按键脚本中
    """
    mouse_type = "mouse"
    mouse_action_move = "move"
    mouse_action_click_left = "click_left"
    mouse_action_click_right = "click_right"
    keyboard_type = "keyboard"

    def __init__(self, save_dir_path, operation_path, videos_name=time.time()):
        super().__init__(save_dir_path)
        self.operation_list = self.parse_operation_file(operation_path)
        self.videos_name = videos_name

    @classmethod
    def parse_operation_file(cls, path):
        if not os.path.exists(path):
            return []
        with open(path, "rU", encoding='UTF-8') as click_file:
            path_list = click_file.read().split("\n")
        result = []
        point_re_string = r"\((\d+),(\d+)\)"
        for operation in path_list:
            operation = operation.strip()
            # '#'是注释符号
            if not operation or operation.startswith("#"):
                continue
            info_list = [item.strip().lower() for item in operation.split()]
            if info_list[0] == cls.mouse_type:
                points = re.findall(point_re_string, info_list[1])
                if not points:
                    continue
                element_info = {"point": points[0], "action": info_list[2]}
                sleep_time = float(info_list[3])
            elif info_list[0] == cls.keyboard_type:
                element_info = info_list[1]
                sleep_time = float(info_list[2])
            else:
                continue
            result.append(OperationElement(info_list[0], element_info, sleep_time))
        return result

    def run(self):

        from pymouse import PyMouse
        from pykeyboard import PyKeyboard
        mouse_client = PyMouse()
        mouse_switch = {
            self.mouse_action_move: lambda op: mouse_client.move(int(op.info.get('point')[0]),
                                                                 int(op.info.get('point')[1])),
            self.mouse_action_click_left: lambda op: mouse_client.click(int(op.info.get('point')[0]),
                                                                        int(op.info.get('point')[1]),
                                                                        1),
            self.mouse_action_click_right: lambda op: mouse_client.click(int(op.info.get('point')[0]),
                                                                         int(op.info.get('point')[1]),
                                                                         2)
        }
        keyboard_client = PyKeyboard()

        for operation in self.operation_list:
            if operation.operation_type == self.mouse_type:
                # 鼠标动作
                mouse_switch[operation.info.get("action")](operation)
            elif operation.operation_type == self.keyboard_type:
                # 键盘动作
                keyboard_client.press_keys(operation.info)
                pass
            time.sleep(operation.sleep_time)
        return f"{self.save_dir}{self.videos_name}"


class OpenCVProducer(ProducerBase):

    def __init__(self, save_dir_path, waite_time=40):
        super().__init__(save_dir_path)
        self.waite_time = waite_time  # 拍摄次数

    def run(self):
        import cv2
        import numpy as np
        wait_time = self.waite_time * 1000

        while True:
            i=0
            try:
                capture = cv2.VideoCapture(0)
                # 定义编码方式并创建VideoWriter对象
                # fourcc = cv2.VideoWriter_fourcc(*"avc1")
                # outfile = cv2.VideoWriter(file_path, fourcc, 25., (640, 480))
                print("create_capture")
                while capture.isOpened():
                    file_name = time.strftime("%Y-%m-%d&%H:%M:%S", time.localtime(time.time()))
                    file_path = f"{self.save_dir}{file_name}.jpg"
                    ret, frame = capture.read()
                    print(i)
                    i += 1
                    if ret:
                        # print(ret)
                        # outfile.write(frame)  # 写入文件
                        # cv2.imshow('frame', frame)
                        cv2.imwrite(file_path, frame)
                        yield file_path
                    else:
                        yield ""
                    time.sleep(self.waite_time)
            finally:
                # outfile.release()
                # capture.release()
                cv2.destroyAllWindows()


class ShellProducer(ProducerBase):

    def __init__(self, save_dir_path, shell_path, shell_start="sh"):
        super().__init__(save_dir_path)
        self.shell_path = shell_path
        self.shell_start = shell_start

    def run(self):
        cmd = f"{self.shell_start}  {self.shell_path}"
        import subprocess
        subprocess.check_call(cmd, shell=True)
