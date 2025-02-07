import pygame

from main_env import WHITE, GREEN, RED, BLUE, scale

# Class des Tâches
class Task:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
        self.taken = False
        self.completed = False

    def draw(self, screen):
        color = WHITE if not self.taken else BLUE
        start_scaled = (int(self.start[0] * scale), int(self.start[1] * scale))
        end_scaled = (int(self.end[0] * scale), int(self.end[1] * scale))
        pygame.draw.circle(screen, GREEN, start_scaled, 3)
        pygame.draw.circle(screen, RED, end_scaled, 3)
        pygame.draw.line(screen, color, start_scaled, end_scaled, 2)


    def take(self):
        self.taken = True

    def complete(self):
        self.completed = True