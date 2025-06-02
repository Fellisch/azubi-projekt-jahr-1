from PySide6.QtCore import QObject, Signal

class SignalBus(QObject):
    cellClicked = Signal(object)

bus = SignalBus()