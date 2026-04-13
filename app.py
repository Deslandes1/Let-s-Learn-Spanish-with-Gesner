import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Enhanced safe import for edge_tts -----
EDGE_TTS_AVAILABLE = False
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except Exception as e:
    st.error(f"❌ Audio Setup Error: {e}")

st.set_page_config(page_title="Learn Spanish with Gesner", layout="wide", page_icon="📘")

def set_shining_style():
    """Applies a 'shining' professional aesthetic with gold accents."""
    st.markdown("""
        <style>
        /* Base Background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white !important;
        }
        
        /* Shining Header */
        .main-header {
            background: linear-gradient(90deg, #FFD700, #B8860B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-weight: 800;
            margin-bottom: 2rem;
            border-bottom: 2px solid rgba(255, 215, 0, 0.3);
        }

        /* Glassmorphism Cards for Tabs/Buttons */
        div[data-baseweb="tab-panel"] {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stButton button {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000 !important;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: scale(1.02);
            box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.5);
        }
        
        /* White text for all standard elements */
        h1, h2, h3, p, label, .stMarkdown {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

async def generate_speech(text, file_path):
    """Core async function for TTS"""
    communicate = edge_tts.Communicate(text, "es-ES-AlvaroNeural")
    await communicate.save(file_path)

def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.warning("Audio disabled. Check requirements.")
        return
    
    if st.button(f"🔊 Listen", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            asyncio.run(generate_speech(text, tmp.name))
            with open(tmp.name, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width:100%"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

# --- App Logic ---
set_shining_style()

# Authentication (Simple)
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 class='main-header'>GLOBALINTERNET.PY</h1>", unsafe_allow_html=True)
        pw = st.text_input("Enter Access Code", type="password")
        if st.button("Unlock Content"):
            if pw == "20082010":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Code")
    st.stop()

# --- Content Sections ---
with st.sidebar:
    st.title("Spanish Mastery")
    lesson = st.slider("Select Lesson", 1, 20, 1)
    st.divider()
    st.info(f"Instructor: Gesner Deslandes\n\nProject: EduHumanity")

# Content generation based on 'lesson' (mapping to your 'temas' list)
st.markdown(f"<h1 class='main-header'>Lesson {lesson}: Ready to Learn</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["Conversation", "Vocabulary", "Quiz"])

with t1:
    content = "¡Hola! Bienvenidos a la lección de hoy. Vamos a practicar español juntos."
    st.write(content)
    play_audio(content, f"main_audio_{lesson}")

with t3:
    st.write("Test your knowledge for this module.")
    ans = st.radio("Choose the correct greeting:", ["Hola", "Adiós", "Gracias"])
    if st.button("Check Answer"):
        if ans == "Hola": st.success("Correct!")
        else: st.error("Try again!")
