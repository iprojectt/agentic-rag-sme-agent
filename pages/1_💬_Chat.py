# pages/1_💬_Chat.py

import streamlit as st
import requests
import json
import re
from datetime import datetime

# --- API Configuration ---
API_BASE_URL = "http://localhost:8000"
API_ASK_URL = f"{API_BASE_URL}/ask"
API_STATUS_URL = f"{API_BASE_URL}/status"
API_DOWNLOAD_URL = f"{API_BASE_URL}/download"
API_EVALUATE_URL = f"{API_BASE_URL}/evaluate"

# --- Page and Style Configuration ---
# Page config is now in the root app.py, but it's good practice to have it here too.
st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #FAFAFA; text-align: center; padding-bottom: 1rem; }
    [data-testid="stChatMessage"] { background-color: #2D3748; border-radius: 0.75rem; border: 1px solid #4A5568; }
    .warning-box { background-color: #4A3E2A; color: #FFD699; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #FF9800; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'messages' not in st.session_state: st.session_state.messages = []
if 'email_configured' not in st.session_state: st.session_state.email_configured = False
if 'initialized' not in st.session_state: st.session_state.initialized = False
if 'last_evaluation_data' not in st.session_state: st.session_state.last_evaluation_data = None

# --- Helpers ---
def check_backend_status():
    try:
        response = requests.get(API_STATUS_URL, timeout=2)
        st.session_state.email_configured = response.json().get("email_configured", False)
    except: st.session_state.email_configured = False; st.error("⚠️ Backend server is not running.")
    st.session_state.initialized = True
if not st.session_state.initialized: check_backend_status()

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.text_input("Your Name", key="user_name", value="User")
    st.text_input("Your Email", key="user_email", placeholder="your.email@example.com")
    st.divider()
    st.subheader("📧 Email Status")
    if st.session_state.email_configured: st.success("✅ Email configured")
    else: st.warning("⚠️ Email not configured")
    st.divider()
    st.subheader("📊 Session Info")
    st.info(f"**Messages:** {len(st.session_state.messages)}")
    if st.button("🔄 Clear Chat History", use_container_width=True):
        st.session_state.messages, st.session_state.last_evaluation_data = [], None
        st.rerun()
    
    if len(st.session_state.messages) >= 2:
        st.divider()
        st.subheader("🕵️‍♂️ Agent Performance")
        if st.button("📊 Evaluate & View Dashboard", use_container_width=True):
            with st.spinner("Evaluating last response..."):
                last_user_q, last_agent_a = None, None
                for msg in reversed(st.session_state.messages):
                    if msg['role'] == 'assistant' and not last_agent_a: last_agent_a = msg['content']
                    if msg['role'] == 'user' and last_agent_a: last_user_q = msg['content']; break
                
                if last_user_q and last_agent_a:
                    try:
                        payload = {"question": last_user_q, "answer": last_agent_a}
                        response = requests.post(API_EVALUATE_URL, json=payload)
                        if response.status_code == 200:
                            st.session_state.last_evaluation_data = response.json()
                            st.switch_page("pages/2_📊_Evaluation_Dashboard.py") # <-- SWITCH TO DASHBOARD
                        else:
                            st.error(f"Eval failed (API Error {response.status_code})")
                    except Exception as e: st.error(f"Eval request failed: {e}")

# --- Main App ---
st.markdown('<h1 class="main-header">🚀 Time Management & Productivity Agent</h1>', unsafe_allow_html=True)
# ... (The rest of the chat app logic remains the same)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "download_info" in message: st.download_button(label=f"📥 Download {message['download_info']['filename']}", data=message['download_info']['data'], file_name=message['download_info']['filename'])
        if "reasoning_steps" in message and message["reasoning_steps"]:
            with st.expander("Show Agent's Reasoning"): st.code("\n\n".join(message["reasoning_steps"]), language="text")

def extract_filepath(text: str):
    match = re.search(r"reports/([\w\._\-\s]+.docx)", text)
    if match: return match.group(1).strip()
    return None

def get_streaming_response(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        answer_placeholder, download_placeholder = st.empty(), st.empty()
        reasoning_placeholder = st.expander("Show Agent's Reasoning", expanded=True)
        reasoning_steps_content = reasoning_placeholder.empty()
        final_answer, collected_steps = "", []
        try:
            history_to_send = [{k: v for k, v in msg.items() if k != "download_info"} for msg in st.session_state.messages[-10:]]
            payload = {"question": prompt, "chat_history": history_to_send}
            with requests.post(API_ASK_URL, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line and line.decode('utf-8').startswith('data: '):
                        data = json.loads(line.decode('utf-8')[6:])
                        if data.get("type") == "step": collected_steps.append(data.get("data")); reasoning_steps_content.code("\n\n".join(collected_steps), language='text')
                        elif data.get("type") == "final_answer": final_answer = data.get("data"); answer_placeholder.markdown(final_answer)
            new_message = {"role": "assistant", "content": final_answer, "reasoning_steps": collected_steps}
            if filename := extract_filepath(final_answer):
                file_url = f"{API_DOWNLOAD_URL}/{filename}"; file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    file_data = file_response.content; download_placeholder.download_button(label=f"📥 Download {filename}", data=file_data, file_name=filename)
                    new_message["download_info"] = {"filename": filename, "data": file_data}
            st.session_state.messages.append(new_message)
        except Exception as e: st.error(f"Connection Error: {e}"); st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

if prompt := st.chat_input("Ask a follow-up question..."):
    get_streaming_response(prompt)