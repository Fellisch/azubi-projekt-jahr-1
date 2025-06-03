from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from gui.menuContainer import MenuContainer
from gui.inputField import InputField
from gui.myButton import MyButton, ButtonType
from gui.core.confiq import Colors

class LoginForm(MenuContainer):
    # Define signals
    loginAttempt = Signal(str, str) # username, password
    guestAccessRequested = Signal()
    signupRequested = Signal() # Added for completeness for signup button

    def __init__(self, parent=None):
        # MenuContainer default background is Colors.SECONDARY, which matches Login.jpeg container
        super().__init__(parent, padding=40) # Adjusted padding slightly

        # Username InputField - default styling is fine
        self.usernameInput = InputField(placeholder_text="Enter Username...")
        self.addWidget(self.usernameInput)

        # Password InputField - default styling, is_password=True for obscuring text
        self.passwordInput = InputField(placeholder_text="Password...", is_password=True)
        self.addWidget(self.passwordInput)
        
        # Add some spacing after password input
        self.layout.addSpacing(20)

        # Login Button - styled to match Login.jpeg
        self.loginBtn = MyButton(
            text='Login',
            button_type=ButtonType.NORMAL,
            borderWidth=0, # No border as per design
            fontSize=24,   # Larger font size
            padding='15px 30px', # Adjusted padding
            background_color=Colors.PRIMARY, # Light yellow background
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.loginBtn)

        # Info Label: "Don't have an account?"
        self.infoLabel = QLabel("Don't have an account?")
        self.infoLabel.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; font-size: 16px; margin-top: 20px;")
        self.addWidget(self.infoLabel)

        # Sign up Button - styled as a link, matching FONT_PRIMARY
        self.signupBtn = MyButton(
            text='sign up here',
            button_type=ButtonType.LINK,
            fontSize=16,
            text_color=Colors.FONT_PRIMARY # Match other text, not default blue link
        )
        self.addWidget(self.signupBtn)
        
        # Add significant spacing before Guest button to push it down
        self.layout.addStretch(1)

        # Play as Guest Button - styled similarly to Login button
        self.guestBtn = MyButton(
            text='Play as Guest',
            button_type=ButtonType.NORMAL,
            borderWidth=0,
            fontSize=22, # Slightly smaller than Login
            padding='12px 25px',
            background_color=Colors.PRIMARY,
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.guestBtn)

        # Connect buttons to handlers
        self.loginBtn.clicked.connect(self.handle_login_attempt)
        self.guestBtn.clicked.connect(self.handle_guest_access)
        self.signupBtn.clicked.connect(self.handle_signup_request)

        self.usernameInput.returnPressed.connect(self.handle_login_attempt)
        self.passwordInput.returnPressed.connect(self.handle_login_attempt)

    def handle_login_attempt(self):
        self.clear_error() # Clear previous errors
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if not username or not password:
            self.display_error("Username and password cannot be empty.")
            return
            
        self.loginAttempt.emit(username, password)

    def handle_guest_access(self):
        self.guestAccessRequested.emit()

    def handle_signup_request(self):
        self.signupRequested.emit()

    # Add error display methods like in SignupForm
    def display_error(self, message):
        if not hasattr(self, 'errorLabel'):
            self.errorLabel = QLabel()
            self.errorLabel.setStyleSheet("color: red; font-size: 14px; margin-bottom: 10px;") # Added margin
            # Insert error label, e.g., before the Login button
            self.layout.insertWidget(self.layout.indexOf(self.loginBtn), self.errorLabel, alignment=Qt.AlignHCenter)
        self.errorLabel.setText(message)
        self.errorLabel.show()

    def clear_error(self):
        if hasattr(self, 'errorLabel') and self.errorLabel.isVisible():
            self.errorLabel.hide()
            self.errorLabel.setText("")

    def clear_fields(self):
        self.usernameInput.clear()
        self.passwordInput.clear()
        self.clear_error() # Also clear any existing error messages
