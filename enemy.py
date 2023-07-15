import random

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Enemy, self).__init__()

        self.enemy_anim = []
        for i in range(1, 5):
            img_path = f"IMG/fireball_0{i}.png"
            img = pygame.image.load(img_path).convert_alpha()
            self.enemy_anim.append(img)

        self.index = 0
        self.surf = self.enemy_anim[self.index]
        self.rect = self.surf.get_rect(center=(random.randint(width + 20, width + 100), random.randint(0, height)))
        self.speed = random.randint(11, 25)

        self.mask = pygame.mask.from_surface(self.surf)

    def animation(self):
        # Increment the index to switch to the next animation frame
        self.index = self.index + 1 if self.index < 3 else 0
        self.surf = self.enemy_anim[self.index]

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def collide_with(self, other):
        if self.rect.colliderect(other.rect):
            offset_x = other.rect.x - self.rect.x
            offset_y = other.rect.y - self.rect.y
            return self.mask.overlap(other.mask, (offset_x, offset_y)) is not None
        return False
