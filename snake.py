import pygame
import random
import time
import math


class Game(object):
    def __init__(self):
        pygame.init()
        self.height = 400
        self.width = 400
        self.border_width = 10
        self.s = pygame.display.set_mode((self.height, self.width))
        self.speed = 20
        self.set_start_state()

    def set_start_state(self):
        self.snake_size = 20
        self.food_size = 20
        self.xs = [
            self.width / 2 - self.snake_size,
            self.width / 2 - self.snake_size,
            self.width / 2 - self.snake_size,
            self.width / 2 - self.snake_size,
        ]
        self.ys = [
            self.height / 2 - self.snake_size,
            self.height / 2 - 2 * self.snake_size,
            self.height / 2 - 3 * self.snake_size,
            self.height / 2 - 4 * self.snake_size,
        ]
        self.dirs = random.choice([0, 1, 2, 3])
        self.score = 0
        self.applepos = (
            random.randint(
                self.border_width + self.food_size,
                self.height - self.food_size - self.border_width,
            ),
            random.randint(
                self.border_width + self.food_size,
                self.width - self.food_size - self.border_width,
            ),
        )
        self.appleimage = pygame.Surface((self.food_size, self.food_size))
        self.appleimage.fill((0, 255, 0))
        self.img = pygame.Surface((self.food_size, self.food_size))
        self.img.fill((0, 0, 0))
        self.game_over = False
        self.new_distance = 0
        self.old_distance = 0

    def collide(self, x1, x2, y1, y2, w1, w2, h1, h2):
        if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
            return True
        else:
            return False

    def reward(self, apple_eaten):
        if self.new_distance < self.old_distance:
            reward = 0.4
        else:
            reward = -0.4
        if apple_eaten:
            reward = 1.0
        return reward

    def die(self):
        reward = -1
        self.draw_board()
        image = pygame.surfarray.array3d(pygame.display.get_surface())
        time.sleep(1 / 10)
        return image, reward, True
        
    def direction_snake(self, actions):
        action = actions
        if action == 2 and self.dirs != 0:
            self.dirs = 2
        elif action == 0 and self.dirs != 2:
            self.dirs = 0
        elif action == 3 and self.dirs != 1:
            self.dirs = 3
        elif action == 1 and self.dirs != 3:
            self.dirs = 1
        dirs = self.dirs
        self.move_snake(dirs)