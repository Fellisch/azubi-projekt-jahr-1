from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from gui.menuContainer import MenuContainer
from gui.inputField import InputField
from gui.myButton import MyButton, ButtonType
from gui.core.confiq import Colors

class SignupForm(MenuContainer):
    signupAttempted = Signal(str, str)
    loginLinkActivated = Signal()
    guestAccessRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent, padding=40)

        self.usernameInput = InputField(placeholder_text="Enter Username...")
        self.addWidget(self.usernameInput)

        self.passwordInput = InputField(placeholder_text="Password...", is_password=True)
        self.addWidget(self.passwordInput)
        
        self.layout.addSpacing(20)

        self.signupBtnMain = MyButton(
            text='Sign up',
            button_type=ButtonType.NORMAL,
            borderWidth=0,
            fontSize=24,
            padding='15px 30px',
            background_color=Colors.PRIMARY,
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.signupBtnMain)

        self.infoLabel = QLabel("Already have an account?")
        self.infoLabel.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; font-size: 16px; margin-top: 20px;")
        self.addWidget(self.infoLabel)

        self.loginLinkBtn = MyButton(
            text='login here',
            button_type=ButtonType.LINK,
            fontSize=16,
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.loginLinkBtn)
        
        self.layout.addStretch(1)

        self.guestBtn = MyButton(
            text='Play as Guest',
            button_type=ButtonType.NORMAL,
            borderWidth=0,
            fontSize=22,
            padding='12px 25px',
            background_color=Colors.PRIMARY,
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.guestBtn)

        self.signupBtnMain.clicked.connect(self.handle_signup_attempt)
        self.loginLinkBtn.clicked.connect(self.handle_login_link_activated)
        self.guestBtn.clicked.connect(self.handle_guest_access)

    def handle_signup_attempt(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if not username or not password:
            self.display_error("Username and password cannot be empty.")
            return
            
        self.signupAttempted.emit(username, password)

    def handle_login_link_activated(self):
        self.loginLinkActivated.emit()

    def handle_guest_access(self):
        self.guestAccessRequested.emit()

    def display_error(self, message):
        if not hasattr(self, 'errorLabel'):
            self.errorLabel = QLabel()
            self.errorLabel.setStyleSheet("color: red; font-size: 14px;")
            self.layout.insertWidget(self.layout.indexOf(self.signupBtnMain), self.errorLabel, alignment=Qt.AlignHCenter)
        self.errorLabel.setText(message)
        self.errorLabel.show()

    def clear_error(self):
        if hasattr(self, 'errorLabel') and self.errorLabel.isVisible():
            self.errorLabel.hide()
            self.errorLabel.setText("") 