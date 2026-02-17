import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# Configuración de la página
st.set_page_config(page_title="Evaluación sensorial", layout="wide")

# ---- ESTILOS PARA TEMA OSCURO ----
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    /* Texto de las etiquetas */
    .stTextInput label, .stNumberInput label, .stSelectbox label, 
    .stRadio label, .stCheckbox label {
        color: white !important;
    }
    /* Fondo de los inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select, 
    .stTextArea textarea {
        background-color: #333 !important;
        color: white !important;
        border-color: #555 !important;
    }
    /* Botones */
    .stButton button {
        background-color: #444;
        color: white;
        border: 1px solid #666;
    }
    .stButton button:hover {
        background-color: #555;
        color: white;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #222;
    }
    .stTabs [data-baseweb="tab"] {
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #333;
    }
    /* Dataframe */
    .stDataFrame {
        background-color: #222;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título común
st.title("Evaluación sensorial")

# Inicializar el estado de la sesión para almacenar las respuestas
if 'responses' not in st.session_state:
    st.session_state.responses = []

# --- FORMULARIO PRINCIPAL (con limpieza automática al enviar) ---
with st.form(key="encuesta_form", clear_on_submit=True):
    # Crear las pestañas (solo 2)
    tab1, tab2 = st.tabs([
        "inicial",
        "Encuesta"
    ])

    # ---------- PESTAÑA 1: Inicial (Influye en la percepción) ----------
    with tab1:
        st.header("Influye en la percepción")
        # Las preguntas de esta pestaña se mantienen igual, pero también se numerarán
        # (aunque no se fusionan, las incluimos en el formulario con sus números)
        # Vamos a numerar las preguntas de la pestaña 1 también para mantener consistencia.
        # Usaremos un contador que comenzará en 1 y se incrementará en cada pregunta.

        # Inicializamos un contador de preguntas (se usará luego en el diccionario)
        # Pero como las preguntas están en distintas pestañas, necesitamos un número global.
        # Definiremos una lista de preguntas con sus claves y etiquetas para luego construir el diccionario.
        # Para simplificar, asignaremos manualmente los números.

        # Pregunta 1
        st.markdown("**1. Condición médica**")
        cond_medica = st.radio(
            "¿Tiene alguna condición médica que afecte el gusto, el olfato o la sensibilidad oral (como sinusitis, rinitis, resfrío, gripe, congestión nasal u otra afección en este momento, etc.)?",
            options=["Sí", "No"],
            index=1,
            key="cond_medica",
            horizontal=True,
            label_visibility="collapsed"  # Ocultamos la etiqueta porque ya pusimos el número arriba
        )

        # Pregunta 2
        st.markdown("**2. Medicamentos**")
        medicamentos = st.radio(
            "¿Toma actualmente algún medicamento que pueda alterar el gusto, el olfato o la salivación (como antihistamínicos, antibióticos, ansiolíticos, etc.)?",
            options=["Sí", "No"],
            index=1,
            key="medicamentos",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 3
        st.markdown("**3. Alergias alimentarias**")
        alergias = st.radio(
            "¿Tiene alguna alergia alimentaria relacionada con aceite de oliva, lactosa, gluten, proteínas del huevo algún condimento?",
            options=["Sí", "No"],
            index=1,
            key="alergias",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 4
        st.markdown("**4. Fumado última hora**")
        fumado = st.radio(
            "¿Ha fumado cigarrillos u otros productos en la última hora, antes de hacer esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="fumado",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 5
        st.markdown("**5. Alcohol última hora**")
        alcohol = st.radio(
            "¿Ha consumido alcohol en la última hora, antes de hacer esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="alcohol",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 6
        st.markdown("**6. Café/chicles/menta última hora**")
        cafe = st.radio(
            "¿Ha consumido café, chicles, menta en la última hora, antes de hacer esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="cafe",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 7
        st.markdown("**7. Cepillado justo antes**")
        cepillado = st.radio(
            "¿Se cepilló los dientes justo antes del test?",
            options=["Sí", "No"],
            index=1,
            key="cepillado",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 8
        st.markdown("**8. Fatiga/sueño**")
        fatigado = st.radio(
            "¿Se siente fatigado/a o con sueño?",
            options=["Sí", "No"],
            index=1,
            key="fatigado",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 9
        st.markdown("**9. Estrés/ansiedad**")
        estres = st.radio(
            "¿Siente estrés, ansiedad o malestar emocional?",
            options=["Sí", "No"],
            index=1,
            key="estres",
            horizontal=True,
            label_visibility="collapsed"
        )

    # ---------- PESTAÑA 2: Encuesta (Datos personales + Encuesta del producto) ----------
    with tab2:
        st.header("Encuesta Completa")

        # Mostrar número de ficha (no es una pregunta)
        st.markdown(f"**Ficha N.º:** {len(st.session_state.responses) + 1} (se asignará al guardar)")

        # --- Datos personales (continuación de la numeración) ---
        # Pregunta 10
        st.markdown("**10. Nombre**")
        nombre = st.text_input("Nombre", key="nombre", label_visibility="collapsed")

        # Pregunta 11
        st.markdown("**11. Apellido**")
        apellido = st.text_input("Apellido", key="apellido", label_visibility="collapsed")

        # Pregunta 12
        st.markdown("**12. Edad**")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1, key="edad", label_visibility="collapsed")

        # Pregunta 13
        st.markdown("**13. Género**")
        genero = st.selectbox(
            "Sexo o Género",
            options=["Femenino", "Masculino", "Prefiero no responder"],
            key="genero",
            label_visibility="collapsed"
        )

        # Pregunta 14
        st.markdown("**14. ¿Volvería a participar?**")
        volveria = st.radio(
            "¿Volvería a participar en esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="volveria",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Campo condicional (no es una pregunta numerada, es un subcampo de la 14)
        if volveria == "Sí":
            contacto = st.text_input("Contacto (número de teléfono)", key="contacto")
        else:
            st.session_state["contacto"] = ""

        # --- Encuesta sobre el producto (continuación) ---
        st.markdown("---")  # Separador visual
        st.markdown("**Encuesta sobre el producto**")
        st.markdown("*Este aderezo tiene aceite de oliva, aceite de girasol y leche de cabra*")

        # Pregunta 15
        st.markdown("**15. ¿Conoce este tipo de producto?**")
        conoce = st.radio("¿Conoce este tipo de producto?", options=["Sí", "No"], index=1, key="conoce", horizontal=True, label_visibility="collapsed")

        # Pregunta 16
        st.markdown("**16. ¿Ha probado antes este tipo de producto?**")
        ha_probado = st.radio("¿Ha probado este tipo de producto antes?", options=["Sí", "No"], index=1, key="ha_probado", horizontal=True, label_visibility="collapsed")

        # Pregunta 17
        st.markdown("**17. ¿Suele consumir aderezos similares? (Seleccione todos los que correspondan)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            mayonesa = st.checkbox("Mayonesa", key="sim_mayonesa")
        with col2:
            aioli = st.checkbox("Aioli", key="sim_aioli")
        with col3:
            cesar = st.checkbox("Salsas César", key="sim_cesar")
        with col4:
            otros_sim = st.checkbox("Otros", key="sim_otros")

        # Subcampo condicional (no numerado aparte)
        otros_sim_text = ""
        if otros_sim:
            otros_sim_text = st.text_input("Especifique otros aderezos similares", key="sim_otros_text")
        else:
            st.session_state["sim_otros_text"] = ""

        # Pregunta 18
        st.markdown("**18. ¿Cree que todos los integrantes de su hogar consumirían este aderezo por sus ingredientes?**")
        consumirian = st.radio(
            "¿Cree que todos los integrantes de su hogar consumirían este aderezo por sus ingredientes?",
            options=["Sí", "No"],
            index=1,
            key="consumirian",
            horizontal=True,
            label_visibility="collapsed"
        )

        # Pregunta 19
        st.markdown("**19. ¿Con qué frecuencia consume aderezos?**")
        frecuencia = st.text_input("Frecuencia", key="frecuencia", label_visibility="collapsed")

        # Pregunta 20
        st.markdown("**20. ¿Qué cantidad de aderezos consumen en su hogar por mes?**")
        cantidad = st.text_input("Cantidad mensual", key="cantidad", label_visibility="collapsed")

        # Pregunta 21
        st.markdown("**21. Marca de aderezos más consumida normalmente en su hogar**")
        marca = st.selectbox(
            "Marca",
            options=["Mayonesa", "Aioli", "Salsas César", "Otros"],
            key="marca",
            label_visibility="collapsed"
        )
        otros_marca_text = ""
        if marca == "Otros":
            otros_marca_text = st.text_input("Especifique otra marca", key="marca_otros_text")
        else:
            st.session_state["marca_otros_text"] = ""

    # --- BOTÓN DE ENVÍO (dentro del formulario) ---
    submitted = st.form_submit_button("Guardar respuesta")

    # --- PROCESAMIENTO DEL FORMULARIO (solo si se envió) ---
    if submitted:
        nueva_ficha = len(st.session_state.responses) + 1
        # Construimos el diccionario con claves que incluyen el número de pregunta
        respuesta = {
            "Ficha N°": nueva_ficha,
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # Preguntas de la pestaña 1 (numeradas del 1 al 9)
            "P1_Condición médica": cond_medica,
            "P2_Medicamentos": medicamentos,
            "P3_Alergias": alergias,
            "P4_Fumado última hora": fumado,
            "P5_Alcohol última hora": alcohol,
            "P6_Café/chicles/menta": cafe,
            "P7_Cepillado antes": cepillado,
            "P8_Fatiga/sueño": fatigado,
            "P9_Estrés/ansiedad": estres,
            # Preguntas de la pestaña 2 (a partir de la 10)
            "P10_Nombre": nombre,
            "P11_Apellido": apellido,
            "P12_Edad": edad,
            "P13_Género": genero,
            "P14_Volvería a participar": volveria,
            "P14_Contacto": st.session_state.contacto if volveria == "Sí" else "",
            "P15_Conoce producto": conoce,
            "P16_Ha probado antes": ha_probado,
            "P17_Consume Mayonesa": "Sí" if mayonesa else "No",
            "P17_Consume Aioli": "Sí" if aioli else "No",
            "P17_Consume Salsas César": "Sí" if cesar else "No",
            "P17_Consume Otros similares": otros_sim_text if otros_sim else "",
            "P18_Todos consumirían": consumirian,
            "P19_Frecuencia consumo": frecuencia,
            "P20_Cantidad mensual": cantidad,
            "P21_Marca preferida": marca,
            "P21_Otra marca especificada": otros_marca_text if marca == "Otros" else ""
        }
        st.session_state.responses.append(respuesta)
        st.success(f"Respuesta guardada correctamente. Ficha N° {nueva_ficha}")

# ---------- SECCIÓN DE EXPORTACIÓN (fuera del formulario) ----------
st.divider()
st.header("Exportar datos")

if st.session_state.responses:
    df = pd.DataFrame(st.session_state.responses)
    st.dataframe(df)

    # Botón para descargar Excel (formato .xlsx correcto)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Respuestas')
    output.seek(0)

    st.download_button(
        label="📥 Descargar como Excel",
        data=output,
        file_name=f"evaluacion_sensorial_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Aún no hay respuestas guardadas. Complete y guarde al menos una para poder exportar.")
