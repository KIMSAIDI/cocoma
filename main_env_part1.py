import os
import pygame
import random
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Initialisation de Pygame
pygame.init()

from Taxi_class import *
from task_class import *
from utils import *


def main():
    # Initialisation de la fenêtre
    screen = pygame.display.set_mode((WINDOW_SIZE + INFO_PANEL_WIDTH, WINDOW_SIZE))
    pygame.display.set_caption("Simulation de taxis")

    # Génération aléatoire de taxis et de tâches
    taxis = [
        Taxi((random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)), f"T{i+1}")
        for i in range(NUM_TAXIS)
    ]
    tasks = [
        Task(
            (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
            (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))
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
                        (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))
                    )
                )

        # Vérifier les tâches disponibles pour chaque taxi
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

        draw_task_allocations(screen, taxis, WINDOW_SIZE)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()