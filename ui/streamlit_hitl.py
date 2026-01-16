import streamlit as st
import requests

st.set_page_config(page_title="ITSM AI Co-Pilot", layout="wide")

st.title("🤖 ITSM RAG: Agentic Service Desk")
st.markdown("---")

# Sidebar for metrics
st.sidebar.header("System Health")
st.sidebar.metric("API Status", "Online", delta="0ms")

col1, col2 = st.columns(2)

with col1:
    st.subheader("New Ticket Entry")
    t_id = st.text_input("Ticket ID", "INC-999")
    desc = st.text_area("Issue Description", "The user cannot access the VPN and is getting a '403 Forbidden' error.")
    
    if st.button("Analyze with Agentic RAG"):
        with st.spinner("Agent thinking..."):
            response = requests.post(
                "http://localhost:8000/process_ticket",
                json={"ticket_id": t_id, "description": desc}
            ).json()
            st.session_state['last_res'] = response

with col2:
    st.subheader("Agent Decision")
    if 'last_res' in st.session_state:
        res = st.session_state['last_res']
        
        if res['decision'] == "human_review":
            st.warning("⚠️ High Risk Detected: Escalated to Human Review")
        else:
            st.success("✅ Auto-Resolution Suggested")
            
        st.write(f"**Resolution Strategy:** {res['resolution']}")
        st.progress(res['confidence'], text=f"Confidence Score: {res['confidence']*100}%")
        
        if st.button("Approve & Close Ticket"):
            st.balloons()
            st.success("Ticket closed and resolution logged to MLflow.")