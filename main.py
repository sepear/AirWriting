"""# -*- coding: utf-8 -*-"""
"""
Created on Wed Dec 23 12:09:12 2020

@author: kerorito
"""
# Quizás os hace falta ejecutar lo siguiente
# pip install imutils 
# pip install PIL

# Explicación de Tkinter para el que le interese...
# https://python-para-impacientes.blogspot.com/p/tutorial-de-tkinter.html

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np

# importamos las herramientas de procesado de imagen
from imageProcessing import *
from cnnModel import model

# importamos las herramientas del modelo
from cnnModel import *

debug = False
RGB_R = 100
RGB_G = 100
RGB_B = 100
global predicctionText
prediccionText = "Predicción: inicio" # Variable para comunicarnos con Tkinter

class AplicacionGUI():
    def __init__(self):
        self.root = tk.Tk()  # Creamos la raiz de tkinter
        self.root.title('Reconocimiento AirWriting')  # Ponemos título a la ventana
        self.root.geometry('1280x720')  # Definimos el tamaño
        self.imageCounter = 0
        global imagenReconocidaImage
        imagenReconocidaImage = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        imagenReconocidaImage = cv2.cvtColor(imagenReconocidaImage, cv2.COLOR_BGR2RGBA)
        print("INICIANDO GUI")

        videoframe = tk.Frame(self.root)
        videoframe.grid(row=0, column=0)

        video = tk.Label(videoframe)  # AÑadimos el video a la raiz
        video.grid(row=1, column=0)
        self.root.columnconfigure(0, weight=1, minsize=720 / 2)
        self.root.columnconfigure(1, weight=1, minsize=720 / 2)
        self.root.rowconfigure(0, weight=1, minsize=720 / 8)
        self.root.rowconfigure(1, weight=1, minsize=720 / 8)

        texto1 = tk.Label(videoframe, text="Cámara")  # Creamos un texto y lo añadimos a la raiz
        texto1.grid(row=0, column=0)

        buttonframe = tk.Frame(self.root)
        buttonframe.grid(row=2, column=0)

        imagenGuardar = ImageTk.PhotoImage(Image.open("images/save.png"))  # Cargamos el icono de guardar
        bGuardar = tk.Button(buttonframe, text='Guardar', image=imagenGuardar,
                             command=self.guardar)  # Creamos un botón con ola imagen anterior y que ejecutará la función correspondiente
        bGuardar.grid(row=0, column=0)

        imagenReset = Image.open("images/reset.png")
        imagenReset = imagenReset.resize((68, 68),
                                         Image.ANTIALIAS)  # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenResetRedimensionada = ImageTk.PhotoImage(imagenReset)
        breset = tk.Button(buttonframe, text='Restart', image=imagenResetRedimensionada, command=self.reset)
        breset.grid(row=0, column=1)

        imagenDebug = Image.open("images/computervision.png")
        imagenDebug = imagenDebug.resize((68, 68),
                                         Image.ANTIALIAS)  # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenDebugRedimensionada = ImageTk.PhotoImage(imagenDebug)
        bdebug = tk.Button(buttonframe, text='Debug', image=imagenDebugRedimensionada, command=self.fdebug)
        bdebug.grid(row=0, column=3)

        rgbframe = tk.LabelFrame(self.root, text="RGB")
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

        videodebugframe = tk.Frame(self.root)
        videodebugframe.grid(row=0, column=1)

        texto2 = tk.Label(videodebugframe, text="Imagen dibujada")
        texto2.grid(row=0, column=0)

        render = ImageTk.PhotoImage(
            Image.open("images/placeholder.png"))  # Cargamos una imagen de placeholder hasta que se obtenga la real
        placeholder = tk.Label(videodebugframe, image=render)
        placeholder.image = render
        placeholder.grid(row=1, column=0)

        prediccion = tk.StringVar(self.root, value="-")
        texto3 = tk.Label(self.root, textvariable=prediccion, font=("Arial",50))
        texto3.grid(row=2, column=1)

        imagenSkinFilter = Image.open("images/config.png")
        imagenSkinFilter = imagenSkinFilter.resize((68, 68),
                                                   Image.ANTIALIAS)  # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenSkinFilterRedimensionada = ImageTk.PhotoImage(imagenSkinFilter)
        bclose = tk.Button(buttonframe, text='Configuracion', image=imagenSkinFilterRedimensionada,
                           command=self.cerrarVentana)
        bclose.grid(row=0, column=2)

        def on_closing():  # Función para cerrar Tkinter y soltar la cámara
            cam.release()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        def show_frame():  # Esta función nos permite convertir la entrada de la webcam en imágenes válidas para tkinter
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            global imagenReconocidaImage  # Nos traemos la variable global con la nueva imagen de la predicción y la actualizamos
            global RGB_R
            global RGB_G
            global RGB_B

            RGB_R = self.R_RGB.get()
            RGB_G = self.G_RGB.get()
            RGB_B = self.B_RGB.get()

            main(
                frame)  # CAMBIO HECHO POR SERGIO, COMO LUEGO SE LE HACEN COSAS INTERMEDIAS, EMJOR PASARLO EN BGR Y LUEGO YA AL FINAL SE PASA A RGBA

            if (debug):
                imagen_dibujada = cv2image
            else:
                imagen_dibujada = applyMask(imagenReconocidaImage, cv2image)

            scale_percent_width = 85 * self.root.winfo_width() / 1280  # percent of original size
            scale_percent_height = 85 * self.root.winfo_height() / 720  # percent of original size
            scale_percent_width = scale_percent_width if scale_percent_width > 60 else 60
            scale_percent_height = scale_percent_height if scale_percent_height > 60 else 60
            width = int(imagen_dibujada.shape[1] * scale_percent_width / 100)
            height = int(imagen_dibujada.shape[0] * scale_percent_height / 100)
            dim = (width, height)
            # resize image
            imagen_dibujada = cv2.resize(imagen_dibujada, dim, interpolation=cv2.INTER_AREA)
            img = Image.fromarray(imagen_dibujada)

            imgtk = ImageTk.PhotoImage(image=img)
            video.imgtk = imgtk
            video.configure(image=imgtk)

            width = int(imagenReconocidaImage.shape[1] * scale_percent_width / 100)
            height = int(imagenReconocidaImage.shape[0] * scale_percent_height / 100)
            dim = (width, height)
            # resize image
            imagen_dibujada = cv2.resize(imagenReconocidaImage, dim, interpolation=cv2.INTER_AREA)
            imgAnalizada = Image.fromarray(imagen_dibujada)
            imgAnalizada = ImageTk.PhotoImage(image=imgAnalizada)
            placeholder.configure(image=imgAnalizada)
            placeholder.image = imgAnalizada
            self.dibujo = imagen_dibujada
            global prediccionText  # Nos traemoos la variable global con el nuevo texto de la predicción y lo actualizamos
            prediccion.set(prediccionText)

            self.root.after(10, show_frame)

        show_frame()  # Ejecutamos un frame
        self.root.mainloop()  # Bucle de Tkinter para generar la ventana y el contenido

    def cerrarVentana(self):
        self.root.destroy()
        launchWindow(True)

    def fdebug(self):
        global debug
        debug = not debug
        self.reset()

    def guardar(self):  # Cuando se hace click en guardar se llama a esta función
        print("Guardar pulsado")
        fileaddr = "savedImages/" + str(self.imageCounter) + "saved.png"
        # self.dibujo[self.dibujo>40] = 255 #hacer luego en cnn

        cv2.imwrite(fileaddr, self.dibujo)
        self.imageCounter += 1

    def reset(self):  # Cuando se hace click en reset se llama a esta función
        print("Reset pulsado")
        global imagenReconocidaImage
        imagenReconocidaImage = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        imagenReconocidaImage = cv2.cvtColor(imagenReconocidaImage, cv2.COLOR_BGR2RGBA)


class skinfilterGUI():
    def __init__(self):
        self.root = tk.Tk()  # Creamos la raiz de tkinter
        self.root.title('Reconocimiento SkinFilter')  # Ponemos título a la ventana
        self.root.geometry('1280x720')  # Definimos el tamaño

        self.frameCounter = 0

        self.root.columnconfigure(0, weight=1, minsize=240)
        self.root.columnconfigure(1, weight=1, minsize=240)
        self.root.columnconfigure(2, weight=1, minsize=240)

        self.root.rowconfigure(0, weight=1, minsize=720 / 8)
        self.root.rowconfigure(1, weight=1, minsize=720 / 8)

        video1frame = tk.Frame(self.root)
        video1frame.grid(row=0, column=0)
        texto1 = tk.Label(video1frame, text="Cámara")  # Creamos un texto y lo añadimos a la raiz
        texto1.grid(row=0, column=0)
        video1 = tk.Label(video1frame)  # AÑadimos el video1 a la raiz
        video1.grid(row=1, column=0)

        video2frame = tk.Frame(self.root)
        video2frame.grid(row=0, column=1)
        texto2 = tk.Label(video2frame, text="Máscara HSV")  # Creamos un texto y lo añadimos a la raiz
        texto2.grid(row=0, column=0)
        video2 = tk.Label(video2frame)  # AÑadimos el video2 a la raiz
        video2.grid(row=1, column=0)

        video3frame = tk.Frame(self.root)
        video3frame.grid(row=0, column=2)
        texto3 = tk.Label(video3frame, text="Máscara HSV aplicada")  # Creamos un texto y lo añadimos a la raiz
        texto3.grid(row=0, column=0)
        video3 = tk.Label(video3frame)  # AÑadimos el video3 a la raiz
        video3.grid(row=1, column=0)

        video4frame = tk.Frame(self.root)
        video4frame.grid(row=1, column=0)
        texto4 = tk.Label(video4frame, text="Filtro media")  # Creamos un texto y lo añadimos a la raiz
        texto4.grid(row=0, column=0)
        video4 = tk.Label(video4frame)  # AÑadimos el video3 a la raiz
        video4.grid(row=1, column=0)

        video5frame = tk.Frame(self.root)
        video5frame.grid(row=1, column=1)
        texto5 = tk.Label(video5frame, text="Erosión")  # Creamos un texto y lo añadimos a la raiz
        texto5.grid(row=0, column=0)
        video5 = tk.Label(video5frame)  # AÑadimos el video3 a la raiz
        video5.grid(row=1, column=0)

        video6frame = tk.Frame(self.root)
        video6frame.grid(row=1, column=2)
        texto6 = tk.Label(video6frame, text="Dilatación")  # Creamos un texto y lo añadimos a la raiz
        texto6.grid(row=0, column=0)
        video6 = tk.Label(video6frame)  # AÑadimos el video3 a la raiz
        video6.grid(row=1, column=0)

        # Definimos todos los sliders y los seteamos con el valor de las variables globales por defecto
        hsvframe = tk.LabelFrame(self.root, text="HSV")
        hsvframe.grid(row=8, column=0)

        self.h_min = tk.Scale(hsvframe, from_=0, to=179, orient=tk.HORIZONTAL)
        self.h_min.set(h_min_global)
        label_1 = tk.Label(hsvframe, text="h_min")
        label_1.grid(row=8, column=0)
        self.h_min.grid(row=8, column=1)

        self.h_max = tk.Scale(hsvframe, from_=0, to=179, orient=tk.HORIZONTAL)
        self.h_max.set(h_max_global)
        label_2 = tk.Label(hsvframe, text="h_max")
        label_2.grid(row=9, column=0)
        self.h_max.grid(row=9, column=1)

        self.s_min = tk.Scale(hsvframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.s_min.set(s_min_global)
        label_3 = tk.Label(hsvframe, text="s_min")
        label_3.grid(row=10, column=0)
        self.s_min.grid(row=10, column=1)

        self.s_max = tk.Scale(hsvframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.s_max.set(s_max_global)
        label_4 = tk.Label(hsvframe, text="s_max")
        label_4.grid(row=11, column=0)
        self.s_max.grid(row=11, column=1)

        self.v_min = tk.Scale(hsvframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.v_min.set(v_min_global)
        label_5 = tk.Label(hsvframe, text="v_min")
        label_5.grid(row=12, column=0)
        self.v_min.grid(row=12, column=1)

        self.v_max = tk.Scale(hsvframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.v_max.set(v_max_global)
        label_6 = tk.Label(hsvframe, text="v_max")
        label_6.grid(row=13, column=0)
        self.v_max.grid(row=13, column=1)

        # sliders erosion dilatacion y blur
        pruebasframe = tk.LabelFrame(self.root, text="Pruebas")
        pruebasframe.grid(row=8, column=1)

        # self.FMSize_B = tk.Scale(pruebasframe, from_=1, to=20, orient=tk.HORIZONTAL)
        # self.FMSize_B.set(FMSize[0])
        label_7 = tk.Label(pruebasframe, text="FMSize")
        label_7.grid(row=15, column=0)
        #        self.FMSize_B.grid(row=15, column=1)
        global FMSize
        global EKSize
        global EIteraciones
        global DKSize
        global DIteraciones

        #        EKSize_B3 = tk.Button(EKSizeframe, text='(3,3)',command=self.cerrarVentana)
        #       EKSize_B3.grid(row=0,column=0)
        #      EKSize_B5 = tk.Button(EKSizeframe, text='(5,5)',command=self.cerrarVentana)
        #     EKSize_B5.grid(row=0,column=1)
        FMSizeframe = tk.Frame(pruebasframe)
        FMSizeframe.grid(row=15, column=1)
        self.FMSize_valor = tk.IntVar()
        self.FMSize_valor.set(FMSize[0])
        tk.Radiobutton(FMSizeframe, text="(3,3)", variable=self.FMSize_valor, value=3, command=self.seleccionar).grid(
            row=0, column=0)
        tk.Radiobutton(FMSizeframe, text="(5,5)", variable=self.FMSize_valor, value=5, command=self.seleccionar).grid(
            row=0, column=1)
        tk.Radiobutton(FMSizeframe, text="(9,9)", variable=self.FMSize_valor, value=9, command=self.seleccionar).grid(
            row=0, column=2)

        # self.EKSize_B = tk.Scale(pruebasframe, from_=0, to=20, orient=tk.HORIZONTAL)
        # self.EKSize_B.set(EKSize[0])
        label_8 = tk.Label(pruebasframe, text="EKSize")
        label_8.grid(row=16, column=0)
        # self.EKSize_B.grid(row=16, column=1)
        EKSizeframe = tk.Frame(pruebasframe)
        EKSizeframe.grid(row=16, column=1)
        self.EKSize_valor = tk.IntVar()
        self.EKSize_valor.set(EKSize[0])
        tk.Radiobutton(EKSizeframe, text="(3,3)", variable=self.EKSize_valor, value=3, command=self.seleccionar).grid(
            row=0, column=0)
        tk.Radiobutton(EKSizeframe, text="(5,5)", variable=self.EKSize_valor, value=5, command=self.seleccionar).grid(
            row=0, column=1)
        tk.Radiobutton(EKSizeframe, text="(9,9)", variable=self.EKSize_valor, value=9, command=self.seleccionar).grid(
            row=0, column=2)

        self.EIteraciones_B = tk.Scale(pruebasframe, from_=0, to=20, orient=tk.HORIZONTAL)
        self.EIteraciones_B.set(EIteraciones)
        label_9 = tk.Label(pruebasframe, text="EIteraciones")
        label_9.grid(row=17, column=0)
        self.EIteraciones_B.grid(row=17, column=1)

        # self.DKSize_B = tk.Scale(pruebasframe, from_=0, to=20, orient=tk.HORIZONTAL)
        # self.DKSize_B.set(DKSize[0])
        label_10 = tk.Label(pruebasframe, text="DKSize")
        label_10.grid(row=18, column=0)
        # self.DKSize_B.grid(row=18, column=1)

        DKSizeframe = tk.Frame(pruebasframe)
        DKSizeframe.grid(row=18, column=1)
        self.DKSize_valor = tk.IntVar()
        self.DKSize_valor.set(DKSize[0])
        tk.Radiobutton(DKSizeframe, text="(3,3)", variable=self.DKSize_valor, value=3, command=self.seleccionar).grid(
            row=0, column=0)
        tk.Radiobutton(DKSizeframe, text="(5,5)", variable=self.DKSize_valor, value=5, command=self.seleccionar).grid(
            row=0, column=1)
        tk.Radiobutton(DKSizeframe, text="(9,9)", variable=self.DKSize_valor, value=9, command=self.seleccionar).grid(
            row=0, column=2)

        self.DIteraciones_B = tk.Scale(pruebasframe, from_=0, to=20, orient=tk.HORIZONTAL)
        self.DIteraciones_B.set(DIteraciones)
        label_11 = tk.Label(pruebasframe, text="DIteraciones")
        label_11.grid(row=19, column=0)
        self.DIteraciones_B.grid(row=19, column=1)

        imagenSkinFilter = Image.open("images/back.png")  # Botón para volver
        imagenSkinFilter = imagenSkinFilter.resize((68, 68),
                                                   Image.ANTIALIAS)  # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
        imagenSkinFilterRedimensionada = ImageTk.PhotoImage(imagenSkinFilter)
        bclose = tk.Button(self.root, text='volver', image=imagenSkinFilterRedimensionada, command=self.cerrarVentana)
        bclose.grid(row=8, column=2, rowspan=2)

        def on_closing():  # Función para cerrar Tkinter y soltar la cámara
            print("closing")
            cam.release()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        def show_frame():  # Se ejecuta una vez por frame
            self.frameCounter += 1
            if cam.get(cv2.CAP_PROP_FRAME_COUNT) == self.frameCounter:
                cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.frameCounter = 0

            _, img = cam.read()
            img = cv2.flip(img, 1)
            # self.root.winfo_width()
            # self.root.winfo_height()
            # escala = (452,339)
            # img = img.resize((452,339), Image.ANTIALIAS)
            scale_percent_width = 60 * self.root.winfo_width() / 1280  # percent of original size
            scale_percent_height = 60 * self.root.winfo_height() / 720  # percent of original size
            scale_percent_width = scale_percent_width if scale_percent_width > 60 else 60
            scale_percent_height = scale_percent_height if scale_percent_height > 60 else 60
            width = int(img.shape[1] * scale_percent_width / 100)
            height = int(img.shape[0] * scale_percent_height / 100)
            dim = (width, height)
            # resize image
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            img1 = Image.fromarray(img)

            imgtk1 = ImageTk.PhotoImage(image=img1)
            video1.imgtk = imgtk1
            video1.configure(image=imgtk1)

            imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            global h_min_global
            global h_max_global
            global s_min_global
            global s_max_global
            global v_min_global
            global v_max_global
            h_min_global = self.h_min.get()  # Almacenamos el valor de los sliders en las variables globales
            h_max_global = self.h_max.get()
            s_min_global = self.s_min.get()
            s_max_global = self.s_max.get()
            v_min_global = self.v_min.get()
            v_max_global = self.v_max.get()

            global FMSize
            global EKSize
            global EIteraciones
            global DKSize
            global DIteraciones

            # FMSize = (self.FMSize_B.get(),self.FMSize_B.get())
            # EKSize = (self.EKSize_B.get(),self.EKSize_B.get())
            EIteraciones = self.EIteraciones_B.get()
            # DKSize = (self.DKSize_B.get(),self.DKSize_B.get())
            DIteraciones = self.DIteraciones_B.get()

            lower = np.array([h_min_global, s_min_global, v_min_global])  # Calculamos la máscara
            upper = np.array([h_max_global, s_max_global, v_max_global])
            mask = cv2.inRange(imgHsv, lower, upper)

            result = cv2.bitwise_and(img, img, mask=mask)

            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            # escala = (640,480)

            # escala = (320,240)
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            img1 = Image.fromarray(cv2image)

            # img1 = img1.resize(escala, Image.ANTIALIAS) # Este icono nos hace falta redimensionarlo, al mismo tamaño que el icono anterior
            imgtk1 = ImageTk.PhotoImage(image=img1)
            video1.imgtk = imgtk1
            video1.configure(image=imgtk1)

            img2 = Image.fromarray(mask)
            # img2 = img2.resize((452,339), Image.ANTIALIAS)
            imgtk2 = ImageTk.PhotoImage(image=img2)
            video2.imgtk = imgtk2
            video2.configure(image=imgtk2)

            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
            img3 = Image.fromarray(result)
            imgtk3 = ImageTk.PhotoImage(image=img3)
            video3.imgtk3 = imgtk3
            video3.configure(image=imgtk3)

            filtro_media = cv2.blur(mask, FMSize)
            filtro_media = cv2.cvtColor(filtro_media, cv2.COLOR_BGR2RGBA)
            img4 = Image.fromarray(filtro_media)
            # img4 = img4.resize(escala, Image.ANTIALIAS)
            imgtk4 = ImageTk.PhotoImage(image=img4)
            video4.imgtk4 = imgtk4
            video4.configure(image=imgtk4)

            erosion_kernel = np.ones(getEKSize(), np.uint8)
            filtro_erosion = cv2.erode(filtro_media, erosion_kernel, iterations=getEIteraciones())
            filtro_erosion = cv2.cvtColor(filtro_erosion, cv2.COLOR_BGR2RGBA)
            img5 = Image.fromarray(filtro_erosion)
            # img5 = img5.resize(escala, Image.ANTIALIAS)
            imgtk5 = ImageTk.PhotoImage(image=img5)
            video5.imgtk5 = imgtk5
            video5.configure(image=imgtk5)

            dilation_kernel = np.ones(getDKSize(), np.uint8)
            filtro_dilatacion = cv2.dilate(filtro_erosion, dilation_kernel, iterations=getDIteraciones())
            filtro_dilatacion = cv2.cvtColor(filtro_dilatacion, cv2.COLOR_BGR2RGBA)
            img6 = Image.fromarray(filtro_dilatacion)
            # img6 = img6.resize(escala, Image.ANTIALIAS)
            imgtk6 = ImageTk.PhotoImage(image=img6)
            video6.imgtk6 = imgtk6
            video6.configure(image=imgtk6)

            self.root.after(10, show_frame)  # programamos el siguiente fotograma

        show_frame()  # Ejecutamos un frame
        self.root.mainloop()  # Bucle de Tkinter para generar la ventana y el contenido

    def cerrarVentana(self):  # Nos devuelve al programa principal
        self.root.destroy()
        launchWindow()

    def seleccionar(self):
        global FMSize
        global EKSize
        global DKSize
        FMSize = (self.FMSize_valor.get(), self.FMSize_valor.get())
        EKSize = (self.EKSize_valor.get(), self.EKSize_valor.get())
        DKSize = (self.DKSize_valor.get(), self.DKSize_valor.get())


def setPrediccionText(text):  # Esta función actualiza la variable global para que cambie en Tkinter. Recibe un String
    global prediccionText
    prediccionText = "Predicción " + text


def setImagenReconocida(
        array):  # Esta función actualiza la variable global para que cambie en Tkinter. Recibe un array de numpy
    global imagenReconocidaImage
    imagenReconocidaImage = array


def getSkinFilteredImage(frame):  # Recibe un fotograma le aplica el skinfilter y devuelve la máscara
    global h_min_global
    global h_max_global
    global s_min_global
    global s_max_global
    global v_min_global
    global v_max_global
    # print("h_min_global "+h_min_global)
    imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min_global, s_min_global, v_min_global])
    upper = np.array([h_max_global, s_max_global, v_max_global])
    mask = cv2.inRange(imgHsv, lower, upper)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return mask


####################################################################################################################################

# A partir de aquí lo que os interesa y podeis tocar

def main(fotograma):  # Este método main se ejecutará una vez por fotograma, aquí está toda la lógica del programa
    # El parámetro fotograma es, un fotograma xD hay que aplicar toda la lógica y funciones desde aquí
    # getSkinFilteredImage(frame) con esta funcion nos devolverá el filtro aplicado al fotograma pasado
    # NOTA IMPORTANTE : Para debuguear la imagen que esteis trabajando, usar la funcion setimagenreconocida, os la mostrará por pantalla aunque rompiendo la interfaz, hasta nuevo aviso será así
    # print("Fotograma")
    # a = media(fotograma)
    # b = skinfilter(a)
    # recortar(fotograma)
    # prediccion(fotograma)
    skinfiltered = getSkinFilteredImage(fotograma)  # ESTO HAY QUE ARREGLARLO PORQUE NO SALE COMO DEBERÍA
    # setPrediccionText("-") # Ejemplo de como cambiar el texto de la predicción
    # setImagenReconocida(np.zeros((40,40))*150) # Ejemplo de como cambiar la imagen de la predicción

    ############## Suavizado ###############
    global FMSize
    # filtro_media_size = FMSize;  #Función para que alberto haga la función y la enlace con los "botoncitos" los más comunes son (3,3) y (5,5)

    filtro_media = cv2.blur(skinfiltered,
                            FMSize)  # (3,3) sustituir por "filtro_media_size" cuando la función esté hecha

    ############### Erosión #########################

    # erosion_kernel_size = getEKSize(); #Función para determinar el tamaño del kernel y alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)

    erosion_kernel = np.ones(getEKSize(),
                             np.uint8)  # (3,3) sustituir por erosion_kernel_size cuando la función esté hecha)

    # iteraciones_erosion = getEIteraciones() #Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones.

    erosion = cv2.erode(filtro_media, erosion_kernel,
                        iterations=getEIteraciones())  # iterations = iteraciones cuando la función esté hecha

    # Nota: iteraciones = 0 -> no hay erosión

    ############### Dilatación ###################

    # dilation_kernel_size = getDKSize(); #Función para determinar el tamaño del kernel y Alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)

    dilation_kernel = np.ones(getDKSize(),
                              np.uint8)  # (3,3) sustituir por dilation_kernel_size cuando la función esté hecha)

    # iteraciones_dilation = getDIteraciones() #Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones.

    Dilation = cv2.dilate(erosion, dilation_kernel,
                         iterations=getDIteraciones())  # iterations = iteraciones cuando la función esté hecha

    # Nota: iteraciones = 0 -> no hay Dilatación

    ########### Imagen ya procesada ###########################

    # https: // stackoverflow.com / questions / 44588279 / find - and -draw - the - largest - contour - in -opencv - on - a - specific - color - python

    # OJO CAMBIO TEMPORAL DE SERGIO EN EL QUE ME SALTO LO QUE NO SEA HSV PARA TESTEAR:anulado ahora
    imgray = cv2.cvtColor(Dilation, cv2.COLOR_BGR2GRAY)
    #imgray=Dilation
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Asumimos que la mano es el contorno más grande, ya que estará en primer plano

    # AQUÍ PUEDE EXPLOTAR SI NO HAY VARIOS, MIRAR EL LEN O HACER TRY/EXECPTION
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        # https: // www.pyimagesearch.com / 2016 / 02 / 01 / opencv - center - of - contour /
        M = cv2.moments(c)  # M es el centroide
        try:
            cX = int(M["m10"] / M["m00"])  # estas sus coordenadas
            cY = int(M["m01"] / M["m00"])
        except:
            pass
        x, y, w, h = cv2.boundingRect(c)
        # draw the biggest contour (c) in green

        imagen_procesada = cv2.cvtColor(imgray, cv2.COLOR_BGR2RGB)

        try:
            cv2.circle(imagen_procesada, (cX, cY), 7, (255, 0, 0), -1)
        except:
            pass
        cv2.rectangle(imagen_procesada, (x, y), (x + w, y + h), (0, 255, 0), 2)

        hand_hull = cv2.convexHull(c,
                                   False)  # ponemos en false para que devuelva los indices de los puntos del contorno
        hand_hull_coordinates = cv2.convexHull(c, True)  # ponemos en true para que devuelva las coordenadas

        # IMPORTANTE!!!!!!!!!!!!!!! ESTE ES EL PUNTO QUE VAMOS A PINTAR(ASUMIDO COMO PUNTA DE DEDO)
        try:
            punto_mas_lejano = masLejano(hand_hull_coordinates, (cX, cY))
        except:
            pass

        # https: // opencv - python - tutroals.readthedocs.io / en / latest / py_tutorials / py_imgproc / py_contours / py_contour_features / py_contour_features.html

        # imagen_procesada[:] = 0
        # cv2.drawContours(imagen_procesada, [c], contourIdx=0, color=(0, 255, 0))
        # cv2.drawContours(imagen_procesada, [hand_hull], contourIdx=0, color=(255, 0, 0))
        drawing = np.zeros((imagen_procesada.shape[0], imagen_procesada.shape[1], 3), dtype=np.uint8)
        for i in range(len([c])):
            color = (255, 0, 0)
            # cv2.drawContours(imagen_procesada, [c], i, color)
            cv2.drawContours(imagen_procesada, [hand_hull], i, color, 2)

        cv2.circle(imagen_procesada, punto_mas_lejano, radius=10, color=(0, 255, 255),
                   thickness=-1)  # thickness -1 for filled circle

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
        cv2.circle(imagenReconocidaImage, punto_mas_lejano, radius=10, color=(RGB_R, RGB_G, RGB_B),
                   thickness=-1)  # thickness -1 for filled circle
        global debug
        if (debug):
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

        model_input = cv2.resize(imagenReconocidaImage, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)

        nuevaimagen = cv2.cvtColor(model_input, cv2.COLOR_RGBA2GRAY)
        nuevaimagen = np.reshape(nuevaimagen, newshape=(28, 28, 1))
        cv2.imwrite("savedImages/modelinput.png", nuevaimagen)
        prediction = model.predict(np.array([nuevaimagen, ]))
        print(f"prediction:{prediction}")
        maxElement = np.amax(prediction)
        result = np.where(prediction == np.amax(maxElement))
        global prediccionText
        if prediction[0, result[1][0]] > 0.9:
            print(f"valor:{str(result[1][0])}")
            valor = str(result[1][0])
            prediccionText = "Predicción:"+str(valor)
        else:
            prediccionText = "Predicción: -"

########### Funciones auxiliares procesamiento ##########

def getEKSize():
    return EKSize


# Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones en erosion.
def getEIteraciones():
    return EIteraciones


# Función para determinar el tamaño del kernel y Alberto lo enlace con los "botoncitos". Los más comunes son (3,3) y (5,5)
def getDKSize():
    return DKSize


# Función para que el usuario desde el panel de "botoncitos" pueda elegir el número de iteraciones en dilatacion.
def getDIteraciones():
    return DIteraciones


def launchWindow(skinfilter=False):
    if (skinfilter):
        mi_app = skinfilterGUI()  # Lanzamos la aplicación
    else:
        mi_app = AplicacionGUI()  # Lanzamos la aplicación


if __name__ == '__main__':  # Inicializamos la aplicación al estilo python
    launchWindow()
