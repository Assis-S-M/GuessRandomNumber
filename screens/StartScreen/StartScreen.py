import json
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QWidget, QBoxLayout, QLabel, QLineEdit, QMessageBox
from components.MessageBox.MessageBox import AlertMessage
from random import randrange

class LabeledInput(QWidget):

    input_finished = Signal(int)

    def __init__(self, label_text):
        super().__init__()
        self.input_value = 1

        self.labeled_input_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)

        self.input_label = QLabel(f'{label_text}')
        self.input_label.setFixedSize(QSize(360, 50))
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText('Click button with empty input to play one round')
        self.input_line.setInputMask('00')
        self.input_line.editingFinished.connect(lambda: self.validate_input(self.input_line.text()))

        self.labeled_input_layout.addWidget(self.input_label)
        self.labeled_input_layout.addWidget(self.input_line)

        self.setLayout(self.labeled_input_layout)

    def validate_input(self, input):
        input = int(input) if input != '' else 1

        if input > 50 or input < 1:
            out_of_limit_alert = AlertMessage(alert_text = "Please type a number between 1 and 50", icon = QMessageBox.Icon.Warning)

            out_of_limit_alert.exec()
            self.input_line.clear()
        else:
            self.input_value = input
            self.input_finished.emit(input)

    def get_rounds_count(self):
        return self.input_value
    
class StartScreen(QWidget):

    start_game = Signal(int, list)

    def __init__(self):
        super().__init__()

        self.game_title = QLabel("Guess the Number Game!")
        self.game_title.setObjectName('game_title')
        self.game_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rounds_input = LabeledInput(label_text = "Type how many guessing rounds you want")
        self.rounds_input.input_finished.connect(self.decide_random_numbers)

        self.rounds_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.rounds_layout.addWidget(self.game_title)
        self.rounds_layout.addWidget(self.rounds_input)

        self.setLayout(self.rounds_layout)
 
    def decide_random_numbers(self, rounds_count):
        random_numbers = []
        deciding_numbers = True

        while deciding_numbers:
            if rounds_count == 0:
                deciding_numbers = False
                continue

            random_numbers.append(randrange(1, 11, 1))
            rounds_count -= 1
        
        self.start_game.emit(self.rounds_input.get_rounds_count(), random_numbers)