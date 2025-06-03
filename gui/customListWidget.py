from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QLabel, QApplication
from PySide6.QtGui import QColor, QCursor, QMouseEvent
from PySide6.QtCore import Qt, Signal, QPoint, QEvent, QRect
from gui.core.confiq import Colors

class CustomListWidget(QWidget):
    selectionChanged = Signal(str)

    def __init__(self, title="Select", items=None, parent=None):
        super().__init__(parent)

        self.title = title
        self.items = items or []
        self.is_open = False
        self.current_selected_text = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.display_label = QLabel("▼ " + self.title)
        self.display_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.TERTIARY};
                color: {Colors.FONT_PRIMARY};
                font-size: 16px;
                border: 1px solid {Colors.FONT_PRIMARY};
                border-radius: 10px;
                padding: 8px 10px;
                min-width: 150px;
                text-align: center;
            }}
        """)
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.layout.addWidget(self.display_label)

        self.list_widget = QListWidget()
        self.list_widget.setWindowFlags(Qt.Popup)
        self.list_widget.setFocusPolicy(Qt.NoFocus)

        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.TERTIARY};
                color: {Colors.FONT_PRIMARY};
                font-size: 16px;
                border: 1px solid {Colors.FONT_PRIMARY};
                border-radius: 10px;
                padding: 5px;
                min-width: 150px;
            }}
            QListWidget::item {{
                padding: 12px;
                text-align: center;
            }}
            QListWidget::item:selected {{
                background-color: {Colors.CTA_HOVER}; 
                color: {Colors.FONT_PRIMARY};
            }}
            QListWidget::item:hover {{
                background-color: {Colors.CTA_HOVER};
                color: {Colors.FONT_PRIMARY};
            }}
        """)

        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.add_items(self.items)

        self.display_label.mousePressEvent = self.toggle_list
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

    def add_items(self, items):
        self.items = items
        self.list_widget.clear()
        for text in items:
            item = QListWidgetItem(text)
            item.setBackground(QColor(Colors.PRIMARY))
            item.setForeground(QColor(Colors.FONT_PRIMARY))
            self.list_widget.addItem(item)

    def toggle_list(self, event=None):
        if self.is_open:
            self._close_list_and_cleanup()
        else:
            pos = self.display_label.mapToGlobal(self.display_label.rect().bottomLeft())
            self.list_widget.move(pos)
            self.list_widget.resize(self.display_label.width(), min(150, len(self.items) * (34)))
            self.list_widget.show()
            self.is_open = True
            QApplication.instance().installEventFilter(self)

    def _close_list_and_cleanup(self):
        if self.is_open:
            self.list_widget.hide()
            self.is_open = False
            QApplication.instance().removeEventFilter(self)

    def handle_item_clicked(self, item):
        self.current_selected_text = item.text()
        self.display_label.setText("▼ " + self.current_selected_text)
        self._close_list_and_cleanup()
        self.selectionChanged.emit(item.text())

    def get_selected_item_text(self):
        if self.current_selected_text is not None:
            return self.current_selected_text
        elif self.items:
            return self.items[0]
        return None

    def set_selected_index(self, index):
        if 0 <= index < len(self.items):
            self.list_widget.setCurrentRow(index)
            self.current_selected_text = self.items[index]
            self.display_label.setText("▼ " + self.current_selected_text)
            self.selectionChanged.emit(self.items[index])

    def eventFilter(self, watched, event):
        if self.is_open and event.type() == QEvent.Type.MouseButtonPress:
            if isinstance(event, QMouseEvent):
                click_pos = event.globalPosition().toPoint()

                display_label_global_rect = QRect(self.display_label.mapToGlobal(QPoint(0,0)), self.display_label.size())
                
                list_widget_global_rect = self.list_widget.geometry()

                if display_label_global_rect.contains(click_pos) or \
                   list_widget_global_rect.contains(click_pos):
                    return False
                
                self._close_list_and_cleanup()
                return True
        
        return super().eventFilter(watched, event)