from typing import Dict, List, NoReturn, Any, Never
from itertools import permutations
import re
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import QSize, QMargins, Qt
from PySide6.QtGui import QIcon, QPixmap
from helpers import (
    Paths,
    load_settings,
    preprocess_qss_files,
    flatten_2d_list,
    settings_dict,
    apply_color_to_x_o_icons,
)

# filling the X and O icon with the corresponding color in the settings file
apply_color_to_x_o_icons()


class _Square(QPushButton):
    # the id of square, starting from 0
    counter = -1

    def __init__(self, *args, **kwargs):
        """This class creates a square of a board and gives it additional attributes to keep track
        of all squares."""
        super().__init__(*args, **kwargs)

        self.populated = False

        # calling methods
        self._create_square()

    def _increment(self) -> NoReturn:
        """This method increases one when a square is created. Better to backtrack the id of each square."""
        _Square.counter += 1

    def _create_square(self) -> Never:
        """A simple method for creating a square in a board."""

        # getting the size of the square from settings
        self.setFixedSize(
            QSize(settings_dict["square-width"], settings_dict["square-height"])
        )

        # giving the square its own style
        self.setStyleSheet(
            preprocess_qss_files(
                Paths.style("square-style.qss"),
                load_settings(Paths.setting("settings.json")),
            )
        )

        # cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._increment()

    def o(self):
        """load the o.svg icon and set it on the button."""
        self.setIcon(QPixmap(Paths.icon("o.svg")))
        self.setIconSize(QSize(45, 45))

    def x(self):
        """load the x.svg icon and set it on the button."""
        self.setIcon(QPixmap(Paths.icon("x.svg")))
        self.setIconSize(QSize(45, 45))


class Board(QWidget):
    def __init__(self, *args, **kwargs):
        """This class creates the board game for tic-tac-toe."""
        super().__init__(*args, **kwargs)

        self.squares: List[List[_Square]] = []  # contains all board cells
        self.player_o = True  # means it's player's o turn
        self.player_x = False  # means it's not player's x turn
        self.player_o_turns = []  # all the turns player o took
        self.player_x_turns = []  # all the turns player x took

        # patterns to know if player one or not ==> [(col, row), (col, row), (col, row)]
        self.winning_pattern = [
            list(permutations([[0, 0], [0, 1], [0, 2]], 3)),
            list(permutations([[1, 0], [1, 1], [1, 2]], 3)),
            list(permutations([[2, 0], [2, 1], [2, 2]], 3)),
            list(permutations([[2, 0], [2, 1], [2, 2]], 3)),
            list(permutations([[0, 0], [1, 0], [2, 0]], 3)),
            list(permutations([[0, 1], [1, 1], [2, 1]], 3)),
            list(permutations([[0, 2], [1, 2], [2, 2]], 3)),
            list(permutations([[0, 0], [1, 1], [2, 2]], 3)),
            list(permutations([[0, 2], [1, 1], [2, 0]], 3)),
        ]

        self._settings()
        self._build()
        self.play()

    def empty_board(self):
        """True if the board cells are not populated, otherwise False."""
        return all([not s.populated for s in flatten_2d_list(self.squares)])

    def _settings(self):
        """A setting method for the board"""
        # controlling the size policy
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setObjectName("board")

    def handle_player(self, e, square, i):
        if e.button() == Qt.MouseButton.LeftButton:

            if self.player_o and not square.populated and square.icon().isNull():
                self.player_o = False
                self.player_x = True
                square.populated = True
                self.parent().player_status_label.setText("Player's X Turn")
                self.parent().player_status_label.setStyleSheet(
                    "color: {};".format(settings_dict["light-red"])
                )
                square.o()
                self.player_o_turns.append([i // 3, i % 3])

                self.check()

            elif self.player_x and not square.populated and square.icon().isNull():
                self.player_o = True
                self.player_x = False
                square.populated = True
                self.parent().player_status_label.setText("Player's O Turn")
                self.parent().player_status_label.setStyleSheet(
                    "color: {};".format(settings_dict["light-green"])
                )
                square.x()
                self.player_x_turns.append([i // 3, i % 3])  # row, col
                self.check()

    def check(self):
        self.winner_o = False
        self.winner_x = False

        for pattern in self.winning_pattern:
            for i in pattern:
                if (
                    list(i)[0] in self.player_o_turns
                    and list(i)[1] in self.player_o_turns
                    and list(i)[2] in self.player_o_turns
                ):
                    self.winner_o = True
                    for s in flatten_2d_list(self.squares):
                        s.populated = True

                elif (
                    list(i)[0] in self.player_x_turns
                    and list(i)[1] in self.player_x_turns
                    and list(i)[2] in self.player_x_turns
                ):
                    self.winner_x = True
                    for s in flatten_2d_list(self.squares):
                        s.populated = True

        if self.winner_o:
            self.show_congrats_message(winner="Player O", loser="Player X")
            self.parent().player_status_label.setStyleSheet(
                "color: {};".format(settings_dict["light-green"])
            )
            self.parent().player_status_label.setText("Player's O Won. Click Replay")

        elif self.winner_x:
            self.parent().player_status_label.setText("Player's X Won. Click Replay")
            self.parent().player_status_label.setStyleSheet(
                "color: {};".format(settings_dict["light-red"])
            )
            self.show_congrats_message(winner="Player X", loser="Player O")

        elif (
            not self.winner_o
            and not self.winner_x
            and all([s.populated for s in flatten_2d_list(self.squares)])
        ):
            self.parent().player_status_label.setStyleSheet(
                "color: {};".format("white")
            )
            self.parent().player_status_label.setText("Draw! Click Replay")
            self.show_congrats_message(
                "It's a draw!", "Nobody body won the game.\nClick Replay to play again."
            )

    def play(self):
        for i, square in enumerate(flatten_2d_list(self.squares)):
            square.mousePressEvent = (
                lambda e=None, square=square, i=i: self.handle_player(e, square, i)
            )

    def show_congrats_message(
        self,
        text: str = "Congratulations, {}",
        info: str = "You won and {} lost.\nClick Replay to play again",
        winner: str = "",
        loser: str = "",
    ):
        # message box
        self.message = QMessageBox()
        self.message.setFixedSize(
            QSize(
                settings_dict["message-window-size"][0],
                settings_dict["message-window-size"][1],
            )
        )

        win_icon = QPixmap(Paths.icon("win-icon.svg"))
        win_icon = win_icon.scaled(QSize(90, 90), Qt.AspectRatioMode.KeepAspectRatio)
        self.message.setIconPixmap(win_icon)
        self.message.setWindowIcon(QIcon(QPixmap(Paths.icon("game-icon.svg"))))
        self.message.setText(text.format(winner))
        self.message.setInformativeText(info.format(loser))
        a = self.message.exec()

    def reset(self):
        """Reset the board to its default state"""

        # removing icons from cells
        for s in flatten_2d_list(self.squares):
            s.populated = False
            s.setIcon(QIcon())

        # default everything
        if self.winner_o:
            self.player_o = True
            self.player_x = False
            self.parent().player_status_label.setText("Player's O turn.")
            self.parent().player_status_label.setStyleSheet(
                "color: {};".format(settings_dict["light-green"])
            )

        elif self.winner_x:
            self.player_x = True
            self.player_o = False
            self.parent().player_status_label.setText("Player's X turn.")
            self.parent().player_status_label.setStyleSheet(
                "color: {};".format(settings_dict["light-red"])
            )

        else:
            self.player_o = True
            self.player_x = False
            self.parent().player_status_label.setText("Player's O turn.")
            self.parent().player_status_label.setStyleSheet(
                "color: {};".format(settings_dict["light-green"])
            )

        self.winner_o = False
        self.winner_x = False
        self.player_o_turns = []
        self.player_x_turns = []

    def _build(self) -> NoReturn:
        """Building the board of cells"""
        self.grid_layout = QGridLayout()
        for i in range(3):

            rows = []
            for j in range(3):

                square: _Square = _Square()
                self.grid_layout.addWidget(square, i, j)
                rows.append(square)

            self.squares.append(rows)

        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.grid_layout)


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # calling methods
        self._settings()
        self._build()

        self.replay_button.clicked.connect(self.replay)

    def _build(self):
        self.player_status_label = QLabel("Player's O turn")
        self.player_status_label.setStyleSheet(
            "color: {};".format(settings_dict["light-green"])
        )

        self.player_status_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        self.board = Board()
        self.board.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.addWidget(self.board)

        self.replay_button = QPushButton("Replay")
        self.replay_button.setObjectName("replay")
        self.exit_game_button = QPushButton("Exit Game")
        self.exit_game_button.setObjectName("exit")

        self.replay_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.exit_game_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        self.exit_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.replay_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.replay_button, alignment=Qt.AlignmentFlag.AlignTop)
        layout2.addWidget(self.exit_game_button, alignment=Qt.AlignmentFlag.AlignTop)

        layout.setSpacing(0)
        layout2.setSpacing(0)

        self.parent_layout = QGridLayout()
        self.parent_layout.addWidget(self.player_status_label, 0, 0)
        self.parent_layout.addLayout(layout, 1, 0)
        self.parent_layout.addLayout(layout2, 1, 1)

        self.parent_layout.setSpacing(0)
        self.setLayout(self.parent_layout)

    def _settings(self):
        """This method adjusts the settings of the window such as width, height, style...etc"""

        self.window_size: List[float, float] = settings_dict["window-size"]

        # applying
        self.setFixedSize(QSize(self.window_size[0], self.window_size[1]))
        self.setWindowIcon(QIcon(QPixmap(Paths.icon("game-icon.svg"))))
        self.setWindowTitle("Tic-Tac-Toe")

    def replay(self):
        try:
            if self.board.empty_board():
                QMessageBox.information(
                    self, "Empty Board", "The board is already empty!"
                )
            else:
                self.board.reset()
        except:
            QMessageBox.information(self, "Empty Board", "The board is already empty!")
