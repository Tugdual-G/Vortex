# Vortex
**Dynamique des vortex**

Calcul et visualisation en temps réel de la dynamique d'un fluide.

Ce programme est un premier essais assez naif et daté. Une remise en forme du code, un passage en volume fini et l'utilisation d'un solveur multigrilles seraient nécesaire, cela dit, le principe est simple et intuitif pour une premiere approche. 

<img src="vortex.gif" align="center" width="33%"></img>

Possibilité de remplir le domaine de vortex générés aléatoirements.

Méthode basée sur la vorticité et la fonction de courrant, équation de poisson résolue par méthode Gauss-Seidel. L'intégration en temps est réalisée selon la méthode d'Euler ou Runge-Kutta 4.  

Le fluide et ses propriétés est représenté par la classe "sea". Les méthodes de la classe sea sont basée sur l'équation de la vorticité et la fonction de courant.

## Méthode
La vorticité est définie comme $\omega = \nabla \times u$, cette quatité décrit le cisaillement et la rotation locale d'un volume infinitésimal de fluide.

Pour un fluide de densité et viscosité constante en 3 dimensions,
$$\nabla \times \left( \frac{D u}{D t} = -\frac{1}{\rho} \nabla p + g + \nu \nabla^2 u \right)$$
$$\implies \frac{D \omega}{D t} = \left( \omega \cdot \nabla \right) u + \nu \nabla^2 \omega$$

Dans un flux en 2 dimensions, les lignes de vorticité ne peuvent pas être étirées et la vorticité doit se conserver, l'équation prend alors la forme d'une équation d'advection-diffusion non-linéaire,
$$\frac{D \omega}{D t} = \nu \nabla^2 \omega$$

On utilise ensuite la fonction de courant $\psi$ pour résoudre l'équation. 
$\psi$ est definie comme potentiel vecteur tel que,
$$u = \nabla \times \psi$$
 La fonction de courant permet de définir le flux total passant au travers d'une courbe.

## Prérequis
Nécessite python 3, numpy, et matplotlib. Au lancement du programme, des vortex sont générés aléatoirement en tant que conditions initiales. Possibilité de créer des vortex circulaires avec la methode vortex, ou des feuilles de vorticité avec la méthode line. 

## Utilisation 

Lancement de la simulation:

    python vortex.py

**Note**

Si besoin, module solveur Euler en fortran à compiler avec la comande:

    python3 -m numpy.f2py -c -m solver solver.f90

Module solveur Runge-Kutta 4 en fortran à compiler avec la comande:

    python3 -m numpy.f2py -c -m solver solver_rk4.f90

L'ajout de la condition de non-glissement (no_slip = True) sur les bords peut faire dégénérer la simulation si la viscosité est trop basse, une grille d'espace plus fine peut aider également. 
