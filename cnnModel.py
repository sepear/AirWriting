#TODO: Aquí el modelo predictivo; recibe imagen y devuelve caracter
import keras

model = keras.models.load_model('cnnModel.h5')

prediccionText = "Predicción:" # Variable para comunicarnos con Tkinter
