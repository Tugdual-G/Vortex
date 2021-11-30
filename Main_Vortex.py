# -*- coding: utf-8 -*-
"""
Modélisation de vortex dans une boite fermée.
Affiche l'état initial et final. Peut enregistrer les images 
de la modélisation dans le répertoire courant.

Created on Sun Nov 29 21:03:33 2020
@author: tugdual
"""
import matplotlib.pyplot as plt
import math
import sys
from sea import sea
import numpy as np
import matplotlib.animation as animation
from time import time

# img = mpimg.imread('/home/tugdual/Documents/Programmation/vortex/Vortex_random_FFMpegWriter/manu.png')
# img = np.flipud(img[:,:,0])

# Paramètres de base de l'affichage
# Temps de modélisation entre chaque image enregistrée
Delta_t_img = 0.02
# Apparence de l'affichage "nearest" pour pixels, "gouraud" pour lisse.
shade = "gouraud"
cmap = "viridis"
# False veut dire que les couleurs sont normalisés à chaque image.
vmax = False

# number of grid points in x and y directions:
reso = 128
# Size of the video in inchs:
taille = 3

# Création de l'étendue de fluide "pond".
pond = sea(reso, 8.0, 8.0)

# uwall est la vitesse du bord supérieur et inférieur de la boite
pond.u_t_wall = 0
pond.u_b_wall = 0
pond.no_slip = False

# time step:
pond.dt = 0.0001

# Création de vortex dans pond.
# Récupération de la grille d'espace.
X = pond.X
Y = pond.Y

pond.rand(20, L=0.9, N=50)
# pond.noise(50)
# pond.line() crée une ligne de vorticité
# pond.line(-2.5,0.75,5,300,0.04)
# pond.line(-2.5,-0.75,5,300,0.04)

pond.vortex(-1, 0.7, sens=30, largeur=4)
pond.vortex(-1, -0.7, sens=-30, largeur=4)
pond.vortex(-2.5, 0.7, sens=30, largeur=4)
pond.vortex(-2.5, -0.7, sens=-30, largeur=4)


# w_max permet de niveller la teinte de l'affichache
W_max = None
if vmax:
    W_max = np.amax(pond.W()[2 : pond.qy - 2, 2 : pond.qx - 2]) * 1.4

# Affichage des conditions initiales.
print("Patientez...")
plt.figure("glimpse", figsize=(taille, taille))
plt.clf()
plt.pcolormesh(X, Y, pond.W, cmap=cmap, shading=shade, vmax=W_max)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show(block=False)
plt.pause(1)
plt.close()


# temps de simulation
direct = False
while True:
    try:
        while True:
            rep_direct = str(
                input(
                    "Calcul direct sans pause et sans affichage intermédiaire? [y/n]:"
                )
            )
            if rep_direct == "y":
                direct = True
                break
            elif rep_direct == "n":
                direct = False
                break
            else:
                print("[y/n]?")
        break
    except TypeError:
        print("Tu fais quoi là !?")

if direct == True:
    while True:
        try:
            t_max = float(input("Temps de simulation en secondes (0 = Exit):"))

            break
        except ValueError:
            print("Tu fais quoi là !?")
else:
    while True:
        try:
            t_max = float(
                input(
                    "Temps de simulation en seconde avant prochaine pause (0 = Exit):"
                )
            )

            break
        except ValueError:
            print("Tu fais quoi là!?")

#%%
moyenne = 0
somme_t_ex = 0
somme_t = 0
# frames liste les valeurs de la vorticité au cour du temps.
frames = [np.abs(pond.W)]
it = 0
while t_max > 0:
    somme_t += t_max
    erreur = 0
    it += 1
    t0 = time()
    # Résolution de l'équation et stokage des valeurs
    for i in range(math.ceil(t_max / Delta_t_img)):

        # résolution de l'equation
        erreur += pond.Vortex_solv(tmax=Delta_t_img)

        # Utilliser .copy() pour ne pas stoker des arrays mutables
        frames += [np.abs(pond.W)]

        sys.stdout.write(
            "\x1b[2K\r    %i iterations sur %i" % (i, math.ceil(t_max / Delta_t_img))
        )

    temps_ex = time() - t0
    somme_t_ex += temps_ex
    print("\ntemps d'execution=", round(temps_ex, 2), "s")
    moyenne = somme_t_ex / somme_t
    print("temps moyen d'execution par secondes simulées:", round(moyenne, 3))
    # Affichage de l'état de pond après calcul jusqu'au temps demandé.
    print("temps final simulé : ", round(somme_t, 2))
    print("max vorticité =", np.amax(pond.W))
    print("max f courant =", np.amax(pond.Phi))
    print("Arrets forcés convergence de phi pour le cycle:", int(erreur))
    if direct == False:
        plt.figure("glimpse", figsize=(taille, taille))
        plt.clf()
        plt.pcolormesh(X, Y, pond.W, cmap=cmap, shading=shade, vmax=W_max)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
        plt.close()
    if direct:
        t_max = 0
    else:
        # Repartir pour un tour?
        t_t = temps_ex / t_max
        print("Temps d'execution estimé par secondes simulées:", round(t_t, 0), "s")

        while True:
            try:
                t_max = float(
                    input(
                        "Temps de simulation en seconde avant prochaine pause (0 = Exit):"
                    )
                )

                break
            except ValueError:
                print("Tu fais quoi là!?")

        print("Temps d'execution estimé:", round(t_t * t_max, 0), "s")


if direct == False:
    while True:
        try:
            while True:
                rep_enr = str(input("Enregister images? [y/n]:"))
                if rep_enr == "y":
                    direct = True
                    break
                elif rep_enr == "n":
                    direct = False
                    break
                else:
                    print("[y/n]?")

            break
        except TypeError:
            print("Tu fais quoi là !?")

if direct:
    # Préparation de l'affichage pour enregistrement
    fig1, ax1 = plt.subplots(num="animation", figsize=(taille, taille))
    plt.axis("off")
    plt.tight_layout(pad=0)
    nbr = len(frames)
    for i, frame in enumerate(frames):
        ax1.pcolormesh(X, Y, frame, cmap=cmap, shading=shade, vmax=W_max)
        fig1.savefig(f"images_output/{i:08}.png")
        sys.stdout.write("\x1b[2K\r    %i images enregistrees sur %i" % (i, nbr))


print("\nFIN")
