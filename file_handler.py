from os.path import join, getsize
from glob import glob
from time import time, sleep
from sync import Sync

class File:
    def __init__(self, filename, duration):
        self.name = filename
        self.start = time()
        self.size = getsize(filename)
        self.duration = duration * 60 * 60 # 把小时转换成秒

    def __str__(self):
        return self.name

    def can_upload(self):

        # 如果文件大小还有涨幅，则不能上传
        now_size = getsize(self.name)
        if now_size > self.size:
            self.size = now_size
            self.start = time()
            return False

        # 如果文件停止增长之后没有持续self.duration的时间，不能上传
        if time() - self.start > self.duration:
            return True
        else:
            return False

class FileHandler:
    def __init__(self, dir, prefix="", suffix=".zip", duration=1.):
        """
        :param dir:要检测的路径
        :param prefix: 要上传的文件前缀
        :param suffix: 要上传的文件后缀
        :param duration: 上传到本机的文件判断是否已上传完毕需要等待的时间
        """
        self.monitor_root = dir

        self.glob_path = join(self.monitor_root, prefix + "*" + suffix)
        self.file_set = set(glob(self.glob_path))
        self.monitor_files = []

        self.duration = duration


    def _check_change(self):
        now_file_set = set(glob(join(self.glob_path)))
        add_files = now_file_set - self.file_set
        self.file_set = now_file_set
        if len(add_files) == 0:
            return []
        else:
            print("has checked {}".format(" ".join([file for file in add_files])))
            return add_files

    def run(self, target_root, username="root", server_ip="10.60.17.248", max_num_retry=5):
        """
        :param target_root: 目标服务器路径
        :param username: 用户名默认root
        :param server_ip: 目标服务器ip
        :param max_num_retry: 最大重试次数
        """
        uploader = Sync(target_root, username, server_ip, max_num_retry)

        while True:

            upload_list = []
            for i, file in enumerate(self.monitor_files):
                if file.can_upload():
                    print("uploading {}...".format(file))
                    uploader.upload(file)
                    upload_list.append(i)
            for idx in upload_list[::-1]:
                self.monitor_files.pop(idx)

            add_files = self._check_change()
            self.monitor_files += [File(file, duration=self.duration) for file in add_files]
            sleep(1)





