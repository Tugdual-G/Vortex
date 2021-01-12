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
from sea import sea
import matplotlib.animation as animation
from time import time
            #Paramètres de base de l'affichage

#Temps de modélisation entre chaque image enregistrée
Delta_t_img = 0.05
#taille de l'affichage en pouces
taille = 4

            #Création de l'étendue de fluide "pond".
pond = sea(8, 8, resolution = 150)

            #Création de vortex dans pond.
pond.noise(5)

#pond.vortex( -2.5, 0.7, sens = -1, largeur = 0.01)
#pond.vortex(-2.5, -0.7, sens = 1, largeur = 0.01)
#pond.vortex(1, -1.5 , sens = -0)
#pond.vortex(-3, -1, sens = 0)

#pond.line() crée une ligne de vorticité
pond.line(-3,1,6,10,1)
pond.line(-3,-1,6,10,1)

#Récupération de la grille d'espace.  
X = pond.X()
Y = pond.Y()

#Affichage des conditions initiales.  
plt.subplots(figsize=(taille,taille))
plt.pcolormesh(X,Y,(pond.W()**2)**0.5,cmap = 'viridis', shading='gouraud') 
plt.axis('off')
plt.tight_layout(pad = 0) 
plt.show()
plt.close()

#Que souhaite t-on enregistrer?
gif = False
while True:
    try:
        while True:
            rep_gif = str(input('Enregister format gif? [y/n]:'))
            if rep_gif == 'y':
                gif = True
                break
            elif rep_gif == 'n':
                gif = False
                break
            else:
                print('[y/n]?')

        break
    except ValueError():
        print('Tu fais quoi là !?')

mp4 = False
while True:
    try:
        while True:
            rep_mp4 = str(input('Enregister format mp4? [y/n]:'))
            if rep_mp4 == 'y':
                mp4 = True
                break
            elif rep_mp4 == 'n':
                mp4 = False
                break
            else:
                print('[y/n]?') 

        break
    except ValueError():
        print('Tu fais quoi là !?')   


#temps de simulation
direct = False
while True:
    try:
        while True:
            rep_direct = str(input('Calcul direct sans pause et sans affichage intermédiaire? [y/n]:'))
            if rep_direct == 'y':
                direct = True
                break
            elif rep_direct == 'n':
                direct = False
                break
            else:
                print('[y/n]?')        
        break
    except ValueError():
        print('Tu fais quoi là !?')

if direct == True:   
    while True:
        try:
            t_max = float(input('Temps de simulation en seconde(0 pour sortir).'
                         '\n (Si plus de 5s l\'enregistrement sera très long):'))        
            break
        except ValueError():
            print('Tu fais quoi là !?')
else:
    while True:
        try:
            t_max = float(input('Temps de simulation en seconde avant prochaine pause' 
            '(0 pour sortir). \n Si plus de 5s l\'enregistrement sera très long:'))
            
            break
        except ValueError():
            print('Tu fais quoi là!?')

          

#frames liste les valeurs de la vorticité au cour du temps. 
frames = []
while t_max > 0:
    t0 = time()
    #Résolution de l'équation et stokage des valeurs            
    for i in range(math.ceil(t_max/Delta_t_img)):

        #Vorticity snapshot      
        frames.append(pond.W())
       
        #résolution de l'equation          
        pond.Vortex_solv(tmax = Delta_t_img )
        
        print(i+1,"iterations sur",math.ceil(t_max/Delta_t_img))   
    temps_ex = time()-t0
    #Affichage de l'état de pond après calcul jusqu'au temps demandé.
    plt.subplots(figsize=(taille,taille))
    plt.pcolormesh(X,Y,(pond.W()**2)**0.5,cmap = 'viridis', shading='gouraud')
    plt.axis('off')
    plt.tight_layout(pad = 0)
    if direct == False:
        plt.show()
        plt.close()
    print('temps d\'execution=',round(temps_ex,0),'s') 
    if direct:
        t_max = 0
    else:
        #Repartir pour un tour?     
        t_t = temps_ex/t_max
        print('Temps d\'execution estimé par secondes simulées:',round(t_t,0),'s')
        t_max = float(input('Temps de simulation avant prochaine pause:')) 
        print('Temps d\'execution estimé:',round(t_t*t_max,0),'s')
#Vorticity snapshot      
frames.append(pond.W())


#Préparation de l'affichage pour enregistrement
fig1, ax1 = plt.subplots(figsize=(taille,taille))     
plt.axis('off')
plt.tight_layout(pad = 0)
img = ax1.pcolormesh(X,Y,(pond.W()**2)**0.5, 
                           cmap = 'viridis', shading='gouraud') 

#Fonction permetant de faire défiler les images de la vorticité
def diapo(n):
    global img
    img.remove()
    img = ax1.pcolormesh(X,Y,(frames[n]**2)**0.5, 
                           cmap = 'viridis', shading='nearest') 
    
#Création de l'animation
animator = animation.FuncAnimation(fig1, diapo,
                                   frames=len(frames),
                                   interval=Delta_t_img*1000,
                                   repeat = True)

if mp4:   
    file_name = 'vrtx.mp4'
    animator.save(file_name, dpi=96, writer= 'ffmpeg' )

if gif:   
    file_name = 'vrtx.gif'
    animator.save(file_name, dpi=96, writer= 'ffmpeg' )

