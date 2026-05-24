import pandas as pd
import numpy as np

# =========================
# FEATURE IMPORTANCE ENGINE
# =========================

def explain_prediction(

    scaled_data
):

    feature_names = [

        "Radius",
        "Texture",
        "Perimeter",
        "Area",

        "Concavity",

        "Worst Radius",
        "Worst Perimeter",
        "Worst Area"
    ]

    # =========================
    # USE INPUT MAGNITUDE
    # =========================

    impacts = np.abs(
        scaled_data[0]
    )

    # NORMALIZE

    impacts = (

        impacts / impacts.sum()

    ) * 100

    # CREATE DATAFRAME

    shap_df = pd.DataFrame({

        "Feature": feature_names,

        "Impact": impacts

    })

    shap_df = shap_df.sort_values(

        by="Impact",

        ascending=False
    )

    return shap_df