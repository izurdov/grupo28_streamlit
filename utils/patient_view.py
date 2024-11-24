import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Dashboard Paciente", layout="wide")

current_time = datetime.now()
yesterday_sleep = np.random.uniform(low=4, high=9, size=(24,))
x_axis = list(range(0, 24))

chat_messages = [
    "Doctor: ¡Hola! ¿Cómo estás hoy?",
    "Paciente: Hola doctor, estoy bien gracias.",
    "Doctor: Perfecto. Esperaba eso. ¿Dormiste bien anoche?"
]

def plot_sleep_analysis(x_axis, y_data):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_axis, y_data, marker='o', linestyle='-')
    ax.set_title('Análisis de Sueño - Ayer')
    ax.set_xlabel('Hora del día')
    ax.set_ylabel('Calidad del sueño (escala 1-10)')
    ax.grid(True)
    return fig

user_name = "Paciente Kike"
st.title(f"Bienvenido, {user_name}")

# Mensajes sobre la cita y los mensajes pendientes
appointment_message = "Cita Martes 17/4 a las 10:00 AM"
messages_count = np.random.randint(3, 8)

st.write(appointment_message)
st.write(f"Tienes {messages_count} mensajes sin leer.")

sleep_analysis_plot = plot_sleep_analysis(x_axis, yesterday_sleep)
st.pyplot(sleep_analysis_plot)

col1, col2 = st.columns(2)

with col1:
    if st.button('Llamar al Doctor'):
        st.success("Estás en llamada con el doctor.")

with col2:
    if st.button('Videollamada con el Doctor'):
        st.success("Iniciando videollamada...")

st.sidebar.header("Chat con tu médico")
for message in chat_messages:
    st.sidebar.write(message)

if len(chat_messages) < 10:
    new_message = "Paciente: Gracias por preguntar, me siento bien."
    chat_messages.append(new_message)