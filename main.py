import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")

# Conectar la llave de forma segura
try:
    llave = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=llave)
    # Usamos la versión 'latest' para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("Revisa la configuración de tu GEMINI_KEY en Secrets.")
    st.stop()

st.title("✨ Dios te habla hoy")
st.write("Escribe tu sentir y recibe una palabra de fe.")

pregunta = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if pregunta:
        with st.spinner("Buscando una palabra para ti..."):
            try:
                prompt = f"El usuario se siente {pregunta}. Proporciona un versículo bíblico y un breve mensaje de esperanza."
                response = model.generate_content(prompt)
                st.markdown("---")
                # Mostramos la respuesta con un formato limpio
                st.success(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Error al generar mensaje: {e}")
    else:
        st.warning("Escribe algo primero para poder ayudarte.")
