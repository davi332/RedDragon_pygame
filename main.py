import pygame, sys
from support import *
from movingBG import MovingBG
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Red Dragon")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("IMG/bg.png").convert_alpha()

        self.bg1 = MovingBG(SCREEN_WIDTH, 0, 0)
        self.bg2 = MovingBG(SCREEN_WIDTH, SCREEN_WIDTH, 0, True)

        self.moving_bg_sprites = pygame.sprite.Group()
        self.moving_bg_sprites.add(self.bg1)
        self.moving_bg_sprites.add(self.bg2)

        self.enemies = pygame.sprite.Group()

        # player
        self.player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.PLAYER_ANIM = pygame.event.custom_type()
        self.ENEMY_ANIM = pygame.event.custom_type()
        self.ADD_ENEMY = pygame.event.custom_type()

        pygame.time.set_timer(self.ADD_ENEMY, 250)
        pygame.time.set_timer(self.PLAYER_ANIM, 130)
        pygame.time.set_timer(self.ENEMY_ANIM, 130)

        #
        self.FONT = pygame.font.Font("font/BD_Cartoon_Shout.ttf", 38)
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.score = 0

    def draw(self, screen):
        screen.fill((128, 128, 128))

        screen.blit(self.background, (0, 0))
        for entity in self.moving_bg_sprites:
            screen.blit(entity.surf, entity.rect)

        #
        for entity in self.all_sprites:
            screen.blit(entity.surf, entity.rect)

        if self.game_over:
            self.player.index = 0
            draw_game_over(screen)

        # score
        score_txt = self.FONT.render(f"Score: {self.score}", True, "white")
        screen.blit(score_txt, (SCREEN_WIDTH - score_txt.get_width() - 20, 10))

        pygame.display.update()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif self.game_over and event.key == pygame.K_RETURN:
                    self.reset()

            elif event.type == self.PLAYER_ANIM:
                self.player.player_animation()

            elif event.type == self.ENEMY_ANIM:
                for enemy in self.enemies:
                    enemy.animation()

            elif event.type == self.ADD_ENEMY:
                if not self.game_over:
                    new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.all_sprites.add(new_enemy)
                    self.enemies.add(new_enemy)

                    self.score = self.calculate_score()

    def update(self):
        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)

            self.enemies.update()
            self.moving_bg_sprites.update()
        for enemy in self.enemies:
            if self.player.collide_with(enemy):
                self.game_over = True
                break

    def reset(self):
        self.player.reset()
        self.all_sprites.empty()
        self.enemies.empty()
        self.all_sprites.add(self.player)
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.score = 0

    def calculate_score(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        second = int(elapsed_time / 1000)
        return second

    def run(self):
        while True:
            self.handle_event()
            self.update()
            self.draw(self.screen)

            self.clock.tick(FPS)
            pygame.display.update()


def draw_game_over(screen):
    game_over_font = pygame.font.Font("font/BD_Cartoon_Shout.ttf", 42)
    game_over_txt = game_over_font.render("Game Over!", True, "white")
    game_over_rect = game_over_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    restart_font = pygame.font.Font("font/BD_Cartoon_Shout.ttf", 40)
    restart_txt = restart_font.render("Press Enter to Restart", True, "white")
    restart_rect = restart_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

    screen.blit(game_over_txt, game_over_rect)
    screen.blit(restart_txt, restart_rect)


if __name__ == "__main__":
    game = Game()
    game.run()
