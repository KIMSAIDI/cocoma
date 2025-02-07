import pygame
import random

from main_env import GRID_SIZE, TAXI_RADIUS, scale, WHITE, GREY, YELLOW, RED, GREEN, BLUE, FONT

# Fonction pour dessiner du texte
def draw_text(screen, text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Class des Taxis
class Taxi:

    def __init__(self, position):
        self.position = position
        self.all_tasks = []
        self.path = []
        self.current_task = None
        self.destination = None
        self.task_started = False
        self.speed = 1

    def update(self):
        self.update_task()
        if self.destination:
            self.move(self.destination)

    def draw(self, screen):
        # Convertir la position à l'échelle de l'écran
        pos_scaled = (int(self.position[0] * scale), int(self.position[1] * scale))
        pygame.draw.circle(screen, YELLOW, pos_scaled, TAXI_RADIUS)

        # Afficher la destination au-dessus du taxi
        if self.destination:
            dest_scaled = (
                int(self.destination[0] * scale),
                int(self.destination[1] * scale),
            )
            text = f"Dest: {dest_scaled[0]}, {dest_scaled[1]}"
            draw_text(screen, text, pos_scaled[0], pos_scaled[1] - 15, WHITE)

    def move(self, destination):
        dx = destination[0] - self.position[0]
        dy = destination[1] - self.position[1]
        distance = (dx**2 + dy**2) ** 0.5
        if distance < self.speed:   # Si la distance est inférieure à la vitesse, on atteint la destination
            self.position = destination
            self.destination = None
        else:
            self.position = (
                    self.position[0] + (dx / distance) * self.speed,
                    self.position[1] + (dy / distance) * self.speed,
                )
            
    def check_task(self, tasks):
        tasks_changed = False

        for task in tasks:
            if task not in self.all_tasks:
                self.all_tasks.append(task)
                tasks_changed = True

        for task in self.all_tasks:
            if task not in tasks or  task.taken:
                self.all_tasks.remove(task)
                tasks_changed = True

        if tasks_changed:
            self.path = self.all_tasks.copy()
            random.shuffle(self.path)



    def update_task(self):
        
        if self.current_task:
            if self.position != self.current_task.end:
                return
            
            self.current_task.complete()
            self.current_task = None
            self.destination = None

        if self.path:
            if self.position == self.path[0].start:
                self.current_task = self.path.pop(0)
                self.current_task.take()
                self.destination = self.current_task.end
                return
            
            self.destination = self.path[0].start
            return
        
        self.destination = (GRID_SIZE // 2, GRID_SIZE // 2)




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