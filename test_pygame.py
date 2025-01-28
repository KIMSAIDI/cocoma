import os
import pygame
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Initialisation de Pygame
pygame.init()

# Paramètres
GRID_SIZE = 200
WINDOW_SIZE = 800
TAXI_RADIUS = 5
FPS = 60
NUM_TAXIS = 5
NUM_NEW_TASKS_MIN = 5
NUM_NEW_TASKS_MAX = 10 # Si <= à NUM_NEW_TASKS_MIN le nombre de tâches générées sera de NUM_NEW_TASKS_MIN
NUM_TASKS = 3

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


# Class des Taxis
class Taxi:

    def __init__(self, position):
        self.position = position
        self.all_tasks = []
        self.path = []
        self.current_task = None
        self.destination = None
        self.speed = 1

    def update(self):
        if self.destination:
            self.move(self.destination)
        else:
            if self.current_task:
                self.destination = self.current_task.end
                self.current_task = None

            else:
                self.update_task()

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

    def set_destination(self, destination):
        self.destination = destination

    def update_task(self):
        if not self.current_task:
            self.current_task = self.path.pop(0)
            self.set_destination(self.current_task.start)


# Class des Tâches
class Task:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5

    def draw(self, screen):
        start_scaled = (int(self.start[0] * scale), int(self.start[1] * scale))
        end_scaled = (int(self.end[0] * scale), int(self.end[1] * scale))
        pygame.draw.circle(screen, GREEN, start_scaled, 3)
        pygame.draw.circle(screen, RED, end_scaled, 3)
        pygame.draw.line(screen, WHITE, start_scaled, end_scaled, 2)


# Fonction pour dessiner du texte
def draw_text(screen, text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))


def main():
    # Initialisation de la fenêtre
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Simulation de taxis")

    # Génération aléatoire de taxis et de tâches
    taxis = [
        Taxi((random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)))
        for _ in range(NUM_TAXIS)
    ]
    tasks = [
        Task(
            (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
            (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)),
        )
        for _ in range(NUM_TASKS)
    ]

    # Boucle principale
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dessin de l'environnement
        screen.fill(GREY)

        for t in taxis:
            if not t.destination:
                task = random.choice(tasks)
                t.set_destination(task.start)

        # Déplacement des taxis
        for taxi in taxis:
            taxi.update()
            taxi.draw(screen)

        # Dessin des tâches
        for task in tasks:
            task.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
