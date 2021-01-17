# Vortex
Programme python modélisant l'évolution des vortex dans un fluide. Le fluide et ses propriétés est représenté par la classe "sea". Les méthodes de la classe sea sont basée sur l'équation de la vorticité et la fonction de courant. Le résultat est enregistré en gif ou en mp4. Nécessite ffmpeg, numpy, matplotlib. Possibilité de créer des vortex circulaires avec la methode vortex, ou des feuilles de vorticité avec la méthode line. Module solveur en fortran à compiler avec la comande:

python3 -m numpy.f2py -c -m solver solver.f90
