import streamlit as st
import time
from real_time_input import audio_input
from query_crewai import solve_query
from real_time_output import audio_output
import warnings
warnings.filterwarnings("ignore")

# # Helper to update log
# def update_log(log_box, log_list, new_message):
#     log_list.append(new_message)
#     log_box.text("\n".join(log_list))



# Page Configuration and Styling
st.set_page_config(layout="wide", page_title="Audio Query Solver", page_icon="🎙️")
with st.sidebar:
    st.title("🧠 How to Use")
    st.markdown("""
    1. Click **Start Speaking 🎤** to begin.
    2. Speak your query clearly.
    3. The app will transcribe, translate, respond, and play audio.
    4. Scroll down to see the logs and text.
    """)
    st.info("Supports multilingual input!")

# Styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main > div {
            background: linear-gradient(to right, #f3e8ff, #ffffff, #f3e8ff);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .title {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            color: #5e17eb;
            margin-bottom: 2rem;
        }

        .stButton>button {
            background-color: #5e17eb;
            color: white;
            border: None;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            border-radius: 10px;
            transition: background-color 0.3s;
        }

        .stButton>button:hover {
            background-color: #4c12cc;
        }

        .stTextArea textarea {
            border-radius: 10px;
            background-color: #2b2b2b; /* Slight black-grey */
            color: white;
            border: 1px solid #555;
        }

        .log-container {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 1rem;
            color: white;
            font-size: 0.95rem;
            min-height: 250px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown('<div class="title">🎙️ A Real-Time Multilingual Voice Assistant 🌐</div>', unsafe_allow_html=True)


# Layout
col1, col2 = st.columns(2)

with col2:
    st.subheader("Progress Log")
    bar = st.progress(0)
    progress_text = st.empty()
    log_placeholder = st.empty()
    if "log_list" not in st.session_state:
        st.session_state.log_list = []

    def update_log(log_box, log_list, new_message):
        log_list.append(f"• {new_message}")
        with log_box.container():
            st.markdown(f'<div class="log-container">{"<br>".join(log_list)}</div>', unsafe_allow_html=True)

def update_progress(progress, bar, text_box):
    bar.progress(progress)
    text_box.markdown(f"**Progress: {progress}%**")

with col1:
    st.subheader("Voice Input Section")
    if st.button("Start Speaking 🎤"):
        st.session_state.log_list = []
        update_progress(0,bar, progress_text)
        update_log(log_placeholder, st.session_state.log_list, "Please speak, audio is processing.....")
        

        lang, context = audio_input()
        update_log(log_placeholder, st.session_state.log_list, "Language is detected!!")
        update_progress(20,bar, progress_text)

        update_log(log_placeholder, st.session_state.log_list, "Transcription is done!!")
        update_progress(30,bar, progress_text)

        st.text_area("Transcribed", f"Language of user is: \n{lang}\n\n Query is: \n{context}\n\n", height=150)

        update_log(log_placeholder, st.session_state.log_list, "Generating Response....")

        response = str(solve_query(context))
        update_progress(70,bar, progress_text)

        audio_text = response[:300] if len(response) > 300 else response
        update_log(log_placeholder, st.session_state.log_list, "listen audio now!!")
        update_progress(90,bar, progress_text)
        time.sleep(3)
        audio_output(audio_text, lang)
        st.text_area("Answer:", f"Response: \n{response}\n\n", height=150)
        update_progress(100,bar, progress_text)
        update_log(log_placeholder, st.session_state.log_list, "Done! Try some other query:)")

