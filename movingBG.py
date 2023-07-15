import pygame


class MovingBG(pygame.sprite.Sprite):
    def __init__(self, width, x, y, flip=False):
        super(MovingBG, self).__init__()

        surf = pygame.image.load("IMG/bg.png").convert_alpha()

        if flip:
            self.surf = pygame.transform.flip(surf, True, False)
        else:
            self.surf = surf

        self.rect = self.surf.get_rect(topleft=(x, y))
        self.width = width

    def update(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right <= 0:
            self.rect = self.surf.get_rect(topleft=(self.width, 0))
