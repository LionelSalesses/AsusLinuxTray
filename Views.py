from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QCheckBox, QRadioButton, QWidgetAction, QLabel, QFrame, QSizePolicy
import PyQt5.QtCore
from QIconLabel import QIconLabel
from Controllers import GfxController, PowerProfileController, CmdExecError
from Theme import iconTheme, styleSheets



class SelectorWidget(QWidget):
    def __init__(self, options, initiallyCheckedOption, onSelect, parent=None):
        super().__init__(parent=parent)
        self.onSelect = onSelect
        self.initUI(options, initiallyCheckedOption)
    
    def initUI(self, options, initiallyCheckedOption):
        # Vertical inner layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create button group for mutually exclusive radio/checkbox buttons
        self.selectorGroup = QButtonGroup(self)
        
        self.options = {}
        for optionID, option in enumerate(options):
            optionText, optionWidgetClass = option
            optionWidget = optionWidgetClass(optionText)
            if optionText == initiallyCheckedOption:
                optionWidget.setChecked(True)
            self.selectorGroup.addButton(optionWidget, id=optionID)
            self.layout.addWidget(optionWidget)
            self.options[optionID] = optionWidget
        
        self.selectorGroup.buttonClicked.connect(self.onClick)
        
    def setSelectedOption(self, option):
        for optionID, optionWidget in self.options.items():
            if option == optionWidget.text():
                optionWidget.setChecked(True)
                return
        raise RuntimeError(
            "SelectorWidget.setSelectedOption(): Unregistered option '"+ option +"'"
        )
        
    def onClick(self, _):
        optionID = self.selectorGroup.checkedId()
        selectedOption = self.options[optionID].text()
        self.onSelect(selectedOption)


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
        self.selectorWidget.setSelectedOption(currentProfile)
    
    def onSelect(self, selectedOption):
        print("Select power profile '" + selectedOption + "'")
        try:
            self.powerProfileController.setProfile(selectedOption)
            self.notifyMethod(
                "Power profile successfully changed to '" + selectedOption + "'"
            )
            print("Power profile successfully changed to " + selectedOption + "'")
        except CmdExecError as e:
            self.notifyMethod(
                "Failed to set '" + selectedOption + "' as new power profile.\n"
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
        self.selectorWidget.setSelectedOption(currentMode)
        self.dGPUStatusLabel.setText(self.dGPUStatus())
    
    def onSelect(self, selectedOption):
        print("Select gfx mode '" + selectedOption + "'")
        try:
            self.gfxController.setMode(selectedOption)
            self.notifyMethod(
                "Graphics mode changed to '" + selectedOption + "', a logout is required to complete."
            )
            print("Gfx mode successfully changed to " + selectedOption + "'")
        except CmdExecError as e:
            self.notifyMethod(
                "Failed to set '" + selectedOption + "' as new graphics mode.\n"
                "Message: " + e.message
            )
        self.refresh()
    
