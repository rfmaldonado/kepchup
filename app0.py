import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Recolección de Datos", page_icon="📊")

# Título de la aplicación
st.title("📊 Sistema de Recolección de Datos")
st.markdown("Ingresa 3 datos cuantitativos y 3 datos cualitativos")

# Inicializar el DataFrame en session_state si no existe
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = pd.DataFrame(columns=[
        'fecha', 
        'cuantitativo_1', 'cuantitativo_2', 'cuantitativo_3',
        'cualitativo_1', 'cualitativo_2', 'cualitativo_3'
    ])

# Crear un formulario para la entrada de datos
with st.form("formulario_datos", clear_on_submit=True):
    st.header("📝 Ingreso de Datos")
    
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Datos Cuantitativos")
        # Campos numéricos
        cuant_1 = st.number_input("Cuantitativo 1", value=0.0, step=0.1)
        cuant_2 = st.number_input("Cuantitativo 2", value=0.0, step=0.1)
        cuant_3 = st.number_input("Cuantitativo 3", value=0.0, step=0.1)
    
    with col2:
        st.subheader("Datos Cualitativos")
        # Campos de texto
        cual_1 = st.text_input("Cualitativo 1")
        cual_2 = st.text_input("Cualitativo 2")
        cual_3 = st.text_input("Cualitativo 3")
    
    # Botón para agregar datos
    submitted = st.form_submit_button("💾 Guardar Datos")
    
    if submitted:
        if cual_1 and cual_2 and cual_3:  # Validar que los campos cualitativos no estén vacíos
            # Crear nuevo registro
            nuevo_registro = {
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'cuantitativo_1': cuant_1,
                'cuantitativo_2': cuant_2,
                'cuantitativo_3': cuant_3,
                'cualitativo_1': cual_1,
                'cualitativo_2': cual_2,
                'cualitativo_3': cual_3
            }
            
            # Agregar al DataFrame
            st.session_state.dataframe = pd.concat([
                st.session_state.dataframe, 
                pd.DataFrame([nuevo_registro])
            ], ignore_index=True)
            
            st.success("✅ Datos guardados exitosamente!")
        else:
            st.warning("⚠️ Por favor completa todos los campos cualitativos")

# Mostrar los datos almacenados
st.header("📋 Datos Almacenados")
if not st.session_state.dataframe.empty:
    st.dataframe(st.session_state.dataframe, use_container_width=True)
    
    # Estadísticas básicas
    st.subheader("📈 Estadísticas de Datos Cuantitativos")
    st.write(st.session_state.dataframe[['cuantitativo_1', 'cuantitativo_2', 'cuantitativo_3']].describe())
else:
    st.info("No hay datos almacenados aún. Agrega algunos datos usando el formulario arriba.")

# Sección para descargar los datos
st.header("💾 Exportar Datos")
if not st.session_state.dataframe.empty:
    # Opciones de formato
    formato = st.radio("Selecciona el formato de descarga:", 
                       ["CSV", "Excel", "JSON"], horizontal=True)
    
    if formato == "CSV":
        csv = st.session_state.dataframe.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="datos_recolectados.csv",
            mime="text/csv"
        )
    
    elif formato == "Excel":
        # Para Excel necesitamos crear un archivo temporal
        excel_file = st.session_state.dataframe.to_excel(
            index=False, 
            engine='openpyxl'
        )
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_file,
            file_name="datos_recolectados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    elif formato == "JSON":
        json = st.session_state.dataframe.to_json(orient="records", indent=2)
        st.download_button(
            label="📥 Descargar JSON",
            data=json,
            file_name="datos_recolectados.json",
            mime="application/json"
        )
    
    # Botón para limpiar todos los datos
    if st.button("🗑️ Limpiar Todos los Datos"):
        st.session_state.dataframe = pd.DataFrame(columns=st.session_state.dataframe.columns)
        st.rerun()
else:
    st.warning("Agrega datos para habilitar la descarga")

# Información adicional
st.sidebar.header("ℹ️ Información")
st.sidebar.info("""
**Instrucciones:**
1. Completa los 6 campos del formulario
2. Haz clic en 'Guardar Datos'
3. Los datos se almacenan temporalmente
4. Descarga los datos en el formato que prefieras

**Tipos de datos:**
- **Cuantitativos:** Números (ej: 10.5, 100, 3.14)
- **Cualitativos:** Texto (ej: 'Alto', 'Verde', 'Aprobado')
""")

# Contador de registros
if not st.session_state.dataframe.empty:
    st.sidebar.metric("📊 Registros almacenados", len(st.session_state.dataframe))
