import yaml

def generate_dcop_yaml(taxis, tasks, taxi_costs, filename='partie2.yaml'):
    dcop_data = {
        'name': 'dcop_file',
        'objective': 'min',
        'domains': {
            'taches': {
                'values': tasks
            }
        },
        'variables': {},
        'constraints': [],
        'agents': []
    }

    # les taxis sont les variables avec le domaine des tâches
    for taxi in taxis:
        dcop_data['variables'][taxi] = {
            'domain': 'taches'
        }

    # les contraintes de coût pour chaque taxi
    for idx, taxi in enumerate(taxis):
        # pour ajouter tout les coûts
        cost_data = {
            f'cout{idx + 1}': {
                'type': 'extensional',
                'variables': taxi,
                'values': {}
            }
        }
        # 
        for task, cost in taxi_costs[taxi].items():
            # on ajoutes tout les coûts différents de chaque tâches pour le taxi de la boucle
            cost_data[f'cout{idx + 1}']['values'][cost] = task
        dcop_data['constraints'].append(cost_data)

    # contrainte pour assurer que chaque taxi a sa propre tâche
    if len(taxis) > 1:
        for i in range(len(taxis)):
            for j in range(i + 1, len(taxis)):
                dcop_data['constraints'].append({
                    f'diff_{i+1}_{j+1}': {
                        'type': 'intention',
                        'function': f'10 if {taxis[i]} == {taxis[j]} else 0'
                    }
                })

    # on assigner un agent pour chaque taxi
    for idx, taxi in enumerate(taxis):
        dcop_data['agents'].append(f'a{idx + 1}')

    # Écriture dans un fichier YAML
    with open(filename, 'w') as file:
        yaml.dump(dcop_data, file, default_flow_style=False)

# Exemple d'utilisation
taxis = ['T1', 'T2']
tasks = ['t1', 't2', 't3']
taxi_costs = {
    'T1': {1: 't1', 2: 't2', 3: 't3'},
    'T2': {2: 't1', 0: 't2', 1: 't3'}
}

generate_dcop_yaml(taxis, tasks, taxi_costs)
