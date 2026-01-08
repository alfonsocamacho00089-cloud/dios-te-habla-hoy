import streamlit as st
from groq import Groq
from gtts import gTTS
import os
from datetime import datetime

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

# Conexión con la llave de Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura tu GROQ_API_KEY en Secrets.")
    st.stop()

st.title("✨ Dios habla contigo")

# Añadimos la tercera pestaña: "Devocional Diario"
tab1, tab2, tab3 = st.tabs(["📖 Palabra de Aliento", "🙏 Consejo de Dios", "☀️ Devocional Diario"])

# --- PESTAÑA 1: PALABRA RÁPIDA ---
with tab1:
    st.subheader("Recibe un mensaje de fe")
    sentir_corto = st.text_input("¿Cómo te sientes hoy?", key="corto")
    
    if st.button("Recibir Versículo"):
        if sentir_corto:
            with st.spinner("Palabra de Dios..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres Jesús de Nazareth. Da un versículo bíblico y un mensaje corto de aliento sobre ese versículo."},
                        {"role": "user", "content": sentir_corto}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                respuesta = chat_completion.choices[0].message.content
                st.info(respuesta)
                
                audio_file = texto_a_voz(respuesta, "aliento.mp3")
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Escribe una emoción.")

# --- PESTAÑA 2: CONSEJO DE DIOS ---
with tab2:
    st.subheader("Consejo y Sabiduría")
    problema = st.text_area("¿Qué situación estás pasando?", height=150)
    
    if st.button("Pedir Consejo a Dios"):
        if problema:
            with st.spinner("Dios te dará la respuesta que buscas..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres un pastor cristiano compasivo. Brinda un consejo basado en la biblia, un versículo y una bendición."},
                        {"role": "user", "content": problema}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                respuesta_larga = chat_completion.choices[0].message.content
                st.success(respuesta_larga)
                
                audio_file = texto_a_voz(respuesta_larga, "consejo.mp3")
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Cuéntanos qué te preocupa.")

# --- PESTAÑA 3: DEVOCIONAL DIARIO ---
with tab3:
    fecha_hoy = datetime.now().strftime("%d de %B de %Y")
    st.subheader(f"Devocional para hoy: {fecha_hoy}")
    st.write("Presiona el botón para descubrir la enseñanza que Dios tiene preparada para ti hoy.")
    
    if st.button("Leer Devocional de Hoy"):
        with st.spinner("Preparando tu alimento espiritual..."):
            # Usamos la fecha en el mensaje para que la IA genere algo "nuevo" cada día
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres un mentor espiritual. Crea un devocional diario que incluya: 1) Un título inspirador, 2) Un versículo clave, 3) Una reflexión profunda de 2 párrafos y 4) Una oración breve para empezar el día."},
                    {"role": "user", "content": f"Genera el devocional para el día {fecha_hoy}"}
                ],
                model="llama-3.3-70b-versatile",
            )
            devocional = chat_completion.choices[0].message.content
            st.markdown(devocional)
            
            audio_file = texto_a_voz(devocional, "devocional.mp3")
            if audio_file:
                st.audio(audio_file, format="audio/mp3")

st.markdown("---")
st.caption("Hecho con fe para bendecir tu vida.")
