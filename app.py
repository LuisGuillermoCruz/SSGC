from flask import Flask, render_template
import flask
from flask_cors import CORS
import torch
import io 
from flask import current_app as app 
from flask import send_file
import ntpath
from shutil import rmtree
from flask import Flask, render_template, request
from random import sample
#Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename 
import os
from os import remove



app = Flask(__name__)# instanciamos la app
CORS(app)


def stringAleatorio():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

#Definiendo rutas
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['GET', 'POST'])
def predict():


    if request.method == 'POST':

        #Script para archivo
        file     = request.files['archivo']
        basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename) #Nombre original del archivo
            
        #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension           = os.path.splitext(filename)[1]
        nuevoNombreFile     = stringAleatorio() + extension

        print(filename)
     
        upload_path = os.path.join (basepath, 'static', nuevoNombreFile) 
        file.save(upload_path)
    
    #Eliminamos la ultima prediccion
    path_detect_1 = f"{basepath}/runs/detect/exp"

    if path_detect_1:
        rmtree(path_detect_1)

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    # Images
    img = f'{basepath}/static/{nuevoNombreFile}'
    name = ntpath.basename(img)

    # Inference
    results = model(img)
    results.save()

    # Results
    cadena = results.print()
    print(type(cadena))
    filename = f'{basepath}/runs/detect/exp/{nuevoNombreFile}'

    #Removiendo el primero archivo que se subio de la carpeta static
    #remove(f"C:/Users/luisg/OneDrive/Desktop/SS/SSGC/static/{filename}")

    return send_file(filename, mimetype='image/jpg')


#Ejecutando la aplicacion
if __name__ == "__main__":
    app.run()