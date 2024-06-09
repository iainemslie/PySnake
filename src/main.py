from settings import *

from random import randint
from os.path import join


class Timer:
    def __init__(self, interval):
        self.interval = interval
        self.lastUpdateTime = 0

    def update_event(self):
        currentTime = pygame.time.get_ticks()
        if (currentTime - self.lastUpdateTime >= self.interval):
            self.lastUpdateTime = currentTime
            return True
        return False


class Food(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.generate_random_pos()
        self.rect = self.image.get_frect(
            topleft=(self.generate_random_pos()[0],
                     self.generate_random_pos()[1])
        )

    def generate_random_pos(self):
        return (randint(0, CELL_COUNT - 1) * CELL_SIZE, randint(0, CELL_COUNT - 1) * CELL_SIZE)

    def set_new_pos(self):
        self.rect.topleft = self.generate_random_pos()


class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos = pos
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(DARK_GREEN)
        self.rect = self.image.get_frect(topleft=self.pos)


class Snake():
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.body = [
            SnakeSegment(pygame.Vector2(
                6 * CELL_SIZE, 9 * CELL_SIZE), all_sprites),
            SnakeSegment(pygame.Vector2(
                5 * CELL_SIZE, 9 * CELL_SIZE), all_sprites),
            SnakeSegment(pygame.Vector2(
                4 * CELL_SIZE, 9 * CELL_SIZE), all_sprites)
        ]
        self.direction = pygame.Vector2(1, 0)
        self.add_segment = False

    def update(self):
        self.body.insert(
            0, (SnakeSegment(self.body[0].pos + self.direction * CELL_SIZE, self.all_sprites)))
        if self.add_segment:
            self.add_segment = False
        else:
            self.body.pop().kill()


class Game:
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(
            (CELL_SIZE * CELL_COUNT, CELL_SIZE * CELL_COUNT))
        pygame.display.set_caption("PySnake")
        pygame.mouse.set_visible(False)
        self.running = True

        self.update_interval = 200
        self.timer = Timer(self.update_interval)

        # imports
        self.load_data()

        # groups
        self.all_sprites = pygame.sprite.Group()

        # sprites and game objects
        self.food = Food(self.food_surf, self.all_sprites)
        self.snake = Snake(self.all_sprites)

    def load_data(self):
        self.food_surf = pygame.image.load(join('..', 'graphics', 'food.png'))

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.snake.direction.x != -1:
            self.snake.direction = pygame.Vector2(1, 0)
        if keys[pygame.K_LEFT] and self.snake.direction.x != 1:
            self.snake.direction = pygame.Vector2(-1, 0)
        if keys[pygame.K_DOWN] and self.snake.direction.y != -1:
            self.snake.direction = pygame.Vector2(0, 1)
        if keys[pygame.K_UP] and self.snake.direction.y != 1:
            self.snake.direction = pygame.Vector2(0, -1)

    def check_food_collision(self):
        if self.snake.body[0].rect.colliderect(self.food.rect):
            self.food.set_new_pos()
            self.snake.add_segment = True
            self.update_interval -= 2
            self.timer.interval = self.update_interval

    def check_edge_collision(self):
        if self.snake.body[0].rect.x == (CELL_COUNT * CELL_SIZE) or self.snake.body[0].rect.x <= -1:
            self.game_over()
        if self.snake.body[0].rect.y == CELL_COUNT * CELL_SIZE or self.snake.body[0].rect.y <= -1:
            self.game_over()

    def check_tail_collision(self):
        tail = self.snake.body[1:]
        head = self.snake.body[0]
        for segment in tail:
            if head.rect.colliderect(segment.rect):
                self.game_over()

    def game_over(self):
        self.__init__()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # input
            self.get_input()

            # logic
            self.check_food_collision()
            self.check_edge_collision()
            self.check_tail_collision()

            if self.timer.update_event():
                self.snake.update()
            self.all_sprites.update()

            # draw
            self.display_surf.fill(LIGHT_GREEN)
            self.all_sprites.draw(self.display_surf)

            # pygame.draw.rect(self.display_surf, DARK_GREEN, (OFFSET-5,
            #                  OFFSET-5, CELL_SIZE*CELL_COUNT, CELL_SIZE*CELL_COUNT+10), 5, 2)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
