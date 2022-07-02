# Path to theme icons
iconTheme = {
    'PowerProfileSection': 'icons/cpu.png',
    'GfxModeSection':      'icons/vga.png',
    'Tray':                'icons/cpu_1_w.png',
    'dGPUStatus':          'icons/gpu.png',
    'Warning':             'icons/warning.png',
}

# Stylesheet
qss = """
    /* ----- Message box style ----- */
    /* QMessageBox > QLabel {
        color: black;
    }*/
    
    /* ----- Menu style ----- */
    QMenu{
        background-color: rgba(43, 43, 43, 90%);
        border-bottom-left-radius:5px;
        border-bottom-right-radius:5px;
        color: rgb(255, 255, 255);
        padding-left:15px;
        padding-right:5px;
    }
    QMenu::item {
        background-color: transparent;
        padding:3px 20px;
        margin:10px 20px;
    }
    QMenu::separator{
        height:4px;
        background:gray;
        margin-left:5px;
        margin-right:5px;
        margin-top:10px;
        margin-bottom:4px;
    }
    QMenu::item:selected {
        background-color: gray; 
    }
    
    /* ------ QIconLabel style ----- */
    QIconLabel #textLabel {
        color: rgb(255, 255, 255);
    }
    
    QIconLabel#dGPUStatusWidget {
        margin-left:8px;
    }
    
    QIconLabel#pendingGfxModeAlertWidget #textLabel {
        border: 3px solid rgba(254, 146, 106, 55%);
        padding-left:5px;
        padding-right:7px;
        padding-top:5px;
        padding-bottom:5px;
    }
    
    /* ------ Selector widget style ----- */
    QCheckBox {
        color: rgb(255, 255, 255);
        spacing: 20px;
    }
    QCheckBox::hover {
        background-color: rgba(80, 80, 80, 50%);
    }
    QCheckBox::indicator {
        border: 3px solid #5A5A5A;
        background: none;
    }
    QCheckBox::checked {
        font: bold;
        color: rgba(254, 146, 106, 100%);
    }
    QCheckBox::indicator:checked {
        background: rgba(254, 146, 106, 75%);
        border: 2px solid lightgray;
    }
    QCheckBox::indicator:unchecked:pressed {
        background: rgba(254, 146, 106, 20%);
    }
"""

