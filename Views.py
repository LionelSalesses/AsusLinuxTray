from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QCheckBox, QRadioButton, QWidgetAction, QLabel, QFrame, QSizePolicy
import PyQt5.QtCore
from QIconLabel import QIconLabel
from Controllers import GfxController, PowerProfileController, CmdExecError
from Theme import iconTheme, styleSheets



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
            "SelectorWidget.setSelectedAlternative(): Unregistered alternative '"+ alternative +"'"
        )
        
    def onClick(self, _):
        widgetID = self.selectorGroup.checkedId()
        selectedAlternative = self.selectorAlternatives[widgetID].text()
        self.onSelect(selectedAlternative)


class PowerProfileView(QWidget):
    def __init__(self, powerProfileController, notifyMethod, parent=None):
        super().__init__(parent=parent)
        assert isinstance(powerProfileController, PowerProfileController)
        self.powerProfileController = powerProfileController
        self.notifyMethod = notifyMethod
        self.initUI()
        self.setStyleSheet(styleSheets['PowerProfileView'])
    
    def initUI(self):
        # Vertical inner layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create view title
        self.viewTitle = QIconLabel(
            QIcon(iconTheme['PowerProfileSection']),
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
        self.selectorWidget.setStyleSheet(styleSheets['PowerProfileView::Selector'])
        self.layout.addWidget(self.selectorWidget)
    
    def refresh(self):
        currentProfile = self.powerProfileController.getCurrentProfile()
        self.selectorWidget.setSelectedAlternative(currentProfile)
    
    def onSelect(self, selectedAlternative):
        print("Select power profile '" + selectedAlternative + "'")
        try:
            self.powerProfileController.setProfile(selectedAlternative)
            self.notifyMethod(
                "Power profile successfully changed to '" + selectedAlternative + "'"
            )
            print("Power profile successfully changed to " + selectedAlternative + "'")
        except CmdExecError as e:
            self.notifyMethod(
                "Failed to set '" + selectedAlternative + "' as new power profile.\n"
                "Message: " + e.message
            )
        self.refresh()


class GfxModeView(QWidget):
    def __init__(self, gfxController, notifyMethod, parent=None):
        super().__init__(parent=parent)
        assert isinstance(gfxController, GfxController)
        self.gfxController = gfxController
        self.notifyMethod = notifyMethod
        self.initUI()
        self.setStyleSheet(styleSheets['GfxModeView'])
    
    def initUI(self):
        # Vertical inner layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create view title
        self.viewTitle = QIconLabel(
            QIcon(iconTheme['GfxModeSection']),
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
        self.selectorWidget.setStyleSheet(styleSheets['GfxModeView::Selector'])
        
        # Spacing
        self.layout.addSpacing(10)
        
        # dGPU status widget
        self.dGPUStatusLabel = QIconLabel(
            QIcon(iconTheme['dGPUStatus']), self.dGPUStatus(), size=20, hSpacing=5
        )
        self.dGPUStatusLabel.setStyleSheet(styleSheets['GfxModeView::QIconLabel'])
        self.layout.addWidget(self.dGPUStatusLabel)
    
    def dGPUStatus(self):
        return self.gfxController.getGPUVendor() + " GPU status: " + self.gfxController.get_dGPUStatus()
    
    def refresh(self):
        currentMode = self.gfxController.getCurrentMode()
        self.selectorWidget.setSelectedAlternative(currentMode)
        self.dGPUStatusLabel.setText(self.dGPUStatus())
    
    def onSelect(self, selectedAlternative):
        print("Select gfx mode '" + selectedAlternative + "'")
        try:
            self.gfxController.setMode(selectedAlternative)
            self.notifyMethod(
                "Graphics mode changed to '" + selectedAlternative + "', a logout is required to complete."
            )
            print("Gfx mode successfully changed to " + selectedAlternative + "'")
        except CmdExecError as e:
            self.notifyMethod(
                "Failed to set '" + selectedAlternative + "' as new graphics mode.\n"
                "Message: " + e.message
            )
        self.refresh()
    
