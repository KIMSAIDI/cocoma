import subprocess

# Nombre de répétitions
num_runs = 5

# Chemin vers le fichier à exécuter
script_name = "main_env_part2.py"

# Exécuter le script 'num_runs' fois
for _ in range(num_runs):
    try:
        subprocess.run(["python", script_name], check=True)  # Lancer le script avec Python
        print(f"Exécution réussie de {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_name}: {e}")
