from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def minimax(state, depth: int, max_player: bool, game):
    if depth == 0 or game.winner() != None:
        return state.eval_state(), state

    if max_player:
        maxEval = float("-inf")
        best_move = None
        for move in get_all_moves(state, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float("inf")
        best_move = None
        for move in get_all_moves(state, RED, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def get_all_moves(state, color, game):
    moves = []
    for piece in state.get_all_pieces(color):
        valid_moves = state.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game, state, piece)
            temp_state = deepcopy(state)
            temp_piece = temp_state.get_piece(piece.row, piece.col)
            new_state = simulate_move(temp_piece, move, temp_state, game, skip)
            moves.append(new_state)

    return moves

def simulate_move(piece, move, state, game, skip):
    state.move(piece, move[0], move[1])
    if skip:
        state.remove(skip)
    
    return state


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,0,63), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(50)