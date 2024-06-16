import streamlit as st
from code1 import read_and_clean_data, data_summary
from code2 import analyze_data

# Leer y limpiar datos
df = read_and_clean_data()
summary = data_summary(df)

# Crear pestañas
tab1, tab2 = st.tabs(["Datos", "Análisis y Visualización"])

# Mostrar el contenido en las pestañas correspondientes
with tab1:
    st.header("Causas de muerte en el mundo 1990-2019")
    st.write(df)
    st.header("Resumen estadístico de los datos")
    # mostrar summary sin la columna de year
    st.write(summary.iloc[:,1:])

with tab2:
    st.header("Análisis y Visualización de Datos")
    st.write("Análisis completo")
    result = analyze_data(df)
    st.write(result)
