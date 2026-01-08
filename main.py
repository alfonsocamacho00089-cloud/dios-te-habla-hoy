import streamlit as st
from groq import Groq
from gtts import gTTS
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Función para convertir texto a voz
def texto_a_voz(texto, filename="respuesta.mp3"):
    try:
        tts = gTTS(text=texto, lang='es')
        tts.save(filename)
        return filename
    except:
        return None

# Conexión con Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura tu GROQ_API_KEY en Secrets.")
    st.stop()

# --- VERSÍCULO DEL DÍA (ESTÁTICO AL INICIO) ---
st.markdown("<h1 style='text-align: center;'>✨ Dios habla contigo</h1>", unsafe_content_html=True)

@st.cache_data(ttl=86400)
def obtener_versiculo_dia():
    try:
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Da un versículo bíblico corto de esperanza para hoy con su cita. Solo el texto y la cita."}],
            model="llama-3.3-70b-versatile",
        )
        return res.choices[0].message.content
    except:
        return "Todo lo puedo en Cristo que me fortalece. - Filipenses 4:13"

st.info(f"🌟 **VERSÍCULO DEL DÍA**\n\n{obtener_versiculo_dia()}")

st.markdown("---")

# --- MENÚ DE NAVEGACIÓN POR BOTONES ---
if 'menu' not in st.session_state:
    st.session_state.menu = 'inicio'

# Diseño de botones en cuadrícula
col1, col2 = st.columns(2)
with col1:
    if st.button("🙏 PALABRA DE ALIENTO", use_container_width=True):
        st.session_state.menu = 'aliento'
    if st.button("☀️ DEVOCIONAL DIARIO", use_container_width=True):
        st.session_state.menu = 'devocional'
with col2:
    if st.button("🙏 CONSEJO DE DIOS", use_container_width=True):
        st.session_state.menu = 'consejo'
    if st.button("📜 LEER LA BIBLIA", use_container_width=True):
        st.session_state.menu = 'biblia'

st.markdown("---")

# --- LÓGICA DE SECCIONES ---

if st.session_state.menu == 'aliento':
    st.subheader("📖 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        with st.spinner("Escuchando..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres Jesus de Nazareth. Da un versículo y aliento corto."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            audio = texto_a_voz(res, "aliento.mp3")
            if audio: st.audio(audio)

elif st.session_state.menu == 'consejo':
    st.subheader("🙏 Consejo de Dios")
    problema = st.text_area("Cuéntale a Dios tu situación:")
    if st.button("Pedir Sabiduría"):
        with st.spinner("Buscando en la Palabra..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres un pastor compasivo. Da un consejo bíblico detallado."},
                          {"role": "user", "content": problema}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            audio = texto_a_voz(res, "consejo.mp3")
            if audio: st.audio(audio)

elif st.session_state.menu == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Devocional"):
        with st.spinner("Preparando..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Crea un devocional con título, versículo, reflexión y oración."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.write(res)
            audio = texto_a_voz(res, "devocional.mp3")
            if audio: st.audio(audio)

elif st.session_state.menu == 'biblia':
    st.subheader("📜 La Santa Biblia")
    # API Directa para leer la Biblia
    libro = st.selectbox("Selecciona un Libro", ["Genesis", "Exodo", "Levitico", "Numeros", "Deuteronomio", "Mateo", "Marcos", "Lucas", "Juan", "Salmos"])
    capitulo = st.number_input("Capítulo", min_value=1, step=1)
    
    if st.button("Abrir Biblia"):
        # Usamos la IA para que nos traiga el capítulo rápido y en español
        with st.spinner("Abriendo las escrituras..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Muestra el texto completo del libro de {libro} capítulo {capitulo}. Versión Reina Valera 1960."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(f"### {libro} {capitulo}")
            st.write(res)

if st.session_state.menu != 'inicio':
    if st.button("⬅️ Volver al Menú"):
        st.session_state.menu = 'inicio'
        st.rerun()
