
# External packages
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx,get_script_run_ctx
from subprocess import Popen

import speech_recognition as sr
import librosa
import numpy as np
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from pydub import AudioSegment


# 1. Función para convertir audio a texto
def audio_a_texto(ruta_audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(ruta_audio) as source:
        audio_data = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio_data, language="es-ES")
            return texto
        except sr.UnknownValueError:
            return "No se pudo transcribir el audio."
        except sr.RequestError as e:
            return f"Error en el reconocimiento de voz: {e}"

# 2. Función para detectar emociones en audio
def detectar_emociones(ruta_audio):
    # Cargar el archivo de audio
    y, sr_rate = librosa.load(ruta_audio, sr=None)
    # Extraer características como el RMS (Root Mean Square)
    rms = np.mean(librosa.feature.rms(y=y))
    # Clasificar emociones de manera básica según intensidad (puedes reemplazar con modelos avanzados)
    if rms > 0.02:
        return "Emoción: excitación o estrés."
    else:
        return "Emoción: calma o neutral."

# 3. Procesamiento de texto con PLN
def predecir_brote(texto, modelo, vectorizador):
    texto_limpio = texto.lower()
    texto_vectorizado = vectorizador.transform([texto_limpio])
    prediccion = modelo.predict(texto_vectorizado)
    probabilidad = modelo.predict_proba(texto_vectorizado)
    if prediccion[0] == 1:
        return "Alerta: posible brote psicótico. Probabilidad: {:.2f}%".format(probabilidad[0][1] * 100)
    else:
        return "Texto normal. Probabilidad: {:.2f}%".format(probabilidad[0][0] * 100)

# 4. Entrenamiento básico de modelo de texto
textos = [
    "Todo está bien, estoy feliz.",
    "Escucho voces que me dicen cosas.",
    "Tengo miedo, me persiguen todo el tiempo.",
    "Hoy fue un día productivo en el trabajo.",
    "Siento que mi mente está dividida en mil pedazos.",
]

etiquetas = [0, 1, 1, 0, 1]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(textos)
modelo_texto = MultinomialNB()
modelo_texto.fit(X, etiquetas)

# 5. Sistema completo
def analizar_audio(ruta_audio):
    st.write("1. Análisis del audio...")
    emociones = detectar_emociones(ruta_audio)
    st.write(emociones)

    st.write("\n2. Transcripción de audio a texto...")
    texto = audio_a_texto(ruta_audio)
    st.write(f"Texto transcrito: {texto}")

    if texto != "No se pudo transcribir el audio.":
        st.write("\n3. Análisis del texto...")
        resultado_texto = predecir_brote(texto, modelo_texto, vectorizer)
        st.write(resultado_texto)

# Ruta al archivo de audio de prueba
#wav_audio = AudioSegment.from_file("audio2.mp4", format="mp4")
#wav_audio.export("audio2.wav", format="wav")
#Demos análisis
#ruta_audio_prueba = "audio2.wav"
#analizar_audio(ruta_audio_prueba)

st.set_page_config(
    page_title="Grupo 28",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Logo
#st.logo("RUTALOGO", size="large", link=None, icon_image=None)
#st.logo( "/Users/jorgeoyagaorus/Desktop/GRUPO28/img/Logo.png",
#    size='large',
#    link="https://grupo28-app.streamlit.io",
#    icon_image="/Users/jorgeoyagaorus/Desktop/GRUPO28/img/Logo.png",
#)

# Main page heading
st.title("Proyecto grupo 28")

# Sidebar
st.sidebar.header("Dashboard")

st.header("Pacientes", divider=True)

#audio = st.file_uploader("Upload an audio file", type=["mp3"])
audio = st.file_uploader("Upload an audio file")


if audio is not None:
   #analizar_audio(audio.name) 
   analizar_audio("/Users/jorgeoyagaorus/Desktop/GRUPO28/grupo28_streamlit-main/audio1.wav")
