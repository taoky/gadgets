#!/usr/bin/env python3
# File: sudoku.py
# Author: Tao Keyu

# Contains a class which has a 9x9 grid, including all things necessary about a sudoku "backend"
# This class is made to not mix up with the Qt UI.

import random
import sys


def eprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


class Sudoku:
    # defines a sudoku grid
    def __init__(self):
        self.grid = [[None for _ in range(9)] for _ in range(9)]  # generate an empty grid
        self.isActive = [[True for _ in range(9)] for _ in range(9)]  # can be filled in by user
        self.allowNums = set(range(1, 10))  # {1, 2, ..., 9}
        self.available = [[set(self.allowNums) for _ in range(9)] for _ in range(9)]
        self.allCoords = [(x, y) for i in range(9) for y, x in enumerate([i] * 9)]

    def check_row(self, row, ignore_none=False):
        if row not in range(9):
            raise ValueError
        nums = list(self.allowNums)
        i = self.grid[row]
        for j in i:
            val = j
            if ignore_none and val is None:
                continue
            if val is None or val not in nums:
                return False
            nums.remove(val)
        return True

    def check_col(self, col, ignore_none=False):
        if col not in range(9):
            raise ValueError
        nums = list(self.allowNums)
        for i in self.grid:
            val = i[col]
            if ignore_none and val is None:
                continue
            if val is None or val not in nums:
                return False
            nums.remove(val)
        return True

    def check_sub_grid(self, sub_grid, ignore_none=False):
        if sub_grid not in range(9):
            raise ValueError
        nums = list(self.allowNums)
        if sub_grid in (0, 1, 2):
            rows = (0, 1, 2)
            cols = tuple(map(lambda x: x + 3 * sub_grid, (0, 1, 2)))
        elif sub_grid in (3, 4, 5):
            rows = (3, 4, 5)
            cols = tuple(map(lambda x: x + 3 * (sub_grid - 3), (0, 1, 2)))
        else:
            rows = (6, 7, 8)
            cols = tuple(map(lambda x: x + 3 * (sub_grid - 6), (0, 1, 2)))
        for i in rows:
            for j in cols:
                val = self.grid[i][j]
                if ignore_none and val is None:
                    continue
                if val is None or val not in nums:
                    return False
                nums.remove(val)
        return True

    def check_all(self, ignore_none=False):
        """
        This function is used to check whether user's input is right.
        :return: bool
        """
        for i in range(9):
            if not self.check_row(i, ignore_none) or not self.check_col(i, ignore_none) \
                    or not self.check_sub_grid(i, ignore_none):
                return False
        return True

    def get_available(self, i, j):
        available = set(self.allowNums)
        for p in range(9):
            if p != i:  # p is row
                if self.grid[p][j] in available:
                    available.remove(self.grid[p][j])
            if p != j:  # p is column
                if self.grid[i][p] in available:
                    available.remove(self.grid[i][p])
            x, y = i // 3 * 3 + p // 3, j // 3 * 3 + p % 3
            if (x, y) != (i, j):
                if self.grid[x][y] in available:
                    available.remove(self.grid[x][y])
        return available

    def update_available(self, i, j):
        for p in range(9):
            self.available[p][j] = self.get_available(p, j)
            self.available[i][p] = self.get_available(i, p)

            x, y = i // 3 * 3 + p // 3, j // 3 * 3 + p % 3
            self.available[x][y] = self.get_available(x, y)

    def solve_sudoku(self, override=True):
        def dfs(i, j):
            self.depth += 1
            if self.depth > 20000:
                raise RecursionError("Depth too high, force restart")
            if j >= 9:
                i += 1
                j = 0
            if i >= 9:
                eprint("\nSolved board at depth {}".format(self.depth))
                return True
            eprint("\r{}: dfs({}, {})".format(self.depth, i, j), end="")
            if self.isActive[i][j]:
                available = self.get_available(i, j)
                available = random.sample(available, len(available))
                for k in available:
                    self.grid[i][j] = k
                    if not dfs(i, j + 1):
                        self.grid[i][j] = None
                    else:
                        return True
                return False
            else:
                return dfs(i, j + 1)

        if override:
            self.clear_sudoku()

        found = True
        while found:
            found = False
            for x, y in self.allCoords:
                if self.grid[x][y] is not None:
                    continue

                available = self.get_available(x, y)
                if len(available) == 0:
                    eprint("No possible number for ({}, {})".format(x, y))
                    return False

                if len(available) == 1:
                    found = True
                    self.grid[x][y] = next(iter(available))
                    self.update_available(x, y)

        while True:
            try:
                self.depth = 0
                result = dfs(0, 0)
                return result
            except KeyboardInterrupt:
                eprint("\n" + repr(self))
                self.clear_sudoku()
                return False
            except RecursionError as e:
                eprint("\n{}".format(e))
                eprint("Current State:\n" + repr(self))
                self.clear_sudoku()

    def reset_sudoku(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = None
                self.isActive[i][j] = True

    def clear_sudoku(self):
        for i in range(9):
            for j in range(9):
                if self.isActive[i][j]:
                    self.grid[i][j] = None
                    self.available[i][j] = self.get_available(i, j)

    def generate_sudoku(self, num_holes=32, tries=1):
        def random_dig_holes():
            all_coords = [(x, y) for i in range(9) for y, x in enumerate([i] * 9)]
            random_holes = random.sample(all_coords, num_holes)
            for x, y in random_holes:
                self.grid[x][y] = None
                self.isActive[x][y] = True

        self.reset_sudoku()
        if not self.solve_sudoku():
            self.generate_sudoku(num_holes, tries=tries+1)
            return
        self.isActive = [[False for _ in range(9)] for _ in range(9)]  # nowhere to fill at this time
        random_dig_holes()

    def __repr__(self):
        return "\n".join(
            (" ".join(["{}"]*9)).format(*['.' if x is None else x for x in self.grid[i]])
            for i in range(9)
        )


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import ui

    app = QApplication(sys.argv)
    qSudoku = ui.SudokuUI()
    sys.exit(app.exec_())
