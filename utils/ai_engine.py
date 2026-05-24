import joblib
import numpy as np

model = joblib.load(
    "models/ensemble_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

def predict_cancer(

    age,
    tumor_size,
    pain_level,

    family_history,
    skin_changes,

    smoking,
    alcohol,
    diabetes,

    exercise,
    stress,
    fatigue
):

    age_factor = age / 100

    family_factor = (
        1.25
        if family_history == "Yes"
        else 1.0
    )

    skin_factor = (
        1.3
        if skin_changes == "Yes"
        else 1.0
    )

    smoking_factor = (
        1.35
        if smoking == "Yes"
        else 1.0
    )

    alcohol_factor = (
        1.15
        if alcohol == "Yes"
        else 1.0
    )

    diabetes_factor = (
        1.2
        if diabetes == "Yes"
        else 1.0
    )

    fatigue_factor = (
        1.15
        if fatigue == "Yes"
        else 1.0
    )

    if exercise == "High":

        exercise_factor = 0.8

    elif exercise == "Moderate":

        exercise_factor = 1.0

    else:

        exercise_factor = 1.2

    combined_factor = (

        family_factor *

        skin_factor *

        smoking_factor *

        alcohol_factor *

        diabetes_factor *

        fatigue_factor *

        exercise_factor
    )

    radius = (
        tumor_size * 0.42
        * combined_factor
    )

    texture = (
        pain_level * 2.5
        * skin_factor
    )

    perimeter = (
        tumor_size * 3.5
        * combined_factor
    )

    area = (
        tumor_size * 30
        * age_factor
    )

    concavity = (
        0.4
        if skin_changes == "Yes"
        else 0.12
    )

    worst_radius = (
        radius + (age * 0.05)
    )

    worst_perimeter = (
        perimeter + (stress * 2)
    )

    worst_area = (
        area + (tumor_size * 20)
    )

    input_data = np.array([[

        radius,
        texture,
        perimeter,
        area,
        concavity,

        worst_radius,
        worst_perimeter,
        worst_area

    ]])

    scaled_data = scaler.transform(
        input_data
    )

    prediction = model.predict(
        scaled_data
    )

    probability = model.predict_proba(
        scaled_data
    )

    risk = round(
        probability[0][0] * 100,
        2
    )

    return prediction, risk, scaled_data