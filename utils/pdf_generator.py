from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    title: str,
    content: str
):
    if not content:
        content = "No report available."

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(title, styles["Title"])
    )

    elements.append(
        Spacer(1, 12)
    )

    for line in content.split("\n"):

        elements.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    doc.build(elements)

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes


def generate_txt(
    content: str
):

    return content.encode("utf-8")