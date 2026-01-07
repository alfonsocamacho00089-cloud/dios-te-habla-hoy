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

tab1, tab2 = st.tabs(["🙏 Palabra de Aliento", "⚔️ Reprensión Bíblica"])

with tab1:
    sentir = st.text_input("¿Cómo te sientes hoy?", key="t1")
    if st.button("Recibir Versículo"):
        with st.spinner("Buscando una palabra..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres un guía espiritual compasivo. Da un versículo y un mensaje corto de esperanza."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.info(res)
            audio_data = generar_audio(res)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")

with tab2:
    st.subheader("Exhortación y Corrección")
    st.write("Escribe la conducta o situación que necesita ser corregida a la luz de la Palabra.")
    falta = st.text_area("¿Qué área necesita reprensión?", placeholder="Ej: He estado siendo deshonesto en mi trabajo...", key="t2")
    
    if st.button("Recibir Reprensión"):
        if falta:
            with st.spinner("La Palabra es como espada de dos filos..."):
                res = client.chat.completions.create(
                    messages=[{
                        "role": "system", 
                        "content": """Eres un mentor espiritual firme y directo. 
                        Tu misión es reprender y exhortar al usuario basándote en la Biblia.
                        1. Confronta el error o pecado con seriedad pero con el fin de restaurar.
                        2. Usa versículos de corrección (como Proverbios o las cartas de Pablo).
                        3. Llama al arrepentimiento y da un paso práctico para cambiar.
                        4. Sé directo, no uses palabras suaves si el pecado es claro."""
                    },
                    {"role": "user", "content": falta}],
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                st.warning(res) # Usamos amarillo (warning) para que se sienta la seriedad
                audio_data = generar_audio(res)
                if audio_data:
                    st.audio(audio_data, format="audio/mp3")
        else:
            st.warning("Escribe qué situación quieres confrontar.")

st.markdown("---")
st.caption("Instruye al niño en su camino, y aun cuando fuere viejo no se apartará de él. - Prov. 22:6")
