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
    # Crear las pestañas (solo 3)
    tab1, tab2, tab3 = st.tabs([
        "inicial",
        "Datos Personales",
        "Encuesta"
    ])

    # ---------- PESTAÑA 1: Inicial (Influye en la percepción) ----------
    with tab1:
        st.header("Influye en la percepción")

        cond_medica = st.radio(
            "¿Tiene alguna condición médica que afecte el gusto, el olfato o la sensibilidad oral (como sinusitis, rinitis, resfrío, gripe, congestión nasal u otra afección en este momento, etc.)?",
            options=["Sí", "No"],
            index=1,
            key="cond_medica",
            horizontal=True
        )
        medicamentos = st.radio(
            "¿Toma actualmente algún medicamento que pueda alterar el gusto, el olfato o la salivación (como antihistamínicos, antibióticos, ansiolíticos, etc.)?",
            options=["Sí", "No"],
            index=1,
            key="medicamentos",
            horizontal=True
        )
        alergias = st.radio(
            "¿Tiene alguna alergia alimentaria relacionada con aceite de oliva, lactosa, gluten, proteínas del huevo algún condimento?",
            options=["Sí", "No"],
            index=1,
            key="alergias",
            horizontal=True
        )
        fumado = st.radio(
            "¿Ha fumado cigarrillos u otros productos en la última hora, antes de hacer esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="fumado",
            horizontal=True
        )
        alcohol = st.radio(
            "¿Ha consumido alcohol en la última hora, antes de hacer esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="alcohol",
            horizontal=True
        )
        cafe = st.radio(
            "¿Ha consumido café, chicles, menta en la última hora, antes de hacer esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="cafe",
            horizontal=True
        )
        cepillado = st.radio(
            "¿Se cepilló los dientes justo antes del test?",
            options=["Sí", "No"],
            index=1,
            key="cepillado",
            horizontal=True
        )
        fatigado = st.radio(
            "¿Se siente fatigado/a o con sueño?",
            options=["Sí", "No"],
            index=1,
            key="fatigado",
            horizontal=True
        )
        estres = st.radio(
            "¿Siente estrés, ansiedad o malestar emocional?",
            options=["Sí", "No"],
            index=1,
            key="estres",
            horizontal=True
        )

    # ---------- PESTAÑA 2: Datos personales ----------
    with tab2:
        st.header("Datos Personales")

        # Nota: el número de ficha se calcula al guardar, no es un campo editable
        st.markdown(f"**Ficha N.º:** {len(st.session_state.responses) + 1} (se asignará al guardar)")

        nombre = st.text_input("Nombre", key="nombre")
        apellido = st.text_input("Apellido", key="apellido")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1, key="edad")
        genero = st.selectbox(
            "Sexo o Género",
            options=["Femenino", "Masculino", "Prefiero no responder"],
            key="genero"
        )

        volveria = st.radio(
            "¿Volvería a participar en esta prueba?",
            options=["Sí", "No"],
            index=1,
            key="volveria",
            horizontal=True
        )

        # Campo condicional (se muestra solo si volveria == "Sí")
        if volveria == "Sí":
            contacto = st.text_input("Contacto (número de teléfono)", key="contacto")
        else:
            # Aseguramos que la clave exista para evitar errores al guardar
            st.session_state["contacto"] = ""

    # ---------- PESTAÑA 3: Encuesta sobre el producto ----------
    with tab3:
        st.header("Encuesta")
        st.markdown("**Este aderezo tiene aceite de oliva, aceite de girasol y leche de cabra**")

        conoce = st.radio("¿Conoce este tipo de producto?", options=["Sí", "No"], index=1, key="conoce", horizontal=True)
        ha_probado = st.radio("¿Ha probado este tipo de producto antes?", options=["Sí", "No"], index=1, key="ha_probado", horizontal=True)

        st.markdown("**¿Suele consumir aderezos similares?**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            mayonesa = st.checkbox("Mayonesa", key="sim_mayonesa")
        with col2:
            aioli = st.checkbox("Aioli", key="sim_aioli")
        with col3:
            cesar = st.checkbox("Salsas César", key="sim_cesar")
        with col4:
            otros_sim = st.checkbox("Otros", key="sim_otros")

        # Campo condicional para "Otros"
        otros_sim_text = ""
        if otros_sim:
            otros_sim_text = st.text_input("Especifique otros aderezos similares", key="sim_otros_text")
        else:
            st.session_state["sim_otros_text"] = ""

        consumirian = st.radio(
            "¿Cree que todos los integrantes de su hogar consumirían este aderezo por sus ingredientes?",
            options=["Sí", "No"],
            index=1,
            key="consumirian",
            horizontal=True
        )

        frecuencia = st.text_input("¿Con qué frecuencia consume aderezos?", key="frecuencia")
        cantidad = st.text_input("¿Qué cantidad de aderezos consumen en su hogar por mes?", key="cantidad")

        marca = st.selectbox(
            "Marca de aderezos más consumida normalmente en su hogar",
            options=["Mayonesa", "Aioli", "Salsas César", "Otros"],
            key="marca"
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
        respuesta = {
            "Ficha N°": nueva_ficha,
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # Tab1
            "Condición médica": cond_medica,
            "Medicamentos": medicamentos,
            "Alergias": alergias,
            "Fumado última hora": fumado,
            "Alcohol última hora": alcohol,
            "Café/chicles/menta": cafe,
            "Cepillado antes": cepillado,
            "Fatiga/sueño": fatigado,
            "Estrés/ansiedad": estres,
            # Tab2
            "Nombre": nombre,
            "Apellido": apellido,
            "Edad": edad,
            "Género": genero,
            "Volvería a participar": volveria,
            "Contacto": st.session_state.contacto if volveria == "Sí" else "",
            # Tab3
            "Conoce producto": conoce,
            "Ha probado antes": ha_probado,
            "Consume Mayonesa": "Sí" if mayonesa else "No",
            "Consume Aioli": "Sí" if aioli else "No",
            "Consume Salsas César": "Sí" if cesar else "No",
            "Consume Otros similares": otros_sim_text if otros_sim else "",
            "Todos consumirían": consumirian,
            "Frecuencia consumo": frecuencia,
            "Cantidad mensual": cantidad,
            "Marca preferida": marca,
            "Otra marca especificada": otros_marca_text if marca == "Otros" else ""
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
