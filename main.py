import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# Conexión con la llave de Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Configura tu GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

st.title("✨ Dios habla contigo")

# Crear las dos pestañas
tab1, tab2 = st.tabs(["🙏 Palabra del Día", "📖 Consejero Espiritual"])

# --- PESTAÑA 1: PALABRA RÁPIDA ---
with tab1:
    st.subheader("Recibe un mensaje de fe")
    sentir_corto = st.text_input("¿Cómo te sientes hoy? (Ej: Triste, Feliz, Cansado)", key="corto")
    
    if st.button("Recibir Versículo"):
        if sentir_corto:
            with st.spinner("Buscando una palabra para ti..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres un guía espiritual. Da un versículo bíblico y un mensaje corto de aliento."},
                        {"role": "user", "content": sentir_corto}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                st.info(chat_completion.choices[0].message.content)
        else:
            st.warning("Escribe una emoción para empezar.")

# --- PESTAÑA 2: CONSEJERO PROFUNDO ---
with tab2:
    st.subheader("Consejo y Sabiduría")
    st.write("Cuéntale a la IA lo que te preocupa para recibir guía detallada.")
    problema = st.text_area("¿Qué situación estás pasando?", placeholder="Ej: Tengo problemas con mi familia y no sé qué hacer...", height=150)
    
    if st.button("Pedir Consejo"):
        if problema:
            with st.spinner("La IA está orando y reflexionando tu respuesta..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": """Eres un consejero espiritual lleno de sabiduría y compasión. 
                            1. Escucha con empatía. 
                            2. Brinda pasos prácticos para resolver el conflicto. 
                            3. Cita un versículo bíblico que se aplique.
                            4. Despídete con una palabra de bendición.
                            Habla con un tono cálido y paternal."""
                        },
                        {"role": "user", "content": problema}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                st.success(chat_completion.choices[0].message.content)
        else:
            st.warning("Cuéntanos un poco más para poder darte un buen consejo.")

st.markdown("---")
st.caption("App creada para llevar luz y esperanza. 2026")
