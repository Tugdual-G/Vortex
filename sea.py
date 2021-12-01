# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 11:45:13 2021

@author: tugdual
"""
import numpy as np
from math import floor, ceil
from solver import jellyfish
from random import uniform

# print(jellyfish.__doc__)


class sea:
    """La classe sea modélise une étendue de fluide en 2 dimensions avec comme
    attributs les grilles d'espace X et Y, la vorticité W,
    la fonction de courant Phi et le pas de la grille h"""

    def __init__(self, resolution, L=float(), H=float()):
        self._xmax = L / 2
        self._ymax = H / 2
        q = resolution
        # définition du pas de la grille, h.
        # On prend en compte la possible diférence entre L et H,
        # pas forcément très utile comme fonctionnalité
        if L == H:
            self._h = L / q
            self.qx = q
            self.qy = q
        elif L > H:
            self._h = L / q
            self.qx = q
            self.qy = int(H / self._h, 0)

        else:
            self._h = H / q
            self.qy = q
            self.qx = int(L / self._h, 0)

        x = np.linspace(-self._xmax, self._xmax, self.qx)
        y = np.linspace(-self._ymax, self._ymax, self.qy)
        self.X, self.Y = np.meshgrid(x, y)
        self.W = self.X * 0
        self.Phi = self.X * 0
        self.dt = 0.001
        # precision of the stream function:
        self.conv = 0.0001
        # viscosité
        self.nu = 0.0001

        self.u_t_wall = 0
        self.u_b_wall = 0
        self.no_slip = False

    def vortex(self, x, y, sens, largeur=0.1):
        """Créé un vortex de coordonnées x et y"""
        if sens != 0:
            R = np.sqrt((self.X - x) ** 2 + (self.Y - y) ** 2)
            self.W = self.W + sens * 10 * np.exp(
                -(R ** 2) * 100 / (largeur)
            )  # sens*largeur*100/(largeur+R**2)

    def line(self, x=-0.5, y=0, L=1, vort=10, e=2):
        """Crée une ligne sur laquelle est concentrée la vorticité,
        une tranche de feuille de vorticité"""
        x1 = floor(self.qx / 2 + x * self.qx / (2 * self._xmax))
        l = floor(L * self.qx / (2 * self._xmax))
        y1 = floor(self.qy / 2 + y * self.qy / (2 * self._xmax))
        e = e * self.qy / (4 * self._ymax)
        e = ceil(e)
        self.W[y1 + e : y1 + e + 1, x1 : x1 + l - 1] = (
            vort / 2
        )  # + self.W[y1+e:y1+e+1,x1:x1+l-1]
        self.W[y1 - e : y1 + e, x1 : x1 + l - 1] = vort  # + self.W[y1-e:y1+e,x1:x1+l-1]
        self.W[y1 - e - 1 : y1, x1 : x1 + l - 1] = (
            vort / 2
        )  # + self.W[y1-e-1:y1,x1:x1+l-1]
        self.W[y1 - e : y1 + e, x1 - 1] = vort / 2  # + self.W[y1-e:y1+e,x1-1]
        self.W[y1 - e : y1 + e, x1 + l - 1] = vort / 2  # + self.W[y1-e:y1+e,x1+l-1]

    def noise(self, intensity):
        self.W = (
            self.W
            + ((np.random.random(self.W.shape) - np.random.random(self.W.shape))) ** 7
            * intensity
        )

    def rand(self, intensity, L=0.7, N=100):
        x = uniform(-self._xmax * L, self._xmax * L)
        y = uniform(-self._ymax * L, self._ymax * L)
        largeur = 0
        i = 1
        xl = []
        yl = []
        xl.append(x)
        yl.append(y)
        while i < N:
            occupe = False
            largeur0 = largeur
            largeur = uniform(1, 20)
            j = 1
            while occupe == False and j < len(xl):

                if (((x - xl[j - 1]) ** 2 + (y - yl[j - 1]) ** 2) ** 0.5) < (
                    ((largeur + largeur0) ** 0.7) * 4 / 100
                ):
                    occupe = True
                j += 1
            if occupe == False:
                i += 1
                if largeur > 8:
                    sens = uniform(-(intensity ** 0.8), intensity ** 0.8)
                else:
                    sens = uniform(-intensity, intensity)
                self.vortex(x, y, sens, largeur)
                xl.append(x)
                yl.append(y)

            x = uniform(-self._xmax * L, self._xmax * L)
            y = uniform(-self._ymax * L, self._ymax * L)

    def Vortex_solv(
        self,
        tmax=1,
    ):
        erreur = 0
        """ Résout l'équation de la vorticité"""
        self.W, self.Phi, erreur = jellyfish(
            self.W,
            self.Phi,
            tmax,
            self.dt,
            self._h,
            self.conv,
            self.nu,
            self.u_t_wall,
            self.u_b_wall,
            erreur,
            self.no_slip,
        )
        return erreur
