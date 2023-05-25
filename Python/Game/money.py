import pygame
import random
from pygame import mixer
mixer.init()
coinGrab = mixer.Sound('select-sound-121244.mp3')


class Collector:
    def __init__(self, width, height, true_height):
        self.size = 25
        self.color = (4, 63, 77)
        self.x = width // 2
        self.y = true_height // 2

    def draw(self, surface):
        pygame.gfxdraw.filled_circle(
            surface, self.x, self.y, self.size, self.color)
        pygame.gfxdraw.aacircle(
            surface, self.x, self.y, self.size, self.color)


class Coin:
    # create a coin object randomly in the screen
    def __init__(self, width, height, true_height, player):
        # force the coin to spawn in the side different from the player
        self.size = 10
        if player.x > width / 2:
            self.x = random.randint(
                0 + (self.size * 2), width / 2 - (self.size * 2))
            self.y = random.randint(self.size * 2, height - (self.size * 2))
        else:
            self.x = random.randint(
                width / 2 + (self.size * 2), width - (self.size * 2))
            self.y = random.randint(
                true_height - height + (self.size * 2), true_height - (self.size * 2))

        # gold
        self.color = (255, 215, 0)

    def draw(self, surface):
        pygame.gfxdraw.filled_circle(
            surface, self.x, self.y, self.size, self.color)
        pygame.gfxdraw.aacircle(
            surface, self.x, self.y, self.size, self.color)

    def check_collision(self, player):
        # check if distance from coin center is less than 20 units from player center
        if (player.x - self.x)**2 + (player.y - self.y)**2 < (player.radius*2)**2:
            if player.x < self.x:
                self.x -= 5
            else:
                self.x += 5

            if player.y < self.y:
                self.y -= 5
            else:
                self.y += 5
        if (player.x - self.x)**2 + (player.y - self.y)**2 < 10**2:
            coinGrab.play()
            return True
        return False
