from SystemManagerTray import SystemManagerTray
from PyQt5.QtWidgets import QApplication, QWidget
from Theme import qss


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    
    parentWidget = QWidget()
    parentWidget.setStyleSheet(qss)
    tray = SystemManagerTray(app, parent=parentWidget)
    
    tray.show()
    app.exec_()


