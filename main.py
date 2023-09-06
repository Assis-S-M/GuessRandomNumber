import os
import sys
import json

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from components.MainWindow.MainWindow import MainWindow

def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_json_data(game_data):
    json_data = json.dumps(game_data)

    with open(resource_path('save_data.json'), 'w') as json_file:
        json_file.write(json_data)

app = QApplication(sys.argv)

QFontDatabase.addApplicationFont(resource_path('styles\GoodDog.otf'))
QFontDatabase.applicationFontFamilies(0)
app.setFont(QFont('GoodDog', 10))

game_data = json.load(open(resource_path('save_data.json')))

window = MainWindow(game_data)
window.save_recent_game_data.connect(save_json_data)

with open(resource_path(f"styles\game_style.qss"), 'r', encoding = 'utf-8') as style:
    window.setStyleSheet(style.read())

window.setWindowIcon(QIcon(resource_path(f'styles\icon.ico')))
window.show()

app.exec()
app.quit()