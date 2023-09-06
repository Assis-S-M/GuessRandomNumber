from PySide6.QtCore import Qt, QSize, QObject, Signal
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMessageBox, QLabel, QPushButton, QLineEdit, QBoxLayout, QWidget
from components.MessageBox.MessageBox import AlertMessage

class InputWindow(QWidget):
    
    your_guess = Signal(int, name = 'guessMade')

    def __init__(self):
        super().__init__()

        self.guess_input_label = QLabel("Type a number between 1 and 10")
        self.guess_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.guess_input_line = QLineEdit()
        self.guess_input_line.setInputMask('00')
        self.guess_input_line.editingFinished.connect(lambda: self.validate_input(self.guess_input_line.text()))
        
        self.guess_input_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.guess_input_layout.addWidget(self.guess_input_label)
        self.guess_input_layout.addWidget(self.guess_input_line)

        self.setWindowTitle("Make a Guess!")
        self.setFixedSize(QSize(300, 100))
        self.setLayout(self.guess_input_layout)

    def validate_input(self, input):
        input = int(input) if input != '' else 0

        if input > 10 or input < 1:
            out_of_limit_alert = AlertMessage(alert_text = "Please type a number between 1 and 10", icon = QMessageBox.Icon.Warning)

            out_of_limit_alert.exec()
            self.guess_input_line.clear()
        else:
            self.your_guess.emit(input)
            self.guess_input_line.clear()
            self.hide()

class RoundsDisplay(QWidget):
    def __init__(self, rounds_till_end):
        super().__init__()

        self.rounds_till_end = rounds_till_end

        self.rounds_label = QLabel(f"You have {self.rounds_till_end} guessing rounds left \nPress space to guess again")
        self.rounds_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rounds_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)        
        self.rounds_layout.addWidget(self.rounds_label)

        self.setLayout(self.rounds_layout)

    def update_rounds(self, new_rounds):
        self.rounds_till_end = new_rounds
        self.rounds_label.setText(f"You have {self.rounds_till_end} guessing rounds left \nPress space to guess again")

    def get_rounds_till_end(self):
        return self.rounds_till_end

class ResultsDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)

        self.number_label = QLabel()
        self.number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_label.setStyleSheet('font-size: 40px ')
        
        self.results_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.results_layout.addWidget(self.result_label)
        self.results_layout.addWidget(self.number_label)

        self.setLayout(self.results_layout)

    def update_labels(self, guess_result, true_number):
        self.result_label.setText(f"{guess_result}")
        self.number_label.setText(f"{true_number}")

class PointsDisplay(QWidget):

    def __init__(self):
        super().__init__()

        self.points = 0
        self.right_guesses = 0
        self.wrong_guesses = 0
        self.setFixedHeight(90)
        
        self.points_label = QLabel(f"Points: {self.points}")
        self.right_guesses_label = QLabel(f"Right: {self.right_guesses}")
        self.right_guesses_label.setObjectName('right_guesses_label')

        self.wrong_guesses_label = QLabel(f"Wrong: {self.wrong_guesses}")
        self.wrong_guesses_label.setObjectName('wrong_guesses_label')

        self.guesses_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.guesses_layout.addWidget(self.right_guesses_label)
        self.guesses_layout.addWidget(self.wrong_guesses_label)

        self.guesses_widget = QWidget()
        self.guesses_widget.setLayout(self.guesses_layout)

        self.points_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.points_layout.addWidget(self.points_label, alignment = Qt.AlignmentFlag.AlignLeft)
        self.points_layout.addWidget(self.guesses_widget, alignment = Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.points_layout)

    def update_points(self, new_points):
        # self.points += new_points

        if self.points + new_points > 0:
            self.points += new_points
        else:
            self.points = 0

        if new_points > 0:
            self.right_guesses += 1
        else:
            self.wrong_guesses += 1
        
        self.points_label.setText(f"Score: {self.points}")
        self.right_guesses_label.setText(f"Right: {self.right_guesses}")
        self.wrong_guesses_label.setText(f"Wrong: {self.wrong_guesses}")


class GameFrame(QWidget):
    
    game_over = Signal(int, list)

    def __init__(self, rounds_till_end = 1, random_numbers = []):
        super().__init__()
        self.random_numbers = random_numbers
        self.current_number = 0

        self.input_window = InputWindow()
        self.input_window.your_guess.connect(self.compare_guess)

        self.rounds_display = RoundsDisplay(rounds_till_end)
        self.points_display = PointsDisplay()
        self.points_display.setObjectName('points_display')

        self.game_frame_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.game_frame_layout.addWidget(self.rounds_display)
        self.game_frame_layout.addWidget(self.points_display)
        
        self.setLayout(self.game_frame_layout)

        self.input_shortcut = QShortcut(QKeySequence('Space'), self)
        self.input_shortcut.activated.connect(lambda: self.input_window.show())

    def compare_guess(self, your_guess):

        try:
            getattr(self, 'results_display')
        except AttributeError:
            self.results_display = ResultsDisplay()
            self.game_frame_layout.insertWidget(1, self.results_display)

        if your_guess == self.random_numbers[self.current_number]:
            self.results_display.update_labels("You guessed the number correctly, the number was: ", your_guess)
            self.results_display.number_label.setObjectName('number_label_correct')
            self.points_display.update_points(3)
        else:
            self.results_display.update_labels("You sadly guessed the number incorrectly, the number was: ", self.random_numbers[self.current_number])
            self.results_display.number_label.setObjectName('number_label_wrong')
            self.points_display.update_points(-1)
        
        self.results_display.setStyleSheet(self.rounds_display.styleSheet())
        self.rounds_display.update_rounds(self.rounds_display.rounds_till_end - 1)
        self.current_number += 1
        self.check_game_over()

    def check_game_over(self):
        if self.rounds_display.get_rounds_till_end() == 0:
            self.game_over.emit(self.points_display.points, self.random_numbers)

    def set_game_frame_info(self, rounds_till_end, random_numbers):
        self.rounds_display.rounds_till_end = rounds_till_end
        self.rounds_display.rounds_label.setText(f"You have {rounds_till_end} guessing rounds left \nPress space to guess again")

        self.random_numbers = random_numbers