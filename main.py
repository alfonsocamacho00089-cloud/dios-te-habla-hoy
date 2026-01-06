import streamlit as st
import google.generativeai as genai

# Configuración visual
st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")

# Conectar con la llave
try:
    llave = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=llave)
    # Esta es la forma más segura de llamar al modelo actual
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error: Revisa tu GEMINI_KEY en los Secrets de Streamlit.")
    st.stop()

st.title("✨ Dios te habla hoy")
st.write("Escribe tu sentir y recibe una palabra de fe.")

pregunta = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if pregunta:
        with st.spinner("Buscando una palabra para ti..."):
            try:
                # Prompt optimizado
                prompt = f"Actúa como un guía espiritual. El usuario dice: {pregunta}. Dame un versículo bíblico y un consejo corto de esperanza."
                # Usamos la configuración estándar
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success(response.text)
                st.balloons()
            except Exception as e:
                # Si falla el 1.5-flash, intentamos con el pro automáticamente
                try:
                    model_alt = genai.GenerativeModel('gemini-pro')
                    response = model_alt.generate_content(prompt)
                    st.success(response.text)
                except:
                    st.error("Google está tardando en responder. Intenta de nuevo en un momento.")
    else:
        st.warning("Escribe algo primero.")
