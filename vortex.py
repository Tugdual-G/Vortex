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
from time import time
from os import makedirs
from realtime_display import Plot_sender

# Output path
IMG_OUTPUT = "images_output/"

# Paramètres de base de l'affichage
# Temps de modélisation entre chaque image enregistrée
Delta_t_img = 0.05
# temps de simulation
t_max = 10
# Apparence de l'affichage "nearest" pour pixels, "gouraud" pour lisse.
cmap = "inferno"
# False veut dire que les couleurs sont normalisés à chaque image.
vmax = False

# number of grid points in x and y directions:
reso = 256
# Size of the video in inchs:
taille = 3

# Création de l'étendue de fluide "pond".
pond = sea(reso, 8.0, 8.0)

# uwall est la vitesse du bord supérieur et inférieur de la boite
pond.u_t_wall = 0
pond.u_b_wall = 0
pond.no_slip = False

# time step:
pond.dt = 0.01
# Kinematic viscosity
pond.nu = 0.001

# Création de vortex dans pond.
# Récupération de la grille d'espace.
X = pond.X
Y = pond.Y

# Random vortices
pond.rand(20, L=0.9, N=50)
# pond.noise(50)
# pond.line() crée une ligne de vorticité
# pond.line(-2.5,0.75,5,300,0.04)
# pond.line(-2.5,-0.75,5,300,0.04)

# define vortices
# pond.vortex(-1, 0.7, sens=30, largeur=4)
# pond.vortex(-1, -0.7, sens=-30, largeur=4)
# pond.vortex(-2.5, 0.7, sens=30, largeur=4)
# pond.vortex(-2.5, -0.7, sens=-30, largeur=4)


# temps de simulation
direct = False
while True:
    try:
        while True:
            rep_direct = str(input("Calcul direct sans pause ? [y/n]:"))
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
        print("!?")


moyenne = 0
somme_t_ex = 0
somme_t = 0
# frames liste les valeurs de la vorticité au cour du temps.
frames = [np.abs(pond.W)]
it = 0
pond.Vortex_solv(tmax=pond.dt * 2)
print(f"max stream function = {np.amax(np.abs(pond.Phi))}")
# Initialize the real-time display
splot = Plot_sender(freq=Delta_t_img)
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
        splot.plot_send(pond.W)

        sys.stdout.write(
            "\x1b[2K\r    %i iterations sur %i" % (i, math.ceil(t_max / Delta_t_img))
        )

    temps_ex = time() - t0
    somme_t_ex += temps_ex
    print(f"\ntemps d'execution={temps_ex:.2} s")
    moyenne = somme_t_ex / somme_t
    print(f"temps moyen d'execution par secondes simulées: {moyenne:.2} s")
    # Affichage de l'état de pond après calcul jusqu'au temps demandé.
    print(f"temps final simulé : {somme_t} s ")
    print(f"Arrets forcés convergence phi:{erreur}")
    if direct:
        t_max = 0
    else:
        # Repartir pour un tour?
        t_t = temps_ex / t_max
        while True:
            try:
                t_max = float(
                    input(
                        "Temps de simulation en seconde avant prochaine pause (0 = Exit):"
                    )
                )

                break
            except ValueError:
                print("!?")

        print(f"Temps d'execution estimé: {t_t*t_max:.1} s")

splot.plot_send(pond.W, finished=True)


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
            print("!?")

if direct:
    # Préparation de l'affichage pour enregistrement
    makedirs(IMG_OUTPUT, exist_ok=True)
    fig1, ax1 = plt.subplots(num="animation", figsize=(taille, taille))
    plt.axis("off")
    plt.tight_layout(pad=0)
    nbr = len(frames)
    im = ax1.imshow(frames[0], cmap=cmap)
    for i, frame in enumerate(frames):
        im.set_array(frame)
        fig1.savefig(f"{IMG_OUTPUT}{i:08}.png")
        sys.stdout.write("\x1b[2K\r    %i images enregistrees sur %i" % (i + 1, nbr))


print("\nFIN")
