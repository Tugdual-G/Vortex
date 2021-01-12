#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 11:45:13 2021

@author: tugdual
"""
from math import ceil
import numpy as np

class sea():
    """La classe sea modélise une étendue de fluide en 2 dimensions avec comme
    attributs les grilles d'espace X et Y, la vorticité W, 
    la fonction de courant Phi et le pas de la grille h"""
    def __init__(self,L,H,resolution):
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
            self._qy = int(round(H/self._h,0))

        else:
            self._h = H/q
            self._qy = q
            self._qx = int(round(L/self._h,0))
        
        x = np.linspace(-self._xmax, self._xmax,self._qx)
        y = np.linspace(-self._ymax, self._ymax,self._qy)    
        self._X, self._Y = np.meshgrid(x,y)
        self._W = self._X*0
        self._Phi = self._X*0
        self.Poisson()
    
    def W(self):
        return self._W
    def Phi(self):
        return self._Phi
    def X(self):
        return self._X
    def Y(self):
        return self._Y
    
    def vortex(self,x,y,sens):
        """Créé un vortex de coordonnées x et y"""
        if sens != 0:
            R = np.sqrt((self._X-x)**2 + (self._Y-y)**2)
            self._W = self._W + sens/(0.05+R**2)
    def line(self,y,vort):
        """Crée une ligne sur laquelle est concentrée la vorticité,
        une tranche de feuille de vorticité"""
        self._W[y:y+3,100:300] = vort
    
    def noise(self,intensity):
        self._W = self._W + ((np.random.random(self._W.shape) - 
                   np.random.random(self._W.shape)))**5*intensity
     
    def Poisson(self, delta_conv = 0.0001):
        """ Résout l'équation de poisson avec W comme fonction source""" 
        ecart = 1
        qx = self._qx
        qy = self._qy
        #précision de la solution
        while ecart > delta_conv:
            Phi0 = self._Phi
            self._Phi[1:qy-2,1:qx-2] = 0.25*(self._h**2*self._W[1:qx-2,1:qy-2]
                                             + Phi0[2:qx-1,1:qy-2] 
                                             + Phi0[0:qx-3,1:qy-2]
                                             + Phi0[1:qx-2,2:qy-1]
                                             + Phi0[1:qx-2,0:qy-3])
        
            ecart = np.amax(np.abs(self._Phi-Phi0))



    def Vortex_solv(self, tmax=1, dt=0.0001, delta_convgce=0.0001):
        """ Résout l'équation de la vorticité"""
        n_it = ceil(tmax/dt)
        h = self._h
        #résolution de l'equation
        for i in range(n_it):
            gradW_x, gradW_y, = np.gradient(self._W, h)
            gradPhi_x, gradPhi_y = np.gradient(self._Phi, h)   
            #terme d'advection
            advec = gradPhi_x*gradW_y - gradPhi_y*gradW_x
            #solution 
            self._W = self._W + dt* advec 
            #résolution de la fonction de courant, équation de Poisson
            self.Poisson()            

