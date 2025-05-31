from PySide6.QtWidgets import QLabel
from gui.menuContainer import MenuContainer
from gui.inputField import InputField
from gui.myButton import MyButton, ButtonType
from gui.core.confiq import Colors

class LoginForm(MenuContainer):
    def __init__(self, parent=None):
        super().__init__(parent, padding=20, background=Colors.SECONDARY)

        self.usernameInput = InputField(placeholder_text="Enter Username...")
        self.addWidget(self.usernameInput)

        self.passwordInput = InputField(placeholder_text="Password...")
        self.addWidget(self.passwordInput)

        self.loginBtn = MyButton(text='Login', borderWidth=0, fontSize=30, padding='20px 54px')
        self.addWidget(self.loginBtn)

        self.infoLabel = QLabel("Don't have an account?")
        self.infoLabel.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; font-size: 18px;")
        self.addWidget(self.infoLabel)

        self.signupBtn = MyButton(text='sign up here', borderWidth=0, fontSize=16, button_type=ButtonType.LINK)
        self.addWidget(self.signupBtn)

        self.guestBtn = MyButton(text='Play as Guest', borderWidth=0, fontSize=30, padding='20px 54px')
        self.addWidget(self.guestBtn)
