import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Dios habla contigo", page_icon="✨")

# 2. CONEXIÓN CON GROQ (API)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Configura tu GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 3. FUNCIÓN PARA CONVERTIR TEXTO A VOZ (AUDIO)
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

# 4. INICIALIZACIÓN DE LA MEMORIA (SESSION STATE)
if 'menu' not in st.session_state:
    st.session_state.menu = 'inicio'
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []
if 'temp_dev' not in st.session_state:
    st.session_state.temp_dev = None

# --- CABECERA Y VERSÍCULO DEL DÍA ---
st.title("✨ Dios habla contigo")

@st.cache_data(ttl=86400) # Se actualiza cada 24 horas
def obtener_versiculo_dia():
    try:
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Da un versículo bíblico corto de aliento con su cita para hoy."}],
            model="llama-3.3-70b-versatile"
        )
        return res.choices[0].message.content
    except:
        return "Jehová es mi pastor; nada me faltará. - Salmos 23:1"

st.info(f"🌟 **VERSÍCULO DEL DÍA**\n\n{obtener_versiculo_dia()}")
st.divider()

# --- MENÚ DE NAVEGACIÓN (BOTONES GRANDES) ---
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

# Botón especial para los guardados
if st.button("📂 TUS DEVOCIONALES DE DIOS TE HABLA HOY", use_container_width=True):
    st.session_state.menu = 'mis_guardados'

st.divider()

# --- LÓGICA DE LAS SECCIONES ---

# SECCIÓN: ALIENTO
if st.session_state.menu == 'aliento':
    st.subheader("🙏 Palabra de Aliento")
    sentir = st.text_input("¿Cómo te sientes hoy?")
    if st.button("Recibir Mensaje"):
        with st.spinner("Dios te escucha..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Eres Jesús de Nazareth. Da un versículo y aliento corto."},
                          {"role": "user", "content": sentir}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.success(res)
            st.audio(texto_a_voz(res))

# SECCIÓN: CONSEJO
elif st.session_state.menu == 'consejo':
    st.subheader("📖 Consejo de Dios")
    st.write("Cuéntale a Dios tus preocupaciones. La IA te responderá como un pastor compasivo y podrás seguir conversando con ella.")

    # 1. Inicializar el historial de mensajes si no existe
    if 'chat_consejo' not in st.session_state:
        st.session_state.chat_consejo = []

    # 2. Mostrar los mensajes que ya se han escrito (el historial)
    for mensaje in st.session_state.chat_consejo:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # 3. Barra para escribir (Aquí es donde le pides apoyo y respondes)
    prompt = st.chat_input("Escribe aquí lo que hay en tu corazón...")

    if prompt:
        # Mostrar tu mensaje en pantalla
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Guardar tu mensaje en la memoria
        st.session_state.chat_consejo.append({"role": "user", "content": prompt})

        # Generar la respuesta de la IA
        with st.chat_message("assistant"):
            with st.spinner("Escuchando y buscando en la Palabra..."):
                # Se envía TODO el historial para que la IA no olvide de qué están hablando
                mensajes_para_ia = [
                    {"role": "system", "content": "Eres un pastor cristiano lleno de amor y sabiduría. Tu meta es dar consejo bíblico y apoyo emocional. Escucha con paciencia, usa versículos y permite que el usuario se desahogue."}
                ] + st.session_state.chat_consejo
                
                res = client.chat.completions.create(
                    messages=mensajes_para_ia,
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                st.markdown(res)
                # Generar el audio de la respuesta
                audio_file = texto_a_voz(res)
                if audio_file:
                    st.audio(audio_file)
        
        # Guardar la respuesta de la IA en la memoria
        st.session_state.chat_consejo.append({"role": "assistant", "content": res})

    # Botón opcional para borrar la charla y empezar de nuevo
    if st.session_state.chat_consejo:
        if st.button("Borrar conversación y empezar de cero"):
            st.session_state.chat_consejo = []
            st.rerun()
# SECCIÓN: DEVOCIONAL DIARIO
elif st.session_state.menu == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Nuevo Devocional"):
        with st.spinner("Preparando..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "Crea un devocional con título, versículo, reflexión y oración."}],
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
elif st.session_state.menu == 'devocional':
    st.subheader("☀️ Devocional Diario")
    if st.button("Generar Nuevo Devocional"):
        with st.spinner("Preparando alimento basado en la sana doctrina..."):
            res = client.chat.completions.create(
                messages=[{
                    "role": "system", 
                    "content": """Eres un mentor bíblico ortodoxo. Crea un devocional con la siguiente estructura estricta:
                    1. Título inspirador.
                    2. Versículo clave (Reina Valera 1960).
                    3. Enseñanza Bíblica: Basada estrictamente en las palabras de Jesús o las epístolas de los apóstoles (priorizando a Pablo). Debe ser una explicación profunda de la sana doctrina.
                    4. Reflexión para nuestros días: Un párrafo muy corto que conecte la enseñanza con el mundo actual.
                    5. Aplicación para nuestra vida: Pasos prácticos para vivir esa palabra hoy.
                    6. Oración breve.
                    
                    Importante: No uses la palabra 'Reflexión' para la aplicación. Usa exactamente los títulos mencionados."""
                }],
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
# SECCIÓN: LA BIBLIA COMPLETA
elif st.session_state.menu == 'biblia':
    st.subheader("📜 La Santa Biblia")
    libros_completos = [
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
    libro_sel = st.selectbox("Selecciona un Libro", libros_completos)
    cap = st.number_input("Capítulo", min_value=1, step=1)
    if st.button("Abrir Biblia"):
        with st.spinner("Cargando escrituras..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Texto de {libro_sel} {cap} Reina Valera 1960."}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.markdown(f"### {libro_sel} {cap}")
            st.write(res)

# BOTÓN DE VOLVER (Siempre visible si no estás en el inicio)
if st.session_state.menu != 'inicio':
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.menu = 'inicio'
        st.session_state.temp_dev = None
        st.rerun()

st.divider()
st.caption("2026 - Una palabra de Dios para tu vida.")
