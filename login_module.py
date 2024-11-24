import streamlit as st
import pandas as pd

usuarios = pd.DataFrame({
    'username': ['javier', 'paciente'],
    'password': ['pass_javier', 'pass_paciente'],
    'tipo': ['doctor', 'paciente']
})

user_logged = None


def login_user(username, password):
    global user_logged
    for index, row in usuarios.iterrows():
        if row['username'] == username and row['password'] == password:
            user_logged = row
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
            else:
                st.session_state.page = 'paciente'
        else:
            st.error('Usuario o contraseña incorrectos')


def show_doctor_page():
    st.title('Bienvenido, Dr.')
    if st.button('Cerrar sesión'):
        logout_user()
        st.session_state.page = 'login'


def show_patient_page():
    st.title('Bienvenido, paciente')
    if st.button('Cerrar sesión'):
        logout_user()
        st.session_state.page = 'login'


if 'page' not in st.session_state:
    st.session_state.page = 'login'

if st.session_state.page == 'login':
    show_login_page()
    st.rerun()
elif st.session_state.page == 'doctor':
    show_doctor_page()
    st.rerun()
elif st.session_state.page == 'paciente':
    show_patient_page()
    st.rerun()
