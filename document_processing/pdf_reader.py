import fitz


HEADER_MARGIN = 70
FOOTER_MARGIN = 70


def extract_pdf_text(uploaded_file) -> str:
    """
    Extract text from PDF while removing headers and footers
    using page layout coordinates.
    """

    if uploaded_file is None:
        return ""

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    document_text = []

    for page in pdf:

        page_height = page.rect.height

        blocks = page.get_text("blocks")

        # print("\n---------------- PAGE ----------------")

        # for block in blocks:

        #     x0, y0, x1, y1, text, *_ = block

        #     print(
        #         f"Y={y0:.1f} -> {text[:60]}"
        #     )

        page_lines = []

        for block in blocks:

            x0, y0, x1, y1, text, *_ = block

            text = text.strip()

            if not text:
                continue

            # ----------------------------
            # Remove Header
            # ----------------------------

            if y0 < HEADER_MARGIN:
                continue

            # ----------------------------
            # Remove Footer
            # ----------------------------

            if y1 > page_height - FOOTER_MARGIN:
                continue

            page_lines.append(text)

        document_text.append("\n".join(page_lines))

    pdf.close()

    return "\n\n".join(document_text)