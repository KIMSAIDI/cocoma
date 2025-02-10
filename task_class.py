import pygame

#from main_env import WHITE, GREEN, RED, BLUE, scale
#from main_env_part1 import WHITE, GREEN, RED, BLUE, scale, draw_text
from utils import *


# Class des Tâches
class Task:
    nb_tasks = 0
    waiting_time_sum = 0
    waiting_time_std = 0
    waiting_time_min = float('inf')
    waiting_time_max = 0

    def __init__(self, start, end, name):
        self.id = Task.nb_tasks
        Task.nb_tasks += 1
        self.start = start
        self.end = end
        self.distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
        self.allocated = False
        self.taken = False
        self.completed = False
        self.waiting_time = 0
        self.name = name

    def __str__(self):
        return f"Task {self.id}"

    def __repr__(self):
        return f"Task {self.id}"

    def draw(self, screen):
        color = WHITE if not self.taken else BLUE
        start_scaled = (int(self.start[0] * scale), int(self.start[1] * scale))
        end_scaled = (int(self.end[0] * scale), int(self.end[1] * scale))
        pygame.draw.circle(screen, GREEN, start_scaled, 3)
        pygame.draw.circle(screen, RED, end_scaled, 3)
        pygame.draw.line(screen, color, start_scaled, end_scaled, 2)
        draw_text(screen, f"t{self.id}, time: {self.waiting_time}", start_scaled[0], start_scaled[1] - 15, WHITE)


    def take(self):
        if not self.taken:
            Task.waiting_time_sum += self.waiting_time
            Task.waiting_time_max = max(Task.waiting_time_max, self.waiting_time)
            Task.waiting_time_min = min(Task.waiting_time_min, self.waiting_time)
            self.taken = True

    def complete(self):
        self.completed = True

    def allocate(self):
        self.allocated = True
    
    def update(self):
        if not self.taken:
            self.waiting_time += 1