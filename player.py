import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, sW, sH):
        super(Player, self).__init__()

        self.player_anim = []
        for i in range(1, 9):
            img_path = f"IMG/dragon_0{i}.png"
            img = pygame.image.load(img_path).convert_alpha()
            self.player_anim.append(img)

        self.index = 0

        self.surf = self.player_anim[self.index]
        self.rect = self.surf.get_rect(center=(sW // 2, sH // 2))

        self.mask = pygame.mask.from_surface(self.surf)

        self.sW = sW
        self.sH = sH

    def handle_movement(self, keys):
        movements = {
            pygame.K_w: (0, -5),  # Up
            pygame.K_s: (0, 5),  # Down
            pygame.K_a: (-5, 0),  # Left
            pygame.K_d: (5, 0)  # Right
        }

        for key, movement in movements.items():
            if keys[key]:
                self.rect.move_ip(movement[0], movement[1])

        # Limit the player's movement within the screen boundaries
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.sW)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.sH)

    def player_animation(self):
        # Increment the index to switch to the next animation frame
        self.index = self.index + 1 if self.index < 7 else 0
        self.surf = self.player_anim[self.index]

    def update(self, keys):
        self.handle_movement(keys)
        # Update the position of the rect based on the player's position
        self.rect.center = (self.rect.centerx, self.rect.centery)

    def collide_with(self, other):
        if self.rect.colliderect(other.rect):
            offset_x = other.rect.x - self.rect.x
            offset_y = other.rect.y - self.rect.y

            return self.mask.overlap_mask(other.mask, (offset_x, offset_y)) is not None
        return False

    def reset(self):
        self.rect = self.rect = self.surf.get_rect(center=(self.sW // 2, self.sH // 2))
