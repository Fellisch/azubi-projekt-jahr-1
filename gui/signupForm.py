from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from gui.menuContainer import MenuContainer
from gui.inputField import InputField
from gui.myButton import MyButton, ButtonType
from gui.core.confiq import Colors

class SignupForm(MenuContainer):
    # Signals: username, password
    signupAttempted = Signal(str, str)
    loginLinkActivated = Signal()
    guestAccessRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent, padding=40) # Same padding as LoginForm

        self.usernameInput = InputField(placeholder_text="Enter Username...")
        self.addWidget(self.usernameInput)

        self.passwordInput = InputField(placeholder_text="Password...", is_password=True)
        self.addWidget(self.passwordInput)
        
        # Optional: Add a "Confirm Password" field if desired (not in SignupScreen.jpeg)
        # self.confirmPasswordInput = InputField(placeholder_text="Confirm Password...", is_password=True)
        # self.addWidget(self.confirmPasswordInput)

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
            text='login here', # Text from SignupScreen.jpeg, might need 'or' if strictly following image text
            button_type=ButtonType.LINK,
            fontSize=16,
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.loginLinkBtn)
        
        # The "or" text from "login here or" could be a separate QLabel if exact match is needed
        # Or, the loginLinkBtn text could be "login here or"

        self.layout.addStretch(1) # Pushes guest button to bottom

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

        # Connect buttons
        self.signupBtnMain.clicked.connect(self.handle_signup_attempt)
        self.loginLinkBtn.clicked.connect(self.handle_login_link_activated)
        self.guestBtn.clicked.connect(self.handle_guest_access)

    def handle_signup_attempt(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        # Optional: Add validation for empty fields or password mismatch here
        if not username or not password:
            self.display_error("Username and password cannot be empty.")
            print("ERROR: Username and password cannot be empty.")
            return
            
        print(f"Signup attempt: User: {username}") # Password not printed for security
        self.signupAttempted.emit(username, password)

    def handle_login_link_activated(self):
        print("Login link activated on signup form.")
        self.loginLinkActivated.emit()

    def handle_guest_access(self):
        print("Guest button clicked on signup form.")
        self.guestAccessRequested.emit()

    def display_error(self, message):
        # Placeholder: Implement a way to show errors on the form
        # e.g., by adding an error QLabel to the layout
        if not hasattr(self, 'errorLabel'):
            self.errorLabel = QLabel()
            self.errorLabel.setStyleSheet("color: red; font-size: 14px;")
            # Insert error label, e.g., before the main signup button
            self.layout.insertWidget(self.layout.indexOf(self.signupBtnMain), self.errorLabel, alignment=Qt.AlignHCenter)
        self.errorLabel.setText(message)
        self.errorLabel.show()

    def clear_error(self):
        if hasattr(self, 'errorLabel') and self.errorLabel.isVisible():
            self.errorLabel.hide()
            self.errorLabel.setText("") 