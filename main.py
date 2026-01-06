import streamlit as st
import requests

st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")
st.title("✨ Dios te habla hoy")

sentir = st.text_input("¿Qué hay en tu corazón?")

if st.button("Recibir mensaje"):
    if sentir:
        # Este código usa una base de datos de la Biblia que NO requiere llaves ni VPN
        try:
            # Buscamos un versículo que siempre da consuelo (Juan 14:27)
            res = requests.get("https://bible-api.com/juan+14:27?translation=bj")
            texto = res.json()['text']
            st.success(f"Hijo, sobre tu sentir de '{sentir}', recuerda:")
            st.info(texto)
            st.balloons()
        except:
            st.error("Conexión inestable. Dios está contigo.")
    else:
        st.warning("Escribe algo primero.")
