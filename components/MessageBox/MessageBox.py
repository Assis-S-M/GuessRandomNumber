from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QLabel

class AlertMessage(QMessageBox):
    def __init__(self, alert_text, icon):
        super().__init__()

        self.setText(f"{alert_text}")
        self.setIcon(icon)