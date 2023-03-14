from utils import SudokuBoard


if __name__ == '__main__':
    s = '070000043\
040009610\
800634900\
094052000\
358460020\
000800530\
080070091\
902100005\
007040802'
    board = SudokuBoard.from_str(s)
    board.print()
    board.solve(visual=True)
