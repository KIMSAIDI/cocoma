from task_class import Task
from Taxi_class import Taxi

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

def PSI(taxis, tasks):
    # Vérifier les tâches disponibles pour chaque taxi
    for t in taxis:
        available_tasks = [task for task in tasks if not task.taken]
        t.check_task3(available_tasks)

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
            winning_taxi.path.append(task)
            task.allocate()

def SSI(taxis, tasks):
    # Assigner les tâches une par une
    task_allocations = {}
    taxis_positions = {}
    for taxi in tasks:
        if taxi.current_task:
            taxis_positions[taxi] = taxi.current_task.end
        else:
            taxis_positions[taxi] = taxi.position
    
    for task in tasks:
        # Collecte des enchères des taxis disponibles pour la tâche
        all_bids = []
        for taxi in taxis:
            all_bids.append((taxi, bid_for_task(taxi, task, taxis_positions[taxi])))
        
        # Choisir le taxi qui fait la meilleure enchère
        winning_taxi, best_bid = min(all_bids, key=lambda x: x[1])
        
        # Assigner la tâche au meilleur enchérisseur
        task_allocations[task] = (winning_taxi, best_bid)
        
        # Assigner la tâche au taxi gagnant et marquer la tâche comme allouée
        for t in taxis:
            if t.has_task(task):
                t.remove_task(task)
        winning_taxi.path.append(task)
        taxis_positions[winning_taxi] = task.end
        task.allocate()

    # Retourner les attributions
    return task_allocations

# def SSI(taxis, tasks):
#     # Assigner les tâches une par une
#     task_allocations = {}
#     taxis_allocations = {}
#     taxis_positions = {}
#     taxis_procosts = {}
#     for taxi in tasks:
#         if taxi.current_task:
#             taxis_positions[taxi] = taxi.current_task.end
#             taxis_procosts[taxi] = ((pos[0] - task.end[0])**2 + (pos[1] - task.end[1])**2) ** 0.5
#         else:
#             taxis_positions[taxi] = taxi.position
#             taxis_procosts[taxi] = 0

#     for task in tasks:
#         # Collecte des enchères des taxis disponibles pour la tâche
#         all_bids = []
#         for taxi in taxis:
#             all_bids.append((taxi, bid_for_task(taxi, task, taxis_positions[taxi])))
#             for t in taxis_allocations[taxi]:
#                 if t.has_task(task):
#                     all_bids.append((taxi, 0))
#             if taxi not in taxis_allocations:
