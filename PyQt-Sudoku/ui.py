# File: ui.py
# Author: Tao Keyu

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sudoku

class SudokuUI(QWidget):
    def __init__(self):
        super().__init__()
        self.gridSize = 9
        self.cellSize = 35
        self.sudokuGrid = sudoku.Sudoku()

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.grid = QGridLayout()
        self.diff_str = "Difficulty: {0} ({1} cells to fill)"
        self.mode_str = "Mode: {}"
        self.isComputer = True
        self.diffLabel = QLabel(self.diff_str)
        self.modeLabel = QLabel(self.mode_str)
        self.init_ui()

    def init_ui(self):
        """
        structure of UI: QVBoxLayout() -> QHBoxLayout() stores buttons & QGridLayout() stores Sudoku &
        QLabel shows difficulty & mode
        :return:
        """

        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.diffLabel)
        self.vbox.addWidget(self.modeLabel)

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                # cell = QLabel()
                # cell.setFixedSize(self.cellSize, self.cellSize)
                # cell.setFrameShape(QFrame.Box)
                # cell.setStyleSheet("background-color:#ff0000;")
                cell = SudokuCell()
                cell.setFixedSize(self.cellSize, self.cellSize)
                # cell.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                cell.setAlignment(Qt.AlignCenter)
                reg_exp = QRegExp("[1-9]")
                validator = QRegExpValidator(reg_exp)
                cell.setValidator(validator)
                cell.setMaxLength(1)
                cell.textEdited.connect(self.edit_cell)

                self.grid.addWidget(cell, i, j, Qt.AlignCenter)

        generate_button = QPushButton("Generate")
        solve_button = QPushButton("Solve")
        check_button = QPushButton("Check")
        clear_button = QPushButton("Clear")
        reset_button = QPushButton("Reset")
        self.diffSpin = QSpinBox()
        self.diffSpin.setRange(1, 80)
        self.diffSpin.setValue(32)
        self.hbox.addWidget(generate_button)
        self.hbox.addWidget(solve_button)
        self.hbox.addWidget(check_button)
        self.hbox.addWidget(clear_button)
        self.hbox.addWidget(reset_button)
        self.hbox.addWidget(self.diffSpin)

        generate_button.clicked.connect(self.new_sudoku)
        solve_button.clicked.connect(self.solve_sudoku)
        check_button.clicked.connect(self.check_sudoku)
        clear_button.clicked.connect(self.clear_sudoku)
        reset_button.clicked.connect(self.reset_sudoku)

        self.setLayout(self.vbox)
        self.setWindowTitle("Sudoku! PyQt5")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)

        self.new_sudoku()
        self.show()
        self.setFixedSize(self.size())

    def update_ui(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                cell = self.grid.itemAtPosition(i, j).widget()
                num = self.sudokuGrid.grid[i][j]
                active = self.sudokuGrid.isActive[i][j]
                if num:
                    cell.setText(str(num))
                else:
                    cell.setText("")
                if not active:
                    cell.setStyleSheet("background-color:#c3d6e8;")
                    cell.setReadOnly(True)
                else:
                    cell.setStyleSheet("")
                    cell.setReadOnly(False)

    def new_sudoku(self):
        self.diffLabel.setText(self.diff_str.format(self.calculate_difficulty(), self.diffSpin.value()))
        self.sudokuGrid.generate_sudoku(self.diffSpin.value())  # generate a sudoku with 32 holes by default
        self.modeLabel.setText(self.mode_str.format("Computer"))
        self.isComputer = True
        self.update_ui()

    def solve_sudoku(self):
        valid = True
        if not self.isComputer:
            cnt = 0
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    if self.sudokuGrid.grid[i][j] is not None:
                        self.sudokuGrid.isActive[i][j] = False
                        cnt += 1
            valid = self.sudokuGrid.check_all(True)
            self.diffLabel.setText(self.diff_str.format(self.calculate_difficulty(cnt), 9 * 9 - cnt))
        if valid:
            status = self.sudokuGrid.solve_sudoku(override=self.isComputer)
        if not valid or not status:
            QMessageBox.critical(self, "Error!", "This Sudoku is not solvable!")
        self.update_ui()

    def clear_sudoku(self):
        self.sudokuGrid.clear_sudoku()
        self.update_ui()

    def reset_sudoku(self):
        self.sudokuGrid.reset_sudoku()
        self.modeLabel.setText(self.mode_str.format("Human"))
        self.diffLabel.setText("")
        self.isComputer = False
        self.update_ui()

    def check_sudoku(self):
        status = self.sudokuGrid.check_all()
        if status:
            msg = "You solved this Sudoku successfully!"
        else:
            msg = "You didn't solve this Sudoku. Try again!"
        QMessageBox.information(self, "Check Sudoku", msg)

    def edit_cell(self):
        sender = self.sender()
        # print(sender)
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                cell = self.grid.itemAtPosition(i, j).widget()
                if cell == sender:
                    try:
                        num = int(sender.text())
                    except ValueError:  # means None
                        num = None
                    self.sudokuGrid.grid[i][j] = num

    def calculate_difficulty(self, given=None):
        """
        Table:
        Extremely easy: given more than 50
        Easy: given 36~49
        Medium: given 32~35
        Difficult: given 28~31
        Evil: given 22~27
        by http://zhangroup.aporc.org/images/files/Paper_3485.pdf
        Unknown: given < 22
        :return: str
        """
        if given is None:
            given = 9 * 9 - self.diffSpin.value()
        if given >= 50:
            ret = "Extremely easy"
        elif given >= 36:
            ret = "Easy"
        elif given >= 32:
            ret = "Medium"
        elif given >= 28:
            ret = "Difficult"
        elif given >= 22:
            ret = "Evil"
        else:
            ret = "Unknown"
        return ret


class SudokuCell(QLineEdit):
    def __init__(self, parent=None):
        super(SudokuCell, self).__init__(parent)

    def mousePressEvent(self, e):
        if not self.isReadOnly():
            self.selectAll()
