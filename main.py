import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Función para convertir texto a voz
def texto_a_voz(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("respuesta.mp3")
    return "respuesta.mp3"

# Conexión con la llave de Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura tu GROQ_API_KEY en Secrets.")
    st.stop()

st.title("✨ Dios habla contigo")

tab1, tab2 = st.tabs(["🙏 Palabra del Día", "📖 Consejero Espiritual"])

# --- PESTAÑA 1: PALABRA RÁPIDA ---
with tab1:
    st.subheader("Recibe un mensaje de fe")
    sentir_corto = st.text_input("¿Cómo te sientes hoy?", key="corto")
    
    if st.button("Recibir Versículo"):
        if sentir_corto:
            with st.spinner("Buscando una palabra..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres un guía espiritual. Da un versículo bíblico y un mensaje corto de aliento."},
                        {"role": "user", "content": sentir_corto}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                respuesta = chat_completion.choices[0].message.content
                st.info(respuesta)
                
                # Generar Audio
                audio_file = texto_a_voz(respuesta)
                st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Escribe una emoción.")

# --- PESTAÑA 2: CONSEJERO PROFUNDO ---
with tab2:
    st.subheader("Consejo y Sabiduría")
    problema = st.text_area("¿Qué situación estás pasando?", height=150)
    
    if st.button("Pedir Consejo"):
        if problema:
            with st.spinner("La IA está reflexionando..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres un pastor cristiano compasivo. un versículo y una bendición."},
                        {"role": "user", "content": problema}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                respuesta_larga = chat_completion.choices[0].message.content
                st.success(respuesta_larga)
                
                # Generar Audio
                audio_file = texto_a_voz(respuesta_larga)
                st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Cuéntanos qué te preocupa.")
