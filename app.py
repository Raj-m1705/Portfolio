import streamlit as st
from pathlib import Path
from your_rag_module import query_rag  # Replace with your RAG query function

st.set_page_config(
    page_title="Interactive Portfolio",
    page_icon=":briefcase:",
    layout="wide",
)

# CSS for eye-catching design
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Interactive Portfolio Chatbot")

# Sidebar for PDF downloads
st.sidebar.header("Pre-made Profiles")
pdf_files = {
    "Profile 1": "assets/profile1.pdf",
    "Profile 2": "assets/profile2.pdf",
    "Profile 3": "assets/profile3.pdf",
    "Profile 4": "assets/profile4.pdf",
    "Profile 5": "assets/profile5.pdf",
}

# Placeholder for suggested PDFs
if 'suggested_pdfs' not in st.session_state:
    st.session_state.suggested_pdfs = []

for name, path in pdf_files.items():
    with open(path, "rb") as f:
        st.sidebar.download_button(label=f"Download {name}", data=f, file_name=f"{name}.pdf")

# Chat interface
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.text_input("Ask me anything about my career, skills, or experience:")

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

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from your RAG pipeline
    bot_response = query_rag(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Suggest relevant PDFs
    st.session_state.suggested_pdfs = suggest_pdfs(user_input)

# Display chat messages
for msg in st.session_state.messages:
    role = "You" if msg["role"] == "user" else "Bot"
    st.markdown(f"<div class='chat-box'><b>{role}:</b> {msg['content']}</div>", unsafe_allow_html=True)

# Show suggested PDFs
if st.session_state.suggested_pdfs:
    st.markdown("### Suggested PDFs for you:")
    for pdf_name in st.session_state.suggested_pdfs:
        pdf_path = pdf_files[pdf_name]
        with open(pdf_path, "rb") as f:
            st.download_button(label=f"Download {pdf_name}", data=f, file_name=f"{pdf_name}.pdf")
