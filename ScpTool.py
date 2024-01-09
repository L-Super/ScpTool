from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox

from ScpToolCli import ScpToolCli
from ScpToolGui import Ui_ScpToolGui


# .ui文件转为py:
# pyuic6 -o ScpToolGui.py ScpToolGui.ui
# 调用：
# ui = Ui_ScpToolGui()
# ui.setupUi(self)
class ScpTool(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_ScpToolGui()
        self.ui.setupUi(self)

        self.ui.startButton.clicked.connect(self.start_button_clicked)
        self.ui.localFileButton.clicked.connect(self.choose_file)
        self.ui.localSaveButton.clicked.connect(self.choose_dir)

        # 信号connect会显示无属性，暂不知如何使用
        # self.progress_signal = QtCore.pyqtSignal(str)

    def check_is_empty(self, widget):
        """
        检查LinetEdit是否为空
        :param widget:
        :return: empty return true, otherwise return false
        """
        text = widget.text()
        if text == '':
            which_str = None
            if widget.objectName() == "userLineEdit":
                which_str = "user is empty"
            elif widget.objectName() == "ipLineEdit":
                which_str = "ip is empty"

            if self.ui.tabWidget.currentIndex() == 0:
                if widget.objectName() == "localFileLineEdit":
                    which_str = "local file path is empty"
                if widget.objectName() == "remoteSaveLineEdit":
                    which_str = "remote file path is empty"
            elif self.ui.tabWidget.currentIndex() == 1:
                if widget.objectName() == "remoteFileLineEdit":
                    which_str = "remote file path is empty"
                if widget.objectName() == "localSaveLineEdit":
                    which_str = "local file path is empty"

            QMessageBox.warning(self, '警告', which_str)

            return True
        return False

    def choose_file(self):
        # TODO: 支持多文件上传
        # files = QFileDialog.getOpenFileNames(self)
        # print('choose file:', files)
        #
        # if len(files[0]) != 0:
        #     file_list = ''
        #     for file in files[0]:
        #         file_list += file
        #     self.ui.localFileLineEdit.setText(file_list)
        #
        # return files[0]
        file = QFileDialog.getOpenFileName(self)
        print('choose file:', file)

        if len(file[0]) != 0:
            self.ui.localFileLineEdit.setText(file[0])

        return file[0]

    def choose_dir(self):
        save_dir = QFileDialog.getExistingDirectory(self)

        if save_dir != '':
            self.ui.localSaveLineEdit.setText(save_dir)
        print('choose dir is:', save_dir)
        return save_dir

    def start_button_clicked(self):
        if self.check_is_empty(self.ui.userLineEdit) or self.check_is_empty(self.ui.ipLineEdit):
            return
        ip = self.ui.ipLineEdit.text()
        user = self.ui.userLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if self.ui.tabWidget.currentIndex() == 0:
            if self.check_is_empty(self.ui.localFileLineEdit) or self.check_is_empty(self.ui.remoteSaveLineEdit):
                return
            upload_files = self.ui.localFileLineEdit.text()
            remote_path = self.ui.remoteSaveLineEdit.text()
            self.transfer_files(ip, user, password, upload_files, remote_path, True)
        elif self.ui.tabWidget.currentIndex() == 1:
            if self.check_is_empty(self.ui.remoteFileLineEdit) or self.check_is_empty(self.ui.localSaveLineEdit):
                return
            download_files = self.ui.remoteFileLineEdit.text()
            local_path = self.ui.localSaveLineEdit.text()
            self.transfer_files(ip, user, password, download_files, local_path, False)

    def transfer_files(self, ip, user, password, file, path, is_send: bool):
        """
        传输文件
        :param ip:
        :param user:
        :param password:
        :param file:
        :param path:
        :param is_send:是否为发送文件到远程，否则接收远程文件
        :return:
        """

        cli = ScpToolCli(self)

        status = cli.connect_host(ip, user, password)
        if not status[0]:
            err = status[1]
            QMessageBox.critical(self, '连接失败', err)
            self.ui.textBrowser.append("<font color='red'>" + f'连接远程主机失败，错误信息：{err}' + '<font>')
            return
        else:
            self.ui.textBrowser.append('成功连接远程主机')
        if is_send:
            flag = cli.upload_file(file, path)
            if flag[0]:
                self.ui.textBrowser.append('文件上传成功')
            else:
                self.ui.textBrowser.append(f'文件上传失败，错误信息：{flag[1]}')
        else:
            flag = cli.download_file(path, file)
            if flag[0]:
                self.ui.textBrowser.append('文件下载成功')
            else:
                self.ui.textBrowser.append(f'文件下载失败，错误信息：{flag[1]}')
        cli.close()

    def progress_callback(self, filename, percent_sent):

        file_progress = f'{filename} progress: {percent_sent}%'

        # self.progress_signal.emit(file_progress)

        print('transmission', file_progress)
        self.ui.textBrowser.append(file_progress)
