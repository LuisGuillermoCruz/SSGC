from flask import Flask
import flask
from flask_cors import CORS

app = Flask(__name__)# instanciamos la app
CORS(app)

#Definiendo rutas
@app.route("/")
def hello_word():
    return "Hello, Word!"

@app.route("/predict")
def predict():
    return "Predicciones"

#Ejecutando la aplicacion
if __name__ == "__main__":
    app.run()