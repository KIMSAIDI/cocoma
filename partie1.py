# pseudo code pour la partie 1


# params : x -> abcisse de la map
#          y -> ordonnée de la map
#          nb_agents -> nb de taxis (fixe)


# fonction pour placer les agents sur la map au départ
def place_agent(x, y, nb_agents):
    
    # on enregistre la position de chaque agents dans un dico
    position_agents = dict() # de la forme agent = (position_x, position_x)
        
    # on attribut aléatoirement une place pour chaque agent
    for i in range(nb_agents) :
        
        # on choisit une position aléatoire pour l'agent
        position_x = random.randint(0, x -1)
        position_y = random.randint(0, y -1)
         
        
        # si la position est déjà prise par un autre agent, on rechoisit une nouvelle position
        while (position_x, position_y) in position_agents.values() :
            position_x = random.randint(0, x -1)
            position_y = random.randint(0, y -1)
        
        # on l'ajoute au dico
        position_agents[i] = (position_x, position_y) 
    
    # retourne la position de tous les agents
    return position_agents


# fonction pour donner une tâche à chaque agents (on appelera cette fonction dans la fonction principale à chque pas de temps T) 
def donne_tache(agent_et_ses_taches):
    
    # agent_et_ses_taches est un dico avec tous les agents et toutes leur tâches sous la forme d'une liste, (par exemple : agent_et_ses_taches[agent_i] = [(2,1,), (4,0)] )
    for agent, taches in agent_et_ses_taches.items() :
        
        # on leur donne une nouvelle tâche
        position_x = random.randint(0, x -1)
        position_y = random.randint(0, y -1)
        
        # si la position est déjà prise par un autre agent, on rechoisit une nouvelle position
        while (position_x, position_y) in taches :
            position_x = random.randint(0, x -1)
            position_y = random.randint(0, y -1)
        
        taches.append( (position_x, position_y) )
    
    return

# fonction qui avancer en x le taxi tout en vérifiant que la place n'est pas déjà prise par un autre agent
def avance_en_x(position_agents, agent):
    (position_x, position_y) = position_agents[agent]
    
    if (position_x + 1, position_y) in position_agents.values(): 
        # attendre un pas de temps  que ça se débloque----> comment le coder ? 
        pass
    
    else :
        position_agents[agent] = (position_x+1, position_y)
        
    return 

# fonction qui avancer en y le taxi tout en vérifiant que la place n'est pas déjà prise par un autre agent
def avance_en_y(position_agents):
    (position_x, position_y) = position_agents[agent]
    
    if (position_x, position_y + 1) in position_agents.values(): 
        # attendre un pas de temps  que ça se débloque----> comment le coder ? 
        pass
    
    else :
        position_agents[agent] = (position_x, position_y+1)
        
    return  