from task_class import Task
from Taxi_class import Taxi
from utils import *

def bid_for_tasks(taxi, tasks):
    bids = {}
    pos = taxi.position
    if taxi.current_task:
        pos = taxi.current_task.end
    for task in tasks:
        if not task.taken:  # Seules les tâches disponibles sont mises aux enchères
            distance = ((pos[0] - task.start[0])**2 + (pos[1] - task.start[1])**2) ** 0.5
            bids[task] = distance  # L'enchère est basée sur la distance (plus petite = meilleure offre)
    return bids

def bid_for_task(taxi, task, pos):
        distance = ((pos[0] - task.start[0])**2 + (pos[1] - task.start[1])**2) ** 0.5
        return distance

def psi_auction(taxis, tasks):
    # Collecte des enchères de tous les taxis
    all_bids = []
    for taxi in taxis:
        all_bids.append((taxi, bid_for_tasks(taxi, tasks)))

    # Attribution des tâches aux meilleurs enchérisseurs
    task_allocations = {}
    for taxi, bids in all_bids:
        for task, bid in bids.items():
            if task not in task_allocations or bid < task_allocations[task][1]:
                task_allocations[task] = (taxi, bid)

    # Assigner les tâches gagnées
    for task, (winning_taxi, bid) in task_allocations.items():
        if not task.allocated:
            for t in taxis:
                if t.has_task(task):
                    t.remove_task(task)
            winning_taxi.assign_task(task, ordering=True)
            task.allocate()


def ssi_auction(taxis, tasks, heuristic="prim"):
    unassigned_tasks = tasks[:]  # Copie des tâches restantes

    while unassigned_tasks:
        task = unassigned_tasks.pop(0)  # Prend la première tâche disponible
        best_taxi = None
        best_cost = float("inf")

        for taxi in taxis:
            cost = evaluate_cost(taxi, task, heuristic)

            if cost < best_cost:
                best_cost = cost
                best_taxi = taxi

        if best_taxi:
            best_taxi.assign_task(task, ordering=True)  # Assigner la tâche au meilleur taxi
            task.allocate()  # Marquer la tâche comme allouée

def ssi_auction_with_regret(taxis, tasks, heuristic="prim"):
    unassigned_tasks = tasks[:]  # Copie des tâches restantes

    while unassigned_tasks:
        # Calcul des regrets pour chaque tâche
        task_regrets = []

        for task in unassigned_tasks:
            best_taxi, best_cost, second_best_cost = find_best_and_second_best_bid(taxis, task, heuristic)
            regret = second_best_cost - best_cost  # Calcul du regret

            if best_taxi:
                task_regrets.append((task, best_taxi, best_cost, regret))

        # Trier les tâches par regret décroissant
        task_regrets.sort(key=lambda x: x[3], reverse=True)

        if not task_regrets:
            break  # Plus aucune tâche attribuable

        # Prendre la tâche avec le plus grand regret
        selected_task, winning_taxi, best_cost, regret = task_regrets[0]

        # Assigner la tâche au meilleur taxi
        winning_taxi.assign_task(selected_task, ordering=True)
        selected_task.allocate()
        unassigned_tasks.remove(selected_task)



def evaluate_cost(taxi, task, heuristic):
    """
    Évalue le coût d'ajout d'une tâche à un taxi selon l'heuristique choisie.
    """
    if heuristic == "prim":
        return prim_cost(taxi, task)
    elif heuristic == "insertion":
        return insertion_cost(taxi, task)
    else:
        raise ValueError("Heuristique inconnue")

def prim_cost(taxi, task):
    """
    Retourne le coût d'ajout de la tâche selon l'heuristique de Prim.
    """
    if not taxi.path:
        return distance(taxi.position, task.start)
    
    # Cherche la tâche déjà assignée la plus proche de la nouvelle tâche
    min_dist = min(distance(t.start, task.start) for t in taxi.path)
    return min_dist

def insertion_cost(taxi, task):
    """
    Retourne le coût d'ajout de la tâche selon l'heuristique d'insertion.
    """
    if not taxi.path:
        return distance(taxi.position, task.start)  # Si aucune tâche, on prend la distance directe

    best_increase = float("inf")

    for i in range(len(taxi.path) + 1):
        new_path = taxi.path[:i] + [task] + taxi.path[i:]
        cost = taxi.compute_path_cost(new_path)

        if cost < best_increase:
            best_increase = cost

    return best_increase

def find_best_and_second_best_bid(taxis, task, heuristic):
    """
    Trouve le meilleur et le deuxième meilleur taxi pour une tâche donnée.
    
    Retourne :
    - best_taxi : le taxi avec la meilleure offre
    - best_cost : coût de l’offre du meilleur taxi
    - second_best_cost : coût de l’offre du second meilleur taxi
    """
    best_taxi = None
    best_cost = float("inf")
    second_best_cost = float("inf")

    for taxi in taxis:
        cost = evaluate_cost(taxi, task, heuristic)

        if cost < best_cost:
            second_best_cost = best_cost  # L’ancien meilleur devient le second meilleur
            best_cost = cost
            best_taxi = taxi
        elif cost < second_best_cost:
            second_best_cost = cost  # Mise à jour du second meilleur coût

    return best_taxi, best_cost, second_best_cost
