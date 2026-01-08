import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 1. Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# 2. Conexión con Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Configura tu llave en los Secrets de Streamlit.")
    st.stop()

# 3. Función para voz (Audio)
def texto_a_voz(texto):
    try:
        archivo = "voz_temp.mp3"
        if os.path.exists(archivo):
            os.remove(archivo)
        tts = gTTS(text=texto, lang='es')
        tts.save(archivo)
        return archivo
    except:
        return None

# --- TÍTULO Y VERSÍCULO DEL DÍA ---
st.title("✨ Dios habla contigo")

@st.cache_data(ttl=86400)
def obtener_versiculo_dia():
    try:
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Da un versículo bíblico corto y su cita para hoy."}],
            model="llama-3.3-70b-versatile"
        )
        return res.choices[0].message.content
    except:
        return "Jehová es mi pastor; nada me faltará. - Salmos 23:1"

st.info(f"🌟 **VERSÍCULO DEL DÍA**\n\n{obtener_versiculo_dia()}")

st.divider()

# --- MENÚ PRINCIPAL POR BOTONES ---
if 'menu' not in st.session_state:
    st.session_state.menu = 'inicio'

# Botones grandes para celular
col1, col2 = st.columns(2)
with col1:
    if st.button("🙏 PALABRA DE ALIENTO", use_container_width=True):
        st.session_state.menu = 'aliento'
    if st.button("☀️ DEVOCIONAL DIARIO", use_container_width=True):
        st.session_state.menu = 'devocional'
with col2:
    if st.button("📖 CONSEJO DE DIOS", use_container_width=True):
        st.session_state.menu = 'consejo'
    if st.button("📜 LA SANTA BIBLIA", use_container_width=True):
        st.session_state.menu = 'biblia'

# --- LÓGICA DE LAS SECCIONES ---

if st.session_state.menu == 'aliento':
    st.subheader("🙏 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        with st.spinner("Dios te escucha..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres Jesús. Da un versículo y aliento corto."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            st.audio(texto_a_voz(res))

elif st.session_state.menu == 'consejo':
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
            st.audio(texto_a_voz(res))

elif st.session_state.menu == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Devocional"):
        with st.spinner("Preparando tu alimento espiritual..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Crea un devocional con título, versículo, reflexión y oración."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(res)
            st.audio(texto_a_voz(res))

elif st.session_state.menu == 'biblia':
    st.subheader("📜 La Santa Biblia")
    libros = ["Génesis", "Éxodo", "Salmos", "Mateo", "Juan", "Apocalipsis"] # Puedes añadir más
    libro_sel = st.selectbox("Selecciona un Libro", libros)
    cap = st.number_input("Capítulo", min_value=1, step=1)
    if st.button("Leer"):
        with st.spinner("Abriendo las escrituras..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Muestra el texto de {libro_sel} capítulo {cap} en español Reina Valera 1960."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(f"### {libro_sel} {cap}")
            st.write(res)

# Botón para volver siempre visible si no estás en el inicio
if st.session_state.menu != 'inicio':
    st.divider()
    if st.button("⬅️ Volver al Menú"):
        st.session_state.menu = 'inicio'
        st.rerun()
