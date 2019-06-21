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