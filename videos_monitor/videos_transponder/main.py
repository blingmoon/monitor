# -*- coding:utf-8 -*-
# @Time     : 2020/1/19 11:12
# @Author   : zhouliang02
# @description  :
import os

from urllib3 import encode_multipart_formdata


class TransponderBase(object):

    def push_file(self, file_path):
        raise Exception(f"{type(self)} is not method push_file, can't push {file_path}")


class BaiDuYunTransponder(TransponderBase):
    def __init__(self, access_token):
        self.access_token = access_token
        self.upload_path = "/apps/pcstest_oauth/"

    def push_file(self, file_path):
        file_name = os.path.basename(file_path)
        data = {'file': (file_name, open(file_path, 'rb').read())}
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header = {'Content-Type': encode_data[1]}
        import requests
        url = f"https://c.pcs.baidu.com/rest/2.0/pcs/file?" \
              f"method=upload&access_token={self.access_token}&path={self.upload_path}{file_name}"
        print(requests.post(url, headers=header, data=data).text)
        # encode_multipart_formdata
        # cmd = f"curl -k -L -F \"file={file_path}\" \"https://c.pcs.baidu.com/rest/2.0/pcs/file?" \
        #     f"method=upload&access_token={self.access_token}&path={self.upload_path}{file_name}\""
        # import subprocess
        # subprocess.check_call(cmd, shell=True)


class MacBookTransponder(TransponderBase):

    def push_file(self, file_path):
        pass


class ServerTransponder(TransponderBase):
    def __init__(self, server_ip, server_account, server_upload_dir, upload_soft_path="scp"):
        self.server_ip = server_ip
        self.server_account = server_account
        if not server_upload_dir.endswith("/"):
            server_upload_dir = f"{server_upload_dir}/"
        self.server_upload_dir = server_upload_dir
        self.upload_soft_path = upload_soft_path

    def push_file(self, file_path):
        file_name = os.path.basename(file_path)
        cmd = f"{self.upload_soft_path} '{file_path}' " \
              f"{self.server_account}@{self.server_ip}:{self.server_upload_dir}"
        print(cmd)
        import subprocess
        try:
            subprocess.check_call(cmd, shell=True)
        except Exception as e:
            pass
