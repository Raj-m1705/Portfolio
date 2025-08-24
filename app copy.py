import streamlit as st
from pathlib import Path
from rag import query_rag  # Replace with your RAG query function

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Interactive Portfolio",
    page_icon=":briefcase:",
    layout="wide",
)

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown(
    """
    <style>
    /* App background and font */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Chat message box */
    .chat-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-msg {
        background-color: #dcf8c6;
        margin-left: auto;
    }
    .bot-msg {
        background-color: #ffffff;
        margin-right: auto;
    }
    /* Sidebar headers */
    .sidebar .sidebar-content {
        background: #f0f2f6;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar PDFs
# -----------------------------
st.sidebar.header("Pre-made Profiles")
pdf_files = {
    "Profile 1": "assets/profile1.pdf",
    "Profile 2": "assets/profile2.pdf",
    "Profile 3": "assets/profile3.pdf",
    "Profile 4": "assets/profile4.pdf",
    "Profile 5": "assets/profile5.pdf",
}

# Initialize suggested PDFs in session
if 'suggested_pdfs' not in st.session_state:
    st.session_state.suggested_pdfs = []

# PDF download buttons
for name, path in pdf_files.items():
    if Path(path).exists():
        with open(path, "rb") as f:
            st.sidebar.download_button(label=f"Download {name}", data=f, file_name=f"{name}.pdf")

# -----------------------------
# Chat functionality
# -----------------------------
st.title("🤖 Interactive Portfolio Chatbot")

# Initialize messages in session
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# -----------------------------
# User input
# -----------------------------
def suggest_pdfs(user_query):
    """Basic keyword-based PDF suggestion. Replace with ML/embedding-based if needed."""
    suggestions = []
    keywords = {
        "AI": ["Profile 1", "Profile 3"],
        "Python": ["Profile 2"],
        "Web": ["Profile 4"],
        "Projects": ["Profile 3", "Profile 5"],
        "Experience": ["Profile 1", "Profile 2"],
    }
    for key, pdfs in keywords.items():
        if key.lower() in user_query.lower():
            suggestions.extend(pdfs)
    return list(set(suggestions))


# -----------------------------
# Display chat messages
# -----------------------------
chat_placeholder = st.container()
with chat_placeholder:
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        role_label = "You" if msg["role"] == "user" else "Bot"
        st.markdown(f"<div class='chat-box {role_class}'><b>{role_label}:</b> {msg['content']}</div>", unsafe_allow_html=True)

        
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything about my career, skills, or experience:")
    send_button = st.form_submit_button("Send")

if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Query RAG
    bot_response = query_rag(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Suggest PDFs
    st.session_state.suggested_pdfs = suggest_pdfs(user_input)

# -----------------------------
# Suggested PDFs
# -----------------------------
if st.session_state.suggested_pdfs:
    st.markdown("### Suggested PDFs for you:")
    for pdf_name in st.session_state.suggested_pdfs:
        pdf_path = pdf_files[pdf_name]
        if Path(pdf_path).exists():
            with open(pdf_path, "rb") as f:
                st.download_button(label=f"Download {pdf_name}", data=f, file_name=f"{pdf_name}.pdf")
