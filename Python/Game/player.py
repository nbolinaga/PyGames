import pygame
import pygame.gfxdraw
from pygame import mixer
mixer.init()
safe = mixer.Sound('coins27-36030.mp3')


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 50
        self.radius = 0
        self.prev_radius = 0
        self.rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.carry = 0
        self.small = True

    def shrink(self):
        self.small = True
        self.carry = 0
        safe.play()

    def move(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.radius
        self.rect.y = pos[1] - self.radius
        self.x = pos[0]
        self.y = pos[1]

    def add(self):
        self.small = False
        self.carry += 1

    def draw(self, surface, color):
        if self.carry > self.prev_radius and self.carry < 18:
            self.radius += 2
            self.prev_radius = self.carry
            if self.speed > 5:
                self.speed -= 5
            self.rect = pygame.Rect(
                self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        if self.small == True:
            self.prev_radius = 0
            self.radius = 4
            self.speed = 50
            self.rect = pygame.Rect(
                self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        pygame.gfxdraw.filled_circle(
            surface, self.x, self.y, self.radius, color)
        pygame.gfxdraw.aacircle(
            surface, self.x, self.y, self.radius, color)

        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)

        if self.carry > 18:
            pygame.gfxdraw.aacircle(
                surface, self.x, self.y, 38, (4, 63, 77))
            pygame.gfxdraw.aacircle(
                surface, self.x, self.y, 39, (4, 63, 77))


def handle_color(player, screenSize):
    return (255, 128, 128) if player.x > screenSize[0] / 2 else (128, 255, 255)


def handle_input(player):
    player.move()
