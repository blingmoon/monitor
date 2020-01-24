# -*- coding:utf-8 -*-
# @Time     : 2020/1/19 14:18
# @Author   : zhouliang02
# @description  :


class OperationElement(object):

    def __init__(self, operation_type, info, sleep_time=0):
        self.operation_type = operation_type
        self.info = info
        self.sleep_time = sleep_time

    def to_json(self):
        return {"operation_type": self.operation_type, "info": self.info, "sleep_time": self.sleep_time}





