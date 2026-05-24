import pytesseract
import cv2
import numpy as np

from PIL import Image

# =========================
# ADVANCED OCR ENGINE
# =========================

def extract_text_from_image(image):

    # PIL → NUMPY

    image_np = np.array(image)

    # RGB → GRAYSCALE

    gray = cv2.cvtColor(

        image_np,

        cv2.COLOR_BGR2GRAY
    )

    # REMOVE NOISE

    gray = cv2.GaussianBlur(

        gray,

        (5, 5),

        0
    )

    # THRESHOLD

    thresh = cv2.threshold(

        gray,

        0,

        255,

        cv2.THRESH_BINARY + cv2.THRESH_OTSU

    )[1]

    # OCR CONFIG

    custom_config = r'--oem 3 --psm 6'

    # EXTRACT TEXT

    text = pytesseract.image_to_string(

        thresh,

        config=custom_config
    )

    return text