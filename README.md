# Vortex
**Dynamique des vortex**

Calcul et visualisation en temps réel de la dynamique d'un fluide.

Ce programme est un premier essais mettant en oeuvre une description du fluide basée sur la vorticité et la fonction de courant.
Cette description est dérivée rigoureusement des équation de la mécanique des fluide et n'introduit pas d'approximation supplémentaires. 
Dans ce programme, un schéma numérique en différences finies est utilisé pour discrétiser les opérateurs spatiaux affin de limiter la complexité d'implémentation au maximum.

Un passage en volume fini et l'utilisation d'un solveur multigrilles seraient nécessaire pour obtenir plus de stabilité et de rapidité.
cela dit, le principe est simple et intuitif numériquement pour une première approche. 

<img src="vortex.gif" align="center" width="33%"></img>



## Méthode
La méthode est basée sur la vorticité et la fonction de courant.

La vorticité est définie comme $\bm{\omega} = \nabla \times \bm{u}$, cette quantité décrit le cisaillement et la rotation locale d'un volume infinitésimal de fluide.

Pour un fluide de densité et viscosité constante en trois dimensions,
$$\nabla \times \left( \frac{D \bm{u}}{D t} = -\frac{1}{\rho} \nabla p + \bm{g} + \nu \nabla^2 \bm{u} \right)$$
$$\implies \frac{D \bm{\omega}}{D t} = \nabla \bm{u} \bm{\omega} + \nu \nabla^2 \bm{\omega}$$

Dans un flux en deux dimensions, les lignes de vorticité ne peuvent pas être étirées et la vorticité doit se conserver, l'équation prend alors la forme d'une équation d'advection-diffusion non-linéaire,
$$\frac{D \omega}{D t} = \nu \nabla^2 \omega$$
du point de vue Eulerien,
$$\frac{\partial \omega}{\partial t} + \nabla \omega \bm{u} =  \nu \nabla^2 \omega$$

On utilise ensuite la fonction de courant $\psi$ pour résoudre l'équation. 
$\psi$ est définie comme potentiel vecteur tel que,
$$\bm{u} = \nabla \times \bm{\psi}$$

L'équation de la vorticité en deux dimensions peut se reformuler comme,
$$\frac{\partial \omega}{\partial t}  =  - u \frac{\partial \omega}{\partial x} + v \frac{\partial \omega}{\partial y} \nu \nabla^2 \omega$$
On dispose également de la relation, 
$$\omega = - \nabla^2 \psi$$
Avec les conditions aux limites du domaine ainsi que des conditions initiales on obtient enfin un problème traitable numériquement. 

Il nous faudra donc a chaque pas de temps,
- Résoudre l'équation de Poisson $\omega = - \nabla^2 \psi$
- Calculer le membre de droite (ici en différences finies)
- Intégrer en temps 

L'équation de poisson résolue par méthode Gauss-Seidel. L'intégration en temps peut être réalisée selon la méthode d'Euler ou Runge-Kutta 4.

## Prérequis
- matplotlib
- numpy
- meson
- ninja

        python -m venv .venv ; source .venv/bin/activate; pip install -r requirements.txt 

## Compilation des solveurs
Module solveur Euler en fortran à compiler avec la commande:

    python3 -m numpy.f2py -c -m solver solver.f90

Module solveur Runge-Kutta 4 en fortran à compiler avec la commande:

    python3 -m numpy.f2py -c -m solver solver_rk4.f90

## Utilisation 

Lancement de la simulation:

    python vortex.py

Au lancement du programme, des vortex sont générés aléatoirement en tant que conditions initiales.
Il est possible de créer des vortex circulaires avec la méthode vortex, ou des feuilles de vorticité avec la méthode line. 

Le fluide et ses propriétés est représenté par la classe "sea". 

**Note**

L'ajout de la condition de non-glissement (no_slip = True) sur les bords peut faire dégénérer la simulation si la viscosité est trop basse, une grille d'espace plus fine peut aider également. 
