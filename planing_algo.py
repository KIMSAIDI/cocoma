import itertools
import random

from task_class import Task

def random_task_ordering(taxi_pos, tasks):
    ordered_tasks = tasks.copy()
    random.shuffle(ordered_tasks)
    return ordered_tasks

def greedy_task_ordering(taxi_pos, tasks):
    ordered_tasks = []
    current_position = taxi_pos
    remaining_tasks = tasks.copy()
    
    while remaining_tasks:
        closest_task = min(remaining_tasks, key=lambda task: ((task.start[0] - current_position[0])**2 + (task.start[1] - current_position[1])**2)**0.5)
        ordered_tasks.append(closest_task)
        current_position = closest_task.end
        remaining_tasks.remove(closest_task)
    
    return ordered_tasks

def optimal_task_ordering(taxi_pos, tasks):
    best_order = None
    min_distance = float('inf')

    for perm in itertools.permutations(tasks):
        total_distance = 0
        current_position = taxi_pos
        
        for task in perm:
            total_distance += ((task.start[0] - current_position[0])**2 + (task.start[1] - current_position[1])**2) ** 0.5
            total_distance += ((task.end[0] - task.start[0])**2 + (task.end[1] - task.start[1])**2) ** 0.5
            current_position = task.end
        
        if total_distance < min_distance:
            min_distance = total_distance
            best_order = perm
    
    return list(best_order) if best_order else []