# pages/spain_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

st.title("Análisis de Datos para España")

@st.cache_data
def read_and_clean_data():
    df_annual_deaths = pd.read_csv("Annual cause death numbers new.csv")
    paises_eliminar = ['SouthEast Asia Region who', 'World Bank High Income', 'African Region who', 'G20', 'North America wb', 'World', 'Europe & Central Asia wb', 'Western Pacific Region who', 'World Bank Lower Middle Income', 'World Bank Low Income', 'Eastern Mediterranean Region who', 'OECD Countries', 'European Region who', 'South Asia wb', 'Region of the Americas who', 'East Asia & Pacific wb', 'Middle East & North Africa wb', 'World Bank Upper Middle Income']
    df = df_annual_deaths[~df_annual_deaths['Entity'].isin(paises_eliminar)]
    df.columns = df.columns.str.replace('\n', '') 
    df[df.columns[2:]] = df[df.columns[2:]].astype(int)
    return df

df = read_and_clean_data()
df_spain = df[df.Entity == 'Spain']
causes_of_death = [column for column in df_spain.columns[3:]]

# Selección de tipo de gráfico
chart_type = st.selectbox("Selecciona el tipo de gráfico", ["Línea", "Barra", "Histograma", "Boxplot", "Dispersión", "Par Gráficos"])

# Selección de enfermedades
selected_causes = st.multiselect("Selecciona las causas de muerte", causes_of_death, default=causes_of_death[:5])

# Filtrar los datos según la selección
filtered_df = df_spain[['Year'] + selected_causes]

if chart_type == "Línea":
    fig, ax = plt.subplots()
    for cause in selected_causes:
        ax.plot(filtered_df['Year'], filtered_df[cause], label=cause)
    ax.set_title('Evolución de las causas de muerte seleccionadas en España')
    ax.set_xlabel('Año')
    ax.set_ylabel('Número de casos')
    ax.legend()
    st.pyplot(fig)

elif chart_type == "Barra":
    df_categories = filtered_df.melt(id_vars=['Year'], var_name='Category', value_name='Deaths')
    fig, ax = plt.subplots()
    sns.barplot(x="Year", y="Deaths", hue="Category", data=df_categories, ax=ax)
    ax.set_title('Muertes por causas seleccionadas en España')
    ax.set_xlabel('Año')
    ax.set_ylabel('Número de casos')
    st.pyplot(fig)

elif chart_type == "Histograma":
    fig, ax = plt.subplots()
    filtered_df[selected_causes].hist(bins=20, figsize=(12, 10), xrot=45, ax=ax)
    plt.tight_layout()
    st.pyplot(fig)

elif chart_type == "Boxplot":
    df_categories = filtered_df.melt(id_vars=['Year'], var_name='Category', value_name='Deaths')
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.boxplot(x="Category", y="Deaths", data=df_categories, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title('Boxplot de muertes por categorías seleccionadas')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Muertes')
    st.pyplot(fig)

elif chart_type == "Dispersión":
    if len(selected_causes) != 2:
        st.warning("Selecciona exactamente 2 causas para el gráfico de dispersión.")
    else:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(data=filtered_df, x=selected_causes[0], y=selected_causes[1], s=100, ax=ax)
        ax.set_title(f'Relación entre {selected_causes[0]} y {selected_causes[1]} en España')
        ax.set_xlabel(selected_causes[0])
        ax.set_ylabel(selected_causes[1])
        st.pyplot(fig)

elif chart_type == "Par Gráficos":
    fig = sns.pairplot(data=filtered_df[selected_causes], kind='reg', height=5)
    plt.xticks(rotation=45)
    st.pyplot(fig)
