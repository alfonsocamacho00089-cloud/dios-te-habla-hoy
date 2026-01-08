import streamlit as st
from groq import Groq
from gtts import gTTS
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Función para voz
def texto_a_voz(texto, filename="temp.mp3"):
    try:
        if os.path.exists(filename):
            os.remove(filename)
        tts = gTTS(text=texto, lang='es')
        tts.save(filename)
        return filename
    except:
        return None

# Conexión Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Configura la API Key en Secrets.")
    st.stop()

# --- TÍTULO Y VERSÍCULO DEL DÍA ---
st.markdown("<h1 style='text-align: center;'>✨ Dios habla contigo</h1>", unsafe_content_html=True)

@st.cache_data(ttl=86400)
def obtener_versiculo_dia():
    res = client.chat.completions.create(
        messages=[{"role": "system", "content": "Da un versículo bíblico corto y su cita para hoy."}],
        model="llama-3.3-70b-versatile"
    )
    return res.choices[0].message.content

st.info(f"🌟 **VERSÍCULO DEL DÍA**\n\n{obtener_versiculo_dia()}")

st.markdown("---")

# --- MENÚ PRINCIPAL ---
if 'seccion' not in st.session_state:
    st.session_state.seccion = 'inicio'

# Botones de navegación
col1, col2 = st.columns(2)
with col1:
    if st.button("🙏 PALABRA DE ALIENTO", use_container_width=True):
        st.session_state.seccion = 'aliento'
    if st.button("☀️ DEVOCIONAL DIARIO", use_container_width=True):
        st.session_state.seccion = 'devocional'
with col2:
    if st.button("📖 CONSEJO DE DIOS", use_container_width=True):
        st.session_state.seccion = 'consejo'
    if st.button("📜 LA SANTA BIBLIA", use_container_width=True):
        st.session_state.seccion = 'biblia'

st.markdown("---")

# --- LÓGICA DE SECCIONES ---

if st.session_state.seccion == 'aliento':
    st.subheader("🙏 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Eres Jesus de Nazareth. Da un versículo y aliento corto."},
                      {"role": "user", "content": sentir}],
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        st.success(res)
        st.audio(texto_a_voz(res))

elif st.session_state.seccion == 'consejo':
    st.subheader("📖 Consejo de Dios")
    problema = st.text_area("¿Qué te preocupa?")
    if st.button("Pedir Sabiduría"):
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Eres un pastor compasivo. Da un consejo bíblico."},
                      {"role": "user", "content": problema}],
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        st.success(res)
        st.audio(texto_a_voz(res))

elif st.session_state.seccion == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Devocional"):
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Crea un devocional con título, versículo, reflexión y oración."}],
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        st.markdown(res)
        st.audio(texto_a_voz(res))

elif st.session_state.seccion == 'biblia':
    st.subheader("📜 La Santa Biblia")
    libro = st.selectbox("Selecciona un Libro", ["Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio", "Mateo", "Marcos", "Lucas", "Juan", "Salmos", "Apocalipsis"])
    cap = st.number_input("Capítulo", min_value=1, step=1)
    if st.button("Leer"):
        with st.spinner("Abriendo las escrituras..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Muestra el texto completo de {libro} capítulo {cap} en español Reina Valera 1960."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(f"### {libro} {cap}")
            st.write(res)

if st.session_state.seccion != 'inicio':
    if st.button("⬅️ Volver al Menú"):
        st.session_state.seccion = 'inicio'
        st.rerun()
