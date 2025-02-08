import os
import pygame
import random
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Initialisation de Pygame
pygame.init()

# Paramètres
GRID_SIZE = 200
WINDOW_SIZE = 800
TAXI_RADIUS = 5
FPS = 60
NUM_TAXIS = 3
NUM_NEW_TASKS_MIN = 4
NUM_NEW_TASKS_MAX = 4 # Si <= à NUM_NEW_TASKS_MIN le nombre de tâches générées sera de NUM_NEW_TASKS_MIN
T = 5

# Échelle pour convertir les coordonnées
scale = WINDOW_SIZE / GRID_SIZE

# Couleurs
WHITE = (247, 247, 255)
GREY = (50, 60, 68)
YELLOW = (255, 217, 25)
RED = (199, 0, 57)
GREEN = (76, 173, 139)
BLUE = (57, 88, 146)

# Police pour l'affichage du texte
FONT = pygame.font.Font(None, 24)

from Taxi_class import *
from task_class import *


def main():
    # Initialisation de la fenêtre
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Simulation de taxis")

    # Génération aléatoire de taxis et de tâches
    taxis = [
        Taxi((random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)), f"T{i+1}")
        for i in range(NUM_TAXIS)
    ]
    tasks = [
        Task(
            (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
            (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
            f"t{i+1}"
        )
        for i in range(NUM_NEW_TASKS_MIN)
    ]

    # Boucle principale
    running = True
    clock = pygame.time.Clock()
    start = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dessin de l'environnement
        screen.fill(GREY)

        if time.time() - start > T:
            start = time.time()
            num_new_tasks = random.randint(NUM_NEW_TASKS_MIN, NUM_NEW_TASKS_MAX)
            for _ in range(num_new_tasks):
                tasks.append(
                    Task(
                        (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
                        (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
                        f"t{len(tasks)+1}"
                    )
                )

        for t in taxis:
            available_tasks = [task for task in tasks if not task.taken]
            t.check_task(available_tasks)

        # Déplacement des taxis
        for taxi in taxis:
            taxi.update()
            taxi.draw(screen)

        # Dessin des tâches
        for task in tasks:
            if task.completed:
                tasks.remove(task)
                continue
            
            task.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()