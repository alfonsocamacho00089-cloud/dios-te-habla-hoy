import streamlit as st
from groq import Groq
from gtts import gTTS
from datetime import datetime
import requests

# Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Función para convertir texto a voz
def texto_a_voz(texto, filename="respuesta.mp3"):
    try:
        if os.path.exists(filename): os.remove(filename)
        tts = gTTS(text=texto, lang='es')
        tts.save(filename)
        return filename
    except: return None

# Conexión con Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura tu GROQ_API_KEY en Secrets.")
    st.stop()

# --- 1. VERSÍCULO DEL DÍA (ARRIBA DE TODO) ---
st.markdown("<h1 style='text-align: center;'>✨ Dios habla contigo</h1>", unsafe_content_html=True)
fecha_hoy = datetime.now().strftime("%d/%m/%Y")

# Generar versículo del día automáticamente al iniciar
@st.cache_data(ttl=86400) # Se guarda por 24 horas
def obtener_versiculo_dia():
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": "Da un versículo bíblico inspirador para hoy con su cita. Solo el texto y la cita, muy corto."}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

st.info(f"🌟 **Versículo del Día ({fecha_hoy}):**\n\n{obtener_versiculo_dia()}")

st.markdown("---")

# --- 2. MENÚ DE NAVEGACIÓN (BOTONES) ---
if 'seccion' not in st.session_state:
    st.session_state.seccion = 'Inicio'

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🙏 Aliento"): st.session_state.seccion = 'Aliento'
with col2:
    if st.button("📖 Consejo"): st.session_state.seccion = 'Consejo'
with col3:
    if st.button("☀️ Devocional"): st.session_state.seccion = 'Devocional'
with col4:
    if st.button("📜 Biblia"): st.session_state.seccion = 'Biblia'

st.markdown("---")

# --- 3. LÓGICA DE LAS SECCIONES ---

# --- SECCIÓN: ALIENTO ---
if st.session_state.seccion == 'Aliento':
    st.subheader("🙏 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        with st.spinner("Jesús te responde..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres Jesús. Da un versículo y aliento corto."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.write(res)
            st.audio(texto_a_voz(res, "aliento.mp3"))

# --- SECCIÓN: CONSEJO ---
elif st.session_state.seccion == 'Consejo':
    st.subheader("📖 Consejo de Dios")
    problema = st.text_area("¿Qué te preocupa?")
    if st.button("Pedir Sabiduría"):
        with st.spinner("Buscando en la Palabra..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres un pastor compasivo. Da un consejo bíblico."},
                          {"role": "user", "content": problema}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            st.audio(texto_a_voz(res, "consejo.mp3"))

# --- SECCIÓN: DEVOCIONAL ---
elif st.session_state.seccion == 'Devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Devocional de Hoy"):
        with st.spinner("Preparando alimento espiritual..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Crea un devocional con título, versículo, reflexión y oración."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(res)
            st.audio(texto_a_voz(res, "devocional.mp3"))

# --- SECCIÓN: LA BIBLIA ---
elif st.session_state.seccion == 'Biblia':
    st.subheader("📜 La Santa Biblia")
    st.write("Lee la palabra de Dios desde Génesis hasta Apocalipsis.")
    
    # API gratuita de la Biblia
    libros = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
    
    libro_sel = st.selectbox("Selecciona un Libro", libros)
    cap_sel = st.number_input("Capítulo", min_value=1, value=1)
    
    if st.button("Leer Capítulo"):
        url = f"https://bible-api.com/{libro_sel}+{cap_sel}?translation=rvr1960" # Usando Reina Valera si está disponible o inglés por defecto
        try:
            r = requests.get(url).json()
            st.markdown(f"### {libro_sel} {cap_sel}")
            st.write(r['text'])
        except:
            st.error("No se pudo cargar este capítulo. Intenta con otro.")

st.markdown("---")
st.caption("Hecho para bendecir tu caminar con Dios.")
