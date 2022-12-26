import pygame
import os
import sys

FPS = 50
pygame.init()
size = width, height = 290, 290
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = (width - left) // cell_size
        self.height = (height - top) // cell_size
        self.board = [[0] * self.height for _ in range(self.width)]
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + self.cell_size * i,
                                  self.top + self.cell_size * j,
                                  self.cell_size, self.cell_size), 1)


class Shape(pygame.sprite.Sprite):
    def __init__(self, group, shape_type, left, top, x, y):
        super().__init__(group)
        self.top, self.left, self.x, self.y, self.shape_type = top, left, x, y, shape_type
        self.image = load_image("shape" + str(shape_type))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


    def update(self, ):
        self.image = pygame.transform.rotate(self.image, 90)


if __name__ == '__main__':
    board = Board(width, height)
    shapes = pygame.sprite.Group()
    running = True
    game = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
