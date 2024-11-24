from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_clinical_report(title, content, file_output):

    doc = SimpleDocTemplate(file_output, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()

    style_title = styles['Title']
    style_paragraph = Paragraph(title, style_title)
    story.append(style_paragraph)

    story.append(Spacer(1, 24))

    style_content = styles['BodyText']
    paragraph_content = Paragraph(content, style_content)
    story.append(paragraph_content)

    doc.build(story)

    # todo: añadir logo, ponerlo más bonito, información relevante segun IA mediante dataframes


if __name__ == "__main__":

    patient_name = "Paciente Kike"

    title = f"Informe Clínico - {patient_name}"
    content = """
    Este es un informe detallado sobre el estado actual del paciente.

    - Nos preocupa su comportamiento errático en entornos con mucha gente.
    - Se recomienda pasar más tiempo realizando tareas conjuntas como pasear, realizar algun tipo de deporte o ejercicio
    físico.
    
    
    - Se predice un alto índice de recaída.

    """
    file_output = "../informe_actual.pdf"

    generate_clinical_report(title, content, file_output)