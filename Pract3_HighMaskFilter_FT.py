# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 15:28:01 2020

@author: SEBASTIAN
"""


import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import io,data

#Acquiring image
get=io.imread("LoroDelAmazonas.png")
img=cv2.cvtColor(get, cv2.COLOR_BGR2GRAY)

#Defining discrete fourier transform (not continous data)
dft=cv2.dft(np.float32(img),flags=cv2.DFT_COMPLEX_OUTPUT)
#With open cv it only works with float32

#Shifting starting position of the origin
dft_shift=np.fft.fftshift(dft)

#Obtaining magnitude spectrum
                                #Getting real and imaginary part for the spectrum
magnitude_spectrum=20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,0])+1)


"""High pass filter mask"""

rows,cols=img.shape
#Focusing on the center row and column
crow,ccol=int(rows/2),int(cols/2)
#The mask has two channels
mask=np.ones((rows,cols,2),np.uint8)
#Circular mask
r=3 #Blocks all components within this radio
center=[crow,ccol]
x,y=np.ogrid[:rows,:cols]
mask_area=(x-center[0])**2+(y-center[1])**2<=r*r #Blocking
mask[mask_area]=0 

fshift=dft_shift*mask #Center with mask

#Magnitude of center with mask
fshift_mask_mag=2000*np.log(cv2.magnitude(fshift[:,:,0],fshift[:,:,1]))

f_ishift=np.fft.ifftshift(fshift) #Unshift the center
img_back=cv2.idft(f_ishift) #Inverse discrete FT
img_back=cv2.magnitude(img_back[:,:,0],img_back[:,:,1]) #Magnitude of xy space


# fig=plt.figure(figsize=(12,12))
# ax1=fig.add_subplot(2,2,1)
# ax1.imshow(img,cmap='gray')
# ax1.title.set_text('Input image')
# ax2=fig.add_subplot(2,2,2)
# ax2.imshow(magnitude_spectrum,cmap='gray')
# ax2.title.set_text('FFT of image')
# ax3=fig.add_subplot(2,2,3)
# ax3.imshow(fshift_mask_mag,cmap='gray')
# ax3.title.set_text('FFT + Mask')
# ax4=fig.add_subplot(2,2,4)
plt.imshow(img_back,cmap='gray')
plt.show()






