# 📰 Sistema de Detección de Noticias Falsas

## 📌 Descripción del proyecto
Este proyecto consiste en un sistema capaz de analizar el texto de una noticia y clasificarla como **REAL o FAKE** utilizando técnicas de **Procesamiento de Lenguaje Natural (NLP)** y **Machine Learning**.

El sistema incluye todo el flujo:
- Descarga de datos
- Limpieza y procesamiento del texto
- Entrenamiento de modelos
- API para hacer predicciones
- Dashboard para visualizar resultados

El objetivo es ayudar a detectar contenido engañoso de forma automática.

---

## 👥 Integrantes
- **Dennys** → Data Engineer + NLP Engineer  
- **Kevin** → ML Engineer + Platform & BI  

---

## 🏗️ Arquitectura resumida
El sistema está dividido en 4 partes principales:

1. **Datos**
   - Datasets de Kaggle, LIAR y FakeNewsNet

2. **Procesamiento NLP**
   - Limpieza de texto
   - Tokenización
   - Vectorización (TF-IDF)

3. **Modelo de Machine Learning**
   - Entrenamiento de modelos (Logistic Regression, Random Forest, SVM)
   - Evaluación con métricas
   - Registro con MLflow

4. **Resultados**
   - API REST con FastAPI (`/predict`)
   - Base de datos SQLite
   - Dashboard en Power BI

Flujo:
Datos → Procesamiento → Modelo → API / Dashboard

---

## ⚙️ Cómo ejecutar (provisional)
> ⚠️ El proyecto aún está en desarrollo, estos pasos pueden cambiar.

1. Clonar el repositorio
```bash
git clone <repo-url>
cd repo
```

2. Crear entorno
```bash
conda env create -f environment.yml
conda activate fake-news-env
```

3. Ejecutar pipeline de datos
```bash
python src/pipeline.py
```

4. Entrenar modelo
```bash
python src/train.py
```

5. Ejecutar API
```bash
uvicorn src.api:app --reload
```

6. Acceder a la documentación
```bash
http://localhost:8000/docs
```

---

## 🛠️ Tecnologías

### Lenguaje
- Python 3.11  

### NLP
- NLTK  
- spaCy  

### Machine Learning
- scikit-learn  

### Deep Learning (opcional)
- TensorFlow / Keras  

### Gestión de experimentos
- MLflow  

### Manipulación de datos
- Pandas  
- NumPy  

### API
- FastAPI  

### Base de datos
- SQLite  

### Visualización
- Power BI  

### Control de versiones
- Git + GitHub  

### Entorno
- Conda  
