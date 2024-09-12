import os, sys
from PyQt5.QtWidgets import (
    QApplication
)
from gui.interface import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(os.getcwd())
    window.show()
    sys.exit(app.exec_())