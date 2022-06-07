from utils import SudokuBoard


if __name__ == '__main__':
    s = '070000043040009610800634900094052000358460020000800530080070091902100005007040802'
    board = SudokuBoard.from_str(s)
    board.print()
    board.solve(visual=True)
