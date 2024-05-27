"""Connect4 game with Pygame. Based on Keith Galli's design."""

import sys

import numpy as np
import pygame as pg

# Board Init
CIRCLE_COLORS = {
    "BG_COLOR": (70, 81, 156),
    "CIRCLE": (51, 51, 51),
    "Player1": (255, 0, 0),
    "Player2": (255, 255, 0),
}
ROW_COUNT = 6
COLUMN_COUNT = 7


class Table:
    """Main Board"""

    def __init__(self):
        pass

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def winning_move(self, board, piece):
        # Check horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                subset = list(board[r, c : c + 4])
                if all(subset) and sum(subset) == 4 * piece:
                    return True

        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (
                    board[r][c]
                    == board[r + 1][c]
                    == board[r + 2][c]
                    == board[r + 3][c]
                    == piece
                ):
                    return True

        # Check positively slopes
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (
                    board[r][c]
                    == board[r + 1][c + 1]
                    == board[r + 2][c + 2]
                    == board[r + 3][c + 3]
                    == piece
                ):
                    return True

        # Check negatively slopes
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (
                    board[r][c]
                    == board[r - 1][c + 1]
                    == board[r - 2][c + 2]
                    == board[r - 3][c + 3]
                    == piece
                ):
                    return True

    def finish_game(self, col, turn):
        turn += 1
        game_over = False

        if self.is_valid_location(board=board, col=col):
            row = self.get_next_open_row(board=board, col=col)
            self.drop_piece(board=board, row=row, col=col, piece=turn)

            if self.winning_move(board=board, piece=turn):
                label = myfont.render(
                    f"Player {turn} wins! Game Over",
                    turn,
                    CIRCLE_COLORS[f"Player{turn}"],
                )
                screen.blit(label, (RADIUS, int(SQUARESIZE / 5)))
                game_over = True

        return game_over


# Logic Init
table = Table()
board = table.create_board()


# Pygame Init
pg.init()

SQUARESIZE = int(200)
RADIUS = int(SQUARESIZE / 2.3)
END_GAME_WAIT = 1000  # 1s

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

screen = pg.display.set_mode(size)


class Draw:
    """Pygame main graphics"""

    def __init__(self, board):
        self.board = board

    def draw_circle(self, col, row, player):
        pg.draw.circle(
            screen,
            CIRCLE_COLORS[f"Player{player}"],
            (
                int((col + 1 / 2) * SQUARESIZE),
                height - int((row + 1 / 2) * SQUARESIZE),
            ),
            RADIUS,
        )

    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pg.draw.rect(
                    screen,
                    CIRCLE_COLORS["BG_COLOR"],
                    (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE),
                )
                pg.draw.circle(
                    screen,
                    CIRCLE_COLORS["CIRCLE"],
                    (int((c + 1 / 2) * SQUARESIZE), int((r + 3 / 2) * SQUARESIZE)),
                    RADIUS,
                )

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == 1:
                    self.draw_circle(col=c, row=r, player=1)
                elif self.board[r][c] == 2:
                    self.draw_circle(col=c, row=r, player=2)

        pg.display.update()


draw = Draw(board=board)
draw.draw_board()
pg.display.update()
myfont = pg.font.SysFont("monospace", RADIUS)


def main():
    game_over = False
    turn = 0

    while not game_over:
        # Pygame control
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    sys.exit()

            if event.type == pg.MOUSEMOTION:
                pg.draw.rect(screen, CIRCLE_COLORS["CIRCLE"], (0, 0, width, SQUARESIZE))
                posx = event.pos[0]

                if turn == 0:
                    pg.draw.circle(
                        screen, CIRCLE_COLORS["Player1"], (posx, RADIUS), RADIUS
                    )
                else:
                    pg.draw.circle(
                        screen, CIRCLE_COLORS["Player2"], (posx, RADIUS), RADIUS
                    )

            pg.display.update()

            if event.type == pg.MOUSEBUTTONDOWN:
                pg.draw.rect(screen, CIRCLE_COLORS["CIRCLE"], (0, 0, width, SQUARESIZE))

                posx = event.pos[0]
                col = int(posx / SQUARESIZE)
                game_over = table.finish_game(col=col, turn=turn)

                draw.draw_board()
                turn = (turn + 1) % 2

                if game_over:
                    pg.time.wait(END_GAME_WAIT)


if __name__ == "__main__":
    main()
