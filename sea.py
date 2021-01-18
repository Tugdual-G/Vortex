# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 11:45:13 2021

@author: tugdual
"""
import numpy as np
from math import floor, ceil
from solver import jellyfish
from random import uniform 
#print(jellyfish.__doc__)

class sea():
    """La classe sea modélise une étendue de fluide en 2 dimensions avec comme
    attributs les grilles d'espace X et Y, la vorticité W, 
    la fonction de courant Phi et le pas de la grille h"""
    def __init__(self, resolution, L = float(),H  =float()):
        self._xmax = L/2
        self._ymax = H/2
        q = resolution
        #définition du pas de la grille, h.
        #On prend en compte la possible diférence entre L et H,
        # pas forcément très utile comme fonctionnalité
        if L == H:
            self._h = L/q
            self._qx = q
            self._qy = q
        elif L > H:
            self._h = L/q
            self._qx = q
            self._qy = int(H/self._h,0)

        else:
            self._h = H/q
            self._qy = q
            self._qx = int(L/self._h,0)
        
        x = np.linspace(-self._xmax, self._xmax,self._qx)
        y = np.linspace(-self._ymax, self._ymax,self._qy)    
        self._X, self._Y = np.meshgrid(x,y)
        self._W = self._X*0
        self._Phi = self._X*0
        
        i_range = self._qy - 2
        j_range = self._qx - 2
        
        slct_grid = np.mgrid[0:i_range,0:j_range]+1 
        
        i_space = slct_grid[0,:,:]
        j_space = slct_grid[1,:,:]
        
        self._i = i_space.reshape((1,j_range*i_range))[0,:]
        self._j = j_space.reshape((1,j_range*i_range))[0,:]            
    
    
    def W(self):
        return self._W
    def Phi(self):
        return self._Phi
    def X(self):
        return self._X
    def Y(self):
        return self._Y
    def H(self):
        return self._h
    def qx(self):
        return self._qx
    def qy(self):
        return self._qy
    
    def vortex(self,x,y,sens,largeur=0.1):
        """Créé un vortex de coordonnées x et y"""
        if sens != 0:
            R = np.sqrt((self._X-x)**2 + (self._Y-y)**2)
            self._W = self._W + sens*10*np.exp(-R**2*100/(largeur)) # sens*largeur*100/(largeur+R**2)
    
    def line(self,x=-0.5,y=0,L=1,vort=10, e=2):
        """Crée une ligne sur laquelle est concentrée la vorticité,
        une tranche de feuille de vorticité"""
        x1 = floor(self._qx/2+ x*self._qx/(2*self._xmax))
        l = floor(L*self._qx/(2*self._xmax))
        y1 = floor(self._qy/2 + y*self._qy/(2*self._xmax))
        e = e*self._qy/(4*self._ymax)
        e = ceil(e)
        self._W[y1+e:y1+e+1,x1:x1+l-1] = vort/2 #+ self._W[y1+e:y1+e+1,x1:x1+l-1]
        self._W[y1-e:y1+e,x1:x1+l-1] = vort #+ self._W[y1-e:y1+e,x1:x1+l-1]
        self._W[y1-e-1:y1,x1:x1+l-1] = vort/2# + self._W[y1-e-1:y1,x1:x1+l-1]
        self._W[y1-e:y1+e,x1-1] = vort/2 #+ self._W[y1-e:y1+e,x1-1]
        self._W[y1-e:y1+e,x1+l-1] = vort/2 #+ self._W[y1-e:y1+e,x1+l-1]
        
    def noise(self,intensity):
        self._W = self._W + ((np.random.random(self._W.shape) - 
                   np.random.random(self._W.shape)))**7*intensity
     
    def rand(self, intensity):
        for i in range(7):
            x = uniform(-self._xmax*0.7, self._xmax*0.7)
            y = uniform(-self._ymax*0.7, self._ymax*0.7)
            largeur = uniform(1,20)
            if largeur > 8: 
                sens = uniform(-(intensity)**0.7,intensity**0.7)
            else:
                sens = uniform(-intensity,intensity)
            self.vortex( x, y, sens, largeur)
        for i in range(4):
            x = uniform(-self._xmax*0.7, self._xmax*0.7)
            y = uniform(-self._ymax*0.7, self._ymax*0.7)
            largeur = uniform(1,8)
            sens = uniform(-intensity**0.9,intensity**0.9)
            self.vortex( x, y, sens, largeur)
        


    def Vortex_solv(self, tmax=1, dt=0.0001, delta_convgce=0.0001, nu = 0,
                    t_wall=0, b_wall=0):
        erreur = 0
        """ Résout l'équation de la vorticité"""     
        self._W, self._Phi, erreur = jellyfish(self._W, self._Phi, tmax, dt,
                                          self._h, delta_convgce, nu,
                                          t_wall ,b_wall, erreur)
        return erreur
    



