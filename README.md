# SnakeMalin


Trop malin ce snake!\
⠀
⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ \
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆ \
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿ \
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀ \
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ \
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ \
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉


### Lancer le Snake ###
Pour lancer le Snake, il faut exécuter la commande python3 main.py, mais nous possédons un ensemble de variables à ajouter pour modifier le fonctionnement de notre application :

-s [score_max] sert à modifier le score maximum auquel on veut s'arrêter, plus le score est haut, plus notre Snake prendra du temps à calculer le chemin au début du lancement de l'application (nous expliquerons pourquoi plus tard)

-t [time_delay_between_each_move] sert à accelerer ou ralentir la vitesse de notre Snake, plus la valeur est petite, plus notre Snake sera rapide

-d sert a debugger notre serpent, cette option n'est pas obligatoire, elle à pour but d'afficher l'ensemble des position où va se déplacer notre Snake

Une commande d'exécution pourra donc ressembler à : python3 main.py -s 50 -t 10 -d

### Fonctionnement de notre IA ###

Pour résoudre le Snake, nous utilisons l'algorithme A*, le principe est d'utiliser une valeur heuristique (distance de Manhattan entre notre tête et la nourriture), ainsi, notre algorithme ne prend pas uniquement en compte le point d'arrivée, mais aussi l'ensemble des possibilités déjà recherchées, utilisant la distance entre le point de départ et d'arrivés comme heuristique. Nous calculons ainsi l'ensemble des chemins possibles et nous retournons le meilleur (le plus court). Ce chemin est stocké sous la forme de tuple qui sont l'ensemble des positions dans laquelle il doit se déplacer, puis nous affichons le résultat. (expliquant le temps de chargement qui peut durer plusieurs secondes)

Notre fonction Astar est disponible dans le ficher Solver.py


De plus, ayant ajouté un type de nourriture, nous faisons en sorte que notre IA choisit la nourriture la plus proche


### Ajout fait dans le jeu ####

Pour augmenter la difficulté, nous avons ajouté la présence de mur, qui sont générés de manière aléatoire au début du jeu, et qui a pour but d'éviter que notre snake fassent uniquement des diagonales ou lignes droite pour atteindre la nourriture, comme il pourrait le faire s'il n'y avait pas de mur.


