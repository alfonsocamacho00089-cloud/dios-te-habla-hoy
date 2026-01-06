import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")

# Conectar la llave
try:
    llave = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=llave)
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Error con la llave en Secrets.")
    st.stop()

st.title("✨ Dios te habla hoy")
st.write("Escribe tu sentir y recibe una palabra.")

pregunta = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if pregunta:
        try:
            prompt = f"El usuario se siente {pregunta}. Da un versículo bíblico y un mensaje de fe corto."
            response = model.generate_content(prompt)
            st.success(response.text)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Escribe algo primero.")
