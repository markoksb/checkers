import pygame
from .constants import BLACK, ROWS, COLS, SQUARE_SIZE, RED, WHITE, BG1, BG2, BG
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = 12
        self.white_left = 12
        self.red_kings = 0
        self.white_kings = 0
        self.create_board()

    def draw_squares(self, window):
        #window.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(window, BG1, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(window, BG2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.red_left -= 1
            if piece.color == WHITE:
                self.white_left -= 1

    def get_piece(self, row, col):
        # if row < 0 or row >= ROWS or\
        #     col < 0 or col >= COLS:
        #     return -1
        return self.board[row][col]

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def eval_state(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_valid_moves(self, piece: Piece):
        valid_moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == RED or piece.king:
            valid_moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
            valid_moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            valid_moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            valid_moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return valid_moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for i in range(start, stop, step):
            if left < 0:
                break
            current = self.get_piece(i, left)
            if current == -1:
                break
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(i, left)] = last + skipped
                else:
                    moves[(i, left)] = last
                
                if last:
                    if step == -1:
                        row = max(i - 3, - 1)
                    else:
                        row = min(i + 3, ROWS)

                    moves.update(self._traverse_left(i + step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(i + step, row, step, color, left+1, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for i in range(start, stop, step):
            if right >= COLS:
                break
            current = self.get_piece(i, right)
            if current == -1:
                break
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(i, right)] = last + skipped
                else:
                    moves[(i, right)] = last
                
                if last:
                    if step == -1:
                        row = max(i - 3, - 1)
                    else:
                        row = min(i + 3, ROWS)

                    moves.update(self._traverse_left(i + step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(i + step, row, step, color, right+1, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
