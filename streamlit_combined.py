
import streamlit as st
import pandas as pd
import time
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# Configuración inicial
st.set_page_config(page_title="Aplicación Médica", page_icon="🩺", layout="wide")

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
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# Datos de ejemplo
data = pd.DataFrame({
    "Paciente": ["Paciente A", "Paciente B", "Paciente C", "Paciente D", "Paciente E"],
    "Riesgo de Recaída (%)": [20, 65, 80, 50, 90],
    "Evaluación Cognitiva (%)": [85, 70, 60, 75, 50]
})

# Función: Generar informe en PDF
def generate_report(patient_name):
    filename = f"informe_{patient_name.replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(f"Informe Clínico: {patient_name}", styles["Title"]),
        Spacer(1, 24),
        Paragraph("Este es un informe clínico generado automáticamente.", styles["BodyText"]),
        Spacer(1, 12),
    ]
    doc.build(story)
    add_alert(f"Informe generado para {patient_name}: {filename}", "success")
    return filename

# Función: Añadir alerta al sistema
def add_alert(message, alert_type="info", duration=5):
    expiration_time = time.time() + duration
    st.session_state.alerts.append({"message": message, "type": alert_type, "expires": expiration_time})

# Función: Renderizar alertas activas
def render_alerts():
    current_time = time.time()
    st.session_state.alerts = [
        alert for alert in st.session_state.alerts if alert["expires"] > current_time
    ]
    for alert in st.session_state.alerts:
        if alert["type"] == "info":
            st.info(alert["message"])
        elif alert["type"] == "success":
            st.success(alert["message"])
        elif alert["type"] == "warning":
            st.warning(alert["message"])
        elif alert["type"] == "error":
            st.error(alert["message"])

# Función: Login
def login_user(username, password):
    if username in users_dict and users_dict[username]["password"] == password:
        st.session_state.user_logged = users_dict[username]
        st.session_state.page = "doctor" if users_dict[username]["tipo"] == "doctor" else "paciente"
        return True
    return False

# Función: Logout
def logout_user():
    st.session_state.user_logged = None
    st.session_state.page = "login"

# Función: Mostrar listado de pacientes (solo doctor)
def listado_pacientes():
    st.subheader("📋 Listado de Pacientes")
    gravedad = st.slider("Gravedad mínima (%)", min_value=0, max_value=100, value=50, step=5)
    filtrados = data[data["Riesgo de Recaída (%)"] >= gravedad]
    st.dataframe(filtrados)
    paciente = st.selectbox("Selecciona un paciente", filtrados["Paciente"])
    if st.button("Visualizar Información"):
        st.session_state.selected_patient = paciente
        add_alert(f"Visualizando información de {paciente}.", "info")

# Función: Mostrar gráficos (doctor)
def mostrar_graficos():
    st.subheader("📊 Gráficos de Pacientes")
    # Gráfico interactivo de Plotly
    fig = px.bar(data, x="Paciente", y="Riesgo de Recaída (%)", color="Riesgo de Recaída (%)", 
                 title="Riesgo de Recaída por Paciente", labels={"Riesgo de Recaída (%)": "Riesgo (%)"})
    fig.update_layout(bargap=0.2, template="plotly_white")
    st.plotly_chart(fig)

    # Segundo gráfico: Evaluación cognitiva
    fig2 = px.scatter(data, x="Paciente", y="Evaluación Cognitiva (%)", size="Evaluación Cognitiva (%)", 
                      color="Evaluación Cognitiva (%)", title="Evaluación Cognitiva por Paciente", 
                      labels={"Evaluación Cognitiva (%)": "Cognitiva (%)"})
    fig2.update_traces(marker=dict(opacity=0.8))
    fig2.update_layout(template="plotly_white")
    st.plotly_chart(fig2)

# Función: Mostrar citas (doctor)
def mostrar_citas():
    st.subheader("📅 Citas Programadas")
    if st.session_state.appointments:
        for appointment in st.session_state.appointments:
            st.markdown(f"- **Paciente**: {appointment['paciente']} | **Fecha**: {appointment['fecha']} | **Hora**: {appointment['hora']}")
    else:
        st.info("No hay citas programadas.")

# Función: Chat
def chat():
    st.subheader("💬 Chat")
    mensaje = st.text_input("Escribe tu mensaje:")
    if st.button("Enviar"):
        if mensaje.strip():
            user = "Doctor" if st.session_state.user_logged["tipo"] == "doctor" else "Paciente"
            st.session_state.chat_messages.append(f"{user}: {mensaje}")
    for chat in st.session_state.chat_messages:
        st.markdown(chat)

# Función: Organización de visitas (paciente)
def organizar_visitas():
    st.subheader("📅 Organización de Visitas")
    fecha = st.date_input("Selecciona la fecha de la visita")
    hora = st.time_input("Selecciona la hora de la visita")
    if st.button("Programar Visita"):
        nueva_cita = {"paciente": "Paciente", "fecha": fecha.strftime("%d/%m/%Y"), "hora": hora.strftime("%H:%M")}
        st.session_state.appointments.append(nueva_cita)
        add_alert(f"Visita programada para el {fecha} a las {hora}.", "success")

# Función: Panel del doctor
def doctor_dashboard():
    st.title("Panel del Doctor")
    render_alerts()
    listado_pacientes()
    mostrar_graficos()
    mostrar_citas()
    chat()
    if st.button("Cerrar sesión"):
        logout_user()

# Función: Panel del paciente
def patient_dashboard():
    st.title("Vista del Paciente")
    render_alerts()
    st.subheader("📞 Opciones de Contacto")
    if st.button("📞 Llamar al Doctor"):
        st.info("Llamada de audio iniciada.")
    if st.button("🎥 Videollamada con el Doctor"):
        st.info("Videollamada iniciada.")
    organizar_visitas()
    chat()
    if st.button("Cerrar sesión"):
        logout_user()

# Función: Página de login
def show_login_page():
    st.title("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if login_user(username, password):
            add_alert("Inicio de sesión exitoso.", "success")
        else:
            st.error("Usuario o contraseña incorrectos")

# Navegación
if st.session_state.page == "login":
    show_login_page()
elif st.session_state.page == "doctor":
    doctor_dashboard()
elif st.session_state.page == "paciente":
    patient_dashboard()
