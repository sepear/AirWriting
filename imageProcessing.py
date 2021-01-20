# TODO: Aquí todo el procesado de la imagen, para extraer la punta
# de los dedos y para ir pintando

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np

imagenReconocidaImage = np.ones((40, 40)) * 150  # Variable para comunicarnos con Tkinter

h_min_global = 0  # Par�metros por defecto, una vez se hayan obtenido unos buenos hay que colocarlos aqu�
h_max_global = 179  #
s_min_global = 0  #
s_max_global = 105  #
v_min_global = 154  #
v_max_global = 255  #

# h_min_global = 0   # Par�metros por defecto, una vez se hayan obtenido unos buenos hay que colocarlos aqu�
# h_max_global = 53 #
# s_min_global = 18   #
# s_max_global = 255 #
# v_min_global = 127   #
# v_max_global = 255 #


FMSize = (3, 3)  # tupla de dos n�meros iguales
EKSize = (3, 3)  # idem
EIteraciones = 1  # iter
DKSize = (3, 3)  # tupla
DIteraciones = 1  # iter

cam = cv2.VideoCapture(0)  # Captura de la webcam
_, frame = cam.read()#pillamos frame para tener el shape
print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
print(frame.shape)
UMBRAL_UNIFICACION = 8  # SI DOS PUNTOS ESTÁN A MENOS DE 8 PIXELES DE DISTANCIA, SE UNIFICAN


def masLejano(hand_hull_coordinates, centro):
    distancia_mejor = 0
    mejor = (-1, -1)

    for v in hand_hull_coordinates:
        x = v[0][0]
        y = v[0][1]
        distancia = abs(x - centro[0]) + abs(y - centro[1])
        if distancia > distancia_mejor:
            distancia_mejor = distancia
            mejor = (x, y)
    return mejor


def unificaVertices(hand_hull_coordinates):
    for v1 in hand_hull_coordinates:
        x1 = v1[0][0]
        y1 = v1[0][1]
        for v2 in hand_hull_coordinates:
            x2 = v1[0][0]
            y2 = v1[0][1]
            if v1 != v2:
                distancia = abs(x1 - x2) + abs(y1 - y2)
                if distancia < UMBRAL_UNIFICACION:
                    new_x = int((x1 + x2) / 2)
                    new_y = int((y1 + y2) / 2)

                    x1 = x2 = new_x
                    y1 = y2 = new_y
    # elementos=
    # contruyo aquí el nuevo, si ya está no añado


def applyMask(img1, img2):
    # img1_bg = cv2.bitwise_and(img1,img1,mask = cv2.bitwise_not(img2))
    # img2_fg = cv2.bitwise_and(img2,img2,mask = img2)
    # dst = cv2.add(img1_bg,img2_fg)
    dst = cv2.addWeighted(img1, 1, img2, 1, 0)
    return dst


