import yaml
import math

def generate_yaml_file(taxis, tasks, task_cost, name_file):
    with open(name_file, 'w') as f:
        f.write('name: Taxi Task Allocation Problem\n')
        f.write('objective: min\n')
        f.write('\n')

        # Domaines
        f.write('domains:\n')
        f.write('  taxis:\n')
        f.write('    values:\n')
        for taxi in taxis:
            f.write(f'      - {taxi.name}\n')
        f.write('\n')

        # Variables
        f.write('variables:\n')
        for task in tasks:
            f.write(f'  {task.name}:\n')
            f.write('    domain: taxis\n')
        f.write('\n')

        # Contraintes de préférence (coût)
        f.write('constraints:\n')
        for i, task in enumerate(tasks):
            f.write(f'  pref_{i + 1}:\n')
            f.write('    type: extensional\n')
            f.write(f'    variables: {task.name}\n')
            f.write('    values:\n')
            for j, taxi in enumerate(taxis):
                cost = task_cost[taxi][i]  # Coût pour ce taxi et cette tâche
                f.write(f'      {cost}: {taxi.name}\n')
            f.write('\n')

        # Contraintes pour éviter que deux tâches soient assignées au même taxi
        for i, task1 in enumerate(tasks):
            for j, task2 in enumerate(tasks):
                if i < j:
                    f.write(f'  different_{task1.name}_{task2.name}:\n')
                    f.write('    type: intention\n')
                    f.write(f'    function: 1000 if {task1.name} == {task2.name} else 0\n')
                    f.write('\n')

        # Contraintes de coût pour chaque taxi
        for i, taxi in enumerate(taxis):
            f.write(f'  cout_{taxi.name}:\n')
            f.write('    type: intention\n')
            f.write(f'    function: {task_cost[taxi][0]} if {tasks[0].name} == "{taxi.name}"')
            for j in range(1, len(tasks)):
                f.write(f' else {task_cost[taxi][j]} if {tasks[j].name} == "{taxi.name}"')
            f.write(' else 0\n')
            f.write('\n')

        # Agents
        f.write('agents:\n')
        for task in tasks:
            f.write(f'  {task.name}:\n')
            f.write('    capacity: 1\n')
    
    
    
    
def calculate_cost(position, task):
    # position est la position du taxi et task est la position de DEPART de la tache
    return math.sqrt((position[0] - task[0])**2 + (position[1] - task[1])**2)