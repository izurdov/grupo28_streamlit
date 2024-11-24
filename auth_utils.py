# grupo28_streamlit/auth.py

import pandas as pd

users = pd.DataFrame({
    'username': ['javier', 'paciente'],
    'password': ['pass_javier', 'pass_paciente'],
    'tipo': ['doctor', 'patient']
})

class User_logged:
    def __init__(self):
        self.user_logged = None

    def login(self, username, password):
        user = users[(users['username'] == username) & (users['password'] == password)]
        if not user.empty:
            self.user_logged = user.iloc[0]
            return True
        return False

    def logout(self):
        self.user_logged = None

user_logged = User_logged()