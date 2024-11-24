import streamlit as st

# Convertir los datos de usuarios a un diccionario
users_dict = {
    'javier': {'password': 'pass_javier', 'tipo': 'doctor'},
    'paciente': {'password': 'pass_paciente', 'tipo': 'paciente'}
}

user_logged = None


def login_user(username, password):
    global user_logged
    if username in users_dict and users_dict[username]['password'] == password:
        user_logged = users_dict[username]
        return True
    return False


def logout_user():
    global user_logged
    user_logged = None


def show_login_page():
    st.title('Iniciar sesión')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Iniciar sesión'):
        if login_user(username, password):
            if user_logged['tipo'] == 'doctor':
                st.session_state.page = 'doctor'
                st.rerun()
            else:
                st.session_state.page = 'paciente'
                st.rerun()
        else:
            st.error('Usuario o contraseña incorrectos')


def show_doctor_page():
    st.title('Bienvenido, Dr.')
    if st.button('Cerrar sesión'):
        logout_user()
        st.session_state.page = 'login'
        st.rerun()


def show_patient_page():
    st.title('Bienvenido, paciente')
    if st.button('Cerrar sesión'):
        logout_user()
        st.session_state.page = 'login'
        st.rerun()

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if st.session_state.page == 'login':
    show_login_page()
elif st.session_state.page == 'doctor':
    show_doctor_page()
elif st.session_state.page == 'paciente':
    show_patient_page()
