# Vortex
**Dynamique des vortex**

Ce programme est un premier essais assez naif et daté. Une remise en forme du code et un passage en volume fini seraient nécesaires, cela dit il reste instructif pour une premiere approche. 

<img src="vortex.gif" align="center" width="25%"></img>

Possibilité de remplir le domaine de vortex générés aléatoirements.

Méthode basée sur la vorticité et la fonction de courrant, équation de poisson résolue par méthode Gauss-Seidel. L'intégration en temps est réalisée selon la méthode d'Euler ou Runge-Kutta 4.  

Le fluide et ses propriétés est représenté par la classe "sea". Les méthodes de la classe sea sont basée sur l'équation de la vorticité et la fonction de courant.

## Prérequis
Nécessite numpy, matplotlib, gfortran. Au lancement du programme, des vortex sont générés aléatoirement en tant que conditions initiales. Possibilité de créer des vortex circulaires avec la methode vortex, ou des feuilles de vorticité avec la méthode line. 

## Utilisation 
Module solveur Euler en fortran à compiler avec la comande:

    python3 -m numpy.f2py -c -m solver solver.f90

Module solveur Runge-Kutta 4 en fortran à compiler avec la comande:

    python3 -m numpy.f2py -c -m solver solver_rk4.f90

L'ajout de la condition de non-glissement (no_slip = True) sur les bords peut faire dégénérer la simulation si la viscosité est trop basse, une grille d'espace plus fine peut aider également. 
