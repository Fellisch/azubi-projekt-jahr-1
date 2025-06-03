from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QLabel
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt, Signal, QPoint

class CustomListWidget(QWidget):
    selectionChanged = Signal(str)

    def __init__(self, items=None, parent=None):
        super().__init__(parent)

        self.items = items or []
        self.is_open = False

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Label that looks like the closed dropdown
        self.display_label = QLabel("▼ " + "Select")
        self.display_label.setStyleSheet("""
            QLabel {
                background-color: #E8D8C0; /* Light beige */
                color: #000000; /* Black text */
                font-size: 16px;
                border: 2px solid #0000FF; /* Blue border */
                border-radius: 10px;
                padding: 5px;
                min-width: 150px;
                text-align: center;
            }
        """)
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.layout.addWidget(self.display_label)

        # The popup list widget (initially hidden)
        self.list_widget = QListWidget()
        self.list_widget.setWindowFlags(Qt.Popup)
        self.list_widget.setFocusPolicy(Qt.NoFocus)

        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #E8D8C0; /* Light beige */
                color: #000000; /* Black text */
                font-size: 16px;
                border: 2px solid #0000FF; /* Blue border */
                border-radius: 10px;
                padding: 5px;
                min-width: 150px;
            }
            QListWidget::item {
                padding: 5px;
                text-align: center;
            }
            QListWidget::item:selected {
                background-color: #D3C6B0; /* Slightly darker beige for selected item */
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #D3C6B0; /* Hover effect */
            }
        """)

        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.add_items(self.items)

        # Connections
        self.display_label.mousePressEvent = self.toggle_list
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

        if self.items:
            self.set_selected_index(0)

    def add_items(self, items):
        self.items = items
        self.list_widget.clear()
        for i, text in enumerate(items):
            item = QListWidgetItem(text)
            if i % 2 == 0:
                item.setForeground(QColor("white"))
                item.setBackground(QColor("#4CAF50"))  # Dark green
            else:
                item.setForeground(QColor("black"))
                item.setBackground(QColor("#8BC34A"))  # Light green
            self.list_widget.addItem(item)

    def toggle_list(self, event=None):
        if self.is_open:
            self.list_widget.hide()
            self.is_open = False
        else:
            pos = self.display_label.mapToGlobal(self.display_label.rect().bottomLeft())
            self.list_widget.move(pos)
            self.list_widget.resize(self.display_label.width(), min(150, len(self.items) * 30))  # Dynamic height
            self.list_widget.show()
            self.is_open = True

    def handle_item_clicked(self, item):
        self.display_label.setText("▼ " + item.text())
        self.list_widget.hide()
        self.is_open = False
        self.selectionChanged.emit(item.text())

    def get_selected_item_text(self):
        text = self.display_label.text()
        return text.replace("▼ ", "") if text.startswith("▼ ") else text

    def set_selected_index(self, index):
        if 0 <= index < len(self.items):
            self.list_widget.setCurrentRow(index)
            self.display_label.setText("▼ " + self.items[index])
            self.selectionChanged.emit(self.items[index])