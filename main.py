import streamlit as st
from groq import Groq

st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Conectar con la llave de Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Falta la llave GROQ_API_KEY en Secrets.")
    st.stop()

st.title("✨ Dios habla contigo")
st.write("Recibe una palabra de fe impulsada por IA (Gratis).")

sentir = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir Mensaje"):
    if sentir:
        with st.spinner("Buscando una palabra para ti..."):
            try:
                # Usamos Llama 3 (la IA de Facebook que es gratis en Groq)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres un guía espiritual. Da un versículo bíblico y un mensaje corto de esperanza."},
                        {"role": "user", "content": sentir}
                    ],
                    model="llama3-8b-8192",
                )
                st.markdown("---")
                st.success(chat_completion.choices[0].message.content)
                st.balloons()
            except Exception as e:
                st.error("Error de conexión. Intenta de nuevo.")
    else:
        st.warning("Escribe algo primero.")
