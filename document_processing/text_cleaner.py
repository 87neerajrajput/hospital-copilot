import re


def clean_pdf_text(text: str) -> str:

    if not text:
        return ""

    # -----------------------------------
    # Normalize line endings
    # -----------------------------------

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # -----------------------------------
    # Remove page numbers
    # -----------------------------------

    text = re.sub(
        r"(?im)^page\s+\d+\s*$",
        "",
        text
    )

    text = re.sub(
        r"(?im)^\d+\s*/\s*\d+\s*$",
        "",
        text
    )

    # -----------------------------------
    # Collapse spaces
    # -----------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # -----------------------------------
    # Remove excessive blank lines
    # -----------------------------------

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # -----------------------------------
    # Join broken lines
    # -----------------------------------

    lines = text.split("\n")

    rebuilt = []

    for line in lines:

        line = line.strip()

        if not rebuilt:
            rebuilt.append(line)
            continue

        previous = rebuilt[-1]

        if (
            previous
            and line
            and not previous.endswith(
                (
                    ".",
                    ":",
                    ";",
                    "?",
                    "!"
                )
            )
            and line[0].islower()
        ):
            rebuilt[-1] += " " + line

        else:
            rebuilt.append(line)

    return "\n".join(rebuilt).strip()