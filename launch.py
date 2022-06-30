from SystemManagerTray import SystemManagerTray
from PyQt5.QtWidgets import QApplication, QWidget
from Theme import styleSheets


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(styleSheets['App'])
    parentWidget = QWidget()
    tray = SystemManagerTray(app, parent=parentWidget)
    tray.show()
    app.exec_()


