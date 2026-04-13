import streamlit as st
import asyncio
import edge_tts
import tempfile
import base64
import os
import random

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Let's Learn Spanish with Gesner", layout="wide")

# Colorful CSS with explicit white text for all content, plus visible sidebar selectbox
def set_colorful_style():
    st.markdown(
        """
        <style>
        /* Overall app background – purple gradient */
        .stApp {
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e);
        }
        /* Main header (colorful) */
        .main-header {
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb);
            padding: 1.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .main-header h1 {
            color: white;
            text-shadow: 2px 2px 4px #000000;
            font-size: 2.5rem;
            margin: 0;
        }
        .main-header p {
            color: #fff5cc;
            font-size: 1.2rem;
            margin: 0;
        }
        /* Force ALL text to white everywhere */
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, 
        .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, 
        .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable,
        .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander,
        .stProgress > div, .stMetric label, .stMetric value,
        div, p, span, pre, code, .element-container, .stTextArea label,
        .stText p, .stText div, .stText span, .stText code {
            color: white !important;
        }
        /* Specifically for conversation text (st.text) */
        .stText {
            color: white !important;
            font-size: 1rem;
            background: transparent !important;
        }
        /* Tabs text (white) */
        .stTabs [role="tab"] {
            color: white !important;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            margin: 0 2px;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background: rgba(255,255,255,0.3);
            color: white !important;
        }
        /* Quiz radio button options */
        .stRadio [role="radiogroup"] label {
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            padding: 0.3rem;
            margin: 0.2rem 0;
            color: white !important;
        }
        /* Buttons */
        .stButton button {
            background-color: #ff6b6b;
            color: white;
            border-radius: 30px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #feca57;
            color: black;
        }
        /* Sidebar (already dark, but ensure text white) */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e);
        }
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stText,
        section[data-testid="stSidebar"] label {
            color: white !important;
        }
        /* ----- FIX: Make sidebar lesson selector (selectbox) visible ----- */
        section[data-testid="stSidebar"] .stSelectbox label {
            color: white !important;
        }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
            background-color: #2d1b4e;
            border: 1px solid #ffcc00;
            border-radius: 10px;
        }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div {
            color: white !important;
        }
        section[data-testid="stSidebar"] .stSelectbox svg {
            fill: white;
        }
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span {
            color: white !important;
        }
        /* Dropdown menu items (options) */
        div[data-baseweb="popover"] ul {
            background-color: #2d1b4e;
            border: 1px solid #ffcc00;
        }
        div[data-baseweb="popover"] li {
            color: white !important;
            background-color: #2d1b4e;
        }
        div[data-baseweb="popover"] li:hover {
            background-color: #ff6b6b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_logo():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="3"/>
                <defs>
                    <linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#ff007f;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#ffcc00;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#00ffcc;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
        """,
        unsafe_allow_html=True
    )

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_colorful_style()
    st.title("🔐 Login Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Spanish with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #FFD700;'>Book 1 – Lessons 1 to 20</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

# ------------------------------
# AFTER LOGIN – MAIN APP
# ------------------------------
set_colorful_style()

st.markdown("""
<div class="main-header">
    <h1>📘 Let's Learn Spanish with Gesner</h1>
    <p>Book 1 – 20 lecciones interactivas | Conversaciones cotidianas | Vocabulario | Gramática | Pronunciación | Cuestionarios</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR – LESSON SELECTOR & COMPANY INFO & LOGOUT
# ------------------------------
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Selecciona la lección")
    lesson_number = st.selectbox("Lección", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Tu progreso")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lección {lesson_number} de 20 completada")
    st.markdown("---")
    st.markdown("**Fundador y Desarrollador:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Sitio web principal](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Precio")
    st.markdown("**$299 USD** (libro completo – 20 lecciones, código fuente incluido)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("Todos los derechos reservados")
    st.markdown("---")
    # Logout button
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ------------------------------
# LESSON DATA GENERATION (20 lessons in Spanish)
# ------------------------------
temas = [
    "Presentarse", "Rutina diaria", "En el supermercado", "Pedir comida", "Preguntar direcciones",
    "Hablar de la familia", "En el consultorio médico", "Entrevista de trabajo", "Planear un viaje", "Clima y estaciones",
    "Comprar ropa", "En el banco", "Usar transporte público", "Alquilar un apartamento", "Celebrar un cumpleaños",
    "Ir al cine", "En el gimnasio", "Hacer una llamada", "Escribir un correo", "Hablar de pasatiempos"
]

def generar_conversaciones(tema):
    conv1 = f"A: ¡Hola! ¿Cómo estás hoy?\nB: ¡Estoy bien, gracias! Estoy aprendiendo sobre {tema}.\nA: Eso es maravilloso. ¿Puedes contarme más?\nB: ¡Claro! Practico todos los días."
    conv2 = f"A: Disculpa, ¿podrías ayudarme con {tema}?\nB: ¡Por supuesto! ¿Qué necesitas saber?\nA: Quiero mejorar mi español.\nB: Esa es una gran meta. ¡Sigue practicando!"
    conv3 = f"A: Hola, soy nuevo aquí. ¿Puedes explicarme {tema}?\nB: ¡Absolutamente! Es muy útil para la vida diaria.\nA: ¡Muchas gracias!\nB: De nada. Practiquemos juntos."
    return [conv1, conv2, conv3]

def generar_vocabulario(tema):
    base_words = ["hola", "adiós", "por favor", "gracias", "sí", "no", "tal vez", "siempre", "a veces", "nunca",
                  "rápidamente", "lentamente", "cuidadosamente", "felizmente", "tristemente", "en voz alta", "en voz baja", "brillantemente", "oscuramente", "suavemente"]
    tema_words = [tema.lower().replace(" ", "_") + str(i) for i in range(1, 6)]
    all_words = base_words[:15] + tema_words
    return all_words[:20]

def generar_reglas_gramaticales(tema):
    reglas = [
        "1. Usa el presente simple para hechos y rutinas.",
        "2. Usa 'ser' y 'estar' correctamente (características permanentes vs. estados temporales).",
        "3. Usa 'tener' para expresar posesión y edad.",
        "4. Usa 'poder' para expresar habilidad o permiso.",
        "5. Usa 'hacer' para preguntar sobre el clima (¿Qué tiempo hace?).",
        "6. Los adverbios de frecuencia (siempre, a veces, nunca) van antes del verbo principal.",
        "7. Usa las preposiciones de lugar (en, sobre, debajo de) correctamente.",
        "8. Usa 'hay' para decir que algo existe.",
        "9. Usa 'me gustaría' para peticiones corteses.",
        "10. Usa 'ir a' para planes futuros."
    ]
    random.shuffle(reglas)
    return reglas

def generar_oraciones_pronunciacion(tema):
    oraciones = [
        f"Estoy aprendiendo sobre {tema} hoy.",
        f"¿Podrías explicarme {tema} por favor?",
        f"Practicar {tema} me ayuda a mejorar mi español.",
        f"Hablemos sobre {tema} juntos.",
        f"Entender {tema} es muy útil."
    ]
    return oraciones

def generar_preguntas_cuestionario(tema, textos_conv):
    preguntas = [
        {"pregunta": "¿Cuál es el tema principal de esta lección?", "opciones": [tema, "Deportes", "Música", "Películas"], "respuesta": tema},
        {"pregunta": "¿Qué palabra significa 'dar las gracias'?", "opciones": ["Por favor", "Lo siento", "Gracias", "Disculpe"], "respuesta": "Gracias"},
        {"pregunta": "¿Cómo se pide ayuda de manera cortés?", "opciones": ["Dame ayuda", "Ayuda ahora", "¿Podrías ayudarme por favor?", "Debes ayudar"], "respuesta": "¿Podrías ayudarme por favor?"},
        {"pregunta": "¿Qué significa 'siempre'?", "opciones": ["Nunca", "A veces", "Cada vez", "Raramente"], "respuesta": "Cada vez"},
        {"pregunta": "¿Cuál oración es correcta?", "opciones": ["Él ir a la escuela", "Él va a la escuela", "Él yendo a la escuela", "Él ido a la escuela"], "respuesta": "Él va a la escuela"}
    ]
    return preguntas

@st.cache_data
def obtener_datos_leccion(num_leccion):
    tema = temas[num_leccion - 1]
    conversaciones = generar_conversaciones(tema)
    vocabulario = generar_vocabulario(tema)
    gramatica = generar_reglas_gramaticales(tema)
    pronunciacion = generar_oraciones_pronunciacion(tema)
    cuestionario = generar_preguntas_cuestionario(tema, conversaciones)
    return {
        "tema": tema,
        "conversaciones": conversaciones,
        "vocabulario": vocabulario,
        "gramatica": gramatica,
        "pronunciacion": pronunciacion,
        "cuestionario": cuestionario
    }

# ------------------------------
# DISPLAY LESSON CONTENT
# ------------------------------
datos_leccion = obtener_datos_leccion(lesson_number)

st.markdown(f"## 📖 Lección {lesson_number}: {datos_leccion['tema']}")

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversaciones", "📚 Vocabulario", "📖 Gramática", "🎧 Pronunciación", "❓ Cuestionario"])

# Helper to generate audio from text (Spanish voice)
async def texto_a_audio(texto, archivo):
    await edge_tts.Communicate(texto, "es-ES-AlvaroNeural").save(archivo)

def reproducir_audio(texto, key):
    if st.button(f"🔊 Escuchar audio", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            asyncio.run(texto_a_audio(texto, tmp.name))
            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

# Tab 1: Conversations
with tab1:
    for i, conv in enumerate(datos_leccion["conversaciones"], 1):
        st.markdown(f"**Conversación {i}**")
        st.text(conv)
        reproducir_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

# Tab 2: Vocabulary
with tab2:
    cols = st.columns(4)
    for idx, palabra in enumerate(datos_leccion["vocabulario"]):
        with cols[idx % 4]:
            st.markdown(f"**{palabra.capitalize()}**")
            reproducir_audio(palabra, f"vocab_{lesson_number}_{idx}")

# Tab 3: Grammar
with tab3:
    for regla in datos_leccion["gramatica"]:
        st.markdown(f"- {regla}")

# Tab 4: Pronunciation (listen and repeat)
with tab4:
    st.markdown("Escucha cada oración, luego repite en voz alta.")
    for idx, oracion in enumerate(datos_leccion["pronunciacion"]):
        st.markdown(f"**Oración {idx+1}:** {oracion}")
        reproducir_audio(oracion, f"pron_{lesson_number}_{idx}")
        st.markdown("---")

# Tab 5: Quiz
with tab5:
    st.markdown("Prueba tu comprensión de esta lección.")
    if f"quiz_answers_{lesson_number}" not in st.session_state:
        st.session_state[f"quiz_answers_{lesson_number}"] = {}
    puntaje = 0
    for q_idx, q in enumerate(datos_leccion["cuestionario"]):
        st.markdown(f"**{q_idx+1}. {q['pregunta']}**")
        respuesta = st.radio("Elige una respuesta:", q["opciones"], key=f"quiz_{lesson_number}_{q_idx}", label_visibility="hidden")
        st.session_state[f"quiz_answers_{lesson_number}"][q_idx] = respuesta
        if respuesta == q["respuesta"]:
            puntaje += 1
    if st.button("Verificar respuestas", key=f"check_{lesson_number}"):
        st.success(f"Obtuviste {puntaje} de {len(datos_leccion['cuestionario'])} correctas!")
        if puntaje == len(datos_leccion["cuestionario"]):
            st.balloons()
            st.markdown("🎉 ¡Perfecto! Has dominado esta lección.")

# After lesson 20, show contact info
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 ¡Felicidades! Has completado el Libro 1.")
    st.markdown("""
    ### 📞 Para continuar con el Libro 2, contáctanos:
    - **Gesner Deslandes** – Fundador
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    El Libro 2 contendrá conversaciones más avanzadas, vocabulario, gramática y simulaciones de la vida real.
    """)
