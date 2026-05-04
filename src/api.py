from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from datetime import datetime
import os
import sys

# Importar funciones de la base de datos
sys.path.append(os.path.dirname(__file__))
from database import crear_tablas, insertar_modelo, insertar_noticia, insertar_prediccion, obtener_predicciones

# Inicializar app
app = FastAPI(
    title="CleanNews AI",
    description="API para detección de noticias falsas — Grupo 11",
    version="1.0.0"
)

# Rutas a los modelos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELO_PATH    = os.path.join(BASE_DIR, "../models/mejor_modelo.pkl")
TFIDF_PATH     = os.path.join(BASE_DIR, "../models/tfidf_vectorizer.pkl")
NOMBRE_PATH    = os.path.join(BASE_DIR, "../models/mejor_modelo_nombre.txt")

# Cargar modelo y vectorizador
with open(MODELO_PATH, "rb") as f:
    modelo = pickle.load(f)

with open(TFIDF_PATH, "rb") as f:
    tfidf = pickle.load(f)

with open(NOMBRE_PATH, "r") as f:
    nombre_modelo = f.read().strip()

# Crear tablas y registrar modelo en BD
crear_tablas()
ID_MODELO = insertar_modelo(
    nombre    = nombre_modelo,
    algoritmo = nombre_modelo.replace("_", " "),
    fecha     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

# Preprocesamiento
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))
stemmer    = PorterStemmer()

def limpiar_texto(texto):
    texto = str(texto).lower()
    texto = re.sub(r'http\S+|www\S+', '', texto)
    texto = re.sub(r'[^a-z\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    palabras = [stemmer.stem(p) for p in texto.split() if p not in stop_words]
    return " ".join(palabras)

# Modelos de entrada/salida
class NoticiaInput(BaseModel):
    titulo: str = ""
    texto: str

class PrediccionOutput(BaseModel):
    resultado:  str
    confianza:  float
    porcentaje: str
    mensaje:    str

# ──────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────

@app.get("/")
def root():
    return {
        "proyecto": "CleanNews AI",
        "grupo":    "Grupo 11 — Dennys y Kevin",
        "version":  "1.0.0",
        "docs":     "http://127.0.0.1:8000/docs"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "modelo": nombre_modelo
    }

@app.post("/predict", response_model=PrediccionOutput)
def predecir(noticia: NoticiaInput):
    # Limpiar y vectorizar
    content = limpiar_texto(noticia.titulo + " " + noticia.texto)
    vector  = tfidf.transform([content])

    # Predicción
    pred = modelo.predict(vector)[0]

    # Confianza
    if hasattr(modelo, "predict_proba"):
        prob = modelo.predict_proba(vector)[0]
        confianza = float(max(prob))
    else:
        confianza = 0.99 if pred == 1 else 0.01

    # Umbral de incertidumbre (definido en el PDF)
    if confianza < 0.50:
        resultado = "INCIERTO"
        mensaje   = "El modelo no está seguro. Revisa la noticia manualmente."
    elif pred == 1:
        resultado = "REAL"
        mensaje   = "La noticia parece ser real."
    else:
        resultado = "FAKE"
        mensaje   = "La noticia parece ser falsa."

    # Guardar en base de datos
    id_noticia = insertar_noticia(
        titulo = noticia.titulo or "Sin título",
        texto  = noticia.texto,
        fecha  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    insertar_prediccion(
        prediccion = resultado,
        confianza  = confianza,
        fecha      = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        id_modelo  = ID_MODELO,
        id_noticia = id_noticia
    )

    return PrediccionOutput(
        resultado  = resultado,
        confianza  = confianza,
        porcentaje = f"{confianza*100:.1f}%",
        mensaje    = mensaje
    )

@app.get("/predicciones")
def listar_predicciones():
    rows = obtener_predicciones()
    return [
        {
            "id":         r[0],
            "titulo":     r[1],
            "prediccion": r[2],
            "confianza":  f"{r[3]*100:.1f}%",
            "fecha":      r[4],
            "modelo":     r[5]
        }
        for r in rows
    ]