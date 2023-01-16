import pygame
import os
import sys
from random import randint

FPS = 50
running = True
game = False
drop_timer = 0
new_shape = True
pygame.init()
size = width, height = 290, 380
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
shapes = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = (255, 255, 255)
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


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
        self.image = load_image("shape" + str(shape_type) + ".png", colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.anchored = False
        self.ns, self.dt = False, 1
        self.changes = ''
        self.mask = pygame.mask.from_surface(self.image)
        for sprite in all_sprites.spritedict.keys():
            if pygame.sprite.collide_mask(self, sprite):
                print("Конец Игры")
                self.anchored = True


    def update(self, ev):
        self.changes = ''
        if not self.anchored:
            if ev != 'drop':
                if ev.key == pygame.K_w:
                    rect = self.rect
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = rect.x, rect.y
                    self.changes = 'rot'
                if ev.key == pygame.K_a:
                    self.rect.x -= 30
                    self.changes = 'l'
                if ev.key == pygame.K_d:
                    self.rect.x += 30
                    self.changes = 'r'
                if ev.key == pygame.K_s:
                    self.dt = 0
                    self.rect.y += 30
                    self.changes = 'd'
                self.mask = pygame.mask.from_surface(self.image)
            else:
                self.rect.y += 30
                self.changes = "d"
            for sprite in all_sprites.spritedict.keys():
                if pygame.sprite.collide_mask(self, sprite):
                    if self.changes == 'rot':
                        rect = self.rect
                        self.image = pygame.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = rect.x, rect.y
                        self.mask = pygame.mask.from_surface(self.image)
                    if self.changes == 'l':
                        self.rect.x += 30
                    if self.changes == 'r':
                        self.rect.x -= 30
                    if self.changes == 'd':
                        self.rect.y -= 30
                        self.ns = True
                        self.anchored = True
            if self.anchored:
                self.add(all_sprites)


if __name__ == '__main__':
    Border(9, 9, width - 9, 9)
    Border(9, height - 9, width - 9, height - 9)
    Border(9, 9, 9, height - 9)
    Border(width - 9, 9, width - 9, height - 9)
    board = Board(width, height)
    while running:
        drop_timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                shapes.update(event)
        if drop_timer >= 50:
            shapes.update('drop')
            drop_timer = 0
        if new_shape:
            s = Shape(shapes, randint(1, 7), 10, 10, 70, 40)
            new_shape = False
        if s.dt == 0:
            drop_timer = 0
            s.dt = 1
        if s.ns:
            new_shape = True
            s.ns = False
        screen.fill((0, 0, 0))
        board.render(screen)
        shapes.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
