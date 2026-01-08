import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# 2. CONEXIÓN CON GROQ
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Configura tu GROQ_API_KEY en los Secrets.")
    st.stop()

# 3. FUNCIÓN PARA VOZ (AUDIO)
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

# 4. INICIALIZACIÓN DE MEMORIA
if 'menu' not in st.session_state:
    st.session_state.menu = 'inicio'
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []
if 'chat_consejo' not in st.session_state:
    st.session_state.chat_consejo = []
if 'temp_dev' not in st.session_state:
    st.session_state.temp_dev = None

# --- CABECERA Y VERSÍCULO DEL DÍA ---
st.title("✨ Dios habla contigo")

@st.cache_data(ttl=86400)
def obtener_versiculo_dia():
    try:
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Da un versículo bíblico corto de la versión Reina Valera 1960 con su cita para hoy."}],
            model="llama-3.3-70b-versatile"
        )
        return res.choices[0].message.content
    except:
        return "Jehová es mi pastor; nada me faltará. - Salmos 23:1 (RVR1960)"

st.info(f"🌟 **VERSÍCULO DEL DÍA (RVR1960)**\n\n{obtener_versiculo_dia()}")
st.divider()

# --- MENÚ DE NAVEGACIÓN ---
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

if st.button("📂 TUS DEVOCIONALES DE DIOS TE HABLA HOY", use_container_width=True):
    st.session_state.menu = 'mis_guardados'

st.divider()

# --- LÓGICA DE LAS SECCIONES ---

# SECCIÓN: ALIENTO
if st.session_state.menu == 'aliento':
    st.subheader("🙏 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Eres Jesús de Nazareth. Usa ÚNICAMENTE la versión Reina Valera 1960 para los versículos."},
                      {"role": "user", "content": sentir}],
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        st.success(res)
        st.audio(texto_a_voz(res))

# SECCIÓN: CONSEJO (CON CHAT)
elif st.session_state.menu == 'consejo':
    st.subheader("📖 Consejo de Dios")
    for mensaje in st.session_state.chat_consejo:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escribe aquí lo que hay en tu corazón..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_consejo.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            mensajes_ia = [{"role": "system", "content": "Eres un pastor compasivo. Cita siempre la Reina Valera 1960. Escucha y apoya al usuario."}] + st.session_state.chat_consejo
            res = client.chat.completions.create(messages=mensajes_ia, model="llama-3.3-70b-versatile").choices[0].message.content
            st.markdown(res)
            st.audio(texto_a_voz(res))
        st.session_state.chat_consejo.append({"role": "assistant", "content": res})

# SECCIÓN: DEVOCIONAL DIARIO
elif st.session_state.menu == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Nuevo Devocional"):
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": """Crea un devocional bíblico:
            1. Título. 2. Versículo (Reina Valera 1960). 3. Enseñanza Bíblica (Jesús o Pablo). 
            4. Reflexión para nuestros días (Corta). 5. Aplicación para nuestra vida. 6. Oración."""}],
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        st.session_state.temp_dev = res
        st.markdown(res)
        st.audio(texto_a_voz(res))
    
    if st.session_state.temp_dev:
        if st.button("💾 Guardar en 'Tus Devocionales'"):
            if st.session_state.temp_dev not in st.session_state.favoritos:
                st.session_state.favoritos.append(st.session_state.temp_dev)
                st.toast("¡Guardado!", icon="✅")

# SECCIÓN: TUS DEVOCIONALES GUARDADOS
elif st.session_state.menu == 'mis_guardados':
    st.subheader("📂 Tus Devocionales Guardados")
    if not st.session_state.favoritos:
        st.info("No hay mensajes guardados aún.")
    else:
        for idx, dev in enumerate(reversed(st.session_state.favoritos)):
            with st.expander(f"📖 Mensaje Guardado"):
                st.markdown(dev)
                
# SECCIÓN: LA BIBLIA COMPLETA
elif st.session_state.menu == 'biblia':
    st.subheader("📜 La Santa Biblia (RVR1960)")
    libros = ["Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio", "Josué", "Jueces", "Rut", "1 Samuel", "2 Samuel", "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas", "Esdras", "Nehemías", "Ester", "Job", "Salmos", "Proverbios", "Eclesiastés", "Cantares", "Isaías", "Jeremías", "Lamentaciones", "Ezequiel", "Daniel", "Oseas", "Joel", "Amos", "Abdías", "Jonás", "Miqueas", "Nahúm", "Habacuc", "Sofonías", "Hageo", "Zacarías", "Malaquías", "Mateo", "Marcos", "Lucas", "Juan", "Hechos", "Romanos", "1 Corintios", "2 Corintios", "Gálatas", "Efesios", "Filipenses", "Colosenses", "1 Tesalonicenses", "2 Tesalonicenses", "1 Timoteo", "2 Timoteo", "Tito", "Filemón", "Hebreos", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan", "3 Juan", "Judas", "Apocalipsis"]
    
    libro_sel = st.selectbox("Selecciona un Libro", libros)
    cap = st.number_input("Capítulo", min_value=1, step=1)
    
    if st.button("Abrir Biblia"):
        with st.spinner("Cargando escrituras..."):
            # Aquí añadimos la instrucción de listar los versículos hacia abajo
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"""Muestra el texto de {libro_sel} {cap} en español Reina Valera 1960. 
                IMPORTANTE: Escribe cada versículo en una línea nueva, comenzando con su número (ejemplo: 1 En el principio...), para que aparezcan en fila hacia abajo."""}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            
            st.markdown(f"### {libro_sel} {cap}")
            # Usamos un contenedor con borde para que se vea más organizado
            st.info(res)
# BOTÓN VOLVER
if st.session_state.menu != 'inicio':
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.menu = 'inicio'
        st.session_state.temp_dev = None
        st.rerun()

st.divider()
st.caption("Biblia Versión Reina Valera 1960")
