import streamlit as st
import pandas as pd
from io import BytesIO
import datetime
import uuid

# Configuración de la página
st.set_page_config(page_title="Evaluación sensorial", layout="wide")

# Generar un identificador único de sesión si no existe
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ---- ESTILOS PERSONALIZADOS (igual que antes) ----
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d4edda;
        color: black;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label, 
    .stRadio label, .stCheckbox label {
        color: black !important;
        font-weight: 500;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox select, 
    .stTextArea textarea, .stDateInput input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #aaa !important;
    }
    .stButton button {
        background-color: #28a745;
        color: white;
        border: 1px solid #1e7e34;
    }
    .stButton button:hover {
        background-color: #218838;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #c3e6cb;
        border: 1px solid #28a745;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: black;
        border-radius: 6px;
        padding: 8px 16px;
        margin: 2px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #28a745 !important;
        color: white !important;
        border: 1px solid #1e7e34;
    }
    .stDataFrame {
        background-color: white;
        color: black;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: black;
    }
    hr {
        border-color: #28a745;
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

# Crear las tres pestañas
tab1, tab2, tab3 = st.tabs(["inicial", "encuesta", "datos"])

# ---------- PESTAÑA 1: Inicial (solo informativa) ----------
with tab1:
    st.header("Condiciones que pueden influir en la percepción")
    st.markdown("*(Esta información es solo para referencia del encuestador y no se almacena)*")
    # ... (las mismas preguntas, sin cambios)
    st.radio("¿Tiene alguna condición médica que afecte el gusto...?", options=["Sí", "No"], index=1, key="cond_medica", horizontal=True)
    st.radio("¿Toma actualmente algún medicamento...?", options=["Sí", "No"], index=1, key="medicamentos", horizontal=True)
    st.radio("¿Tiene alguna alergia alimentaria...?", options=["Sí", "No"], index=1, key="alergias", horizontal=True)
    st.radio("¿Ha fumado...?", options=["Sí", "No"], index=1, key="fumado", horizontal=True)
    st.radio("¿Ha consumido alcohol...?", options=["Sí", "No"], index=1, key="alcohol", horizontal=True)
    st.radio("¿Ha consumido café, chicles, menta...?", options=["Sí", "No"], index=1, key="cafe", horizontal=True)
    st.radio("¿Se cepilló los dientes...?", options=["Sí", "No"], index=1, key="cepillado", horizontal=True)
    st.radio("¿Se siente fatigado/a...?", options=["Sí", "No"], index=1, key="fatigado", horizontal=True)
    st.radio("¿Siente estrés...?", options=["Sí", "No"], index=1, key="estres", horizontal=True)

# ---------- PESTAÑA 2: Encuesta (datos que se guardan) ----------
with tab2:
    st.header("Encuesta")
    st.markdown(f"**Sesión ID:** {st.session_state.session_id}")
    st.markdown(f"**Próxima Ficha N.º:** {len(st.session_state.responses) + 1}")

    # Función para resetear todos los campos del formulario
    def reset_encuesta_form():
        st.session_state["nombre"] = ""
        st.session_state["apellido"] = ""
        st.session_state["edad"] = 0
        st.session_state["genero"] = "Femenino"
        st.session_state["volveria"] = "No"
        st.session_state["contacto"] = ""
        st.session_state["conoce"] = "No"
        st.session_state["ha_probado"] = "No"
        st.session_state["sim_mayonesa"] = False
        st.session_state["sim_aioli"] = False
        st.session_state["sim_cesar"] = False
        st.session_state["sim_otros"] = False
        st.session_state["sim_otros_text"] = ""
        st.session_state["consumirian"] = "No"
        st.session_state["frecuencia"] = ""
        st.session_state["cantidad"] = ""
        st.session_state["marca"] = "Mayonesa"
        st.session_state["marca_otros_text"] = ""

    with st.form(key="encuesta_form"):
        # --- Pregunta 1: Nombre ---
        st.markdown("**1. Nombre**")
        nombre = st.text_input("Nombre", key="nombre", label_visibility="collapsed")

        # --- Pregunta 2: Apellido ---
        st.markdown("**2. Apellido**")
        apellido = st.text_input("Apellido", key="apellido", label_visibility="collapsed")

        # --- Pregunta 3: Edad ---
        st.markdown("**3. Edad**")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1, key="edad", label_visibility="collapsed")

        # --- Pregunta 4: Género ---
        st.markdown("**4. Género**")
        genero = st.selectbox("Género", options=["Femenino", "Masculino", "Prefiero no responder"], key="genero", label_visibility="collapsed")

        # --- Pregunta 5: ¿Volvería a participar? ---
        st.markdown("**5. ¿Volvería a participar?**")
        volveria = st.radio("¿Volvería a participar?", options=["Sí", "No"], index=1, key="volveria", horizontal=True, label_visibility="collapsed")

        # --- Pregunta 5b: Contacto (condicional) ---
        if volveria == "Sí":
            contacto = st.text_input("Contacto (número de teléfono)", key="contacto")
        else:
            contacto = ""
            # Aseguramos que el valor en session_state esté vacío si no se muestra
            st.session_state["contacto"] = ""

        st.markdown("---")
        st.markdown("**Información sobre el producto**")
        st.markdown("*Este aderezo tiene aceite de oliva, aceite de girasol y leche de cabra*")

        # --- Pregunta 6: ¿Conoce este tipo de producto? ---
        st.markdown("**6. ¿Conoce este tipo de producto?**")
        conoce = st.radio("¿Conoce este tipo de producto?", options=["Sí", "No"], index=1, key="conoce", horizontal=True, label_visibility="collapsed")

        # --- Pregunta 7: ¿Ha probado antes? ---
        st.markdown("**7. ¿Ha probado antes este tipo de producto?**")
        ha_probado = st.radio("¿Ha probado este tipo de producto antes?", options=["Sí", "No"], index=1, key="ha_probado", horizontal=True, label_visibility="collapsed")

        # --- Pregunta 8: Consumo de aderezos similares (múltiple) ---
        st.markdown("**8. ¿Suele consumir aderezos similares? (puede seleccionar varios)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            mayonesa = st.checkbox("Mayonesa", key="sim_mayonesa")
        with col2:
            aioli = st.checkbox("Aioli", key="sim_aioli")
        with col3:
            cesar = st.checkbox("Salsas César", key="sim_cesar")
        with col4:
            otros_sim = st.checkbox("Otros", key="sim_otros")

        otros_sim_text = ""
        if otros_sim:
            otros_sim_text = st.text_input("Especifique otros aderezos similares", key="sim_otros_text")
        else:
            st.session_state["sim_otros_text"] = ""

        # --- Pregunta 9: ¿Cree que todos consumirían? ---
        st.markdown("**9. ¿Cree que todos los integrantes de su hogar consumirían este aderezo por sus ingredientes?**")
        consumirian = st.radio("¿Cree que todos...?", options=["Sí", "No"], index=1, key="consumirian", horizontal=True, label_visibility="collapsed")

        # --- Pregunta 10: Frecuencia de consumo ---
        st.markdown("**10. ¿Con qué frecuencia consume aderezos?**")
        frecuencia = st.text_input("Frecuencia", key="frecuencia", label_visibility="collapsed")

        # --- Pregunta 11: Cantidad mensual ---
        st.markdown("**11. ¿Qué cantidad de aderezos consumen en su hogar por mes?**")
        cantidad = st.text_input("Cantidad mensual", key="cantidad", label_visibility="collapsed")

        # --- Pregunta 12: Marca preferida ---
        st.markdown("**12. Marca de aderezos más consumida normalmente en su hogar**")
        marca = st.selectbox("Marca", options=["Mayonesa", "Aioli", "Salsas César", "Otros"], key="marca", label_visibility="collapsed")
        otros_marca_text = ""
        if marca == "Otros":
            otros_marca_text = st.text_input("Especifique otra marca", key="marca_otros_text")
        else:
            st.session_state["marca_otros_text"] = ""

        # Botón de guardar
        submitted = st.form_submit_button("Guardar respuesta")

        if submitted:
            nueva_ficha = len(st.session_state.responses) + 1
            respuesta = {
                "ID_Respuesta": f"{st.session_state.session_id}_{nueva_ficha}",
                "Ficha N°": nueva_ficha,
                "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "P1_Nombre": nombre,
                "P2_Apellido": apellido,
                "P3_Edad": edad,
                "P4_Género": genero,
                "P5_Volvería a participar": volveria,
                "P5_Contacto": contacto if volveria == "Sí" else "",
                "P6_Conoce producto": conoce,
                "P7_Ha probado antes": ha_probado,
                "P8_Mayonesa": "Sí" if mayonesa else "No",
                "P8_Aioli": "Sí" if aioli else "No",
                "P8_Salsas César": "Sí" if cesar else "No",
                "P8_Otros similares (especificar)": otros_sim_text if otros_sim else "",
                "P9_Todos consumirían": consumirian,
                "P10_Frecuencia consumo": frecuencia,
                "P11_Cantidad mensual": cantidad,
                "P12_Marca preferida": marca,
                "P12_Otra marca especificada": otros_marca_text if marca == "Otros" else ""
            }
            st.session_state.responses.append(respuesta)
            # Resetear el formulario
            reset_encuesta_form()
            st.success(f"Respuesta guardada correctamente. Ficha N° {nueva_ficha}")
            st.rerun()

# ---------- PESTAÑA 3: Datos (exportación y cierre de sesión) ----------
with tab3:
    st.header("Exportar datos")

    if st.session_state.responses:
        df = pd.DataFrame(st.session_state.responses)
        st.dataframe(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Respuestas')
        output.seek(0)

        # Botón de descarga que además cierra la sesión
        if st.download_button(
            label="Descargar Excel y cerrar sesión",
            data=output,
            file_name=f"evaluacion_sensorial_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            # Limpiar respuestas y generar nuevo session_id
            st.session_state.responses = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    else:
        st.info("Aún no hay respuestas guardadas. Complete y guarde al menos una para poder exportar.")
