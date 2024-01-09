#!python
import os

import paramiko
import scp


class ScpToolCli:
    def __init__(self, gui):
        # 初始化ssh
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client = None
        self.gui = gui

    def __del__(self):
        if self.ssh:
            self.ssh.close()
        if self.client:
            self.client.close()
        print('scp tool cli quit')

    def transmission_progress(self, filename, filesize, file_sent):
        """
        进度回调
        :param filename: 文件名
        :param filesize: 文件大小
        :param file_sent: 已发送的大小
        :return:
        """
        # print("%s's progress: %.2f%%   \r" % (filename, float(file_sent) / float(filesize) * 100))
        # 保留两位小数
        percent_sent = round((file_sent / filesize) * 100, 2)

        print(f'{filename} progress: {percent_sent}%')
        # call ScpTool progress_callback
        self.gui.progress_callback(filename, percent_sent)
        return percent_sent

    def transmission_progress4(self, filename, filesize, file_sent, peer_name):
        """
        进度回调
        :param filename: 文件名
        :param filesize: 文件大小
        :param file_sent: 已发送的大小
        :param peer_name: 对方IP和port
        :return:
        """

        # (192.168.68.154:22) b'mainwindow.h''s progress: 100.00%
        print("(%s:%s) %s's progress: %.2f%%   \r" % (
            peer_name[0], peer_name[1], filename, float(file_sent) / float(filesize) * 100))

    def connect_host(self, host_ip, username, password):
        """
        连接远程主机
        :param host_ip: 主机IP
        :param username: 用户名
        :param password: 密码
        :return:
        """
        try:
            self.ssh.connect(hostname=host_ip, username=username, password=password, compress=True)
            # scp建立连接
            self.client = scp.SCPClient(self.ssh.get_transport(), progress=self.transmission_progress)
        except ConnectionError as err:
            print(f'{err}')
            return False, err
        return True, 'connect success'

    def close(self):
        self.client.close()
        self.ssh.close()

    def upload_file(self, local_file, remote_path):
        """
        上传文件或文件夹
        :param local_file:
        :param remote_path:
        :return:
        """
        is_file = True
        if os.path.isdir(local_file):
            is_file = False

        try:
            self.client.put(local_file, remote_path, recursive=is_file)
        except FileNotFoundError as err:
            print(f'{err}')
            return False, err
        else:
            print("files upload success")
            return True, 'success'

    def download_file(self, local_path, remote_file):
        """
        下载文件或者文件夹
        :param local_path:
        :param remote_file:
        :return:
        """
        try:
            self.client.get(remote_file, local_path, recursive=True)
        except scp.SCPException as err:
            print(f'{err}')
            return False, err
        return True, 'success'


if __name__ == '__main__':
    print("PYTHONPATH:", os.environ.get('PYTHONPATH'))

    # print("PATH:", os.environ.get('PATH'))
    scpTool = ScpToolCli()
    scpTool.connect_host('10.0.2.15', 'leo', '123')
    scpTool.upload_file('C:/Users/LMR/Downloads/cef_binary_113.3.1+g525fa10+chromium-113.0.5672.128_linux64.tar.bz2',
                        '/home/leo/Desktop/')
    # scpTool.upload_file('/home/leo/Desktop/build-ScpTool-Desktop_Qt_5_15_2_GCC_64bit-Debug','/home/leo/')
    # scpTool.download_file('./','/home/leo/get-docker.sh')
    # scpTool.download_file('./', '/home/leo/bb')

    pass
