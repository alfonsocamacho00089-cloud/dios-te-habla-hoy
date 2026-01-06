import streamlit as st
import google.generativeai as genai
import requests

# Configuración de la página
st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")

# 1. Leer la llave de los Secretos
try:
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    # Usamos gemini-pro que es el más estable
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Configura tu GEMINI_KEY en los Secrets de Streamlit.")
    st.stop()

st.title("✨ Dios te habla hoy")
st.write("Escribe lo que sientes y recibe una palabra de fe.")

pregunta = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if pregunta:
        with st.spinner("Buscando una palabra para ti..."):
            try:
                # 2. Generar el mensaje de fe directamente con la IA
                prompt = f"El usuario se siente: {pregunta}. Proporciona un versículo bíblico relevante y un mensaje de esperanza corto (máximo 3 frases)."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Hubo un problema: {e}")
    else:
        st.warning("Por favor, escribe algo primero.")                st.error(f"Ocurrió un error: {e}")
