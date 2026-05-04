import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

# ──────────────────────────────────────────
# TEST 1 — API está corriendo
# ──────────────────────────────────────────
def test_api_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "modelo" in data

# ──────────────────────────────────────────
# TEST 2 — Root endpoint
# ──────────────────────────────────────────
def test_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert "proyecto" in data
    assert data["proyecto"] == "CleanNews AI"

# ──────────────────────────────────────────
# TEST 3 — Predicción noticia FAKE
# ──────────────────────────────────────────
def test_predict_fake():
    payload = {
        "titulo": "SHOCKING: Hillary Clinton arrested by FBI agents",
        "texto": "In what many are calling the biggest political scandal in American history, former Secretary of State Hillary Clinton was arrested early Tuesday morning by a team of FBI agents at her Chappaqua, New York home. Sources close to the investigation say the arrest is related to thousands of deleted emails containing classified information about a secret globalist agenda. President Trump confirmed the news on his personal website saying justice has finally been served. Mainstream media is refusing to cover this story because they are part of the deep state cover up. Share this article before it gets deleted by the liberal social media censors who do not want the truth to come out."
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resultado" in data
    assert "confianza" in data
    assert "porcentaje" in data
    assert data["resultado"] == "FAKE"
    assert data["confianza"] > 0.5

# ──────────────────────────────────────────
# TEST 4 — Predicción devuelve campos correctos
# ──────────────────────────────────────────
def test_predict_response_fields():
    payload = {
        "titulo": "Test noticia",
        "texto": "This is a test article to verify that the API returns all the required fields in the response correctly."
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resultado"  in data
    assert "confianza"  in data
    assert "porcentaje" in data
    assert "mensaje"    in data

# ──────────────────────────────────────────
# TEST 5 — Resultado es uno de los valores válidos
# ──────────────────────────────────────────
def test_predict_valid_resultado():
    payload = {
        "titulo": "Breaking news today",
        "texto": "This is a sample news article used to test that the prediction result is always one of the three valid values expected from the classification system."
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["resultado"] in ["REAL", "FAKE", "INCIERTO"]

# ──────────────────────────────────────────
# TEST 6 — Confianza entre 0 y 1
# ──────────────────────────────────────────
def test_predict_confianza_rango():
    payload = {
        "titulo": "Economy news",
        "texto": "The stock market closed higher on Friday as investors reacted positively to the latest jobs report showing strong employment growth across multiple sectors of the economy including technology and healthcare."
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data["confianza"] <= 1.0

# ──────────────────────────────────────────
# TEST 7 — Historial de predicciones
# ──────────────────────────────────────────
def test_listar_predicciones():
    response = requests.get(f"{BASE_URL}/predicciones")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)