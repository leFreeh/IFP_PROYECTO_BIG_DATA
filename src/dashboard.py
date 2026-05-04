import streamlit as st
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# ──────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────
API_URL = "http://127.0.0.1:8000"
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/cleannews.db")

st.set_page_config(
    page_title="CleanNews AI",
    page_icon="🕵️",
    layout="wide"
)

# ──────────────────────────────────────────
# FUNCIONES
# ──────────────────────────────────────────
def obtener_predicciones_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("""
            SELECT p.id_prediccion, n.titulo, p.prediccion, 
                   p.confianza, p.fecha, m.nombre
            FROM Prediccion p
            JOIN News n   ON p.id_noticia = n.id_noticia
            JOIN Modelo m ON p.id_modelo  = m.id_modelo
            ORDER BY p.fecha DESC
        """, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def color_resultado(val):
    if val == "REAL":
        return "background-color: #d4edda; color: #155724"
    elif val == "FAKE":
        return "background-color: #f8d7da; color: #721c24"
    else:
        return "background-color: #fff3cd; color: #856404"

# ──────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────
st.title("🕵️ CleanNews AI — Dashboard")
st.caption("Sistema de Detección de Noticias Falsas · Grupo 11 · IFP Big Data 2026")

# Estado de la API
try:
    r = requests.get(f"{API_URL}/health", timeout=3)
    if r.status_code == 200:
        data = r.json()
        st.success(f"✅ API conectada · Modelo activo: **{data['modelo'].replace('_', ' ')}**")
    else:
        st.error("❌ API no responde correctamente")
except:
    st.error("❌ API no disponible. Asegúrate de que está corriendo en http://127.0.0.1:8000")

st.divider()

# ──────────────────────────────────────────
# TABS
# ──────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Analizar Noticia", "📊 Estadísticas", "📋 Historial"])

# ──────────────────────────────────────────
# TAB 1 — ANALIZAR NOTICIA
# ──────────────────────────────────────────
with tab1:
    st.subheader("Analiza una noticia")
    st.caption("Introduce el texto de la noticia para clasificarla como REAL, FAKE o INCIERTO")

    titulo = st.text_input("Titular (opcional)")
    texto  = st.text_area("Texto de la noticia", height=200,
                          placeholder="Pega aquí el cuerpo de la noticia... (mínimo 100 palabras para mejor precisión)")

    if st.button("🔍 Analizar", type="primary"):
        if len(texto.strip()) < 20:
            st.warning("⚠️ El texto es demasiado corto. Añade más contenido.")
        else:
            with st.spinner("Analizando..."):
                try:
                    response = requests.post(
                        f"{API_URL}/predict",
                        json={"titulo": titulo, "texto": texto}
                    )
                    result = response.json()

                    col1, col2 = st.columns(2)

                    with col1:
                        if result["resultado"] == "REAL":
                            st.success(f"## ✅ {result['resultado']}")
                        elif result["resultado"] == "FAKE":
                            st.error(f"## 🚨 {result['resultado']}")
                        else:
                            st.warning(f"## ⚠️ {result['resultado']}")

                        st.metric("Confianza", result["porcentaje"])
                        st.info(result["mensaje"])

                    with col2:
                        # Gauge de confianza
                        fig, ax = plt.subplots(figsize=(4, 3))
                        color = "#2ecc71" if result["resultado"] == "REAL" else \
                                "#e74c3c" if result["resultado"] == "FAKE" else "#f39c12"
                        ax.barh(["Confianza"], [result["confianza"]], color=color)
                        ax.barh(["Confianza"], [1 - result["confianza"]],
                                left=[result["confianza"]], color="#ecf0f1")
                        ax.set_xlim(0, 1)
                        ax.set_title("Nivel de confianza")
                        ax.axvline(x=0.50, color="gray", linestyle="--", alpha=0.5)
                        st.pyplot(fig)

                except Exception as e:
                    st.error(f"Error al conectar con la API: {e}")

# ──────────────────────────────────────────
# TAB 2 — ESTADÍSTICAS
# ──────────────────────────────────────────
with tab2:
    st.subheader("Estadísticas de predicciones")

    df = obtener_predicciones_db()

    if df.empty:
        st.info("Todavía no hay predicciones. Analiza algunas noticias primero.")
    else:
        # Métricas generales
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total analizadas", len(df))
        col2.metric("REAL",     len(df[df["prediccion"] == "REAL"]))
        col3.metric("FAKE",     len(df[df["prediccion"] == "FAKE"]))
        col4.metric("INCIERTO", len(df[df["prediccion"] == "INCIERTO"]))

        st.divider()

        col1, col2 = st.columns(2)

        # Gráfica de distribución
        with col1:
            st.markdown("**Distribución de resultados**")
            conteo = df["prediccion"].value_counts()
            colores = {"REAL": "#2ecc71", "FAKE": "#e74c3c", "INCIERTO": "#f39c12"}
            fig, ax = plt.subplots()
            ax.pie(conteo.values,
                   labels=conteo.index,
                   colors=[colores.get(k, "#95a5a6") for k in conteo.index],
                   autopct="%1.1f%%")
            st.pyplot(fig)

        # Confianza media por resultado
        with col2:
            st.markdown("**Confianza media por resultado**")
            confianza_media = df.groupby("prediccion")["confianza"].mean()
            fig, ax = plt.subplots()
            bars = ax.bar(confianza_media.index, confianza_media.values,
                          color=[colores.get(k, "#95a5a6") for k in confianza_media.index])
            ax.set_ylim(0, 1)
            ax.set_ylabel("Confianza media")
            for bar, val in zip(bars, confianza_media.values):
                ax.text(bar.get_x() + bar.get_width()/2, val + 0.01,
                        f"{val:.0%}", ha="center")
            st.pyplot(fig)

# ──────────────────────────────────────────
# TAB 3 — HISTORIAL
# ──────────────────────────────────────────
with tab3:
    st.subheader("Historial de predicciones")

    df = obtener_predicciones_db()

    if df.empty:
        st.info("Todavía no hay predicciones registradas.")
    else:
        df["confianza"] = df["confianza"].apply(lambda x: f"{x*100:.1f}%")
        df.columns = ["ID", "Titular", "Resultado", "Confianza", "Fecha", "Modelo"]

        st.dataframe(
            df.style.applymap(color_resultado, subset=["Resultado"]),
            use_container_width=True,
            hide_index=True
        )