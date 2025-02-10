import pygame

# Paramètres
GRID_SIZE = 200
WINDOW_SIZE = 800
INFO_PANEL_WIDTH = 300
TAXI_RADIUS = 5
FPS = 15
NUM_TAXIS = 5
NUM_NEW_TASKS_MIN = 5
NUM_NEW_TASKS_MAX = 5 # Si <= à NUM_NEW_TASKS_MIN le nombre de tâches générées sera de NUM_NEW_TASKS_MIN
T = 12
NUM_TOTAL_TASKS = 12

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

# Fonction pour dessiner du texte
def draw_text(screen, text, x, y, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_task_allocations(screen, taxis, start_x):
    pygame.draw.rect(screen, GREY, (WINDOW_SIZE, 0, INFO_PANEL_WIDTH, WINDOW_SIZE))  # Fond
    y_offset = 20  # Position du premier texte

    draw_text(screen, "Allocations des Tâches", WINDOW_SIZE + 10, y_offset, WHITE)
    y_offset += 30

    for taxi in taxis:
        draw_text(screen, f"{taxi.name} :", WINDOW_SIZE + 10, y_offset, YELLOW)
        y_offset += 20

        # Affichage de la tâche en cours
        if taxi.current_task:
            draw_text(screen, f"-> t{taxi.current_task.id}", WINDOW_SIZE + 30, y_offset, GREEN)
        else:
            draw_text(screen, "→ Aucune tâche", WINDOW_SIZE + 30, y_offset, RED)
        y_offset += 20

        # Affichage des prochaines tâches (file d'attente)
        if taxi.path:
            draw_text(screen, "Prochaines tâches :", WINDOW_SIZE + 30, y_offset, WHITE)
            y_offset += 20
            task__text = " -> ".join([f"t{task.id}" for task in taxi.path[:5]]) # Afficher au max 5 tâches
            # for task in taxi.path[:3]:  # Afficher au max 3 tâches
            #     draw_text(screen, f"- {task.name}", WINDOW_SIZE + 40, y_offset, BLUE)
            #     y_offset += 20
            draw_text(screen, task__text, WINDOW_SIZE + 40, y_offset, BLUE)
            y_offset += 20
        else:
            draw_text(screen, "Aucune tâche à venir", WINDOW_SIZE + 30, y_offset, RED)

        y_offset += 30  # Espacement entre les taxis

def distance(pos1, pos2):
    return ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2) ** 0.5