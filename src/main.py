import pygame
from menu import Menu
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED
from checkers.game import Game
from algos.minimax import minimax

FPS = 60
WIN = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.SRCALPHA, 32)

pygame.display.set_caption("Checkers")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    clock = pygame.time.Clock()
    game = Game(WIN)
    menu = Menu(game)

    while not game.is_quit():
        clock.tick(FPS)
        
        if game.is_running():
            if game.winner() != None:
                menu.reset( game.winner() )

            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(), 2, True, game)
                game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            
            # if event.type == pygame.MOUSEMOTION:
            #     if menu.is_active():
            #         pos = pygame.mouse.get_pos()
            #         if menu.get_x() < pos[0] and menu.get_x() + menu.get_width() > pos[0] and \
            #             menu.get_y() < pos[1] and menu.get_y() + menu.get_height() > pos[1]:
            #             pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu.is_active():
                    for button in menu.get_buttons():
                        if button.get_rect().left + menu.get_x() < pos[0] and button.get_rect().right + menu.get_x() > pos[0] and\
                            button.get_rect().top + menu.get_y() < pos[1] and button.get_rect().bottom + menu.get_y() > pos[1]:
                            button.activate()

                if game.is_running():
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()
        if menu.is_active():
            menu.draw(WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
