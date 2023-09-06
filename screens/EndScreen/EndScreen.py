from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget, QBoxLayout, QLabel

class EndScreen(QWidget):

    game_finished = Signal(bool)
    game_data_changed = Signal(dict)

    def __init__(self, final_points = 0, random_numbers = [], game_data = {}):
        super().__init__()
        self.final_points = final_points
        self.random_numbers = [str(number) for number in random_numbers]
        self.game_data = game_data
        
        self.number_list_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.number_list_widget = QWidget()

        self.input_shortcut = QShortcut(QKeySequence('Ctrl+N'), self)
        self.input_shortcut.activated.connect(lambda: self.game_finished.emit(True))

        self.end_screen_label = QLabel("Number of rounds reached zero, game over! \nPress Ctrl+N to play again \nYour final score was")        
        self.end_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.points_label = QLabel(f"{self.final_points}")
        self.points_label.setFixedHeight(50)
        self.points_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.highscore_label = QLabel()
        self.highscore_label.setFixedHeight(50)
        self.highscore_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.past_matches = QLabel()
        self.past_matches.setFixedHeight(50)
        self.past_matches.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_data_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.save_data_layout.addWidget(self.highscore_label, alignment = Qt.AlignmentFlag.AlignLeft)
        self.save_data_layout.addWidget(self.past_matches, alignment = Qt.AlignmentFlag.AlignRight)

        self.save_data_widget = QWidget()
        self.save_data_widget.setLayout(self.save_data_layout)

        self.end_screen_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.end_screen_layout.addWidget(self.end_screen_label)
        self.end_screen_layout.addWidget(self.points_label)
        self.end_screen_layout.addWidget(self.number_list_widget)
        self.end_screen_layout.addWidget(self.save_data_widget)

        self.setLayout(self.end_screen_layout)

    def set_end_screen_info(self, final_points, random_numbers, game_data):
        self.final_points = final_points
        self.random_numbers = random_numbers
        self.game_data = game_data
        
        if self.final_points > self.game_data['game_data']['highscore']:
            self.game_data['game_data']['highscore'] = self.final_points
        
        self.game_data['game_data']['past_matches'] += 1

        self.game_data_changed.emit(self.game_data)

        self.points_label.setText(f"{self.final_points}")
        self.points_label.setObjectName('points_label_positive') if final_points > 0 else self.points_label.setObjectName('points_label_negative')

        self.number_list_label = QLabel("The list of random numbers for this play was")
        self.number_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.number_list_layout.addWidget(self.number_list_label)

        numbers_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        numbers_widget = QWidget()

        number_index = 0
        for number in random_numbers:
            setattr(self, f'random_number_{number_index}_label', QLabel(f'{number}'))

            number_label = getattr(self, f'random_number_{number_index}_label')
            number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            number_label.setObjectName('final_number_label')

            numbers_layout.addWidget(number_label)

            if number_index % 9 == 0 and number_index > 0:
                numbers_widget.setLayout(numbers_layout)
                self.number_list_layout.addWidget(numbers_widget)
                
                numbers_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
                numbers_widget = QWidget()

            number_index += 1

        numbers_widget.setLayout(numbers_layout)
        self.number_list_layout.addWidget(numbers_widget)        
        self.number_list_widget.setLayout(self.number_list_layout)
        
        self.highscore_label.setText(f"Highscore: {self.game_data['game_data']['highscore']}")
        self.past_matches.setText(f"Matches: {self.game_data['game_data']['past_matches']}")

        self.setStyleSheet(self.styleSheet())