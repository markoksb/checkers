import pygame
from .constants import RED, WHITE, GREEN, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.__exit = False

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.__is_running = False

    def update(self):
        self.board.draw(self.win)
        if self.selected != None:
            self.draw_valid_moves(self.valid_moves)

    def reset(self):
        self._init()
        self.__is_running = True

    def is_running(self) -> bool:
        return self.__is_running

    def winner(self):
        if self.board.red_left <= 0:
            self.__is_running = False
            return "White"
        elif self.board.white_left <= 0:
            self.__is_running = False
            return "Red"
        return None

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

            self.change_turn()
            return True
        
        return False        
    
    def change_turn(self):
        self.selected = None
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        if self.valid_moves == None:
            return
        for move in moves:
            row, col = move
            pos_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            pos_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.win, GREEN, (pos_x, pos_y), 15)

    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def is_quit(self) -> bool:
        return self.__exit
    
    def quit(self) -> None:
        self.__exit = True