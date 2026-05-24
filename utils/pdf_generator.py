from reportlab.platypus import *

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

# =========================
# PDF REPORT
# =========================

def generate_pdf_report(

    patient_name,
    age,
    risk,
    stage,
    risk_level,
    prediction_text

):

    pdf_file = (
        f"reports/{patient_name}_report.pdf"
    )

    doc = SimpleDocTemplate(

        pdf_file,

        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(

        "AI Medical Cancer Report",

        styles['Title']
    )

    story.append(title)

    story.append(Spacer(1, 20))

    content = f"""

<b>Patient Name:</b> {patient_name}<br/><br/>

<b>Age:</b> {age}<br/><br/>

<b>Prediction:</b> {prediction_text}<br/><br/>

<b>Risk Percentage:</b> {risk}%<br/><br/>

<b>Estimated Stage:</b> {stage}<br/><br/>

<b>Risk Level:</b> {risk_level}<br/><br/>

"""

    paragraph = Paragraph(

        content,

        styles['BodyText']
    )

    story.append(paragraph)

    doc.build(story)

    return pdf_file