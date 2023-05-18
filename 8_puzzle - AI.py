# Imports
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from os import path
import sys


# Import UI file
FORM_CLASS, QMainWindow = loadUiType(path.join(path.dirname(__file__), "GUI.ui"))


class PuzzleSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.moves = []
        self.solution_found = False

    def is_goal_state(self, state):
        return state == [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def move_spot(self, state, move):
        empty_index = state.index(0)
        new_state = state[:]
        new_state[empty_index], new_state[move] = new_state[move], new_state[empty_index]
        return new_state

    def depth_limited_search(self, state, depth):
        if self.is_goal_state(state):
            self.solution_found = True
            return

        if depth == 0:
            return

        for move in self.get_possible_moves(state):
            new_state = self.move_spot(state, move)
            if new_state not in self.moves:
                self.moves.append(new_state)
                self.depth_limited_search(new_state, depth - 1)
                if self.solution_found:
                    return
                self.moves.pop()

    def iterative_deepening_search(self, initial_state):
        depth = 1
        while not self.solution_found:
            self.depth_limited_search(initial_state, depth)
            depth += 1

    def get_possible_moves(self, state):
        moves = []
        empty_index = state.index(0)
        if empty_index % 3 > 0:
            moves.append(empty_index - 1)  # Move left
        if empty_index % 3 < 2:
            moves.append(empty_index + 1)  # Move right
        if empty_index // 3 > 0:
            moves.append(empty_index - 3)  # Move up
        if empty_index // 3 < 2:
            moves.append(empty_index + 3)  # Move down
        return moves


class EightPuzzle(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(EightPuzzle, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.spots = [self.spot_1, self.spot_2, self.spot_3, self.spot_4, self.spot_5, self.spot_6, self.spot_7,
                      self.spot_8, self.spot_9]
        self.solution_moves = []

        self.button_shuffle.clicked.connect(self.shuffle_puzzle)
        self.button_start.clicked.connect(self.start_solver)
        self.button_quit.clicked.connect(self.close)

    def start_solver(self):
        self.disable_spots()
        self.solution_moves.clear()
        current_state = self.get_puzzle_state()
        solver = PuzzleSolver(current_state)
        solver.iterative_deepening_search(current_state)
        self.solution_moves = solver.moves
        QTimer.singleShot(0, self.move_spot_automatically)
        self.label_moves.setText("Moves: " + str(len(self.solution_moves)))

    def move_spot_automatically(self):
        if len(self.solution_moves) > 0:
            next_move = self.solution_moves.pop(0)
            self.update_puzzle_state(next_move)
            QTimer.singleShot(1500, self.move_spot_automatically)
        else:
            self.enable_spots()

    def disable_spots(self):
        for i, spot in enumerate(self.spots):
            if spot.text() == str(i + 1):
                spot.setEnabled(False)
            else:
                spot.setEnabled(True)

    def enable_spots(self):
        for spot in self.spots:
            spot.setEnabled(True)

    def get_puzzle_state(self):
        state = []
        for spot in self.spots:
            text = spot.text()
            if text.isdigit():
                state.append(int(text))
            else:
                state.append(0)
        return state

    def update_puzzle_state(self, state):
        for i, spot in enumerate(self.spots):
            spot.setText(str(state[i]))

    def shuffle_puzzle(self):
        # reset the text label
        self.label_moves.setText("Moves: 0")

        import random
        numbers = list(range(1, 9))
        random.shuffle(numbers)
        numbers.append(0)
        for i, spot in enumerate(self.spots):
            spot.setText(str(numbers[i]))
            if numbers[i] == 0:
                spot.setEnabled(False)
            else:
                spot.setEnabled(True)


# Driver code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = EightPuzzle()
    game.show()
    sys.exit(app.exec())
