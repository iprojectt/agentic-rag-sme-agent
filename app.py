# # # # # # # app.py

# # # # # # """
# # # # # # Streamlit Frontend for the Productivity SME Agent
# # # # # # =================================================
# # # # # # This script creates a user-friendly, web-based chat interface for the agent.

# # # # # # What it does:
# # # # # # 1. Sets up the page title, icon, and layout.
# # # # # # 2. Manages and displays the chat history using Streamlit's session state.
# # # # # # 3. Captures user input from a chat box.
# # # # # # 4. When a user sends a message, it makes a POST request to the FastAPI
# # # # # #    backend API.
# # # # # # 5. Displays the agent's response in the chat interface, handling potential
# # # # # #    connection errors gracefully.

# # # # # # This is a "thin" client - all the complex AI logic lives in the backend.
# # # # # # """
# # # # # # # app.py
# # # # # # """
# # # # # # Streamlit Frontend for the Productivity SME Agent
# # # # # # =================================================
# # # # # # Lightweight chat UI that posts to a FastAPI backend and shows the agent's responses.
# # # # # # """

# # # # # # # app.py
# # # # # # """
# # # # # # Frontend UI (Streamlit) for Productivity SME Agent
# # # # # # ===================================================

# # # # # # This UI sends user queries to the FastAPI backend (/ask),
# # # # # # which runs the LangGraph-based RAG agent.

# # # # # # Run using:
# # # # # #     streamlit run app.py
# # # # # # """

# # # # # # import streamlit as st
# # # # # # import requests

# # # # # # API_URL = "http://localhost:8000/ask"


# # # # # # # -------------------------------------------------------------
# # # # # # # Streamlit App Configuration
# # # # # # # -------------------------------------------------------------
# # # # # # st.set_page_config(
# # # # # #     page_title="Productivity SME Agent",
# # # # # #     page_icon="⚡",
# # # # # #     layout="centered"
# # # # # # )

# # # # # # st.title("⚡ Productivity SME Agent")
# # # # # # st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")


# # # # # # # -------------------------------------------------------------
# # # # # # # Chat Input UI
# # # # # # # -------------------------------------------------------------
# # # # # # user_query = st.text_input("Enter your question:", "")

# # # # # # if st.button("Submit"):

# # # # # #     if not user_query.strip():
# # # # # #         st.warning("Please enter a valid question.")
# # # # # #         st.stop()

# # # # # #     st.write("⏳ *Thinking...*")

# # # # # #     try:
# # # # # #         response = requests.post(API_URL, json={"question": user_query})
# # # # # #         if response.status_code == 200:
# # # # # #             data = response.json()
# # # # # #             st.success("### Answer:")
# # # # # #             st.write(data["answer"])
# # # # # #         else:
# # # # # #             st.error(f"Error: API returned status {response.status_code}")
# # # # # #     except Exception as e:
# # # # # #         st.error("⚠ Unable to reach backend server.")
# # # # # #         st.write(str(e))


# # # # # # # -------------------------------------------------------------
# # # # # # # Footer
# # # # # # # -------------------------------------------------------------
# # # # # # st.markdown(
# # # # # #     """
# # # # # # ---
# # # # # # Made with ❤️ using **LangGraph**, **FastAPI**, and **Streamlit**.
# # # # # # """
# # # # # # )















# # # # # # # --- START OF FILE app.py ---

# # # # # # # app.py
# # # # # # """
# # # # # # Frontend UI (Streamlit) for Productivity SME Agent
# # # # # # ===================================================

# # # # # # This UI sends user queries to the FastAPI backend (/ask),
# # # # # # which runs the LangGraph-based RAG agent and displays its reasoning.

# # # # # # Run using:
# # # # # #     streamlit run app.py
# # # # # # """

# # # # # # import streamlit as st
# # # # # # import requests

# # # # # # API_URL = "http://localhost:8000/ask"


# # # # # # # -------------------------------------------------------------
# # # # # # # Streamlit App Configuration
# # # # # # # -------------------------------------------------------------
# # # # # # st.set_page_config(
# # # # # #     page_title="Productivity SME Agent",
# # # # # #     page_icon="⚡",
# # # # # #     layout="centered"
# # # # # # )

# # # # # # st.title("⚡ Productivity SME Agent")
# # # # # # st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")


# # # # # # # -------------------------------------------------------------
# # # # # # # Chat Input UI
# # # # # # # -------------------------------------------------------------
# # # # # # user_query = st.text_input("Enter your question:", "")

# # # # # # if st.button("Submit"):

# # # # # #     if not user_query.strip():
# # # # # #         st.warning("Please enter a valid question.")
# # # # # #         st.stop()

# # # # # #     st.write("⏳ *Thinking...*")

# # # # # #     try:
# # # # # #         response = requests.post(API_URL, json={"question": user_query})
# # # # # #         if response.status_code == 200:
# # # # # #             data = response.json()
# # # # # #             st.success("### Answer:")
# # # # # #             st.write(data["answer"])

# # # # # #             # Display the reasoning steps in an expander
# # # # # #             with st.expander("Show Agent's Reasoning"):
# # # # # #                 st.write("Here is the step-by-step process the agent took:")
# # # # # #                 reasoning_steps = data.get("reasoning_steps", [])
# # # # # #                 if reasoning_steps:
# # # # # #                     for i, step in enumerate(reasoning_steps, 1):
# # # # # #                         st.text(f"Step {i}:")
# # # # # #                         st.code(step, language="text")
# # # # # #                 else:
# # # # # #                     st.write("No reasoning steps were provided by the backend.")

# # # # # #         else:
# # # # # #             st.error(f"Error: API returned status {response.status_code}")
# # # # # #     except requests.exceptions.ConnectionError as e:
# # # # # #         st.error("⚠ Unable to reach backend server. Is it running?")
# # # # # #         st.write(f"Details: {e}")
# # # # # #     except Exception as e:
# # # # # #         st.error("An unexpected error occurred.")
# # # # # #         st.write(str(e))


# # # # # # # -------------------------------------------------------------
# # # # # # # Footer
# # # # # # # -------------------------------------------------------------
# # # # # # st.markdown(
# # # # # #     """
# # # # # # ---
# # # # # # Made with ❤️ using **LangGraph**, **FastAPI**, and **Streamlit**.
# # # # # # """
# # # # # # )


# # # # # # app.py
# # # # # """
# # # # # Frontend UI (Streamlit) for Productivity SME Agent
# # # # # ===================================================

# # # # # This UI sends user queries to the FastAPI backend (/ask),
# # # # # which runs the LangGraph-based RAG agent and displays its reasoning.

# # # # # Run using:
# # # # #     streamlit run app.py
# # # # # """

# # # # # import streamlit as st
# # # # # import requests
# # # # # import re
# # # # # API_URL = "http://localhost:8000/ask"


# # # # # # -------------------------------------------------------------
# # # # # # Streamlit App Configuration
# # # # # # -------------------------------------------------------------
# # # # # st.set_page_config(
# # # # #     page_title="Productivity SME Agent",
# # # # #     page_icon="⚡",
# # # # #     layout="centered"
# # # # # )

# # # # # st.title("⚡ Productivity SME Agent")
# # # # # st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")


# # # # # # -------------------------------------------------------------
# # # # # # Chat Input UI
# # # # # # -------------------------------------------------------------
# # # # # user_query = st.text_input("Enter your question:", "")

# # # # # if st.button("Submit"):

# # # # #     if not user_query.strip():
# # # # #         st.warning("Please enter a valid question.")
# # # # #         st.stop()

# # # # #     st.write("⏳ *Thinking...*")

# # # # #     try:
# # # # #         # Use the "reasoning" mode to get detailed steps
# # # # #         response = requests.post(API_URL, json={"question": user_query, "mode": "reasoning"})
        
# # # # #         if response.status_code == 200:
# # # # #             data = response.json()
# # # # #             st.success("### Answer:")
# # # # #             st.write(data["answer"])


# # # # #             # --- START OF NEW LOGIC ---
# # # # #             # Check the reasoning steps for a successful file creation message
# # # # #             reasoning_steps = data.get("reasoning_steps", [])
# # # # #             for step in reasoning_steps:
# # # # #                 # Look for the observation from the tool call that confirms success
# # # # #                 if "OBSERVATION (tool)" in step and "'status': 'ok'" in step and "'path':" in step:
# # # # #                     # Use a regular expression to reliably extract the file path
# # # # #                     match = re.search(r"'path':\s*'([^']*)'", step)
# # # # #                     if match:
# # # # #                         saved_path = match.group(1)
# # # # #                         # Display a prominent success message to the user
# # # # #                         st.success(f"✅ Report successfully generated and saved to: **{saved_path}**")
# # # # #                         break # Stop searching once we've found it
# # # # #             # --- END OF NEW LOGIC ---


# # # # #             # Display the reasoning steps in an expander
# # # # #             with st.expander("Show Agent's Reasoning"):
# # # # #                 st.write("Here is the step-by-step process the agent took:")
# # # # #                 reasoning_steps = data.get("reasoning_steps", [])
# # # # #                 if reasoning_steps:
# # # # #                     for i, step in enumerate(reasoning_steps, 1):
# # # # #                         st.text(f"Step {i}:")
# # # # #                         # Use st.code for better formatting of structured text
# # # # #                         st.code(step, language="text")
# # # # #                 else:
# # # # #                     st.write("No reasoning steps were provided by the backend.")

# # # # #         else:
# # # # #             st.error(f"Error: API returned status {response.status_code} - {response.text}")
            
# # # # #     except requests.exceptions.ConnectionError as e:
# # # # #         st.error("⚠ Unable to reach backend server. Is it running?")
# # # # #         st.write(f"Details: {e}")
# # # # #     except Exception as e:
# # # # #         st.error("An unexpected error occurred.")
# # # # #         st.write(str(e))


# # # # # # -------------------------------------------------------------
# # # # # # Footer
# # # # # # -------------------------------------------------------------
# # # # # st.markdown(
# # # # #     """
# # # # # ---
# # # # # Made with ❤️ using **LangGraph**, **FastAPI**, and **Streamlit**.
# # # # # """
# # # # # )




# # # # # app.py
# # # # """
# # # # Frontend UI (Streamlit) for Productivity SME Agent
# # # # ===================================================
# # # # This version includes:
# # # # - A stateful, real-time chat interface with DARK THEME FIXES.
# # # # - REAL-TIME STREAMING of the agent's reasoning steps.
# # # # - Sidebar for user settings and session management.
# # # # - Advanced conversation export and email functionality via the agent.
# # # # """

# # # # import streamlit as st
# # # # import requests
# # # # import json
# # # # from datetime import datetime

# # # # # --- Configuration ---
# # # # API_BASE_URL = "http://localhost:8000"
# # # # API_ASK_URL = f"{API_BASE_URL}/ask"
# # # # API_STATUS_URL = f"{API_BASE_URL}/status"

# # # # # -------------------------------------------------------------
# # # # # Streamlit App Configuration
# # # # # -------------------------------------------------------------
# # # # st.set_page_config(
# # # #     page_title="Productivity SME Agent",
# # # #     page_icon="🚀",
# # # #     layout="wide"
# # # # )

# # # # # --- Custom CSS (with Dark Theme Fix) ---
# # # # st.markdown("""
# # # # <style>
# # # #     .main-header {
# # # #         font-size: 2.5rem;
# # # #         font-weight: bold;
# # # #         color: #FAFAFA; /* Lighter text for dark theme */
# # # #         text-align: center;
# # # #         padding-bottom: 1rem;
# # # #     }
# # # #     /* This targets the container of each chat message */
# # # #     [data-testid="stChatMessage"] {
# # # #         background-color: #2D3748; /* Darker background for chat bubbles */
# # # #         border-radius: 0.75rem;
# # # #         border: 1px solid #4A5568;
# # # #     }
# # # #     .warning-box {
# # # #         background-color: #4A3E2A; /* Darker warning box */
# # # #         color: #FFD699;
# # # #         padding: 1rem;
# # # #         border-radius: 0.5rem;
# # # #         border-left: 4px solid #FF9800;
# # # #         margin: 1rem 0;
# # # #     }
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # -------------------------------------------------------------
# # # # # Session State Initialization
# # # # # -------------------------------------------------------------
# # # # if 'messages' not in st.session_state:
# # # #     st.session_state.messages = []
# # # # if 'email_configured' not in st.session_state:
# # # #     st.session_state.email_configured = False
# # # # if 'initialized' not in st.session_state:
# # # #     st.session_state.initialized = False
# # # # if 'user_name' not in st.session_state:
# # # #     st.session_state.user_name = "User"
# # # # if 'user_email' not in st.session_state:
# # # #     st.session_state.user_email = ""

# # # # # -------------------------------------------------------------
# # # # # Helper Functions
# # # # # -------------------------------------------------------------
# # # # def check_backend_status():
# # # #     """Check if email is configured on the backend."""
# # # #     try:
# # # #         response = requests.get(API_STATUS_URL, timeout=2)
# # # #         if response.status_code == 200:
# # # #             st.session_state.email_configured = response.json().get("email_configured", False)
# # # #         else:
# # # #             st.session_state.email_configured = False
# # # #     except requests.exceptions.RequestException:
# # # #         st.session_state.email_configured = False
# # # #         st.error("⚠️ Backend server is not running. Please start the API server.", icon="🔥")
# # # #     st.session_state.initialized = True

# # # # def format_chat_for_export(messages):
# # # #     """Formats a list of chat messages into a single string for the agent."""
# # # #     formatted_string = ""
# # # #     for msg in messages:
# # # #         role = "User" if msg["role"] == "user" else "Assistant"
# # # #         formatted_string += f"**{role}:**\n{msg['content']}\n\n---\n\n"
# # # #     return formatted_string

# # # # if not st.session_state.initialized:
# # # #     check_backend_status()

# # # # # -------------------------------------------------------------
# # # # # Sidebar
# # # # # -------------------------------------------------------------
# # # # with st.sidebar:
# # # #     st.title("⚙️ Settings")
# # # #     st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
# # # #     st.session_state.user_email = st.text_input("Your Email", value=st.session_state.user_email, placeholder="your.email@example.com")
# # # #     st.divider()
# # # #     st.subheader("📧 Email Status")
# # # #     if st.session_state.email_configured:
# # # #         st.success("✅ Email configured on backend")
# # # #     else:
# # # #         st.markdown('<div class="warning-box">', unsafe_allow_html=True)
# # # #         st.warning("⚠️ Email not configured")
# # # #         with st.expander("ℹ️ How to configure"):
# # # #             st.markdown("""
# # # #             The backend needs environment variables to send emails.
# # # #             1. Create a `.env` file in your project root.
# # # #             2. Add the following (using a Gmail App Password):
# # # #             ```env
# # # #             EMAIL_USER=your_email@gmail.com
# # # #             EMAIL_PASSWORD=your_16_digit_app_password
# # # #             ```
# # # #             3. Restart the backend API server.
# # # #             """)
# # # #         st.markdown('</div>', unsafe_allow_html=True)
# # # #     st.divider()
# # # #     st.subheader("📊 Session Info")
# # # #     st.info(f"**Messages:** {len(st.session_state.messages)}")
# # # #     if st.button("🔄 Clear Chat History", use_container_width=True):
# # # #         st.session_state.messages = []
# # # #         st.rerun()
# # # #     if st.session_state.messages:
# # # #         export_data = { "messages": st.session_state.messages }
# # # #         st.download_button(
# # # #             label="💾 Export as JSON",
# # # #             data=json.dumps(export_data, indent=2),
# # # #             file_name=f"chat_export_{datetime.now().strftime('%Y%m%d')}.json",
# # # #             mime="application/json",
# # # #             use_container_width=True
# # # #         )

# # # # # --- Main App ---
# # # # st.markdown('<h1 class="main-header">🚀 Productivity SME Agent</h1>', unsafe_allow_html=True)
# # # # st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")
# # # # st.divider()

# # # # # -------------------------------------------------------------
# # # # # Export & Email Section
# # # # # -------------------------------------------------------------
# # # # if st.session_state.messages:
# # # #     with st.expander("📤 Export & Email Conversation"):
# # # #         # ... (Export logic remains the same, it will now also stream) ...
# # # #         doc_title = st.text_input("Document Title", value=f"Chat Export - {datetime.now().strftime('%Y-%m-%d')}")
# # # #         send_email_enabled = st.checkbox("📧 Send via Email", disabled=not st.session_state.email_configured)
# # # #         if send_email_enabled and not st.session_state.user_email:
# # # #             st.warning("Please enter your email in the sidebar.")

# # # #         if st.button("🚀 Generate & Process", type="primary", use_container_width=True):
# # # #             if send_email_enabled and not st.session_state.user_email:
# # # #                 st.error("Cannot send email without a recipient address.")
# # # #             else:
# # # #                 chat_content = format_chat_for_export(st.session_state.messages)
# # # #                 prompt = f"Create a DOCX report titled '{doc_title}' with this content:\n\n{chat_content}"
# # # #                 if send_email_enabled:
# # # #                     prompt += f"\n\nAfter creating it, email the report to '{st.session_state.user_email}'."
                
# # # #                 # Add this special task to the chat history to be processed like a normal message
# # # #                 st.session_state.messages.append({"role": "user", "content": prompt})
# # # #                 st.rerun()

# # # # # -------------------------------------------------------------
# # # # # Chat Display
# # # # # -------------------------------------------------------------
# # # # for message in st.session_state.messages:
# # # #     with st.chat_message(message["role"]):
# # # #         st.markdown(message["content"])
# # # #         if "reasoning_steps" in message and message["reasoning_steps"]:
# # # #             with st.expander("Show Agent's Reasoning"):
# # # #                 st.code("\n\n".join(message["reasoning_steps"]), language="text")

# # # # # -------------------------------------------------------------
# # # # # Main Streaming Logic
# # # # # -------------------------------------------------------------
# # # # def get_streaming_response(prompt):
# # # #     """Handles the main logic for streaming and updating the UI."""
# # # #     st.session_state.messages.append({"role": "user", "content": prompt})
    
# # # #     # Immediately display the user's message
# # # #     with st.chat_message("user"):
# # # #         st.markdown(prompt)

# # # #     # Set up containers for the assistant's response
# # # #     with st.chat_message("assistant"):
# # # #         answer_placeholder = st.empty()
# # # #         reasoning_placeholder = st.expander("Show Agent's Reasoning", expanded=True)
# # # #         reasoning_steps_content = reasoning_placeholder.empty()

# # # #         final_answer = ""
# # # #         collected_steps = []
        
# # # #         try:
# # # #             with requests.post(API_ASK_URL, json={"question": prompt, "mode": "reasoning"}, stream=True) as response:
# # # #                 response.raise_for_status() # Will raise an exception for 4xx/5xx errors
# # # #                 for line in response.iter_lines():
# # # #                     if line:
# # # #                         decoded_line = line.decode('utf-8')
# # # #                         if decoded_line.startswith('data: '):
# # # #                             try:
# # # #                                 data = json.loads(decoded_line[6:])
# # # #                                 event_type = data.get("type")
# # # #                                 event_data = data.get("data")

# # # #                                 if event_type == "step":
# # # #                                     collected_steps.append(event_data)
# # # #                                     # Update reasoning steps in real-time
# # # #                                     reasoning_steps_content.code("\n\n".join(collected_steps), language='text')
# # # #                                 elif event_type == "final_answer":
# # # #                                     final_answer = event_data
# # # #                                     # Update final answer
# # # #                                     answer_placeholder.markdown(final_answer)

# # # #                             except json.JSONDecodeError:
# # # #                                 pass # Ignore invalid JSON lines
            
# # # #             # After the stream is finished, save the complete message to session state
# # # #             st.session_state.messages.append({
# # # #                 "role": "assistant",
# # # #                 "content": final_answer,
# # # #                 "reasoning_steps": collected_steps
# # # #             })

# # # #         except requests.exceptions.RequestException as e:
# # # #             error_message = f"Connection Error: Could not reach the backend. Please ensure it's running. Details: {e}"
# # # #             answer_placeholder.error(error_message)
# # # #             st.session_state.messages.append({"role": "assistant", "content": error_message, "reasoning_steps": []})

# # # # # -------------------------------------------------------------
# # # # # Chat Input & Quick Suggestions
# # # # # -------------------------------------------------------------
# # # # st.divider()
# # # # st.caption("✨ **Quick questions:**")
# # # # cols = st.columns(4)
# # # # suggestions = ["What is the Pomodoro Technique?", "How can I stop procrastinating?", "Explain the Eisenhower Matrix.", "Best tools for time blocking?"]

# # # # user_query = ""
# # # # for i, suggestion in enumerate(suggestions):
# # # #     if cols[i].button(suggestion, use_container_width=True):
# # # #         user_query = suggestion

# # # # if prompt := st.chat_input("Ask about productivity...") or user_query:
# # # #     get_streaming_response(prompt)
# # # #     # No rerun here, UI is updated live by the streaming function


# # # # app.py (with chat history)

# # # import streamlit as st
# # # import requests
# # # import json
# # # from datetime import datetime

# # # # --- Configuration ---
# # # API_BASE_URL = "http://localhost:8000"
# # # API_ASK_URL = f"{API_BASE_URL}/ask"
# # # API_STATUS_URL = f"{API_BASE_URL}/status"

# # # st.set_page_config(
# # #     page_title="Productivity SME Agent",
# # #     page_icon="🚀",
# # #     layout="wide"
# # # )

# # # st.markdown("""
# # # <style>
# # #     .main-header { font-size: 2.5rem; font-weight: bold; color: #FAFAFA; text-align: center; padding-bottom: 1rem; }
# # #     [data-testid="stChatMessage"] { background-color: #2D3748; border-radius: 0.75rem; border: 1px solid #4A5568; }
# # #     .warning-box { background-color: #4A3E2A; color: #FFD699; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #FF9800; margin: 1rem 0; }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # if 'messages' not in st.session_state:
# # #     st.session_state.messages = []
# # # if 'email_configured' not in st.session_state:
# # #     st.session_state.email_configured = False
# # # if 'initialized' not in st.session_state:
# # #     st.session_state.initialized = False
# # # if 'user_name' not in st.session_state:
# # #     st.session_state.user_name = "User"
# # # if 'user_email' not in st.session_state:
# # #     st.session_state.user_email = ""

# # # def check_backend_status():
# # #     try:
# # #         response = requests.get(API_STATUS_URL, timeout=2)
# # #         if response.status_code == 200:
# # #             st.session_state.email_configured = response.json().get("email_configured", False)
# # #     except requests.exceptions.RequestException:
# # #         st.session_state.email_configured = False
# # #         st.error("⚠️ Backend server is not running.", icon="🔥")
# # #     st.session_state.initialized = True

# # # def format_chat_for_export(messages):
# # #     formatted_string = ""
# # #     for msg in messages:
# # #         role = "User" if msg["role"] == "user" else "Assistant"
# # #         formatted_string += f"**{role}:**\n{msg['content']}\n\n---\n\n"
# # #     return formatted_string

# # # if not st.session_state.initialized:
# # #     check_backend_status()

# # # with st.sidebar:
# # #     st.title("⚙️ Settings")
# # #     st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
# # #     st.session_state.user_email = st.text_input("Your Email", value=st.session_state.user_email, placeholder="your.email@example.com")
# # #     st.divider()
# # #     st.subheader("📧 Email Status")
# # #     if st.session_state.email_configured:
# # #         st.success("✅ Email configured on backend")
# # #     else:
# # #         st.markdown('<div class="warning-box">', unsafe_allow_html=True)
# # #         st.warning("⚠️ Email not configured")
# # #         with st.expander("ℹ️ How to configure"):
# # #             st.markdown("Set `EMAIL_USER` and `EMAIL_PASSWORD` in your backend's `.env` file and restart the API server.")
# # #         st.markdown('</div>', unsafe_allow_html=True)
# # #     st.divider()
# # #     st.subheader("📊 Session Info")
# # #     st.info(f"**Messages:** {len(st.session_state.messages)}")
# # #     if st.button("🔄 Clear Chat History", use_container_width=True):
# # #         st.session_state.messages = []
# # #         st.rerun()
# # #     if st.session_state.messages:
# # #         export_data = { "messages": st.session_state.messages }
# # #         st.download_button(
# # #             label="💾 Export as JSON",
# # #             data=json.dumps(export_data, indent=2),
# # #             file_name=f"chat_export_{datetime.now().strftime('%Y%m%d')}.json",
# # #             mime="application/json",
# # #             use_container_width=True
# # #         )

# # # st.markdown('<h1 class="main-header">🚀 Productivity SME Agent</h1>', unsafe_allow_html=True)
# # # st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")
# # # st.divider()

# # # if st.session_state.messages:
# # #     with st.expander("📤 Export & Email Conversation"):
# # #         doc_title = st.text_input("Document Title", value=f"Chat Export - {datetime.now().strftime('%Y-%m-%d')}")
# # #         send_email_enabled = st.checkbox("📧 Send via Email", disabled=not st.session_state.email_configured)
# # #         if send_email_enabled and not st.session_state.user_email:
# # #             st.warning("Please enter your email in the sidebar.")

# # #         if st.button("🚀 Generate & Process", type="primary", use_container_width=True):
# # #             if send_email_enabled and not st.session_state.user_email:
# # #                 st.error("Cannot send email without a recipient address.")
# # #             else:
# # #                 chat_content = format_chat_for_export(st.session_state.messages)
# # #                 prompt = f"Create a DOCX report titled '{doc_title}' with this content:\n\n{chat_content}"
# # #                 if send_email_enabled:
# # #                     prompt += f"\n\nAfter creating it, email the report to '{st.session_state.user_email}'."
# # #                 st.session_state.messages.append({"role": "user", "content": prompt})
# # #                 st.rerun()

# # # for message in st.session_state.messages:
# # #     with st.chat_message(message["role"]):
# # #         st.markdown(message["content"])
# # #         if "reasoning_steps" in message and message["reasoning_steps"]:
# # #             with st.expander("Show Agent's Reasoning"):
# # #                 st.code("\n\n".join(message["reasoning_steps"]), language="text")

# # # # --- START OF CHANGE ---

# # # def get_streaming_response(prompt):
# # #     """Handles the main logic for streaming and updating the UI."""
# # #     # Create the payload to send to the backend. It now includes chat_history.
# # #     # We only send the last 10 messages to keep the context window manageable.
# # #     history_to_send = st.session_state.messages[-10:]
    
# # #     payload = {
# # #         "question": prompt,
# # #         "mode": "reasoning",
# # #         "chat_history": history_to_send
# # #     }
    
# # #     st.session_state.messages.append({"role": "user", "content": prompt})
    
# # #     with st.chat_message("user"):
# # #         st.markdown(prompt)

# # #     with st.chat_message("assistant"):
# # #         answer_placeholder = st.empty()
# # #         reasoning_placeholder = st.expander("Show Agent's Reasoning", expanded=True)
# # #         reasoning_steps_content = reasoning_placeholder.empty()

# # #         final_answer = ""
# # #         collected_steps = []
        
# # #         try:
# # #             with requests.post(API_ASK_URL, json=payload, stream=True) as response:
# # #                 response.raise_for_status()
# # #                 for line in response.iter_lines():
# # #                     if line:
# # #                         decoded_line = line.decode('utf-8')
# # #                         if decoded_line.startswith('data: '):
# # #                             try:
# # #                                 data = json.loads(decoded_line[6:])
# # #                                 if data.get("type") == "step":
# # #                                     collected_steps.append(data.get("data"))
# # #                                     reasoning_steps_content.code("\n\n".join(collected_steps), language='text')
# # #                                 elif data.get("type") == "final_answer":
# # #                                     final_answer = data.get("data")
# # #                                     answer_placeholder.markdown(final_answer)
# # #                             except json.JSONDecodeError:
# # #                                 pass
            
# # #             st.session_state.messages.append({
# # #                 "role": "assistant",
# # #                 "content": final_answer,
# # #                 "reasoning_steps": collected_steps
# # #             })
# # #         except requests.exceptions.RequestException as e:
# # #             error_message = f"Connection Error: Could not reach the backend. Details: {e}"
# # #             answer_placeholder.error(error_message)
# # #             st.session_state.messages.append({"role": "assistant", "content": error_message, "reasoning_steps": []})

# # # # --- END OF CHANGE ---

# # # st.divider()
# # # st.caption("✨ **Quick questions:**")
# # # cols = st.columns(4)
# # # suggestions = ["What is the Pomodoro Technique?", "How can I stop procrastinating?", "Explain the Eisenhower Matrix.", "Best tools for time blocking?"]
# # # user_query = ""
# # # for i, suggestion in enumerate(suggestions):
# # #     if cols[i].button(suggestion, use_container_width=True):
# # #         user_query = suggestion

# # # if prompt := st.chat_input("Ask a follow-up question...") or user_query:
# # #     get_streaming_response(prompt)


# # # app.py (with download button)

# # import streamlit as st
# # import requests
# # import json
# # import re # Import the regular expression module
# # from datetime import datetime

# # API_BASE_URL = "http://localhost:8000"
# # API_ASK_URL = f"{API_BASE_URL}/ask"
# # API_STATUS_URL = f"{API_BASE_URL}/status"
# # API_DOWNLOAD_URL = f"{API_BASE_URL}/download" # New download endpoint URL

# # st.set_page_config(page_title="Productivity SME Agent", page_icon="🚀", layout="wide")

# # st.markdown("""
# # <style>
# #     .main-header { font-size: 2.5rem; font-weight: bold; color: #FAFAFA; text-align: center; padding-bottom: 1rem; }
# #     [data-testid="stChatMessage"] { background-color: #2D3748; border-radius: 0.75rem; border: 1px solid #4A5568; }
# #     .warning-box { background-color: #4A3E2A; color: #FFD699; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #FF9800; margin: 1rem 0; }
# # </style>
# # """, unsafe_allow_html=True)

# # if 'messages' not in st.session_state: st.session_state.messages = []
# # if 'email_configured' not in st.session_state: st.session_state.email_configured = False
# # if 'initialized' not in st.session_state: st.session_state.initialized = False
# # if 'user_name' not in st.session_state: st.session_state.user_name = "User"
# # if 'user_email' not in st.session_state: st.session_state.user_email = ""

# # def check_backend_status():
# #     try:
# #         response = requests.get(API_STATUS_URL, timeout=2)
# #         if response.status_code == 200: st.session_state.email_configured = response.json().get("email_configured", False)
# #     except requests.exceptions.RequestException:
# #         st.session_state.email_configured = False
# #         st.error("⚠️ Backend server is not running.", icon="🔥")
# #     st.session_state.initialized = True

# # if not st.session_state.initialized: check_backend_status()

# # # (Sidebar and Export logic are unchanged)
# # with st.sidebar:
# #     st.title("⚙️ Settings")
# #     st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
# #     st.session_state.user_email = st.text_input("Your Email", value=st.session_state.user_email, placeholder="your.email@example.com")
# #     st.divider()
# #     st.subheader("📧 Email Status")
# #     if st.session_state.email_configured: st.success("✅ Email configured on backend")
# #     else:
# #         st.markdown('<div class="warning-box">', unsafe_allow_html=True)
# #         st.warning("⚠️ Email not configured")
# #         with st.expander("ℹ️ How to configure"): st.markdown("Set `EMAIL_USER` and `EMAIL_PASSWORD` in your backend's `.env` file.")
# #         st.markdown('</div>', unsafe_allow_html=True)
# #     st.divider()
# #     st.subheader("📊 Session Info")
# #     st.info(f"**Messages:** {len(st.session_state.messages)}")
# #     if st.button("🔄 Clear Chat History", use_container_width=True):
# #         st.session_state.messages = []
# #         st.rerun()
# #     if st.session_state.messages:
# #         st.download_button(label="💾 Export as JSON", data=json.dumps({"messages": st.session_state.messages}, indent=2), file_name="chat_export.json", mime="application/json", use_container_width=True)

# # st.markdown('<h1 class="main-header">🚀 Productivity SME Agent</h1>', unsafe_allow_html=True)
# # st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")
# # st.divider()

# # # (The existing message loop is now simplified, as the streaming logic handles display)
# # for message in st.session_state.messages:
# #     with st.chat_message(message["role"]):
# #         st.markdown(message["content"])
# #         if "download_info" in message:
# #             info = message["download_info"]
# #             st.download_button(label=f"📥 Download {info['filename']}", data=info['data'], file_name=info['filename'], mime='application/octet-stream')
# #         if "reasoning_steps" in message and message["reasoning_steps"]:
# #             with st.expander("Show Agent's Reasoning"):
# #                 st.code("\n\n".join(message["reasoning_steps"]), language="text")

# # # --- START OF MODIFIED SECTION ---

# # def extract_filepath(text: str):
# #     """Uses regex to find a filepath like 'reports/filename.docx'."""
# #     match = re.search(r"reports/([\w\._-]+)", text)
# #     if match:
# #         return match.group(0), match.group(1) # Returns full path and just filename
# #     return None, None

# # def get_streaming_response(prompt):
# #     st.session_state.messages.append({"role": "user", "content": prompt})
    
# #     with st.chat_message("user"):
# #         st.markdown(prompt)

# #     with st.chat_message("assistant"):
# #         answer_placeholder = st.empty()
# #         download_placeholder = st.empty() # Placeholder for our button
# #         reasoning_placeholder = st.expander("Show Agent's Reasoning", expanded=True)
# #         reasoning_steps_content = reasoning_placeholder.empty()

# #         final_answer = ""
# #         collected_steps = []
        
# #         try:
# #             payload = {"question": prompt, "chat_history": st.session_state.messages[-10:]}
# #             with requests.post(API_ASK_URL, json=payload, stream=True) as response:
# #                 response.raise_for_status()
# #                 for line in response.iter_lines():
# #                     if line and line.decode('utf-8').startswith('data: '):
# #                         data = json.loads(line.decode('utf-8')[6:])
# #                         if data.get("type") == "step":
# #                             collected_steps.append(data.get("data"))
# #                             reasoning_steps_content.code("\n\n".join(collected_steps), language='text')
# #                         elif data.get("type") == "final_answer":
# #                             final_answer = data.get("data")
# #                             answer_placeholder.markdown(final_answer)

# #             # ---- NEW LOGIC: Check for file and add download button ----
# #             new_message = {"role": "assistant", "content": final_answer, "reasoning_steps": collected_steps}
# #             full_path, filename = extract_filepath(final_answer)
            
# #             if filename:
# #                 try:
# #                     # Fetch file from backend
# #                     file_url = f"{API_DOWNLOAD_URL}/{filename}"
# #                     file_response = requests.get(file_url)
# #                     if file_response.status_code == 200:
# #                         # Display button in the placeholder
# #                         download_placeholder.download_button(
# #                             label=f"📥 Download {filename}",
# #                             data=file_response.content,
# #                             file_name=filename,
# #                             mime='application/octet-stream'
# #                         )
# #                         # Store download info in the message for redraws
# #                         new_message["download_info"] = {
# #                             "filename": filename,
# #                             "data": file_response.content
# #                         }
# #                     else:
# #                         answer_placeholder.warning(f"Note: Report was created, but I couldn't fetch it for download (Error {file_response.status_code}).")
# #                 except Exception as e:
# #                     answer_placeholder.error(f"Failed to fetch the report for download: {e}")
            
# #             st.session_state.messages.append(new_message)

# #         except requests.exceptions.RequestException as e:
# #             error_message = f"Connection Error: {e}"
# #             answer_placeholder.error(error_message)
# #             st.session_state.messages.append({"role": "assistant", "content": error_message, "reasoning_steps": []})

# # # --- END OF MODIFIED SECTION ---

# # st.divider()
# # st.caption("✨ **Quick questions:**")
# # cols = st.columns(4)
# # suggestions = ["What is the Pomodoro Technique?", "How can I stop procrastinating?"]
# # user_query = ""
# # for i, suggestion in enumerate(suggestions):
# #     if cols[i].button(suggestion, use_container_width=True):
# #         user_query = suggestion

# # if prompt := st.chat_input("Ask a follow-up question...") or user_query:
# #     get_streaming_response(prompt)

# # app.py (with final fix for JSON serialization on API calls)

# import streamlit as st
# import requests
# import json
# import re
# from datetime import datetime

# API_BASE_URL = "http://localhost:8000"
# API_ASK_URL = f"{API_BASE_URL}/ask"
# API_STATUS_URL = f"{API_BASE_URL}/status"
# API_DOWNLOAD_URL = f"{API_BASE_URL}/download"

# st.set_page_config(page_title="Productivity SME Agent", page_icon="🚀", layout="wide")

# st.markdown("""
# <style>
#     .main-header { font-size: 2.5rem; font-weight: bold; color: #FAFAFA; text-align: center; padding-bottom: 1rem; }
#     [data-testid="stChatMessage"] { background-color: #2D3748; border-radius: 0.75rem; border: 1px solid #4A5568; }
#     .warning-box { background-color: #4A3E2A; color: #FFD699; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #FF9800; margin: 1rem 0; }
# </style>
# """, unsafe_allow_html=True)

# if 'messages' not in st.session_state: st.session_state.messages = []
# if 'email_configured' not in st.session_state: st.session_state.email_configured = False
# if 'initialized' not in st.session_state: st.session_state.initialized = False
# if 'user_name' not in st.session_state: st.session_state.user_name = "User"
# if 'user_email' not in st.session_state: st.session_state.user_email = ""

# def check_backend_status():
#     try:
#         response = requests.get(API_STATUS_URL, timeout=2)
#         if response.status_code == 200: st.session_state.email_configured = response.json().get("email_configured", False)
#     except requests.exceptions.RequestException:
#         st.session_state.email_configured = False
#         st.error("⚠️ Backend server is not running.", icon="🔥")
#     st.session_state.initialized = True

# if not st.session_state.initialized: check_backend_status()

# with st.sidebar:
#     st.title("⚙️ Settings")
#     st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
#     st.session_state.user_email = st.text_input("Your Email", value=st.session_state.user_email, placeholder="your.email@example.com")
#     st.divider()
#     st.subheader("📧 Email Status")
#     if st.session_state.email_configured: st.success("✅ Email configured on backend")
#     else:
#         st.markdown('<div class="warning-box">', unsafe_allow_html=True)
#         st.warning("⚠️ Email not configured")
#         with st.expander("ℹ️ How to configure"): st.markdown("Set `EMAIL_USER` and `EMAIL_PASSWORD` in your backend's `.env` file.")
#         st.markdown('</div>', unsafe_allow_html=True)
#     st.divider()
#     st.subheader("📊 Session Info")
#     st.info(f"**Messages:** {len(st.session_state.messages)}")
#     if st.button("🔄 Clear Chat History", use_container_width=True):
#         st.session_state.messages = []
#         st.rerun()
#     if st.session_state.messages:
#         messages_for_json = [{k: v for k, v in msg.items() if k != "download_info"} for msg in st.session_state.messages]
#         st.download_button(label="💾 Export as JSON", data=json.dumps({"messages": messages_for_json}, indent=2), file_name="chat_export.json", mime="application/json", use_container_width=True)

# st.markdown('<h1 class="main-header">🚀 Productivity SME Agent</h1>', unsafe_allow_html=True)
# st.write("Ask any productivity-related question and get expert guidance powered by RAG + Agentic AI.")
# st.divider()

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         if "download_info" in message:
#             info = message["download_info"]
#             st.download_button(label=f"📥 Download {info['filename']}", data=info['data'], file_name=info['filename'], mime='application/octet-stream')
#         if "reasoning_steps" in message and message["reasoning_steps"]:
#             with st.expander("Show Agent's Reasoning"):
#                 st.code("\n\n".join(message["reasoning_steps"]), language="text")

# def extract_filepath(text: str):
#     match = re.search(r"reports/([\w\._-]+)", text)
#     if match:
#         return match.group(0), match.group(1)
#     return None, None

# # --- START OF MODIFIED SECTION ---

# def get_streaming_response(prompt):
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         answer_placeholder = st.empty()
#         download_placeholder = st.empty()
#         reasoning_placeholder = st.expander("Show Agent's Reasoning", expanded=True)
#         reasoning_steps_content = reasoning_placeholder.empty()

#         final_answer = ""
#         collected_steps = []
        
#         try:
#             # --- FIX IS HERE ---
#             # Create a clean version of the history to send to the API, excluding raw byte data.
#             history_to_send = []
#             for msg in st.session_state.messages[-10:]: # Send last 10 messages
#                 clean_msg = {key: value for key, value in msg.items() if key != "download_info"}
#                 history_to_send.append(clean_msg)
            
#             # Use the clean history in the payload.
#             payload = {"question": prompt, "chat_history": history_to_send}
#             # --- END OF FIX ---

#             with requests.post(API_ASK_URL, json=payload, stream=True) as response:
#                 response.raise_for_status()
#                 for line in response.iter_lines():
#                     if line and line.decode('utf-8').startswith('data: '):
#                         data = json.loads(line.decode('utf-8')[6:])
#                         if data.get("type") == "step":
#                             collected_steps.append(data.get("data"))
#                             reasoning_steps_content.code("\n\n".join(collected_steps), language='text')
#                         elif data.get("type") == "final_answer":
#                             final_answer = data.get("data")
#                             answer_placeholder.markdown(final_answer)

#             new_message = {"role": "assistant", "content": final_answer, "reasoning_steps": collected_steps}
#             full_path, filename = extract_filepath(final_answer)
            
#             if filename:
#                 try:
#                     file_url = f"{API_DOWNLOAD_URL}/{filename}"
#                     file_response = requests.get(file_url)
#                     if file_response.status_code == 200:
#                         file_data = file_response.content
#                         download_placeholder.download_button(
#                             label=f"📥 Download {filename}",
#                             data=file_data,
#                             file_name=filename,
#                             mime='application/octet-stream'
#                         )
#                         # We still store the bytes data for the button to persist on reruns
#                         new_message["download_info"] = {"filename": filename, "data": file_data}
#                     else:
#                         answer_placeholder.warning(f"Note: Report was created, but I couldn't fetch it for download (Error {file_response.status_code}).")
#                 except Exception as e:
#                     answer_placeholder.error(f"Failed to fetch the report for download: {e}")
            
#             st.session_state.messages.append(new_message)

#         except requests.exceptions.RequestException as e:
#             error_message = f"Connection Error: {e}"
#             answer_placeholder.error(error_message)
#             st.session_state.messages.append({"role": "assistant", "content": error_message, "reasoning_steps": []})

# # --- END OF MODIFIED SECTION ---

# st.divider()
# st.caption("✨ **Quick questions:**")
# cols = st.columns(2)
# suggestions = ["What is the Pomodoro Technique?", "How can I stop procrastinating?"]
# user_query = ""
# for i, suggestion in enumerate(suggestions):
#     if cols[i].button(suggestion, use_container_width=True):
#         user_query = suggestion

# if prompt := st.chat_input("Ask a follow-up question...") or user_query:
#     get_streaming_response(prompt)


# app.py (Main Landing Page)

import streamlit as st

st.set_page_config(
    page_title="Productivity SME Agent",
    page_icon="🚀",
    layout="wide"
)

# This automatically redirects the user to the main chat page.
st.switch_page("pages/1_💬_Chat.py")