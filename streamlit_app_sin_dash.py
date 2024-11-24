import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión Psiquiátrica",
    page_icon="🩺",
    layout="wide",
)

# Estado de sesión para manejar datos persistentes
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None

# Datos de ejemplo para pacientes
data = pd.DataFrame({
    "Paciente": ["Paciente A", "Paciente B", "Paciente C", "Paciente D", "Paciente E"],
    "Edad": [30, 45, 50, 40, 60],
    "Riesgo de Recaída (%)": [20, 65, 80, 50, 90],
    "Evaluación Cognitiva": [85, 70, 60, 75, 50]
})

# Función: Mostrar alertas y notificaciones
def mostrar_alertas():
    st.subheader("🔔 Alertas Recientes")
    st.info("📢 Consulta programada con Paciente A para el 25/11/2024.")
    #st.warning("⚠️ Riesgo elevado detectado en Paciente B.")
    #st.success("✅ Ejercicio completado con éxito por Paciente C.")


def mostrar_alertas_audio(porcentaje, emocion):
    #st.subheader("🔔 Alertas Recientes")
    #st.info("📢 Consulta programada con Paciente A para el 25/11/2024.")
    #st.subheader("🔔 Alertas IA Audio")
    if porcentaje < 51:
        st.info("📢 Estado del paciente "+ emocion + " " + str(porcentaje) +"%")
    else:
        st.info("📢 Estado del paciente "+ emocion + " " + str(porcentaje) +"%")
        st.error("Riesgo elevado detectado en Paciente 5237", icon="🚨")






# Función: Mostrar listado de pacientes
def listado_pacientes():
    st.subheader("📋 Listado de Pacientes")
    st.markdown("Filtra pacientes por porcentaje de gravedad o selecciona un paciente.")

    # Filtro por porcentaje de gravedad
    gravedad = st.slider("Gravedad mínima (%)", min_value=0, max_value=100, value=50, step=5)
    filtrados = data[data["Riesgo de Recaída (%)"] >= gravedad]

    st.dataframe(filtrados)

    # Selección de paciente
    paciente = st.selectbox("Selecciona un paciente", filtrados["Paciente"])
    if st.button("Visualizar Información"):
        st.session_state.selected_patient = paciente

# Función: Mostrar información del paciente seleccionado
def informacion_paciente():
    if st.session_state.selected_patient:
        st.subheader(f"🩺 Información de {st.session_state.selected_patient}")
        info = data[data["Paciente"] == st.session_state.selected_patient].iloc[0]
        st.write(f"**Edad:** {info['Edad']} años")
        st.write(f"**Riesgo de Recaída:** {info['Riesgo de Recaída (%)']}%")
        st.write(f"**Evaluación Cognitiva:** {info['Evaluación Cognitiva']}%")
        st.write("**Notas:** Revisión pendiente para ajustar medicación.")
    else:
        st.info("Selecciona un paciente para ver la información.")

# Función: Simular chat con paciente
def chat_paciente():
    st.subheader("💬 Chat con el Paciente")
    st.write("Comunícate en tiempo real con el paciente.")

    with st.form("chat_form"):
        mensaje = st.text_input("Escribe tu mensaje")
        enviado = st.form_submit_button("Enviar")

        if enviado and mensaje:
            st.session_state.chat_messages.append(f"Tú: {mensaje}")
            st.session_state.chat_messages.append(f"Paciente: Gracias por tu mensaje.")

    for chat in st.session_state.chat_messages:
        st.markdown(chat)

# Función: Recopilación de datos de dispositivos
def recopilacion_dispositivos():
    st.subheader("📡 Datos recopilados en tiempo real")
    st.info("Datos obtenidos desde dispositivos externos:")
    st.write("- **Frecuencia cardíaca:** 72 bpm")
    st.write("- **Ritmo respiratorio:** 16 respiraciones/minuto")
    st.write("- **Nivel de oxígeno:** 98%")

# Función: Organización de visitas
def organizar_visitas():
    st.subheader("📅 Organización de Visitas")
    fecha = st.date_input("Selecciona la fecha de la visita")
    hora = st.time_input("Selecciona la hora de la visita")
    if st.button("Programar Visita"):
        st.success(f"Visita programada para {fecha} a las {hora}.")

# Layout principal
st.title("Gestión Psiquiátrica")
st.markdown(
    """
    Bienvenido a este sistema de gestión diseñado para identificar patrones de riesgo, 
    predecir recaídas y personalizar intervenciones en pacientes con esquizofrenia.
    """
)

# Organizar el diseño en dos columnas
col1, col2 = st.columns([2, 1])

# Columna izquierda: Información principal
with col1:
    mostrar_alertas()
    mostrar_alertas_audio(60,"neutro")
    listado_pacientes()
    informacion_paciente()

# Columna derecha: Funciones adicionales
with col2:
    chat_paciente()
    recopilacion_dispositivos()
    organizar_visitas()
