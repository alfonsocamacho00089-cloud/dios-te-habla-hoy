import streamlit as st
import google.generativeai as genai
import requests

# Configuración de seguridad (Se configura en Streamlit Cloud)
GEMINI_KEY = st.secrets["GEMINI_KEY"]

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Dios te habla hoy", page_icon="✨")

# Estilo Moderno
st.markdown("""
    <style>
    .stApp { background-color: #f8fafd; }
    .stButton>button { 
        background-color: #5dade2; color: white; border-radius: 25px; 
        border: none; width: 100%; padding: 10px;
    }
    .card { 
        padding: 25px; border-radius: 15px; background-color: white; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Dios te habla hoy</h2>", unsafe_allow_html=True)

pregunta = st.text_input("¿Qué hay en tu corazón hoy?", placeholder="Ej: Busco paz...")

if st.button("Recibir mensaje"):
    if pregunta:
        with st.spinner("Conectando..."):
            try:
                # API de Biblia gratuita
                res = requests.get(f"https://bible-api.com/{pregunta}?translation=bj")
                if res.status_code == 200:
                    v_texto = res.json()['text']
                    v_ref = res.json()['reference']
                else:
                    v_texto = "No temas, porque yo estoy contigo."
                    v_ref = "Isaías 41:10"

                prompt = f"Eres un guía espiritual. Usuario dice: '{pregunta}'. Basado en '{v_texto}' ({v_ref}), escribe un mensaje de aliento corto y moderno de 3 frases."
                respuesta = model.generate_content(prompt)

                st.markdown(f"<div class='card'>{respuesta.text}<br><br><b>— {v_ref}</b></div>", unsafe_allow_html=True)
            except:
                st.error("Error de conexión. Revisa tu API Key.")
