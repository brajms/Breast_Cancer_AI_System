import streamlit as st

def show_home():

    st.markdown("""

<div style='
padding:50px;
border-radius:25px;
background:rgba(255,255,255,0.05);
backdrop-filter: blur(15px);
'>

<h1>

🧬 Next-Generation Cancer AI

</h1>

<p style='font-size:22px;color:white;'>

Advanced Explainable Multi-Modal Healthcare Platform

</p>

</div>

""", unsafe_allow_html=True)

    st.image(

        "https://images.unsplash.com/photo-1576091160550-2173dba999ef",

        use_container_width=True
    )

    st.markdown("## 🚀 Core Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info("🧠 Explainable AI")

    with col2:

        st.info("📂 Multi-Modal Medical Files")

    with col3:

        st.info("📊 Smart Medical Analytics")

    st.markdown("---")

    st.subheader("🏥 AI Capabilities")

    st.success("✔ Ensemble Machine Learning")

    st.success("✔ SHAP Explainability")

    st.success("✔ OCR Report Analysis")

    st.success("✔ Lifestyle Risk Analysis")

    st.success("✔ PDF Medical Reports")

    st.success("✔ Interactive Analytics Dashboard")