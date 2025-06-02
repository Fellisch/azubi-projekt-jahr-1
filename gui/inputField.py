from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import QSize
from gui.core.confiq import Colors

class InputField(QLineEdit):
    def __init__(
        self,
        parent=None,
        width=499,
        height=100,
        padding=28,
        background=Colors.TERTIARY,
        text_color=Colors.FONT_PRIMARY,
        placeholder_text="",
        is_password=False
    ):
        super().__init__(parent)

        self.setFixedSize(QSize(width, height))
        self.setPlaceholderText(placeholder_text)

        if is_password:
            self.setEchoMode(QLineEdit.EchoMode.Password)

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {background};
                color: {text_color};
                padding: {padding}px;
                border: none;
                border-radius: 10px;
                font-size: 32px;
            }}
            QLineEdit:placeholder {{
                color: rgba(0, 0, 0, 0.5);
            }}
        """)
