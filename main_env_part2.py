import os
import pygame
import random
import time
import yaml
import subprocess
import json


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
pygame.init()

# Paramètres
GRID_SIZE = 200
WINDOW_SIZE = 800
TAXI_RADIUS = 5
FPS = 60
NUM_TAXIS = 3
NUM_NEW_TASKS_MIN = 3
NUM_NEW_TASKS_MAX = 3
NUM_TOTAL_TASKS = 6
T = 8
MAX_UNASSIGNED_TASKS = 10  # Limite le nombre de tâches non prises
scale = WINDOW_SIZE / GRID_SIZE


# Couleurs
WHITE = (247, 247, 255)
GREY = (50, 60, 68)
YELLOW = (255, 217, 25)
RED = (199, 0, 57)
GREEN = (76, 173, 139)
BLUE = (57, 88, 146)

# Police
FONT = pygame.font.Font(None, 24)

#from Taxi_class import *
from task_class import *
from generate_yaml import *
from pydcop.algorithms import dsa
from pydcop.dcop.yamldcop import *


# Fonction pour dessiner du texte
def draw_text(screen, text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Class des Taxis
class Taxi2:

    def __init__(self, position, name, path):
        self.name = name
        self.position = position
        self.path = path # liste des tâches à effectuer
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
        self.destination = (GRID_SIZE // 2 + x_noise, GRID_SIZE // 2 +  y_noise)
        # self.destination = (self.position[0] + x_noise, self.position[1] + y_noise)




# fonction qui appel generate_file_yaml et assigner les nouvelles tâches au taxis
def assign_tasks(taxis, tasks, task_cost):
    
    generate_yaml_file(taxis, tasks, task_cost, "dcop.yaml")
    
    with open("dcop.yaml", "r", encoding="utf-8") as f:
        dcop_str = f.read()  # Lire le contenu du fichier

    dcop = load_dcop(dcop_str=dcop_str, main_dir="yaml")
    
    try:
        result = subprocess.run(
            ["pydcop", "solve", "--algo", "dpop", "dcop.yaml"],
            capture_output=True, text=True, check=True
        )
        str_results = result.stdout
        
        try:
            results_dict = json.loads(str_results)
            assignments = results_dict.get("assignment", {})
           
            # Assigner les tâches aux taxis
            for taxi in taxis:
                for task_name, taxi_name in assignments.items():
                    if taxi_name == taxi.name:
                        for task in tasks:
                            if task.name == task_name:
                                taxi.path.append(task)
                                
                                break
              
            
        except json.JSONDecodeError as e:
            print("Erreur lors de la conversion de la sortie en JSON :", e)
            print("Sortie brute de pydcop :", str_results)
        
        
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'exécution de pydcop solve :", e)
        print("Sortie d'erreur :", e.stderr)
                
    

def main():
    # Initialisation de la fenêtre
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Simulation de taxis")
    
    
    
    # Génération aléatoire de taxis et de tâches
    taxis = [
        Taxi2((random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)), f"T{i+1}", []) # liste de path à vide au début
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
    
    all_tasks_count = NUM_NEW_TASKS_MIN

    # Boucle principale
    running = True
    task_cost = {}
    clock = pygame.time.Clock()
    start = time.time()
    
    # pour chaque taxi, on calcul le coùut associé à chaque tâche
    for taxi in taxis:
        task_cost[taxi] = []
        for task in tasks:
            task_cost[taxi].append(calculate_cost(taxi.position, task.start))

    
    # assignement taxi au tasks
    assign_tasks(taxis, tasks, task_cost)
    # on remet à 0 le calcul des couts des taches
    task_cost = {}
    
    # pour s'assurer que les taches ont toutes des noms différents
    task_counter = len(tasks) + 1
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        
        # Dessin de l'environnement
        screen.fill(GREY)
        
        
        if time.time() - start > T :
            start = time.time()
            num_new_tasks = random.randint(NUM_NEW_TASKS_MIN, NUM_NEW_TASKS_MAX)
            new_task = []
            for i in range(num_new_tasks):
                task_name = f"t{task_counter}"

                new_task.append(
                    Task(
                        (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
                        (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
                        # on s'assure que les noms sont uniques et avec compteur
                        task_name

                    )
                )
                all_tasks_count += 1
              
                tasks.append(new_task[i])
                task_counter += 1 
            
                
            # pour chaque taxi, on calcul le coùut associé à chaque NOUVELLE tâche
            for taxi in taxis:
                task_cost[taxi] = []
                for task in new_task:
                    task_cost[taxi].append(calculate_cost(taxi.position, task.start))

            # on assigne une nouvelle tâche aux taxis qui n'ont pas de current task
            assign_tasks(taxis, new_task, task_cost)
            task_cost = {}
            
            
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
            
        if all_tasks_count == NUM_TOTAL_TASKS and tasks == []:
            end_time = time.time()
            print(f"Temps total de résolution: {end_time - start:.2f} secondes")
            running = False

        pygame.display.flip()
        clock.tick(FPS)
        
        

    pygame.quit()


if __name__ == "__main__":
    main()

