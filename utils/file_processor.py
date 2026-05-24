import fitz
import pandas as pd
import re

from PIL import Image

# =========================
# PROCESS FILE
# =========================

def process_file(uploaded_file):

    file_type = uploaded_file.name.split(".")[-1]

    # =========================
    # CSV
    # =========================

    if file_type == "csv":

        data = pd.read_csv(
            uploaded_file
        )

        return data

    # =========================
    # PDF
    # =========================

    elif file_type == "pdf":

        pdf_data = uploaded_file.read()

        pdf_document = fitz.open(

            stream=pdf_data,

            filetype="pdf"
        )

        extracted_text = ""

        for page in pdf_document:

            extracted_text += page.get_text()

        return extracted_text

    # =========================
    # TXT
    # =========================

    elif file_type == "txt":

        return uploaded_file.read().decode()

    # =========================
    # IMAGE
    # =========================

    elif file_type in [

        "png",
        "jpg",
        "jpeg"

    ]:

        image = Image.open(
            uploaded_file
        )

        return image

# =========================
# EXTRACT MEDICAL VALUES
# =========================

def extract_medical_values(text):

    values = {}

    patterns = {

        "tumor_size": r"tumor size[: ]+(\d+)",

        "pain_level": r"pain[: ]+(\d+)",

        "age": r"age[: ]+(\d+)"
    }

    for key, pattern in patterns.items():

        match = re.search(

            pattern,

            text,

            re.IGNORECASE
        )

        if match:

            values[key] = int(
                match.group(1)
            )

    return values