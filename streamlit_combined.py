import streamlit as st
import cv2
import sounddevice as sd
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# Configuración inicial
st.set_page_config(page_title="Sistema Médico", page_icon="⚕️", layout="wide")

# Datos de usuarios
users_dict = {
    'javier': {'password': 'pass_javier', 'tipo': 'doctor'},
    'paciente': {'password': 'pass_paciente', 'tipo': 'paciente'}
}

# Variables de sesión
if "user_logged" not in st.session_state:
    st.session_state.user_logged = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None
if "video_call_active" not in st.session_state:
    st.session_state.video_call_active = False
if "audio_call_active" not in st.session_state:
    st.session_state.audio_call_active = False

# Datos de ejemplo
data = pd.DataFrame({
    "Paciente": ["Paciente A", "Paciente B", "Paciente C", "Paciente D", "Paciente E"],
    "Edad": [30, 45, 50, 40, 60],
    "Riesgo de Recaída (%)": [20, 65, 80, 50, 90],
    "Evaluación Cognitiva": [85, 70, 60, 75, 50]
})

# Función: Generar PDF del informe
def generate_report(patient_name):
    filename = f"informe_{patient_name.replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(f"Informe Clínico: {patient_name}", styles["Title"]),
        Spacer(1, 24),
        Paragraph(f"Edad: {data[data['Paciente'] == patient_name]['Edad'].values[0]}", styles["BodyText"]),
        Paragraph(f"Riesgo de Recaída: {data[data['Paciente'] == patient_name]['Riesgo de Recaída (%)'].values[0]}%", styles["BodyText"]),
        Paragraph(f"Evaluación Cognitiva: {data[data['Paciente'] == patient_name]['Evaluación Cognitiva'].values[0]}%", styles["BodyText"]),
    ]
    doc.build(story)
    return filename

# Función: Manejo de videollamada
def iniciar_videollamada():
    st.title("🎥 Videollamada Activa")
    cap = cv2.VideoCapture(0)
    st.session_state.video_call_active = True

    while st.session_state.video_call_active:
        ret, frame = cap.read()
        if not ret:
            st.error("No se pudo acceder a la cámara.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, channels="RGB")
        if st.button("Colgar Videollamada"):
            st.session_state.video_call_active = False

    cap.release()
    st.success("Videollamada finalizada.")

# Función: Manejo de llamada de audio
def iniciar_llamada_audio():
    st.title("📞 Llamada Activa")
    st.info("Transmitiendo audio...")
    st.session_state.audio_call_active = True

    if st.button("Colgar Llamada"):
        st.session_state.audio_call_active = False
        st.success("Llamada finalizada.")

# Función: Gráficos
def mostrar_graficos():
    st.subheader("📊 Resumen Gráfico")
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].bar(data["Paciente"], data["Riesgo de Recaída (%)"], color="blue")
    ax[0].set_title("Riesgo de Recaída (%)")
    ax[1].bar(data["Paciente"], data["Evaluación Cognitiva"], color="green")
    ax[1].set_title("Evaluación Cognitiva")
    st.pyplot(fig)

# Función: Chat
def mostrar_chat():
    st.subheader("💬 Chat Directo")
    for chat in st.session_state.chat_messages:
        st.markdown(f"**{chat['sender']}:** {chat['message']}")

    with st.form("chat_form"):
        message = st.text_input("Escribe aquí tu mensaje:")
        if st.form_submit_button("Enviar") and message:
            sender = "Doctor" if st.session_state.user_logged["tipo"] == "doctor" else "Paciente"
            st.session_state.chat_messages.append({"sender": sender, "message": message})

# Función: Login
def login_user(username, password):
    if username in users_dict and users_dict[username]["password"] == password:
        st.session_state.user_logged = users_dict[username]
        st.session_state.page = "doctor" if users_dict[username]["tipo"] == "doctor" else "paciente"
        return True
    return False

# Funciones para el rol de Doctor
def doctor_dashboard():
    st.title("Panel del Doctor")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 Listado de Pacientes")
        gravedad = st.slider("Gravedad mínima (%)", min_value=0, max_value=100, value=50, step=5)
        filtrados = data[data["Riesgo de Recaída (%)"] >= gravedad]
        st.dataframe(filtrados)

        paciente = st.selectbox("Selecciona un paciente", filtrados["Paciente"])
        if st.button("Visualizar Información"):
            st.session_state.selected_patient = paciente

        if st.session_state.selected_patient:
            st.subheader(f"🩺 Información de {st.session_state.selected_patient}")
            info = data[data["Paciente"] == st.session_state.selected_patient].iloc[0]
            st.write(f"**Edad:** {info['Edad']} años")
            st.write(f"**Riesgo de Recaída:** {info['Riesgo de Recaída (%)']}%")
            st.write(f"**Evaluación Cognitiva:** {info['Evaluación Cognitiva']}%")
            if st.button("Generar Informe"):
                filename = generate_report(st.session_state.selected_patient)
                st.success(f"Informe generado: [Descargar {filename}](./{filename})")

    with col2:
        st.subheader("📅 Citas Programadas")
        if st.session_state.appointments:
            for appointment in st.session_state.appointments:
                st.markdown(f"- {appointment['fecha']} a las {appointment['hora']} con {appointment['paciente']}")
        else:
            st.info("No hay citas programadas.")

    mostrar_graficos()
    mostrar_chat()

    if st.button("Cerrar sesión"):
        st.session_state.page = "login"

# Funciones para el rol de Paciente
def patient_dashboard():
    st.title("Vista del Paciente")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Datos del Paciente")
        st.write(f"Horas de sueño (h): 8.34")
        st.write(f"Estado emocional: 🙂")
        st.subheader("📞 Opciones de Contacto")
        if st.button("📞 Llamar al Doctor"):
            iniciar_llamada_audio()
        if st.button("🎥 Videollamada con el Doctor"):
            iniciar_videollamada()

    with col2:
        mostrar_chat()

    if st.button("Cerrar sesión"):
        st.session_state.page = "login"

# Navegación entre roles
if st.session_state.page == "login":
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar") and login_user(username, password):
        st.success("Inicio de sesión exitoso.")
elif st.session_state.page == "doctor":
    doctor_dashboard()
elif st.session_state.page == "paciente":
    patient_dashboard()