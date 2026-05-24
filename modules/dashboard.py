import streamlit as st
import sqlite3
import pandas as pd

import plotly.express as px

# =========================
# DASHBOARD
# =========================

def show_dashboard():

    st.title("📊 AI Medical Dashboard")

    # DATABASE

    conn = sqlite3.connect(

        "database/patients.db",

        check_same_thread=False
    )

    # LOAD DATA

    df = pd.read_sql_query(

        "SELECT * FROM patients",

        conn
    )

    # =========================
    # METRICS
    # =========================

    total_patients = len(df)

    malignant_cases = len(

        df[df["prediction"] == "Malignant"]

    )

    benign_cases = len(

        df[df["prediction"] == "Benign"]

    )

    avg_risk = round(

        df["risk"].mean(),

        2
    ) if len(df) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Patients",
            total_patients
        )

    with col2:

        st.metric(
            "⚠ Malignant",
            malignant_cases
        )

    with col3:

        st.metric(
            "✅ Benign",
            benign_cases
        )

    with col4:

        st.metric(
            "📈 Avg Risk %",
            avg_risk
        )

    st.markdown("---")

    # =========================
    # SEARCH
    # =========================

    search = st.text_input(
        "🔍 Search Patient"
    )

    if search:

        df = df[

            df["name"].str.contains(

                search,

                case=False,

                na=False
            )
        ]

    # =========================
    # PATIENT TABLE
    # =========================

    st.subheader("🏥 Patient History")

    st.dataframe(

        df,

        use_container_width=True
    )

    # =========================
    # PREDICTION PIE CHART
    # =========================

    st.subheader("📊 Prediction Distribution")

    prediction_counts = df["prediction"].value_counts()

    fig1 = px.pie(

        names=prediction_counts.index,

        values=prediction_counts.values,

        title="Prediction Distribution"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =========================
    # RISK CHART
    # =========================

    st.subheader("📈 Risk Analysis")

    fig2 = px.histogram(

        df,

        x="risk",

        nbins=20,

        title="Risk Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =========================
    # STAGE ANALYSIS
    # =========================

    st.subheader("🧬 Stage Analysis")

    stage_counts = df["stage"].value_counts()

    fig3 = px.bar(

        x=stage_counts.index,

        y=stage_counts.values,

        labels={

            "x": "Stage",

            "y": "Count"
        },

        title="Cancer Stage Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =========================
    # DOWNLOAD CSV
    # =========================

    csv = df.to_csv(index=False)

    st.download_button(

        label="📥 Download Patient Records",

        data=csv,

        file_name="patient_history.csv",

        mime="text/csv"
    )