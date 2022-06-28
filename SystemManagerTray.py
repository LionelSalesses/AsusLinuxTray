import sys
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QWidgetAction, QMenu, QMessageBox, QAction, QSystemTrayIcon
import PyQt5.QtCore
from Controllers import GfxController, PowerProfileController, CmdExecError
from Theme import iconTheme, styleSheets
from Views import PowerProfileView, GfxModeView


class SystemManagerTray(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        super().__init__(parent=parent)
        # Check system tray and tray notification are supported
        self.checkSupport()
        
        self.app = app
        
        # Init controllers
        self.initControllers()
        
        # Show tray menu when clicking on tray icon
        self.activated.connect(self.showMenuOnTrigger)
        
        # Set tray icon
        self.icon = QIcon(iconTheme['Tray'])
        self.setIcon(self.icon)
        self.setVisible(True)
        
        # Create menu and add to the tray
        self.menu = self.createMenu(parent=parent)
        self.setMenuStyle(self.menu)
        self.setContextMenu(self.menu)
        
        self.refresh()
    
    def showMenuOnTrigger(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QCursor.pos())
            
    def checkSupport(self):
        if not self.isSystemTrayAvailable() or not self.supportsMessages():
            QMessageBox.critical(
                None,
                "System Manager Tray",
                "System tray is not supported on your system"
            )
            sys.exit(1)
    
    def sendNotification(self, msg):
        self.showMessage("System Manager Tray", msg, QSystemTrayIcon.NoIcon, msecs=4*1000)
        
    def initControllers(self):
        try:
            self.gfxController = GfxController()
            self.powerProfileController = PowerProfileController()
        except CmdExecError as e:
            QMessageBox.critical(
                None,
                "System Manager Tray",
                "Failed to initialize controllers...\n"
                "Message: "+e.message
            )
        print("Controllers initialized")
        
    def refresh(self):
        self.powerProfileView.refresh()
        self.gfxModeView.refresh()
    
    def createMenuAction(self, menu, actionText, method):
        action = QAction(actionText, menu)
        action.triggered.connect(method)
        menu.addAction(action)
        return action
        
    def widgetToAction(self, parent, widget):
        # Create widget action to insert into the menu
        wAction = QWidgetAction(parent)
        wAction.setDefaultWidget(widget)
        return wAction
    
    def createViews(self, menu):
        # Power profile view
        self.powerProfileView = PowerProfileView(
            self.powerProfileController,
            self.sendNotification,
            parent=menu
        )
        menu.addAction(self.widgetToAction(menu, self.powerProfileView))
        
        # Separator
        self.createMenuSeparator(menu)
        
        # Graphics mode
        self.gfxModeView = GfxModeView(
            self.gfxController,
            self.sendNotification,
            parent=menu
        )

        menu.addAction(self.widgetToAction(menu, self.gfxModeView))
    
    def createMenuSeparator(self, menu):
        menu.addSeparator()
        
    def setMenuStyle(self, menu):
        menu.setWindowFlags(menu.windowFlags() | PyQt5.QtCore.Qt.FramelessWindowHint)
        menu.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)
        menu.setStyleSheet(styleSheets['Menu'])

    def createMenu(self, parent=None):
        # Creating the options
        menu = QMenu(parent)
        self.createViews(menu)
        
        # Separator
        self.createMenuSeparator(menu)
        
        # Quit action
        self.createMenuAction(menu, "&Quit", self.app.quit)
        
        menu.aboutToShow.connect(self.refresh)
        return menu
    



