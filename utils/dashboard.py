#Comandos necesarios para implementar Material UI y streamlit-elements
#npm install @mui/material
#pip install streamlit-elements==0.1.*


from streamlit_elements import elements, mui, html

with elements("dashboard"):
  # You can create a draggable and resizable dashboard using
  # any element available in Streamlit Elements.

  from streamlit_elements import dashboard

  # First, build a default layout for every element you want to include in your dashboard

  layout = [
    # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
    dashboard.Item("patients_card", 0, 2, 4, 2, isResizable=False),
    dashboard.Item("alerts_card", 2, 0, 3, 2, isResizable=False),

  ]

  # Next, create a dashboard layout using the 'with' syntax. It takes the layout
  # as first parameter, plus additional properties you can find in the GitHub links below.

  with dashboard.Grid(layout):

    with mui.Card(key="patients_card"):
      mui.Typography("Pacientes",css={"font-size": "40px", "font-weight": "bold", "text-align": "center"})

    with mui.Card(key="alerts_card"):
      mui.Typography("Notificaciones / Alertas recientes",css={"font-size": "40px", "font-weight": "bold", "text-align": "center"})
      mui.Alert("Mensaje importante recibido", severity="warning",css={"width": "80%","align": "center","margin-left":"40px","margin-bottom":"20px"})
      mui.Alert("Mensaje importante recibido", severity="error", css={"width": "80%", "align": "center","margin-left":"40px","margin-bottom":"20px"})






