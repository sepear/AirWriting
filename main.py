# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:09:12 2020

@author: kerorito
"""
# Quizás os hace falta ejecutar lo siguiente
# pip install imutils 
# pip install PIL

# Explicación de Tkinter para el que le interese...
#https://python-para-impacientes.blogspot.com/p/tutorial-de-tkinter.html

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np

prediccionText = "" # Variable para comunicarnos con Tkinter
imagenReconocidaImage = np.ones((40,40))*150 # Variable para comunicarnos con Tkinter 

class AplicacionGUI():
    def __init__(self,fguardar,freset):
        root = tk.Tk() # Creamos la raiz de tkinter
        root.title('Reconocimiento AirWriting') # Ponemos título a la ventana
        root.geometry('1400x800') # Definimos el tamaño
        
        cam = cv2.VideoCapture(0) # Captura de la webcam
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800) # Width
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600) # Height

        video = tk.Label(root) # AÑadimos el video a la raiz
        video.place(x=30,y=50) # Coordenadas para posicionar el video

        texto1 = tk.Label(root, text="Cámara") # Creamos un texto y lo añadimos a la raiz
        texto1.place(x=330, y=20) # Le damos sus coordenadas

        imagenGuardar = ImageTk.PhotoImage(Image.open("images/save.png")) # Cargamos el icono de guardar
        bGuardar = tk.Button(root, text='Guardar',image=imagenGuardar,command=fguardar) # Creamos un botón con ola imagen anterior y que ejecutará la función correspondiente
        bGuardar.place(x=1000, y=460)

        imagenReset = Image.open("images/reset.png")
        imagenReset = imagenReset.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenResetRedimensionada = ImageTk.PhotoImage(imagenReset)
        breset = tk.Button(root, text='Restart',image=imagenResetRedimensionada ,command=freset)
        breset.place(x=1100,y=460)

        texto2 = tk.Label(root, text="Imagen dibujada")
        texto2.place(x=1015,y=225)
        
        render = ImageTk.PhotoImage(Image.open("images/placeholder.png")) # Cargamos una imagen de placeholder hasta que se obtenga la real  
        placeholder = tk.Label(root, image=render)
        placeholder.image = render
        placeholder.place(x=1000, y=250)
        
        prediccion = tk.StringVar(root,value="-")
        texto3 = tk.Label(root, textvariable=prediccion)
        texto3.place(x=1000,y=400)
        
        def show_frame(): # Esta función nos permite convertir la entrada de la webcam en imágenes válidas para tkinter
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            video.imgtk = imgtk
            video.configure(image=imgtk)
            video.after(10, show_frame)
        def logicaDeFuncionamiento(): # Esto se ejecutará una vez por fotograma, a 60fps
            main() # Ejecutamos el método main
            
            global imagenReconocidaImage # Nos traemos la variable global con la nueva imagen de la predicción y la actualizamos
            img =  ImageTk.PhotoImage(image=Image.fromarray(imagenReconocidaImage))
            placeholder.configure(image=img)
            placeholder.image = img
            
            global prediccionText # Nos traemoos la variable global con el nuevo texto de la predicción y lo actualizamos
            prediccion.set(prediccionText)
            root.after(16, logicaDeFuncionamiento) # Programamos la ejecución del siguiente fotograma
            
        show_frame() # Ejecutamos un frame de video
        logicaDeFuncionamiento() # Ejecutamos un frame de lógica 
        root.mainloop() # Bucle de Tkinter para generar la ventana y el contenido

def setPrediccionText(text): # Esta función actualiza la variable global para que cambie en Tkinter. Recibe un String
    global prediccionText
    prediccionText = "Predicción "+text

def setImagenReconocida(array): # Esta función actualiza la variable global para que cambie en Tkinter. Recibe un array de numpy
    global imagenReconocidaImage
    imagenReconocidaImage = array



####################################################################################################################################


# A partir de aquí lo que os interesa y podeis tocar

def guardar(): # Cuando se hace click en guardar se llama a esta función
    print("Guardar pulsado")

def reset(): # Cuando se hace click en reset se llama a esta función
    print("Reset pulsado")

def main(): # Este método main se ejecutará una vez por fotograma, aquí está toda la lógica del programa
    print("Fotograma")
    setPrediccionText("-") # Ejemplo de como cambiar el texto de la predicción
    setImagenReconocida(np.zeros((40,40))*150) # Ejemplo de como cambiar la imagen de la predicción

if __name__ == '__main__': # Inicializamos la aplicación al estilo python 
    mi_app = AplicacionGUI(guardar,reset) # Lanzamos la aplicación 