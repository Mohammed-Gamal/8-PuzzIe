# Imports
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from os import path
import random
import sys


# Import UI file
FORM_CLASS, QMainWindow = loadUiType(path.join(path.dirname(__file__), "GUI.ui"))


class SlidingPuzzle(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(SlidingPuzzle, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Track the number of clicks
        self.no_clicks = 0

        # Handle spot buttons
        self.buttons = [
            self.spot_1, self.spot_2, self.spot_3,
            self.spot_4, self.spot_5, self.spot_6,
            self.spot_7, self.spot_8, self.spot_9
        ]

        self.empty_spot = 5  # Track the empty spot position

        for i, button in enumerate(self.buttons, start=1):
            button.clicked.connect(lambda _, btn=button, num=i: self.move_spot(btn, num))

        # Handle game control buttons
        self.button_shuffle.clicked.connect(self.shuffle_puzzle)
        self.button_quit.clicked.connect(self.close)

    def move_spot(self, spot_button, spot_number):
        # Check if the clicked spot is adjacent to the empty spot
        if self.is_adjacent(spot_number, self.empty_spot):
            # Swap the spot with the empty spot
            spot_text = spot_button.text()
            empty_text = self.buttons[self.empty_spot - 1].text()
            spot_button.setText(empty_text)
            self.buttons[self.empty_spot - 1].setText(spot_text)

            self.empty_spot = spot_number  # Update the empty spot position

    @staticmethod
    def is_adjacent(spot1, spot2):
        # Check if two spots are adjacent based on their positions
        adjacent_spots = {
            1: [2, 4],
            2: [1, 3, 5],
            3: [2, 6],
            4: [1, 5, 7],
            5: [2, 4, 6, 8],
            6: [3, 5, 9],
            7: [4, 8],
            8: [5, 7, 9],
            9: [6, 8]
        }
        return spot2 in adjacent_spots[spot1]

    def shuffle_puzzle(self):
        # Shuffle the spots randomly leaving spot_5 empty
        spots = [1, 2, 3, 4, 6, 7, 8, 9]
        random.shuffle(spots)

        for i, button in enumerate(self.buttons):
            try:
                if i == 4:
                    button.setText("")
                else:
                    button.setText(str(spots[i]))
            except Exception as e:
                print(e)

        self.no_clicks = 0  # Reset the number of clicks

    def closeEvent(self, event):
        # Override closeEvent to display a confirmation dialog
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Driver code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SlidingPuzzle()
    game.show()
    sys.exit(app.exec())
