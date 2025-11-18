# pages/2_📊_Evaluation_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Evaluation Dashboard", page_icon="📊", layout="wide")

st.markdown("<h1 style='text-align: center;'>📊 Real-Time Evaluation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Check if there is evaluation data in the session state
if 'last_evaluation_data' in st.session_state and st.session_state.last_evaluation_data:
    data = st.session_state.last_evaluation_data
    metrics = data.get('metrics', {})
    
    # --- Display the evaluated Q&A ---
    st.subheader("💬 Evaluated Exchange")
    with st.container(border=True):
        st.markdown("##### User Question:")
        st.info(data.get('question', 'N/A'))
        st.markdown("##### Agent's Answer:")
        st.success(data.get('answer', 'N/A'))

    st.subheader("📈 Evaluation Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Key Performance Indicators")
        radar_metrics = {
            "Faithfulness": metrics.get("faithfulness", 0),
            "Completeness": metrics.get("completeness", 0),
            "Quality": metrics.get("quality", 0),
        }
        radar_df = pd.DataFrame(dict(r=list(radar_metrics.values()), theta=list(radar_metrics.keys())))
        fig = go.Figure(data=go.Scatterpolar(r=radar_df["r"], theta=radar_df["theta"], fill="toself"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Hallucination Analysis")
        hallucinations = metrics.get('hallucinations', [])
        if not hallucinations:
            st.success("✅ No hallucinations were detected by the evaluator.")
        else:
            st.error(f"⚠️ {len(hallucinations)} hallucination(s) detected:")
            for h in hallucinations:
                st.write(f"- {h}")
    
    st.subheader("📚 Ground-Truth Context Used for Evaluation")
    contexts = data.get('contexts', [])
    if not contexts:
        st.info("No context was retrieved for this evaluation.")
    else:
        for i, ctx in enumerate(contexts, 1):
            with st.expander(f"Context Document {i}"):
                st.write(ctx)
else:
    st.warning("No evaluation data found. Please run an evaluation from the Chat page first.")
    st.page_link("pages/1_💬_Chat.py", label="Go back to Chat", icon="💬")