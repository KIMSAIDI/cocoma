import pygame
import random

#from main_env import GRID_SIZE, TAXI_RADIUS, scale, WHITE, GREY, YELLOW, RED, GREEN, BLUE, FONT
from utils import *


from planing_algo import random_task_ordering, greedy_task_ordering, optimal_task_ordering
from task_class import Task

# Class des Taxis
class Taxi:

    def __init__(self, position, name):
        self.name = name
        self.position = position
        self.all_tasks = [] # liste de toutes les tâches disponibles
        self.path = [] # liste des tâches à effectuer
        self.current_task = None
        self.destination = None
        self.task_started = False
        self.speed = 1

    def __str__(self):
        return f"Taxi {self.name}"

    def __repr__(self):
        return f"Taxi {self.name}"

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
            if len(self.path) > 0:
                text = f"{self.name}, task: {self.path[0].id}"
            else:
                text = f"{self.name}"
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

        for task in self.all_tasks: # si la tâche n'est plus disponible ou déjà prise
            if task not in tasks or  task.taken:
                self.all_tasks.remove(task)
                tasks_changed = True

        # if tasks_changed:
            # self.path = self.all_tasks.copy()
            # Partie 1
            # self.path = greedy_task_ordering(self.position, self.all_tasks)
            # Partie 3
            # Les tâches sont maintenant attribuées par enchères

    def check_task3(self, tasks):
        self.path = optimal_task_ordering(self.position, self.path)

    def has_task(self, task):
        return task in self.path

    def remove_task(self, task):
        self.path.remove(task)

    def update_task(self):
        
        if self.current_task: # si le taxi a une tâche en cours
            if self.position != self.current_task.end: # si le taxi n'est pas encore arrivé à la fin
                return
            
            self.current_task.complete()
            self.current_task = None
            self.destination = None

        if self.path: # si le taxi a une liste de tâches
            if self.position == self.path[0].start and not self.path[0].taken: # si le taxi est à la position de départ de la tâche et que la tâche n'est pas prise
                self.current_task = self.path.pop(0) # on remove la tâche de sa liste
                self.current_task.take()
                self.destination = self.current_task.end # on met la destination à la fin de la tâche
                return
            
            self.destination = self.path[0].start # sinon on met la destination à la position de départ de la tâche
            return
        
        # Si le taxi n'a plus de tâche à effectuer
        x_noise = random.uniform(-0.5, 0.5)
        y_noise = random.uniform(-0.5, 0.5)
        # self.destination = (GRID_SIZE // 2 + x_noise, GRID_SIZE // 2 +  y_noise)
        # self.destination = (self.position[0] + x_noise, self.position[1] + y_noise)

    
