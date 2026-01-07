import streamlit as st
from groq import Groq
from gtts import gTTS
import base64

# Configuración
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Función optimizada para audio
def generar_audio(texto):
    try:
        tts = gTTS(text=texto, lang='es')
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as f:
            data = f.read()
        return data
    except:
        return None

# Conexión Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Revisa tu llave en Secrets")
    st.stop()

st.title("✨ Dios habla contigo")

tab1, tab2 = st.tabs(["🙏 Palabra", "📖 Consejo"])

with tab1:
    sentir = st.text_input("¿Cómo te sientes?", key="t1")
    if st.button("Recibir Versículo"):
        with st.spinner("Generando..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Da un versículo y un mensaje corto."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.info(res)
            # Audio
            audio_data = generar_audio(res)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")

with tab2:
    problema = st.text_area("¿Qué te preocupa?", key="t2")
    if st.button("Pedir Consejo"):
        with st.spinner("Reflexionando..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres un consejero espiritual. Da pasos prácticos y fe."},
                          {"role": "user", "content": problema}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            # Audio
            audio_data = generar_audio(res)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
