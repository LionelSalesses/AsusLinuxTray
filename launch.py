from SystemManagerTray import SystemManagerTray
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    parentWidget = QWidget()
    tray = SystemManagerTray(app, parent=parentWidget)
    tray.show()
    app.exec_()


