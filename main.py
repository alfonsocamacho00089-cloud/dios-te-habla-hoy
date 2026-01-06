import streamlit as st
import google.generativeai as genai
import requests

# 1. Intentar leer la llave de los Secretos
try:
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
except:
    st.error("❌ No encontré la llave 'GEMINI_KEY' en los Secretos de Streamlit.")
    st.stop()

# 2. Configurar la IA
try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')
    st.error("❌ La llave es incorrecta o no tiene permisos.")
    st.stop()

st.title("✨ Dios te habla hoy")

pregunta = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if pregunta:
        with st.spinner("Buscando respuesta..."):
            try:
                # Buscamos en la Biblia
                res = requests.get(f"https://bible-api.com/{pregunta}?translation=bj")
                v_texto = res.json()['text'] if res.status_code == 200 else "Confía en el Señor."
                
                # Generamos consejo
                prompt = f"Usuario: {pregunta}. Biblia: {v_texto}. Da un mensaje de fe de 2 frases."
                respuesta = model.generate_content(prompt)
                
                st.info(respuesta.text)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
