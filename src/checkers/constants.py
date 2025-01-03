import pygame

WIDTH = 800
HEIGHT = 800

ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH//COLS

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 127, 0)
BLACK = (0, 0, 0)
GREY = (63, 63, 63)
BG1 = (95, 31, 15)
BG2 = (63, 23, 15)
BG = pygame.image.load("/Users/markob/Documents/GFN/lf08 - software2/python/pygame_test/_checkers/src/checkers/assets/bg.jpg")

CROWN = pygame.image.load("/Users/markob/Documents/GFN/lf08 - software2/python/pygame_test/_checkers/src/checkers/assets/crown.png")
CROWN = pygame.transform.scale(CROWN, (44,25))