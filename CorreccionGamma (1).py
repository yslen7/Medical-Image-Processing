"""Importacion de las librerias"""
from skimage import color, io
import numpy as np
import matplotlib.pyplot as plt
plt.close("all")

"""Obtencion de la imagen"""
I = io.imread('tendonys.jpg')
gris = np.uint8(color.rgb2gray(I)*255)
grisd = np.double(gris)
cg=gris.copy()
[fil, col] = gris.shape

"""Sacamos el histograma original de la imagen"""
histn = np.zeros(256)
for i in range(fil):
    for j in range(col):
        pos = gris[i,j]
        histn[pos] = histn[pos] + 1
probn = histn / (fil * col)
Hn = probn.cumsum()

"""Aplicamos la corrección gamma"""
gamma=np.double(input('Valor de gamma: '))
k=255/np.max(grisd**gamma)

for i in range(0, fil):
    for j in range(0, col):
        cg[i,j]=k*grisd[i,j]**(gamma)

cg = np.uint8(cg)

"""Sacamos el histograma de la imagen mejorada"""
histg = np.zeros(256)
for i in range(fil):
    for j in range(col):
        pos = cg[i,j]
        histg[pos] = histg[pos] + 1
probg = histg / (fil * col)
Hg = probg.cumsum()

"""Graficamos los resultados"""
fig = plt.figure(1)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.plot(histn)
ax2.plot(Hn)
ax3.plot(histg)
ax4.plot(Hg)

fig = plt.figure(2)
plt.gray()  # Muestra las graficas en escala de grises
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.imshow(gris)
ax2.imshow(cg)
plt.show()