# 🕵️ CleanNews AI — Detector de Noticias Falsas
**Grupo 11 · Dennys y Kevin · IFP Big Data 2026**

Sistema de detección automática de noticias falsas usando NLP y Machine Learning.
Clasifica una noticia como **REAL**, **FAKE** o **INCIERTO** con un porcentaje de confianza.

---

## 👥 Integrantes

| Integrante | Rol |
|---|---|
| Dennys | Data Engineer + NLP Engineer |
| Kevin | ML Engineer + Platform & BI |

---

## 🏗️ Arquitectura

```
Datos (Kaggle CSV) → Preprocesamiento NLP → Entrenamiento ML → API FastAPI → Dashboard Streamlit
                                                                           ↓
                                                                      SQLite DB
```

---

## 📁 Estructura del proyecto

```
tfg-fakenews/
├── data/
│   ├── True.csv                  ← Descargar de Kaggle (ver abajo)
│   ├── Fake.csv                  ← Descargar de Kaggle (ver abajo)
│   ├── dataset_combinado.csv
│   ├── dataset_preprocesado.csv
│   └── cleannews.db              ← Base de datos SQLite
├── models/
│   ├── mejor_modelo.pkl
│   ├── tfidf_vectorizer.pkl
│   └── mejor_modelo_nombre.txt
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_preprocesamiento.ipynb
│   ├── 03_ml_clasico.ipynb
│   └── 04_mlflow.ipynb
├── outputs/                      ← Gráficas y capturas
├── src/
│   ├── api.py                    ← API FastAPI
│   ├── dashboard.py              ← Dashboard Streamlit
│   └── database.py               ← Base de datos SQLite
├── tests/
│   └── test_api.py               ← 7 tests pytest
├── mlflow_runs/                  ← Experimentos MLflow
├── requirements.txt
└── README.md
```

---

## 📊 Resultados del modelo

| Modelo | Accuracy | F1-Score |
|---|---|---|
| Random Forest | **99.79%** | 🏆 Mejor |
| Linear SVM | 99.59% | |
| Logistic Regression | 99.08% | |
| Naive Bayes | 95.21% | |

> ⚠️ Resultados obtenidos sobre el dataset de entrenamiento (entorno controlado).
> El modelo presenta sesgo de dominio hacia noticias de Reuters 2016-2018.

---

## 🚀 Instalación y uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/leFreeh/IFP_PROYECTO_BIG_DATA.git
cd IFP_PROYECTO_BIG_DATA
```

### 2. Descargar el dataset
Descargar manualmente desde Kaggle:
👉 https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

Colocar `True.csv` y `Fake.csv` en la carpeta `/data/`.

### 3. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar los notebooks en orden
```
01_exploracion.ipynb
02_preprocesamiento.ipynb
03_ml_clasico.ipynb
04_mlflow.ipynb
```

### 6. Arrancar la API
```bash
uvicorn src.api:app --reload
```
Disponible en: `http://127.0.0.1:8000`  
Documentación: `http://127.0.0.1:8000/docs`

### 7. Arrancar el dashboard
En una terminal nueva:
```bash
streamlit run src/dashboard.py
```
Disponible en: `http://localhost:8501`

### 8. Ver experimentos MLflow (opcional)
En una terminal nueva:
```bash
mlflow ui --backend-store-uri mlflow_runs
```
Disponible en: `http://127.0.0.1:5000`

---

## ✅ Tests

Con la API corriendo ejecuta:
```bash
pytest tests/ -v
```
```
7 passed in Xs ✅
```

---

## 🛠️ Tecnologías

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.12 |
| NLP | NLTK |
| ML | scikit-learn |
| Experimentos | MLflow |
| Datos | Pandas, NumPy |
| API | FastAPI + Uvicorn |
| Base de datos | SQLite |
| Dashboard | Streamlit |
| Tests | pytest |
| Versiones | Git + GitHub |

---

## ⚠️ Limitaciones conocidas

- El modelo está entrenado con noticias políticas de EE.UU. (2016-2018)
- Las noticias REAL del dataset pertenecen mayoritariamente a Reuters
- No funciona con noticias en español
- No analiza imágenes, vídeos ni redes sociales en tiempo real

---

## 📄 Licencia del dataset

El dataset de Kaggle tiene licencia **CC0 (Dominio Público)**.