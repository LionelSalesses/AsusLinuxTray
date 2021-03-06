from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLayout, QVBoxLayout, QButtonGroup, QCheckBox, QLabel
from QIconLabel import QIconLabel
from Controllers import GfxController, PowerProfileController, CmdExecError
from Theme import getIconPath



class SelectorWidget(QWidget):
    def __init__(self, alternatives, initiallyCheckedAlternative, onSelect, parent=None):
        super().__init__(parent=parent)
        self.onSelect = onSelect
        self.initUI(alternatives, initiallyCheckedAlternative)
    
    def initUI(self, alternatives, initiallyCheckedAlternative):
        # Vertical inner layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create button group for mutually exclusive radio/checkbox buttons
        self.selectorGroup = QButtonGroup(self)
        
        self.selectorAlternatives = {}
        for widgetID, alternativeInfo in enumerate(alternatives):
            altText, altWidgetClass = alternativeInfo
            altWidget = altWidgetClass(altText)
            if altText == initiallyCheckedAlternative:
                altWidget.setChecked(True)
            self.selectorGroup.addButton(altWidget, id=widgetID)
            self.layout.addWidget(altWidget)
            self.selectorAlternatives[widgetID] = altWidget
        
        self.selectorGroup.buttonClicked.connect(self.onClick)
    
    def setSelectedAlternative(self, alternative):
        for widgetID, altWidget in self.selectorAlternatives.items():
            if alternative == altWidget.text():
                altWidget.setChecked(True)
                return
        raise RuntimeError(
            "Internal error in SelectorWidget.setSelectedAlternative(): "
            "Unregistered alternative '"+ alternative +"'"
        )
    
    def onClick(self, _):
        widgetID = self.selectorGroup.checkedId()
        selectedAlternative = self.selectorAlternatives[widgetID].text()
        self.onSelect(selectedAlternative)


class PowerProfileView(QWidget):
    def __init__(self, powerProfileController, onNotifyError, parent=None):
        super().__init__(parent=parent)
        assert isinstance(powerProfileController, PowerProfileController)
        self.powerProfileController = powerProfileController
        self.onNotifyError = onNotifyError
        self.initUI()
    
    def initUI(self):
        # Vertical inner layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        
        # Create view title
        self.viewTitle = QIconLabel(
            QIcon(getIconPath('PowerProfileSection')),
            "Power profile",
            parent=self
        )
        self.layout.addWidget(self.viewTitle)
        
        # Create selector widget
        self.selectorWidget = SelectorWidget(
            [
                (profile, QCheckBox) for profile in self.powerProfileController.availableProfiles
            ],
            self.powerProfileController.getCurrentProfile(),
            self.onSelect,
            parent=self
        )
        self.layout.addWidget(self.selectorWidget)
    
    def refresh(self):
        currentProfile = self.powerProfileController.getCurrentProfile()
        self.selectorWidget.setSelectedAlternative(currentProfile)
    
    def onSelect(self, selectedAlternative):
        print("Select power profile '" + selectedAlternative + "'")
        try:
            self.powerProfileController.setProfile(selectedAlternative)
            print("Power profile successfully changed to " + selectedAlternative + "'")
        except CmdExecError as e:
            self.onNotifyError(
                'ERROR',
                "Failed to set <b>" + selectedAlternative + "</b> as new power profile.<br>"
                +e.getMessage()
            )
        self.refresh()


class GfxModeView(QWidget):
    def __init__(self, gfxController, onGeometryChange, onNotifyError, parent=None):
        super().__init__(parent=parent)
        assert isinstance(gfxController, GfxController)
        self.gfxController = gfxController
        self.onGeometryChange = onGeometryChange
        self.onNotifyError = onNotifyError
        self.initUI()
    
    def initUI(self):
        # Vertical inner layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        
        # Create view title
        self.viewTitle = QIconLabel(
            QIcon(getIconPath('GfxModeSection')),
            "Graphics mode",
            parent=self
        )
        self.layout.addWidget(self.viewTitle)
        
        # Create selector widget
        self.selectorWidget = SelectorWidget(
            [
                (mode, QCheckBox) for mode in self.gfxController.supportedModes
            ],
            self.gfxController.getCurrentMode(),
            self.onSelect,
            parent=self
        )
        self.layout.addWidget(self.selectorWidget)
        
        # Spacing
        self.layout.addSpacing(10)
        
        # Pending gfx mode alert widget 
        self.pendingGfxModeAlertWidget = QIconLabel(
            QIcon(getIconPath('Warning')), 
            '', size=40, hSpacing=5, parent=self
        )
        self.pendingGfxModeAlertWidget.setObjectName("pendingGfxModeAlertWidget")
        self.layout.addWidget(self.pendingGfxModeAlertWidget)
        self.pendingGfxModeAlertWidget.hide()

        # Spacing
        self.layout.addSpacing(10)
        
        # dGPU status widget
        self.dGPUStatusWidget = QIconLabel(
            QIcon(getIconPath('dGPUStatus')), self.dGPUStatus(), size=20, hSpacing=5, parent=self
        )
        self.dGPUStatusWidget.setObjectName("dGPUStatusWidget")
        self.layout.addWidget(self.dGPUStatusWidget)
    
    def dGPUStatus(self):
        return self.gfxController.getGPUVendor() + " GPU status: " + self.gfxController.get_dGPUStatus()
    
    def refresh(self):
        self.refreshSelectorWidget()
        # Refresh pending mode widget
        self.refreshPendingGfxModeAlertWidget()
        # Refresh dGPU status
        self.dGPUStatusWidget.setText(self.dGPUStatus())
    
    def refreshSelectorWidget(self):
        currentMode = self.gfxController.getCurrentMode()
        self.selectorWidget.setSelectedAlternative(currentMode)
    
    def refreshPendingGfxModeAlertWidget(self):
        pendingMode = self.gfxController.getPendingModeChange()
        if pendingMode == 'none':
            # Disable pending mode alert
            self.pendingGfxModeAlertWidget.hide()
        else:
            # Update and show pending mode alert
            self.pendingGfxModeAlertWidget.setText(
                "Pending mode: <b>" + pendingMode + "</b><br>Logout required to complete"
            )
            self.pendingGfxModeAlertWidget.show()
    
    def onSelect(self, selectedAlternative):
        print("Select gfx mode '" + selectedAlternative + "'")
        try:
            self.gfxController.setMode(selectedAlternative)
            print("Gfx mode successfully changed to '" + selectedAlternative + "'")
            # Update displayed information
            self.refresh()
            # Notify parent of geometry change
            self.onGeometryChange()
        except CmdExecError as e:
            self.onNotifyError(
                'ERROR',
                "Failed to set <b>" + selectedAlternative + "</b> as new graphics mode.<br>"
                +e.getMessage()
            )
            self.refresh()

