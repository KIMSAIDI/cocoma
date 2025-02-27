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
from negotiation_algo import *

NUM_TASKS = 20
NUM_NEW_TASKS = 5

def main():
    # Initialisation de la fenêtre
    screen = pygame.display.set_mode((WINDOW_SIZE + INFO_PANEL_WIDTH, WINDOW_SIZE))
    pygame.display.set_caption("Simulation de taxis")

    # Génération aléatoire de taxis et de tâches
    taxis = [
        Taxi((random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)), f"T{i+1}")
        for i in range(NUM_TAXIS)
    ]
    # tasks = [
    #     Task(
    #         (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
    #         (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))
    #     )
    #     for i in range(NUM_NEW_TASKS_MIN)
    # ]


    num_groups = NUM_TASKS // NUM_NEW_TASKS

    total_tasks = generate_tasks(num_tasks=NUM_TASKS, num_groups=num_groups, grid_size=GRID_SIZE)
    tasks = []
    current_group = 0

    running = True
    clock = pygame.time.Clock()
    start = time.time()
    step = 0

    # Boucle principale
    while current_group < num_groups + 1 or len(tasks) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dessin de l'environnement
        screen.fill(GREY)

        if step % (T * FPS)  == 0:
            start = time.time()

            print("\nCurrent group: ", current_group)

            new_tasks = total_tasks[current_group * (NUM_TASKS // num_groups): (current_group + 1) * (NUM_TASKS // num_groups)]
            for task in new_tasks:
                tasks.append(task)
            current_group += 1

            available_tasks = [task for task in tasks if not task.taken and not task.allocated]
            psi_auction(taxis, available_tasks)
            # ssi_auction(taxis, available_tasks, "insertion")
            # ssi_auction_with_regret(taxis, available_tasks, "insertion")
            
            print("Waiting time mean: ", Task.waiting_time_sum / Task.nb_tasks)
            print("Waiting time max: ", Task.waiting_time_max)
            print("Waiting time min: ", Task.waiting_time_min)
            print("Total distance: ", sum([taxi.total_distance for taxi in taxis]))


        # Déplacement des taxis
        for taxi in taxis:
            taxi.update()
            taxi.draw(screen)

        # Dessin des tâches
        for task in tasks:
            if task.completed:
                tasks.remove(task)
                continue
            
            task.update()
            task.draw(screen)

        draw_task_allocations(screen, taxis, WINDOW_SIZE)

        pygame.display.flip()
        clock.tick(FPS)
        step += 1

    pygame.quit()


if __name__ == "__main__":
    main()