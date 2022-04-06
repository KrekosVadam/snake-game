#!/usr/bin/python3
# #
#
# A snake game created by Jadon Krekos
# Purpose is to be similar to Google's Snake game
# #

import random
import pygame
from pygame.locals import *


##
# Canvas Class
#
##
class Canvas:
    BACKGROUND_COLOUR = "#333333"

    def __init__(self):
        self.SIZE = 40
        self.GRASS_LENGTH = 14
        self.GRASS_COLOUR1 = "#90bd4f"
        self.GRASS_COLOUR2 = "#99c754"

    def draw(self, __window):
        count = 0

        for i in range(1, self.GRASS_LENGTH + 1):
            for z in range(1, self.GRASS_LENGTH + 1):
                if count % 2 == 0:
                    pygame.draw.rect(__window, self.GRASS_COLOUR1, [self.SIZE*z, self.SIZE *i, self.SIZE, self.SIZE])
                else:
                    pygame.draw.rect(__window, self.GRASS_COLOUR2, [self.SIZE*z, self.SIZE*i, self.SIZE, self.SIZE])
                count += 1
            count -= 1

##
# Snake Class
#
##
class Snake:

    def __init__(self, x = 200, y = 200):
        self.snake_size = 40
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.colour = "#2f59c4"
        self.snake_length = []
        self.start = (x, y)
        self.snake_length.append(self.start)
        self.snake_tail = 1
        self.is_alive = True

    def move_left(self):
        if self.x_change < 0:
            return
        self.x_change -= self.snake_size
        self.y_change = 0
        print("left")

    def move_right(self):
        if self.x_change > 0:
            return
        self.x_change += self.snake_size
        self.y_change = 0
        print("right")

    def move_up(self):
        if self.y_change < 0:
            return
        self.x_change = 0
        self.y_change -= self.snake_size
        print("up")

    def move_down(self):
        if self.y_change > 0:
            return
        self.x_change = 0
        self.y_change += self.snake_size
        print("down")

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.snakehead = (self.x, self.y)
        if self.snake_tail > 1:
            if self.snakehead in self.snake_length:
                return False
        self.snake_length.append(self.snakehead)
        if len(self.snake_length) > self.snake_tail:
            del self.snake_length[0]

    def add_segment(self):
        self.snake_tail += 1

    def draw(self, __window):
        for segment in self.snake_length:
            pygame.draw.rect(__window, self.colour, (segment[0], segment[1], self.snake_size, self.snake_size))

##
# Class Food
#
##
class Food:
    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 640
        self.food_size = 40
        self.x = round(random.randrange(40, self.WIDTH - self.food_size * 2) / self.food_size) * self.food_size
        self.y = round(random.randrange(40, self.HEIGHT - self.food_size * 2) / self.food_size) * self.food_size

    def respawn(self, Snake, __window):
        bad_spawn = True
        while bad_spawn == True:
            self.x = round(random.randrange(40, self.WIDTH - self.food_size * 2) / self.food_size) * self.food_size
            self.y = round(random.randrange(40, self.HEIGHT - self.food_size * 2) / self.food_size) * self.food_size
            bad_spawn = False

            for position in Snake.snake_length:
                if position[0] == self.x and position[1] == self.y:
                    bad_spawn = True
                    break
                else:
                    bad_spawn = False

    def draw(self, __window):
        pygame.draw.rect(__window, "#FF0000", (self.x, self.y, self.food_size, self.food_size))

##
# Game Class
#
##
class Game:
    HEIGHT = 640
    WIDTH = 640
    COLOUR = "#333333"


    def __init__(self):
        pygame.font.init()
        pygame.display.set_caption("Snaik")
        self.__window = pygame.display.set_mode((self.HEIGHT, self.WIDTH))

        self.__canvas = Canvas()
        self.__snake = Snake()
        self.__food = Food()

        self.__clock = pygame.time.Clock()

    def run(self):
        self.running = True

        while self.running:
            pygame.time.delay(120)
            self.__handle_events()
            self.__draw_playspace()
            self.__draw_playerelements()
            self.__clock.tick(15)


    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    print("QUITTING...")
                if event.key == pygame.K_LEFT:
                    self.__snake.move_left()
                if event.key == pygame.K_RIGHT:
                    self.__snake.move_right()
                if event.key == pygame.K_UP:
                    self.__snake.move_up()
                if event.key == pygame.K_DOWN:
                    self.__snake.move_down()

        if self.__snake.move() == False:
            pygame.quit()
            quit()

        if self.food_collision() == True:
            self.__snake.add_segment()
            self.__food.respawn(self.__snake, self.__window)

        if self.boundary_collision() == True:
            pygame.quit()
            quit()

        pygame.display.flip()

    def boundary_collision(self):
        if self.__snake.x < 0 or self.__snake.y < 0 or self.__snake.x > self.WIDTH - 40 or self.__snake.y > self.HEIGHT - 40:
            return True
        else:
            return False

    def food_collision(self):
        if self.__snake.x == self.__food.x and self.__snake.y == self.__food.y:
            return True
        else:
            return False

    def score(self):
        counter = 0
        for i in range(self.__snake.snake_length):
            counter += 1
        return counter

    def __draw_playspace(self):
        self.__window.fill(self.COLOUR)
        self.__canvas.draw(self.__window)

    def __draw_playerelements(self):
        self.__snake.draw(self.__window)
        self.__food.draw(self.__window)



Game().run()
