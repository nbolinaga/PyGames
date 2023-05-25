import random
import pygame

size = 10


class bus_left():
    def __init__(self, width, color, spawn):
        self.x = random.randint(0, (width/2) - size)
        self.speed = random.randint(3, 7)
        self.color = color
        self.rect = pygame.Rect(self.x, spawn, size, size * 2)

    def fly_down(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect,
                         width=0, border_radius=10)


class bus_right():
    def __init__(self, width, color, spawn):
        self.x = random.randint((width/2) + size, width)
        self.speed = random.randint(3, 7)
        self.color = color
        self.rect = pygame.Rect(self.x, spawn, size, size * 2)

    def fly_up(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect,
                         width=0, border_radius=10)
