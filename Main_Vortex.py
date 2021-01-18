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
import numpy as np
import matplotlib.animation as animation
from time import time
            #Paramètres de base de l'affichage

#uwall est la vitesse du fluide au contact du bord supérieur et inférieur
u_t_wall = -1
u_b_wall = 1
#viscosité
nu_fluide= 15.6*10**-5
#Temps de modélisation entre chaque image enregistrée
Delta_t_img = 0.1
#Apparence de l'affichage "nearest" pour pixels, "gouraud" pour lisse.
shade = "gouraud"
#None veut dire que les couleurs sont normalisés à chaque image.
W_max = None

while True:
    try:
        while True:
            rep_hd = str(input('calcul haute résolution ? [y/n] :'))
            if rep_hd == 'n':
                reso = 120
                delt = 0.0001
                conv = 0.0001
                taille = 4
                break
            elif rep_hd == 'y':
                reso = 400
                delt = 0.0001
                conv = 0.0001
                taille = 12
                break
            else:
                print('[y/n]?')

        break
    except TypeError:
        print('Tu fais quoi là !?')

            #Création de l'étendue de fluide "pond".
pond = sea(reso, 8.0, 8.0)
            #Création de vortex dans pond.
            

pond.rand(20)
pond.noise(15)
#pond.line() crée une ligne de vorticité
#pond.line(-2,0.5,4,50,0.04)
#pond.line(-2,-0.5,4,50,0.04)

#pond.vortex( -1, 0.7, sens = 30, largeur = 3)
#pond.vortex( -1, -0.7, sens = -30, largeur = 3)
#pond.vortex( -2.5, 0.7, sens = 30, largeur = 3)
#pond.vortex( -2.5, -0.7, sens = -30, largeur = 3)


#résolution de l'equation affin d'initialiser
pond.Vortex_solv(tmax = 0.001, dt = delt, delta_convgce = conv,
		nu = nu_fluide, t_wall= u_t_wall, b_wall= u_b_wall)
W_max = np.amax(pond.W()[2:pond.qy()-2, 2:pond.qx()-2])
#Récupération de la grille d'espace.  
X = pond.X()
Y = pond.Y()


#Affichage des conditions initiales.
print('Patientez...') 
plt.subplots(figsize=(taille,taille))
plt.pcolormesh(X,Y, (pond.W()**2)**0.5,cmap = 'viridis', shading= shade, vmax = W_max) 
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
    except TypeError:
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
    except TypeError:
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
    except TypeError:
        print('Tu fais quoi là !?')

if direct == True:   
    while True:
        try:
            t_max = float(input('Temps de simulation en secondes (0 = Exit):'))
       
            break
        except ValueError:
            print('Tu fais quoi là !?')
else:
    while True:
        try:
            t_max = float(input('Temps de simulation en seconde avant prochaine pause (0 = Exit):'))
            
            break
        except ValueError:
            print('Tu fais quoi là!?')

moyenne = 0
somme_t_ex = 0
somme_t = 0         
#frames liste les valeurs de la vorticité au cour du temps. 
frames = []
it = 0
while t_max > 0:
    somme_t += t_max
    erreur = 0
    it += 1
    t0 = time()
    #Résolution de l'équation et stokage des valeurs            
    for i in range(math.ceil(t_max/Delta_t_img)):
        
        if gif or mp4:
            frames.append(np.round(pond.W(),9))

        #résolution de l'equation
        erreur += pond.Vortex_solv(tmax = Delta_t_img,
                         dt = delt, delta_convgce = conv, nu = nu_fluide,
                         t_wall= u_t_wall, b_wall= u_b_wall)

        print(i+1,"iterations sur",math.ceil(t_max/Delta_t_img)) 
    temps_ex = time()-t0
    somme_t_ex += temps_ex
    print('temps d\'execution=',round(temps_ex,2),'s') 
    moyenne = somme_t_ex/somme_t
    print('temps moyen d\'execution par secondes simulées:', round(moyenne,3))
    #Affichage de l'état de pond après calcul jusqu'au temps demandé.
    plt.subplots(figsize=(taille,taille))
    plt.pcolormesh(X,Y, (pond.W()**2)**0.5, cmap = 'viridis', shading = shade , vmax = W_max)
    plt.axis('off')
    plt.tight_layout(pad = 0)
    print('temps final simulé : ', round(somme_t,2))
    print('max vorticité =',np.amax(pond.W()))
    print('max f courant =',np.amax(pond.Phi()))
    print('Arrets forcés cumulées sur phi pour le cycle:', int(erreur))
    if direct == False:
        plt.show()
        plt.close()
    if direct:
        t_max = 0
    else:
        #Repartir pour un tour?     
        t_t = temps_ex/t_max
        print('Temps d\'execution estimé par secondes simulées:',round(t_t,0),'s')
        
        while True:
            try:
                t_max = float(input('Temps de simulation en seconde avant prochaine pause (0 = Exit):'))
                
                break
            except ValueError:
                print('Tu fais quoi là!?')
                
        print('Temps d\'execution estimé:',round(t_t*t_max,0),'s')
    
    


#Vorticity snapshot      
frames.append(pond.W())

#Préparation de l'affichage pour enregistrement
fig1, ax1 = plt.subplots(figsize=(taille,taille))     
plt.axis('off')
plt.tight_layout(pad = 0)
img = ax1.pcolormesh(X,Y,(pond.W()**2)**0.5, 
                           cmap = 'viridis', shading= shade, vmax = W_max) 
                            
enr = False
if direct == False and (gif or mp4) :
	#enregistrer?
	enr = False
	while True:
		try:
		    while True:
		        rep_enr = str(input('Enregister? [y/n]:'))
		        if rep_enr == 'y':
		            enr = True
		            break
		        elif rep_enr == 'n':
		            enr = False
		            break
		        else:
		            print('[y/n]?')

		    break
		except TypeError:
		    print('Tu fais quoi là !?')

writer = animation.FFMpegWriter(fps = int(2*1/Delta_t_img), bitrate = 5000)

if enr or (direct and (mp4 or gif)):
	#Fonction permetant de faire défiler les images de la vorticité
	def diapo(n):
		global img
		img.remove()
		img = ax1.pcolormesh(X,Y,(frames[n]**2)**0.5, 
		                       cmap = 'viridis', shading = shade, vmax = W_max) 
		
	#Création de l'animation
	anim = animation.FuncAnimation(fig1, diapo,
		                               frames=len(frames), repeat = True)
	print('Patientez ...')
	if mp4:   
		file_name = 'vortx.mp4'
		anim.save(file_name, writer= writer )

	if gif:   
		file_name = 'vortx.gif'
		anim.save(file_name, writer= 'ffmpeg' )
		
print('FIN')	

