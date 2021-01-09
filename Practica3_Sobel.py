'IMAGENOLOGIA'
'Práctica 3: Métodos Propios.- Método SOBEL'
'Yslen González, David Moreno, Sebastián Rodríguez'

#Importación de librerías a usar
from skimage import data, color, io
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

#Leemos nuestra imagen
gris = np.uint8(color.rgb2gray(io.imread('calcificaciontendon.jpg'))*255) 
#Mostramos nuestra imagen original
plt.figure(1)
plt.imshow(gris, cmap="gray")

#Se obtiene el tamaño de la imagen
[filas, columnas]= gris.shape
#Se obtiene el histograma de la imagen original
histograma = np.zeros(256)
for i in range(filas):
    for j in range(columnas):
        pos = gris[i,j]
        histograma[pos]=histograma[pos] + 1

#n será el factor por el que se multiplicarán pixeles adyacentes
#considerando el comentario hecho en clase sobre si al aumentarlo
#se lograba suavizar más la imagen
n=2

#Se aplica la máscara de Sobel a la imagen
Sobel = np.zeros(gris.shape)
dfx=np.zeros(gris.shape)
dfy=np.zeros(gris.shape)
for x in range(filas - 3):
    for y in range(columnas - 3):
        dfx[x+2,y+2]=abs(gris[3+x,1+y]+n*gris[3+x,2+y]+gris[3+x,3+y]-(gris[1+x,1+y]+n*gris[1+x,2+y]+gris[1+x,3+y]))
        if dfx[x+2,y+2]>255:
            dfx[x+2,y+2]=255
        else:
            dfx[x+2,y+2]=dfx[x+2,y+2]
        dfy[x+2,y+2]=abs(gris[1+x,3+y]+n*gris[2+x,3+y]+gris[3+x,3+y]-(gris[1+x,1+y]+n*gris[2+x,1+y]+gris[3+x,1+y]))        
        if dfy[x+2,y+2]>255:
            dfy[x+2,y+2]=255
        else:
            dfy[x+2,y+2]=dfy[x+2,y+2]
        Sobel[x+2,y+2]=dfx[x+2,y+2]+dfy[x+2,y+2]

#Se muestra la nueva imagen obtenida con el método de Sobel
plt.figure(2)
plt.imshow(np.uint8(Sobel), cmap='gray')
plt.show()
plt.draw()
#Se agrega una pausa de 10 segundos para determinar el umbral que se agregará
#para recalcar el borde en la imagen final
plt.pause(10)

#Se ingresa el valor del umbral seleccionado
umbral=int(input("Umbral para recalcar el borde: "))

#Se realiza la suma del 60% de la imagen original + 40% de la imagen obtenida
#con Sobel si el valor de Sobel es menor al umbral seleccionado
#Si el valor es mayor al umbral, se respeta el valor de Sobel para recalcar el borde
Ima = np.zeros(gris.shape)
plt.figure(3)
for i in range(filas):
    for j in range(columnas):
        if Sobel[i,j]<umbral:
            Ima[i,j]=0.4*+Sobel[i,j]+0.6*gris[i,j]
        else:
            Ima[i,j]=Sobel[i,j]
Ima=np.uint8(Ima)

#Se crea el histograma de la imagen mejorada
histograma2 = np.zeros(256)
for x in range(filas):
    for y in range(columnas):
        posicion = Ima[x,y]
        histograma2[posicion]=histograma2[posicion] + 1
        
#Se muestra la imagen original vs. la imagen con bordes remarcados con Sobel
fig3=plt.figure(3)
ax1 = fig3.add_subplot(121)
ax2 = fig3.add_subplot(122)
ax1.imshow(gris, cmap='gray')
ax1.set_title('Imagen Original')
ax2.imshow(np.uint8(Sobel), cmap="gray")
ax2.set_title('Imagen con Sobel') 

#Se muestra la imagen original vs. la imagen final
fig4=plt.figure(4)
ax1 = fig4.add_subplot(121)
ax2 = fig4.add_subplot(122)
ax1.imshow(gris, cmap='gray')
ax1.set_title('Imagen Original')
ax2.imshow(np.uint8(Ima), cmap="gray")
ax2.set_title('Imagen Final')      

#Muestreo de Histograma Original vs. Mejorado
plt.figure(5)
plt.plot(histograma, label='Imagen Original')
plt.plot(histograma2, label='Imagen Mejorada')
plt.title('Histogramas')
plt.legend()

plt.show()