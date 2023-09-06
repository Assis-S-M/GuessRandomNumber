import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QSize, Signal
from screens.StartScreen.StartScreen import StartScreen
from screens.GameFrame.GameFrame import GameFrame
from screens.EndScreen.EndScreen import EndScreen

def resource_path(relative_path):
        
    base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):

    save_recent_game_data = Signal(dict)

    def __init__(self, game_data):
        super().__init__()
        self.game_data = game_data
        self.setWindowTitle('Guess the Number')
        self.setup_start_screen()
        
    def setup_start_screen(self):
        self.start_screen = StartScreen()
        self.start_screen.start_game.connect(self.setup_game_frame)

        self.setCentralWidget(self.start_screen)
        self.setFixedSize(QSize(400, 300))

    def setup_game_frame(self, rounds_count, random_numbers):
        self.game_frame = GameFrame()
        self.game_frame.game_over.connect(self.setup_end_screen)
        self.game_frame.set_game_frame_info(rounds_count, random_numbers)
        self.setCentralWidget(self.game_frame)

    def setup_end_screen(self, final_points, random_numbers):
        self.end_screen = EndScreen()
        self.end_screen.game_data_changed.connect(lambda game_data: self.save_recent_game_data.emit(game_data))
        self.end_screen.game_finished.connect(self.setup_start_screen)
        self.end_screen.set_end_screen_info(final_points, random_numbers, self.game_data)

        self.setFixedHeight(self.end_screen.end_screen_layout.sizeHint().height() * 2)
        self.setCentralWidget(self.end_screen)