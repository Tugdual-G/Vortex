# Vortex
Programme python modélisant l'évolution des vortex dans un fluide.

Méthode basée sur la vorticité et la fonction de courrant, équation de poisson résolue par méthode Gauss-Seidel. L'intégration en temps est réalisée seulon la méthode d'Euler ou Runge-Kutta 4.  

Le fluide et ses propriétés est représenté par la classe "sea". Les méthodes de la classe sea sont basée sur l'équation de la vorticité et la fonction de courant. Le résultat est enregistré en gif ou en mp4. 

Nécessite ffmpeg, numpy, matplotlib, gfortran. Au lancement du programme, des vortex sont générés aléatoirement en tant que conditions initiales. Possibilité de créer des vortex circulaires avec la methode vortex, ou des feuilles de vorticité avec la méthode line. 

Module solveur Euler en fortran à compiler avec la comande:

python3 -m numpy.f2py -c -m solver solver.f90

Module solveur Runge-Kutta 4 en fortran à compiler avec la comande:

python3 -m numpy.f2py -c -m solver solver_rk4.f90

L'ajout de la condition de non-glissement (no_slip = True) sur les bords peut faire dégénérer la simulation si la viscosité est trop basse, une grille d'espace plus fine peut aider également. 
