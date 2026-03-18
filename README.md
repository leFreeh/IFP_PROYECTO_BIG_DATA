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

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd repo
