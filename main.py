import streamlit as st
import random

# Configuración visual
st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")

st.title("✨ Dios te habla hoy")
st.write("Escribe lo que sientes y recibe una palabra de aliento.")

# Lista de versículos guardados directamente en la app (Sin fallos de internet)
versiculos = [
    "La paz les dejo, mi paz les doy. (Juan 14:27)",
    "El Señor es mi pastor, nada me faltará. (Salmo 23:1)",
    "Todo lo puedo en Cristo que me fortalece. (Filipenses 4:13)",
    "No temas, porque yo estoy contigo. (Isaías 41:10)",
    "Vengan a mí los que están cansados y cargados. (Mateo 11:28)",
    "Tu palabra es lumbrera a mis pies y luz en mi camino. (Salmo 119:105)"
]

sentir = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if sentir:
        # Elegimos un versículo al azar de la lista
        mensaje = random.choice(versiculos)
        st.markdown("---")
        st.success(f"Hijo, sobre tu sentir de '{sentir}', recuerda:")
        st.info(mensaje)
        st.balloons()
    else:
        st.warning("Escribe algo primero para recibir tu palabra.")
