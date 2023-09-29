import sys

from PyQt6.QtWidgets import QApplication, QWidget

from ScpTool import ScpTool


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scpTool = ScpTool()
    scpTool.show()
    sys.exit(app.exec())
