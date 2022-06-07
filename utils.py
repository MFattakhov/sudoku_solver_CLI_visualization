from typing import List, Tuple
from bitset import Bitset
import time


class SudokuBoard:
    def __init__(self, board: List[List[int]]) -> None:
        self.board = board
        self._initial_digits = [[bool(board[i][j])
                                 for j in range(9)] for i in range(9)]

    @classmethod
    def from_str(cls, s: str) -> 'SudokuBoard':
        return cls([list(map(int, list(s[9 * i:9 * (i + 1)]))) for i in range(9)])

    def print(self) -> None:
        # makes initial data blue
        board_to_print = [['' for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                board_to_print[i][j] = str(self.board[i][j])
                if self._initial_digits[i][j]:
                    board_to_print[i][j] = f'\033[94m{board_to_print[i][j]}\033[0m'

        for i in range(9):
            if i % 3 == 0 and i != 0:
                print('——————+———————+——————')

            placeholder = '{} {} {} | {} {} {} | {} {} {} '
            print(placeholder.format(*board_to_print[i]))

    def solve(self, visual=False) -> None:
        def get_cell(row: int, col: int) -> int:
            return (row // 3) * 3 + col // 3

        def get_next_row(row: int, col: int) -> int:
            return row + (col + 1) // 9

        def get_next_col(col: int) -> int:
            return (col + 1) % 9

        def next_empty_position(row: int, col: int) -> Tuple[int, int]:
            while row != 9:
                if self.board[row][col] == 0:
                    return (row, col)

                row = get_next_row(row, col)
                col = get_next_col(col)

            return (9, 0)

        def solve_from_position(row_start: int, col_start: int) -> bool:
            row, col = next_empty_position(row_start, col_start)

            if row == 9:
                return True

            cell = get_cell(row, col)
            contains = row_contains[row] | col_contains[col] | cell_contains[cell]

            if contains == (1 << 9) - 1:  # check if 'contains' contains every digit 1-9
                return False

            for digit in range(1, 10):
                if not contains[digit - 1]:
                    self.board[row][col] = digit
                    if visual:
                        # waits a little since the algorithms is too fast
                        time.sleep(0.02)
                        print("\033[H\033[J", end="")  # clears the console
                        self.print()
                    row_contains[row][digit - 1] = 1
                    col_contains[col][digit - 1] = 1
                    cell_contains[cell][digit - 1] = 1

                    if solve_from_position(row, col):
                        return True

                    row_contains[row][digit - 1] = 0
                    col_contains[col][digit - 1] = 0
                    cell_contains[cell][digit - 1] = 0

            if visual:
                # waits a little since the algorithms is too fast
                time.sleep(0.02)
                print("\033[H\033[J", end="")  # clears the console
                self.print()
            self.board[row][col] = 0
            return False

        row_contains = [Bitset(length=9) for _ in range(9)]
        col_contains = [Bitset(length=9) for _ in range(9)]
        cell_contains = [Bitset(length=9) for _ in range(9)]

        for row in range(9):
            for col in range(9):
                digit = self.board[row][col]
                if digit != 0:
                    row_contains[row][digit - 1] = 1
                    col_contains[col][digit - 1] = 1
                    cell_contains[get_cell(row, col)][digit - 1] = 1

        solve_from_position(0, 0)

        if visual:
            print("\033[H\033[J", end="")  # clears the console
            self.print()
