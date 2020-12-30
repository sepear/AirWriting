#TODO: AquÃ­ todo el procesado de la imagen, para extraer la punta
# de los dedos y para ir pintando

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np


imagenReconocidaImage = np.ones((40,40))*150 # Variable para comunicarnos con Tkinter 

h_min_global = 0   # Parámetros por defecto, una vez se hayan obtenido unos buenos hay que colocarlos aquí
h_max_global = 53 #
s_min_global = 18   #
s_max_global = 255 #
v_min_global = 127   #
v_max_global = 255 #


cam = cv2.VideoCapture(0) # Captura de la webcam
