import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión Psiquiátrica",
    page_icon="🩺",
    layout="wide",
)

# Datos de ejemplo para pacientes
data = pd.DataFrame({
    "Paciente": ["Paciente A", "Paciente B", "Paciente C", "Paciente D", "Paciente E"],
    "Edad": [30, 45, 50, 40, 60],
    "Riesgo de Recaída (%)": [20, 65, 80, 50, 90],
    "Evaluación Cognitiva": [85, 70, 60, 75, 50]
})

# Estado de sesión
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None

# Funciones para las secciones
def mostrar_alertas():
    st.subheader("🔔 Alertas Recientes")
    st.info("📢 Consulta programada con Paciente A para el 25/11/2024.")
    st.warning("⚠️ Riesgo elevado detectado en Paciente B.")
    st.success("✅ Ejercicio completado con éxito por Paciente C.")

def listado_pacientes():
    st.subheader("📋 Listado de Pacientes")
    st.markdown("Filtra pacientes por porcentaje de gravedad o selecciona un paciente.")
    gravedad = st.slider("Gravedad mínima (%)", min_value=0, max_value=100, value=50, step=5)
    filtrados = data[data["Riesgo de Recaída (%)"] >= gravedad]
    st.dataframe(filtrados)
    paciente = st.selectbox("Selecciona un paciente", filtrados["Paciente"])
    if st.button("Visualizar Información"):
        st.session_state.selected_patient = paciente

def informacion_paciente():
    if st.session_state.selected_patient:
        st.subheader(f"🩺 Información de {st.session_state.selected_patient}")
        info = data[data["Paciente"] == st.session_state.selected_patient].iloc[0]
        st.write(f"**Edad:** {info['Edad']} años")
        st.write(f"**Riesgo de Recaída:** {info['Riesgo de Recaída (%)']}%")
        st.write(f"**Evaluación Cognitiva:** {info['Evaluación Cognitiva']}%")
    else:
        st.info("Selecciona un paciente para ver la información.")

def chat_paciente():
    st.subheader("💬 Chat con el Paciente")
    with st.form("chat_form"):
        mensaje = st.text_input("Escribe tu mensaje")
        enviado = st.form_submit_button("Enviar")
        if enviado and mensaje:
            st.session_state.chat_messages.append(f"Tú: {mensaje}")
            st.session_state.chat_messages.append(f"Paciente: Gracias por tu mensaje.")
    for chat in st.session_state.chat_messages:
        st.markdown(chat)

def recopilacion_dispositivos():
    st.subheader("📡 Datos recopilados en tiempo real")
    st.info("Datos obtenidos desde dispositivos externos:")
    st.write("- **Frecuencia cardíaca:** 72 bpm")
    st.write("- **Ritmo respiratorio:** 16 respiraciones/minuto")
    st.write("- **Nivel de oxígeno:** 98%")

def organizar_visitas():
    st.subheader("📅 Organización de Visitas")
    fecha = st.date_input("Selecciona la fecha de la visita")
    hora = st.time_input("Selecciona la hora de la visita")
    if st.button("Programar Visita"):
        st.success(f"Visita programada para {fecha} a las {hora}.")

def analisis_datos():
    st.subheader("📊 Análisis de Datos")
    alto_riesgo = data[data["Riesgo de Recaída (%)"] > 70]
    st.write("Pacientes con riesgo elevado:")
    st.dataframe(alto_riesgo)
    
    # Gráfico de barra
    st.markdown("### Riesgo de Recaída por Paciente")
    fig1 = px.bar(
        data,
        x="Paciente",
        y="Riesgo de Recaída (%)",
        color="Riesgo de Recaída (%)",
        title="Nivel de riesgo por paciente",
        labels={"Riesgo de Recaída (%)": "Porcentaje de Recaída"}
    )
    st.plotly_chart(fig1)
    
    # Gráfico de dispersión
    st.markdown("### Riesgo de Recaída vs Evaluación Cognitiva")
    fig2 = px.scatter(
        data,
        x="Evaluación Cognitiva",
        y="Riesgo de Recaída (%)",
        color="Paciente",
        size="Edad",
        title="Relación entre Riesgo de Recaída y Evaluación Cognitiva"
    )
    st.plotly_chart(fig2)

# Navegación con barra lateral
st.sidebar.title("Navegación")
opcion = st.sidebar.radio(
    "Ir a:", 
    ["Inicio", "Alertas", "Pacientes", "Chat", "Dispositivos", "Visitas", "Análisis"]
)

# Mostrar contenido según la opción seleccionada
if opcion == "Inicio":
    st.title("Gestión Psiquiátrica")
    st.markdown(
        """
        Bienvenido a la plataforma de gestión diseñada para identificar patrones de riesgo,
        predecir recaídas y personalizar intervenciones.
        """
    )
elif opcion == "Alertas":
    mostrar_alertas()
elif opcion == "Pacientes":
    listado_pacientes()
    informacion_paciente()
elif opcion == "Chat":
    chat_paciente()
elif opcion == "Dispositivos":
    recopilacion_dispositivos()
elif opcion == "Visitas":
    organizar_visitas()
elif opcion == "Análisis":
    analisis_datos()
