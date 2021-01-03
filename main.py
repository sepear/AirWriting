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

#importamos las herramientas de procesado de imagen
from imageProcessing import *

#importamos las herramientas del modelo 
from cnnModel import *





class AplicacionGUI():
    def __init__(self,fguardar,freset):
        self.root = tk.Tk() # Creamos la raiz de tkinter
        self.root.title('Reconocimiento AirWriting') # Ponemos título a la ventana
        self.root.geometry('1400x800') # Definimos el tamaño
        
        #global cam #definimos para que nos coja la camara
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800) # Width
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600) # Height
    
    
        video = tk.Label(self.root) # AÑadimos el video a la raiz
        video.place(x=30,y=50) # Coordenadas para posicionar el video

        texto1 = tk.Label(self.root, text="Cámara") # Creamos un texto y lo añadimos a la raiz
        texto1.place(x=330, y=20) # Le damos sus coordenadas

        imagenGuardar = ImageTk.PhotoImage(Image.open("images/save.png")) # Cargamos el icono de guardar
        bGuardar = tk.Button(self.root, text='Guardar',image=imagenGuardar,command=fguardar) # Creamos un botón con ola imagen anterior y que ejecutará la función correspondiente
        bGuardar.place(x=1000, y=460+350)

        imagenReset = Image.open("images/reset.png")
        imagenReset = imagenReset.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenResetRedimensionada = ImageTk.PhotoImage(imagenReset)
        breset = tk.Button(self.root, text='Restart',image=imagenResetRedimensionada ,command=freset)
        breset.place(x=1100,y=460+350)

        texto2 = tk.Label(self.root, text="Imagen dibujada")
        texto2.place(x=1015,y=20)
        
        render = ImageTk.PhotoImage(Image.open("images/placeholder.png")) # Cargamos una imagen de placeholder hasta que se obtenga la real  
        placeholder = tk.Label(self.root, image=render)
        placeholder.image = render
        placeholder.place(x=1000, y=50)
        
        prediccion = tk.StringVar(self.root,value="-")
        texto3 = tk.Label(self.root, textvariable=prediccion)
        texto3.place(x=1000,y=400+350)
        
        imagenSkinFilter = Image.open("images/config.png")
        imagenSkinFilter = imagenSkinFilter.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenSkinFilterRedimensionada = ImageTk.PhotoImage(imagenSkinFilter)
        bclose = tk.Button(self.root, text='Configuracion',image=imagenSkinFilterRedimensionada ,command=self.cerrarVentana)
        bclose.place(x=1200,y=560+350)
        def on_closing(): # Función para cerrar Tkinter y soltar la cámara
            print("closing")
            cam.release()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        def show_frame(): # Esta función nos permite convertir la entrada de la webcam en imágenes válidas para tkinter
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            #main(cv2image) # Ejecutamos el método main
            main(frame)#CAMBIO HECHO POR SERGIO, COMO LUEGO SE LE HACEN COSAS INTERMEDIAS, EMJOR PASARLO EN BGR Y LUEGO YA AL FINAL SE PASA A RGBA

            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            video.imgtk = imgtk
            video.configure(image=imgtk)
            
            global imagenReconocidaImage # Nos traemos la variable global con la nueva imagen de la predicción y la actualizamos
            img =  ImageTk.PhotoImage(image=Image.fromarray(imagenReconocidaImage))
            placeholder.configure(image=img)
            placeholder.image = img
            
            global prediccionText # Nos traemoos la variable global con el nuevo texto de la predicción y lo actualizamos
            prediccion.set(prediccionText)            
            
            self.root.after(10, show_frame)

        show_frame() # Ejecutamos un frame 
        self.root.mainloop() # Bucle de Tkinter para generar la ventana y el contenido
        
    def cerrarVentana(self):
   
        self.root.destroy()
        
        
        launchWindow(True)
        
class skinfilterGUI():
    def __init__(self):
        
        self.root = tk.Tk() # Creamos la raiz de tkinter
        self.root.title('Reconocimiento SkinFilter') # Ponemos título a la ventana
        self.root.geometry('975x600') # Definimos el tamaño
        
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # Width
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # Height
    
        
       # self.cap = cv2.VideoCapture(0) # Definimos los parámetros de captura de video
       # self.cap.set(3, 320)
       # self.cap.set(4, 240)
        self.frameCounter = 0
        
        video1 = tk.Label(self.root) # AÑadimos el video1 a la raiz
        video1.grid(row=0,column=0)
        
        video2 = tk.Label(self.root) # AÑadimos el video2 a la raiz
        video2.grid(row=0,column=1)
        
        video3 = tk.Label(self.root) # AÑadimos el video3 a la raiz
        video3.grid(row=0,column=2)

        global h_min_global  # Nos traemos las variables globales
        global h_max_global 
        global s_min_global 
        global s_max_global 
        global v_min_global 
        global v_max_global 
        
        # Definimos todos los sliders y los seteamos con el valor de las variables globales por defecto
        self.h_min = tk.Scale(self.root, from_=0, to=179, orient=tk.HORIZONTAL)
        self.h_min.set(h_min_global)
        label_1 = tk.Label(self.root, text="h_min")
        label_1.grid(row=8, column=0)
        self.h_min.grid(row=8, column=1)
        
        self.h_max = tk.Scale(self.root, from_=0, to=179, orient=tk.HORIZONTAL)
        self.h_max.set(h_max_global)
        label_2 = tk.Label(self.root, text="h_max")
        label_2.grid(row=9, column=0)
        self.h_max.grid(row=9, column=1)        
        
        self.s_min = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.s_min.set(s_min_global)
        label_3 = tk.Label(self.root, text="s_min")
        label_3.grid(row=10, column=0)
        self.s_min.grid(row=10, column=1)
        
        self.s_max = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.s_max.set(s_max_global)
        label_4 = tk.Label(self.root, text="s_max")
        label_4.grid(row=11, column=0)
        self.s_max.grid(row=11, column=1)        
        
        self.v_min = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.v_min.set(v_min_global)
        label_5 = tk.Label(self.root, text="v_min")
        label_5.grid(row=12, column=0)
        self.v_min.grid(row=12, column=1)        
        
        self.v_max = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.v_max.set(v_max_global)
        label_6 = tk.Label(self.root, text="v_max")
        label_6.grid(row=13, column=0)
        self.v_max.grid(row=13, column=1)
        
        imagenSkinFilter = Image.open("images/back.png") # Botón para volver
        imagenSkinFilter = imagenSkinFilter.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenSkinFilterRedimensionada = ImageTk.PhotoImage(imagenSkinFilter)
        bclose = tk.Button(self.root, text='volver',image=imagenSkinFilterRedimensionada ,command=self.cerrarVentana)
        bclose.grid(row=10,column=2)
        def on_closing():# Función para cerrar Tkinter y soltar la cámara
            print("closing")
            cam.release()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        def show_frame(): # Se ejecuta una vez por frame
            self.frameCounter += 1
            if cam.get(cv2.CAP_PROP_FRAME_COUNT) ==self.frameCounter:
                cam.set(cv2.CAP_PROP_POS_FRAMES,0)
                self.frameCounter=0
  
            _, img = cam.read()
            img = cv2.flip(img, 1)
            img1 = Image.fromarray(img)
            imgtk1 = ImageTk.PhotoImage(image=img1)
            video1.imgtk = imgtk1
            video1.configure(image=imgtk1) 
            
            imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            global h_min_global # Nos traemos las variables globales
            global h_max_global 
            global s_min_global 
            global s_max_global 
            global v_min_global 
            global v_max_global 
            h_min_global = self.h_min.get() # Almacenamos el valor de los sliders en las variables globales
            h_max_global = self.h_max.get()
            s_min_global = self.s_min.get()
            s_max_global = self.s_max.get()
            v_min_global = self.v_min.get()
            v_max_global = self.v_max.get()
  
            lower = np.array([h_min_global, s_min_global, v_min_global]) # Calculamos la máscara 
            upper = np.array([h_max_global, s_max_global, v_max_global])
            mask = cv2.inRange(imgHsv, lower, upper)

            result = cv2.bitwise_and(img, img, mask=mask)
  
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
   
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            img1 = Image.fromarray(cv2image)
            imgtk1 = ImageTk.PhotoImage(image=img1)
            video1.imgtk = imgtk1
            video1.configure(image=imgtk1)
            
            img2 = Image.fromarray(mask)
            imgtk2 = ImageTk.PhotoImage(image=img2)
            video2.imgtk = imgtk2
            video2.configure(image=imgtk2)
            
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
            img3 = Image.fromarray(result)
            imgtk3 = ImageTk.PhotoImage(image=img3)
            video3.imgtk3 = imgtk3
            video3.configure(image=imgtk3)
            
            self.root.after(10, show_frame) # programamos el siguiente fotograma
            
        show_frame() # Ejecutamos un frame
        self.root.mainloop() # Bucle de Tkinter para generar la ventana y el contenido
        
    def cerrarVentana(self): # Nos devuelve al programa principal
       
        self.root.destroy()  
        launchWindow()

def getSkinFilteredImage(frame): # Recibe un fotograma le aplica el skinfilter y devuelve la máscara
    global h_min_global 
    global h_max_global 
    global s_min_global 
    global s_max_global 
    global v_min_global 
    global v_max_global
    imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min_global, s_min_global, v_min_global])
    upper = np.array([h_max_global, s_max_global, v_max_global])
    mask = cv2.inRange(imgHsv, lower, upper)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return mask
    
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

def main(fotograma): # Este método main se ejecutará una vez por fotograma, aquí está toda la lógica del programa
    # El parámetro fotograma es, un fotograma xD hay que aplicar toda la lógica y funciones desde aquí
    # getSkinFilteredImage(frame) con esta funcion nos devolverá el filtro aplicado al fotograma pasado
    # NOTA IMPORTANTE : Para debuguear la imagen que esteis trabajando, usar la funcion setimagenreconocida, os la mostrará por pantalla aunque rompiendo la interfaz, hasta nuevo aviso será así
    #print("Fotograma")
    #a = media(fotograma)
    #b = skinfilter(a)
    #recortar(fotograma)
    #prediccion(fotograma)
    skinfiltered= getSkinFilteredImage(fotograma)#ESTO HAY QUE ARREGLARLO PORQUE NO SALE COMO DEBERÍA
    #setPrediccionText("-") # Ejemplo de como cambiar el texto de la predicción
    #setImagenReconocida(np.zeros((40,40))*150) # Ejemplo de como cambiar la imagen de la predicción
    
    ############## Suavizado ###############
    #filtro_media_size = getFMSize();  #Función para que alberto haga la función y la enlace con los "botoncitos" los más comunes son (3,3) y (5,5)
    
    filtro_media = cv2.blur(skinfiltered,(3,3))   # (3,3) sustituir por "filtro_media_size" cuando la función esté hecha
    
    ############### Erosión #########################
    
    #erosion_kernel_size = getEKSize(); #Función para determinar el tamaño del kernel y alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
    
    erosion_kernel = np.ones((3,3), np.uint8)  # (3,3) sustituir por erosion_kernel_size cuando la función esté hecha)
    
    #iteraciones_erosion = getEIteraciones() #Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones.
    
    erosion = cv2.erode(filtro_media, erosion_kernel, iterations = 1) # iterations = iteraciones cuando la función esté hecha 
    
    #Nota: iteraciones = 0 -> no hay erosión
    
    
    ############### Dilatación ###################
    
    #dilation_kernel_size = getDKSize(); #Función para determinar el tamaño del kernel y Alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
    
    dilation_kernel = np.ones((3,3), np.uint8)  # (3,3) sustituir por dilation_kernel_size cuando la función esté hecha)
    
    #iteraciones_dilation = getDIteraciones() #Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones.
    
    Dilation = cv2.erode(erosion, dilation_kernel, iterations = 1) # iterations = iteraciones cuando la función esté hecha 
    
    #Nota: iteraciones = 0 -> no hay Dilatación
    
    ########### Imagen ya procesada ###########################
    
    imagen_procesada = cv2.cvtColor(Dilation, cv2.COLOR_BGR2RGBA)

    print(imagen_procesada)
   
    setImagenReconocida(imagen_procesada)



########### Funciones auxiliares procesamiento ##########
#Función para que alberto haga la función y la enlace con los "botoncitos" los más comunes son (3,3) y (5,5)
def getFMSize():
    pass




#Función para determinar el tamaño del kernel y alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
def getEKSize():
    pass



#Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones en erosion.
def getEIteraciones():
    pass


#Función para determinar el tamaño del kernel y Alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
def getDKSize():
    pass


#Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones en dilatacion.
def getDIteraciones():
    pass











def launchWindow(skinfilter=False):
    if(skinfilter):
        print("lanzando skin ilter")
        mi_app = skinfilterGUI() # Lanzamos la aplicación 
    else:
        mi_app = AplicacionGUI(guardar,reset) # Lanzamos la aplicación 

if __name__ == '__main__': # Inicializamos la aplicación al estilo python 
    launchWindow()
