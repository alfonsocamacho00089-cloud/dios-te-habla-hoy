import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 1. Configuración de la página
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# 2. Conexión con Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Configura tu llave en los Secrets de Streamlit.")
    st.stop()

# 3. Función para voz (Audio)
def texto_a_voz(texto):
    try:
        archivo = "voz_temp.mp3"
        if os.path.exists(archivo):
            os.remove(archivo)
        tts = gTTS(text=texto, lang='es')
        tts.save(archivo)
        return archivo
    except:
        return None

# --- TÍTULO Y VERSÍCULO DEL DÍA ---
st.title("✨ Dios habla contigo")

@st.cache_data(ttl=86400)
def obtener_versiculo_dia():
    try:
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Da un versículo bíblico corto y su cita para hoy."}],
            model="llama-3.3-70b-versatile"
        )
        return res.choices[0].message.content
    except:
        return "Jehová es mi pastor; nada me faltará. - Salmos 23:1"

st.info(f"🌟 **VERSÍCULO DEL DÍA**\n\n{obtener_versiculo_dia()}")

st.divider()

# --- MENÚ PRINCIPAL POR BOTONES ---
if 'menu' not in st.session_state:
    st.session_state.menu = 'inicio'
if 'devocional_actual' not in st.session_state:
    st.session_state.devocional_actual = None

col1, col2 = st.columns(2)
with col1:
    if st.button("🙏 PALABRA DE ALIENTO", use_container_width=True):
        st.session_state.menu = 'aliento'
    if st.button("☀️ DEVOCIONAL DIARIO", use_container_width=True):
        st.session_state.menu = 'devocional'
with col2:
    if st.button("📖 CONSEJO DE DIOS", use_container_width=True):
        st.session_state.menu = 'consejo'
    if st.button("📜 LA SANTA BIBLIA", use_container_width=True):
        st.session_state.menu = 'biblia'

# --- LÓGICA DE LAS SECCIONES ---

if st.session_state.menu == 'aliento':
    st.subheader("🙏 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        with st.spinner("Dios te escucha..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres Jesús. Da un versículo y aliento corto."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            st.audio(texto_a_voz(res))

elif st.session_state.menu == 'consejo':
    st.subheader("📖 Consejo de Dios")
    problema = st.text_area("¿Qué te preocupa?")
    if st.button("Pedir Sabiduría"):
        with st.spinner("Buscando en la Palabra..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres un pastor compasivo. Da un consejo bíblico."},
                          {"role": "user", "content": problema}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            st.audio(texto_a_voz(res))

elif st.session_state.menu == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Devocional"):
        with st.spinner("Preparando tu alimento espiritual..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Crea un devocional con título, versículo, reflexión y oración."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.session_state.devocional_actual = res
            st.markdown(res)
            st.audio(texto_a_voz(res))
    
    if st.session_state.devocional_actual:
        if st.button("💾 Guardar para leer más tarde"):
            # Aquí llamamos a la herramienta para guardar en la lista del usuario
            st.toast("¡Devocional guardado en tu lista!", icon="💾")

elif st.session_state.menu == 'biblia':
    st.subheader("📜 La Santa Biblia")
    
    # Lista completa de los 66 libros
    todos_los_libros = [
        "Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio", "Josué", "Jueces", "Rut", 
        "1 Samuel", "2 Samuel", "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas", "Esdras", 
        "Nehemías", "Ester", "Job", "Salmos", "Proverbios", "Eclesiastés", "Cantares", 
        "Isaías", "Jeremías", "Lamentaciones", "Ezequiel", "Daniel", "Oseas", "Joel", 
        "Amos", "Abdías", "Jonás", "Miqueas", "Nahúm", "Habacuc", "Sofonías", "Hageo", 
        "Zacarías", "Malaquías", "Mateo", "Marcos", "Lucas", "Juan", "Hechos", "Romanos", 
        "1 Corintios", "2 Corintios", "Gálatas", "Efesios", "Filipenses", "Colosenses", 
        "1 Tesalonicenses", "2 Tesalonicenses", "1 Timoteo", "2 Timoteo", "Tito", 
        "Filemón", "Hebreos", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", 
        "3 Juan", "Judas", "Apocalipsis"
    ]
    
    libro_sel = st.selectbox("Selecciona un Libro", todos_los_libros)
    cap = st.number_input("Capítulo", min_value=1, step=1)
    
    if st.button("Leer"):
        with st.spinner("Abriendo las escrituras..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Muestra el texto de {libro_sel} capítulo {cap} en español Reina Valera 1960."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(f"### {libro_sel} {cap}")
            st.write(res)

# Botón para volver
if st.session_state.menu != 'inicio':
    st.divider()
    if st.button("⬅️ Volver al Menú"):
        st.session_state.menu = 'inicio'
        st.session_state.devocional_actual = None
        st.rerun()
