import streamlit as st
import pandas as pd
import sqlite3
import joblib

import plotly.express as px
import plotly.graph_objects as go

from utils.ai_engine import predict_cancer
from utils.risk_engine import calculate_stage
from utils.shap_engine import explain_prediction

from utils.file_processor import (
    process_file,
    extract_medical_values
)

from utils.ocr_engine import extract_text_from_image
from utils.pdf_generator import generate_pdf_report

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(
    "database/patients.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS patients (

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

age INTEGER,

prediction TEXT,

risk REAL,

stage TEXT,

smoking TEXT,

alcohol TEXT,

diabetes TEXT,

exercise TEXT,

stress INTEGER,

fatigue TEXT,

tumor_size REAL,

pain_level INTEGER,

date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

# =========================
# LOAD MODEL
# =========================

model = joblib.load(
    "models/ensemble_model.pkl"
)

# =========================
# MAIN FUNCTION
# =========================

def show_prediction():

    st.title("🩺 Smart Patient Analysis")

    col1, col2 = st.columns(2)

    # =========================
    # LEFT SIDE
    # =========================

    with col1:

        patient_name = st.text_input(
            "👤 Patient Name"
        )

        age = st.slider(
            "🎂 Age",
            10,
            100,
            40
        )

        tumor_size = st.slider(
            "🧬 Tumor Size (mm)",
            1,
            100,
            20
        )

        pain_level = st.slider(
            "⚡ Pain Level",
            0,
            10,
            2
        )

        stress = st.slider(
            "🧠 Stress Level",
            0,
            10,
            3
        )

    # =========================
    # RIGHT SIDE
    # =========================

    with col2:

        family_history = st.selectbox(
            "🧬 Family History",
            ["No", "Yes"]
        )

        skin_changes = st.selectbox(
            "🩹 Skin Changes",
            ["No", "Yes"]
        )

        smoking = st.selectbox(
            "🚬 Smoking",
            ["No", "Yes"]
        )

        alcohol = st.selectbox(
            "🍺 Alcohol Consumption",
            ["No", "Yes"]
        )

        diabetes = st.selectbox(
            "🩸 Diabetes",
            ["No", "Yes"]
        )

        exercise = st.selectbox(
            "🏃 Physical Activity",
            ["Low", "Moderate", "High"]
        )

        fatigue = st.selectbox(
            "😴 Fatigue",
            ["No", "Yes"]
        )

        uploaded_file = st.file_uploader(

            "📂 Upload Medical File",

            type=[
                "csv",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "txt"
            ]
        )

    # =========================
    # BUTTON
    # =========================

    if st.button("🔍 Analyze Patient"):

        try:

            # =========================
            # AI PREDICTION
            # =========================

            with st.spinner(
                "🧠 AI Analyzing Patient Data..."
            ):

                prediction, risk, scaled_data = predict_cancer(

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
                )

            # =========================
            # STAGE
            # =========================

            stage, risk_level, progression = calculate_stage(
                risk
            )

            # =========================
            # RESULT
            # =========================

            if prediction[0] == 0:

                prediction_text = "Malignant"

                st.error(
                    "⚠ Malignant Tumor Detected"
                )

            else:

                prediction_text = "Benign"

                st.success(
                    "✅ Benign Tumor Detected"
                )

            # =========================
            # SAVE DATABASE
            # =========================

            cursor.execute(

    """

    INSERT INTO patients (

        name,
        age,

        prediction,
        risk,
        stage,

        smoking,
        alcohol,
        diabetes,

        exercise,
        stress,
        fatigue,

        tumor_size,
        pain_level

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,

    (

        patient_name,
        age,

        prediction_text,
        risk,
        stage,

        smoking,
        alcohol,
        diabetes,

        exercise,
        stress,
        fatigue,

        tumor_size,
        pain_level
    )
)

            conn.commit()

            # =========================
            # METRICS
            # =========================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Risk %",
                    f"{risk}%"
                )

            with col2:

                st.metric(
                    "Stage",
                    stage
                )

            with col3:

                st.metric(
                    "Risk Level",
                    risk_level
                )

            # =========================
            # GAUGE CHART
            # =========================

            gauge = go.Figure(go.Indicator(

                mode="gauge+number",

                value=risk,

                title={
                    'text': "Cancer Risk"
                },

                gauge={

                    'axis': {
                        'range': [0, 100]
                    },

                    'bar': {
                        'color': "#00FFAA"
                    }
                }
            ))

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

            # =========================
            # SHAP ANALYSIS
            # =========================

            try:

                shap_df = explain_prediction(
    scaled_data
)

                st.subheader(
                    "🧠 Feature Importance"
                )

                fig = px.bar(

                    shap_df,

                    x="Impact",

                    y="Feature",

                    orientation='h',

                    color="Impact"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                pie_fig = px.pie(

                    shap_df,

                    names="Feature",

                    values="Impact",

                    title="Impact Distribution"
                )

                st.plotly_chart(
                    pie_fig,
                    use_container_width=True
                )

            except Exception as shap_error:

                st.warning(
                    f"SHAP Error: {shap_error}"
                )

            # =========================
            # AI RECOMMENDATIONS
            # =========================

            st.subheader(
                "🧠 AI Recommendations"
            )

            recommendations = []

            if smoking == "Yes":

                recommendations.append(
                    "Stop smoking immediately."
                )

            if alcohol == "Yes":

                recommendations.append(
                    "Reduce alcohol consumption."
                )

            if exercise == "Low":

                recommendations.append(
                    "Increase physical activity."
                )

            if stress > 7:

                recommendations.append(
                    "Stress management advised."
                )

            if diabetes == "Yes":

                recommendations.append(
                    "Monitor glucose regularly."
                )

            for rec in recommendations:

                st.warning(rec)

            # =========================
            # PDF REPORT
            # =========================

            pdf_path = generate_pdf_report(

                patient_name,
                age,
                risk,
                stage,
                risk_level,
                prediction_text
            )

            with open(pdf_path, "rb") as pdf_file:

                st.download_button(

                    label="📄 Download PDF Report",

                    data=pdf_file,

                    file_name=f"{patient_name}_report.pdf",

                    mime="application/pdf"
                )

            # =========================
            # FILE ANALYSIS
            # =========================

            if uploaded_file is not None:

                st.subheader(
                    "📂 AI File Analysis"
                )

                processed_data = process_file(
                    uploaded_file
                )

                # CSV

                if isinstance(
                    processed_data,
                    pd.DataFrame
                ):

                    st.dataframe(
                        processed_data.head()
                    )

                    numeric_data = processed_data.select_dtypes(

                        include=['number']
                    )

                    st.line_chart(
                        numeric_data
                    )

                # TEXT/PDF

                elif isinstance(
                    processed_data,
                    str
                ):

                    st.text_area(

                        "Extracted Text",

                        processed_data,

                        height=200
                    )

                    medical_values = extract_medical_values(
                        processed_data
                    )

                    st.write(
                        "Detected Values:",
                        medical_values
                    )

                # IMAGE

                else:

                    st.image(
                        processed_data,
                        use_container_width=True
                    )

                    text = extract_text_from_image(
                        processed_data
                    )

                    st.text_area(

                        "OCR Extracted Text",

                        text,

                        height=200
                    )

        except Exception as e:

            st.error(f"❌ Error: {e}")