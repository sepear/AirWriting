"""# -*- coding: utf-8 -*-"""
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

debug=False
RGB_R = 100
RGB_G = 100
RGB_B = 100   

class AplicacionGUI():
    def __init__(self):
        self.root = tk.Tk() # Creamos la raiz de tkinter
        self.root.title('Reconocimiento AirWriting') # Ponemos título a la ventana
        self.root.geometry('1920x1080') # Definimos el tamaño

        global imagenReconocidaImage
        imagenReconocidaImage = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        imagenReconocidaImage = cv2.cvtColor(imagenReconocidaImage, cv2.COLOR_BGR2RGBA)
        print("INICIANDO GUI")
        video = tk.Label(self.root) # AÑadimos el video a la raiz
        video.grid(row=1,column=0)
        self.root.columnconfigure(0, weight=1 , minsize = 1080)
        
        texto1 = tk.Label(self.root, text="Cámara") # Creamos un texto y lo añadimos a la raiz
        texto1.grid(row=0,column=0)
        
        buttonframe = tk.Frame(self.root)
        buttonframe.grid(row=2,column=0)
        
        imagenGuardar = ImageTk.PhotoImage(Image.open("images/save.png")) # Cargamos el icono de guardar
        bGuardar = tk.Button(buttonframe, text='Guardar',image=imagenGuardar,command=self.guardar) # Creamos un botón con ola imagen anterior y que ejecutará la función correspondiente
        bGuardar.grid(row=0,column=0)
        
        imagenReset = Image.open("images/reset.png")
        imagenReset = imagenReset.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenResetRedimensionada = ImageTk.PhotoImage(imagenReset)
        breset = tk.Button(buttonframe, text='Restart',image=imagenResetRedimensionada ,command=self.reset)
        breset.grid(row=0,column=1)
        
        imagenDebug = Image.open("images/computervision.png")
        imagenDebug = imagenDebug.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenDebugRedimensionada = ImageTk.PhotoImage(imagenDebug)
        bdebug = tk.Button(buttonframe, text='Debug',image=imagenDebugRedimensionada ,command=self.fdebug)
        bdebug.grid(row=0,column=3)
        
        rgbframe = tk.Frame(self.root)
        rgbframe.grid(row=3, column=0)
        
        self.R_RGB = tk.Scale(rgbframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.R_RGB.set(100)
        label_r = tk.Label(rgbframe, text="R")
        label_r.grid(row=0, column=0)
        self.R_RGB.grid(row=0, column=1)      
        
        self.G_RGB = tk.Scale(rgbframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.G_RGB.set(100)
        label_g = tk.Label(rgbframe, text="G")
        label_g.grid(row=1, column=0)
        self.G_RGB.grid(row=1, column=1)
                        
        self.B_RGB = tk.Scale(rgbframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.B_RGB.set(100)
        label_b = tk.Label(rgbframe, text="B")
        label_b.grid(row=2, column=0)
        self.B_RGB.grid(row=2, column=1)      
 
        texto2 = tk.Label(self.root, text="Imagen dibujada")
        texto2.grid(row=0,column=1)
        
        render = ImageTk.PhotoImage(Image.open("images/placeholder.png")) # Cargamos una imagen de placeholder hasta que se obtenga la real  
        placeholder = tk.Label(self.root, image=render)
        placeholder.image = render
        placeholder.grid(row=1,column=1, columnspan = 3)
        self.root.columnconfigure(1, weight=1 , minsize = 800)
        self.root.rowconfigure(1, weight=1 , minsize = 600)
        
        prediccion = tk.StringVar(self.root,value="-")
        texto3 = tk.Label(self.root, textvariable=prediccion)
        texto3.grid(row=2,column=1)
        
        imagenSkinFilter = Image.open("images/config.png")
        imagenSkinFilter = imagenSkinFilter.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenSkinFilterRedimensionada = ImageTk.PhotoImage(imagenSkinFilter)
        bclose = tk.Button(buttonframe, text='Configuracion',image=imagenSkinFilterRedimensionada ,command=self.cerrarVentana)
        bclose.grid(row=0,column=2)
        
        def on_closing(): # Función para cerrar Tkinter y soltar la cámara
            cam.release()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        def show_frame(): # Esta función nos permite convertir la entrada de la webcam en imágenes válidas para tkinter
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            global imagenReconocidaImage # Nos traemos la variable global con la nueva imagen de la predicción y la actualizamos
            global RGB_R
            global RGB_G
            global RGB_B 
            
            RGB_R = self.R_RGB.get()
            RGB_G = self.G_RGB.get()
            RGB_B = self.B_RGB.get()
            
            main(frame)#CAMBIO HECHO POR SERGIO, COMO LUEGO SE LE HACEN COSAS INTERMEDIAS, EMJOR PASARLO EN BGR Y LUEGO YA AL FINAL SE PASA A RGBA
            
            if(debug):
                imagen_dibujada = cv2image
            else:
                imagen_dibujada = applyMask(imagenReconocidaImage, cv2image)
            
            img = Image.fromarray(imagen_dibujada)
            imgtk = ImageTk.PhotoImage(image=img)
            video.imgtk = imgtk
            video.configure(image=imgtk)
            
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
    
    def fdebug(self):
        global debug
        debug = not debug
        self.reset()
    def guardar(self): # Cuando se hace click en guardar se llama a esta función
        print("Guardar pulsado")

    def reset(self): # Cuando se hace click en reset se llama a esta función
        print("Reset pulsado")
        global imagenReconocidaImage
        imagenReconocidaImage = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        imagenReconocidaImage = cv2.cvtColor(imagenReconocidaImage, cv2.COLOR_BGR2RGBA)
        
class skinfilterGUI():
    def __init__(self):
        self.root = tk.Tk() # Creamos la raiz de tkinter
        self.root.title('Reconocimiento SkinFilter') # Ponemos título a la ventana
        self.root.geometry('1920x1080') # Definimos el tamaño
        
        self.frameCounter = 0
        
        self.root.columnconfigure(0, weight=1 , minsize = 452)
        self.root.columnconfigure(1, weight=1 , minsize = 452)
        self.root.columnconfigure(2, weight=1 , minsize = 452)
        
        self.root.rowconfigure(0, weight=1 , minsize = 339)
        self.root.rowconfigure(1, weight=1 , minsize = 339)
        
        video1 = tk.Label(self.root) # AÑadimos el video1 a la raiz
        video1.grid(row=0,column=0)
        
        video2 = tk.Label(self.root) # AÑadimos el video2 a la raiz
        video2.grid(row=0,column=1)
        
        video3 = tk.Label(self.root) # AÑadimos el video3 a la raiz
        video3.grid(row=0,column=2)
        
        video4 = tk.Label(self.root) # AÑadimos el video3 a la raiz
        video4.grid(row=1,column=0)
        
        video5 = tk.Label(self.root) # AÑadimos el video3 a la raiz
        video5.grid(row=1,column=1)
        
        video6 = tk.Label(self.root) # AÑadimos el video3 a la raiz
        video6.grid(row=1,column=2)

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
        
        #sliders erosion dilatacion y blur
        self.FMSize_B = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL)
        self.FMSize_B.set(FMSize[0])
        label_7 = tk.Label(self.root, text="FMSize")
        label_7.grid(row=15, column=0)
        self.FMSize_B.grid(row=15, column=1)

        self.EKSize_B = tk.Scale(self.root, from_=0, to=20, orient=tk.HORIZONTAL)
        self.EKSize_B.set(EKSize[0])
        label_8 = tk.Label(self.root, text="EKSize")
        label_8.grid(row=16, column=0)
        self.EKSize_B.grid(row=16, column=1)

        self.EIteraciones_B = tk.Scale(self.root, from_=0, to=20, orient=tk.HORIZONTAL)
        self.EIteraciones_B.set(EIteraciones)
        label_9 = tk.Label(self.root, text="EIteraciones")
        label_9.grid(row=17, column=0)
        self.EIteraciones_B.grid(row=17, column=1)

        self.DKSize_B = tk.Scale(self.root, from_=0, to=20, orient=tk.HORIZONTAL)
        self.DKSize_B.set(DKSize[0])
        label_10 = tk.Label(self.root, text="DKSize")
        label_10.grid(row=18, column=0)
        self.DKSize_B.grid(row=18, column=1)

        self.DIteraciones_B = tk.Scale(self.root, from_=0, to=20, orient=tk.HORIZONTAL)
        self.DIteraciones_B.set(DIteraciones)
        label_11 = tk.Label(self.root, text="DIteraciones")
        label_11.grid(row=19, column=0)
        self.DIteraciones_B.grid(row=19, column=1)        
        
        imagenSkinFilter = Image.open("images/back.png") # Botón para volver
        imagenSkinFilter = imagenSkinFilter.resize((68,68), Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenSkinFilterRedimensionada = ImageTk.PhotoImage(imagenSkinFilter)
        bclose = tk.Button(self.root, text='volver',image=imagenSkinFilterRedimensionada ,command=self.cerrarVentana)
        bclose.grid(row=10,column=2,rowspan=2)

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
            

            h_min_global = self.h_min.get() # Almacenamos el valor de los sliders en las variables globales
            h_max_global = self.h_max.get()
            s_min_global = self.s_min.get()
            s_max_global = self.s_max.get()
            v_min_global = self.v_min.get()
            v_max_global = self.v_max.get()
            


            FMSize = (self.FMSize_B.get(),self.FMSize_B.get())
            EKSize = (self.EKSize_B.get(),self.EKSize_B.get())
            EIteraciones = self.EIteraciones_B.get() 
            DKSize = (self.DKSize_B.get(),self.DKSize_B.get())
            DIteraciones = self.DIteraciones_B.get()
        
            lower = np.array([h_min_global, s_min_global, v_min_global]) # Calculamos la máscara 
            upper = np.array([h_max_global, s_max_global, v_max_global])
            mask = cv2.inRange(imgHsv, lower, upper)

            result = cv2.bitwise_and(img, img, mask=mask)
  
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            #escala = (640,480) 
            escala = (452,339)
            #escala = (320,240)
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            img1 = Image.fromarray(cv2image)
            
            img1 = img1.resize(escala, Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
            imgtk1 = ImageTk.PhotoImage(image=img1)
            video1.imgtk = imgtk1
            video1.configure(image=imgtk1)
            
            img2 = Image.fromarray(mask)
            img2 = img2.resize(escala, Image.ANTIALIAS)
            imgtk2 = ImageTk.PhotoImage(image=img2)
            video2.imgtk = imgtk2
            video2.configure(image=imgtk2)
            
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
            img3 = Image.fromarray(result)
            img3 = img3.resize(escala, Image.ANTIALIAS)
            imgtk3 = ImageTk.PhotoImage(image=img3)
            video3.imgtk3 = imgtk3
            video3.configure(image=imgtk3)
            
            filtro_media = cv2.blur(mask,FMSize)  
            filtro_media = cv2.cvtColor(filtro_media, cv2.COLOR_BGR2RGBA)
            img4 = Image.fromarray(filtro_media)
            img4 = img4.resize(escala, Image.ANTIALIAS)
            imgtk4 = ImageTk.PhotoImage(image=img4)
            video4.imgtk4 = imgtk4
            video4.configure(image=imgtk4)
            
            erosion_kernel = np.ones(getEKSize(), np.uint8)
            filtro_erosion = cv2.erode(filtro_media, erosion_kernel, iterations = getEIteraciones())            
            filtro_erosion = cv2.cvtColor(filtro_erosion, cv2.COLOR_BGR2RGBA)
            img5 = Image.fromarray(filtro_erosion)
            img5 = img5.resize(escala, Image.ANTIALIAS)
            imgtk5 = ImageTk.PhotoImage(image=img5)
            video5.imgtk5 = imgtk5
            video5.configure(image=imgtk5)

            dilation_kernel = np.ones(getDKSize(), np.uint8)
            filtro_dilatacion = cv2.erode(filtro_erosion, dilation_kernel, iterations = getDIteraciones()) 
            filtro_dilatacion = cv2.cvtColor(filtro_dilatacion, cv2.COLOR_BGR2RGBA)
            img6 = Image.fromarray(filtro_dilatacion)
            img6 = img6.resize(escala, Image.ANTIALIAS)
            imgtk6 = ImageTk.PhotoImage(image=img6)
            video6.imgtk6 = imgtk6
            video6.configure(image=imgtk6)
            
            self.root.after(10, show_frame) # programamos el siguiente fotograma
            
        show_frame() # Ejecutamos un frame
        self.root.mainloop() # Bucle de Tkinter para generar la ventana y el contenido
        
    def cerrarVentana(self): # Nos devuelve al programa principal       
        self.root.destroy()  
        launchWindow()
    
def setPrediccionText(text): # Esta función actualiza la variable global para que cambie en Tkinter. Recibe un String
    global prediccionText
    prediccionText = "Predicción "+text

def setImagenReconocida(array): # Esta función actualiza la variable global para que cambie en Tkinter. Recibe un array de numpy
    global imagenReconocidaImage
    imagenReconocidaImage = array


####################################################################################################################################

# A partir de aquí lo que os interesa y podeis tocar

def main(fotograma): # Este método main se ejecutará una vez por fotograma, aquí está toda la lógica del programa
    # El parámetro fotograma es, un fotograma xD hay que aplicar toda la lógica y funciones desde aquí
    # getSkinFilteredImage(frame) con esta funcion nos devolverá el filtro aplicado al fotograma pasado
    # NOTA IMPORTANTE : Para debuguear la imagen que esteis trabajando, usar la funcion setimagenreconocida, os la mostrará por pantalla aunque rompiendo la interfaz, hasta nuevo aviso será así
    #print("Fotograma")
    #a = media(fotograma)
    #b = skinfilter(a)
    #recortar(fotograma)
    #prediccion(fotograma)
    skinfiltered = getSkinFilteredImage(fotograma)#ESTO HAY QUE ARREGLARLO PORQUE NO SALE COMO DEBERÍA
    #setPrediccionText("-") # Ejemplo de como cambiar el texto de la predicción
    #setImagenReconocida(np.zeros((40,40))*150) # Ejemplo de como cambiar la imagen de la predicción
    
    ############## Suavizado ###############
    global FMSize
    #filtro_media_size = FMSize;  #Función para que alberto haga la función y la enlace con los "botoncitos" los más comunes son (3,3) y (5,5)
    
    filtro_media = cv2.blur(skinfiltered,FMSize)   # (3,3) sustituir por "filtro_media_size" cuando la función esté hecha
    
    ############### Erosión #########################
    
    #erosion_kernel_size = getEKSize(); #Función para determinar el tamaño del kernel y alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
    
    erosion_kernel = np.ones(getEKSize(), np.uint8)  # (3,3) sustituir por erosion_kernel_size cuando la función esté hecha)
    
    #iteraciones_erosion = getEIteraciones() #Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones.
    
    erosion = cv2.erode(filtro_media, erosion_kernel, iterations = getEIteraciones()) # iterations = iteraciones cuando la función esté hecha 
    
    #Nota: iteraciones = 0 -> no hay erosión
    
    
    ############### Dilatación ###################
    
    #dilation_kernel_size = getDKSize(); #Función para determinar el tamaño del kernel y Alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
    
    dilation_kernel = np.ones(getDKSize(), np.uint8)  # (3,3) sustituir por dilation_kernel_size cuando la función esté hecha)
    
    #iteraciones_dilation = getDIteraciones() #Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones.
    
    Dilation = cv2.erode(erosion, dilation_kernel, iterations = getDIteraciones()) # iterations = iteraciones cuando la función esté hecha 
    
    #Nota: iteraciones = 0 -> no hay Dilatación
    
    ########### Imagen ya procesada ###########################

    #https: // stackoverflow.com / questions / 44588279 / find - and -draw - the - largest - contour - in -opencv - on - a - specific - color - python



    #OJO CAMBIO TEMPORAL DE SERGIO EN EL QUE ME SALTO LO QUE NO SEA HSV PARA TESTEAR
    imgray = cv2.cvtColor(skinfiltered, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Asumimos que la mano es el contorno más grande, ya que estará en primer plano

    #AQUÍ PUEDE EXPLOTAR SI NO HAY VARIOS, MIRAR EL LEN O HACER TRY/EXECPTION
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        #https: // www.pyimagesearch.com / 2016 / 02 / 01 / opencv - center - of - contour /
        M = cv2.moments(c)#M es el centroide
        try:
            cX = int(M["m10"] / M["m00"])#estas sus coordenadas
            cY = int(M["m01"] / M["m00"])
        except :
            pass
        x, y, w, h = cv2.boundingRect(c)
        # draw the biggest contour (c) in green
        
        imagen_procesada = cv2.cvtColor(imgray, cv2.COLOR_BGR2RGB)

        try:
            cv2.circle(imagen_procesada, (cX, cY), 7, (255, 0, 0), -1)
        except:
            pass
        cv2.rectangle(imagen_procesada, (x, y), (x + w, y + h), (0, 255, 0), 2)

        hand_hull = cv2.convexHull(c, False)#ponemos en false para que devuelva los indices de los puntos del contorno
        hand_hull_coordinates = cv2.convexHull(c, True)#ponemos en true para que devuelva las coordenadas

        #IMPORTANTE!!!!!!!!!!!!!!! ESTE ES EL PUNTO QUE VAMOS A PINTAR(ASUMIDO COMO PUNTA DE DEDO)
        try:
            punto_mas_lejano = masLejano(hand_hull_coordinates, (cX, cY))
        except:
            pass
        
        #https: // opencv - python - tutroals.readthedocs.io / en / latest / py_tutorials / py_imgproc / py_contours / py_contour_features / py_contour_features.html

        #imagen_procesada[:] = 0
        #cv2.drawContours(imagen_procesada, [c], contourIdx=0, color=(0, 255, 0))
        #cv2.drawContours(imagen_procesada, [hand_hull], contourIdx=0, color=(255, 0, 0))
        drawing = np.zeros((imagen_procesada.shape[0], imagen_procesada.shape[1], 3), dtype=np.uint8)
        for i in range(len([c])):
            color = (255, 0, 0)
            #cv2.drawContours(imagen_procesada, [c], i, color)
            cv2.drawContours(imagen_procesada, [hand_hull], i, color, 2)

        cv2.circle(imagen_procesada, punto_mas_lejano, radius=10, color=(0, 255, 255), thickness=-1)#thickness -1 for filled circle

        """
        Recordatorio para el sergio del futuro:
        
        buscar punto mas lejano de un borde (será el centro de la palma de la mano) // de momento he usado centroide, pero sacar bien el otro
        
        sacar el circulo de mayor radio con centro el punto anterior (quizá añadir unos pixeles de margen extra para afinar mas)
        
        si eliminamos ese circulo, se nos quedan N formas volando, que seran dedos y la muñeca
        
        la muñeca será aquel tal que su largo sea mayor que su ancho y su ancho sea el mas ancho de los anchos
        
        pintar con el punto más lejano del centro que esté en el contorno? //cortando la muñeca
    
        """
        global RGB_R
        global RGB_G
        global RGB_B 
        imagen_procesada = cv2.cvtColor(imagen_procesada, cv2.COLOR_RGB2RGBA)
        cv2.circle(imagenReconocidaImage, punto_mas_lejano, radius=10, color=(RGB_R, RGB_G, RGB_B), thickness=-1)#thickness -1 for filled circle
        global debug
        if(debug):
            print(punto_mas_lejano)
            print("######################3")
            print(hand_hull_coordinates)
            print(f"len:{len(hand_hull_coordinates)}")
            print(type(hand_hull_coordinates))
            print(hand_hull_coordinates[0])
            print(type(hand_hull_coordinates[0]))
            print(hand_hull_coordinates[0][0][0])
            print(type(hand_hull_coordinates[0][0][0]))
            print("######################") 
            setImagenReconocida(imagen_procesada)
        else:
            setImagenReconocida(imagenReconocidaImage)


########### Funciones auxiliares procesamiento ##########
#Función para que alberto haga la función y la enlace con los "botoncitos" los más comunes son (3,3) y (5,5)

#Función para determinar el tamaño del kernel y alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
def getEKSize():
    return EKSize

#Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones en erosion.
def getEIteraciones():
    return EIteraciones

#Función para determinar el tamaño del kernel y Alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
def getDKSize():
    return DKSize

#Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones en dilatacion.
def getDIteraciones():
    return DIteraciones

def launchWindow(skinfilter=False):
    if(skinfilter):
        mi_app = skinfilterGUI() # Lanzamos la aplicación 
    else:
        mi_app = AplicacionGUI() # Lanzamos la aplicación 

if __name__ == '__main__': # Inicializamos la aplicación al estilo python 
    launchWindow()