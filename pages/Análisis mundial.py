import pandas as pd
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import folium_static # type: ignore

# Carga y limpieza de datos
@st.cache_data
def load_data():
    df = pd.read_csv("Annual cause death numbers new.csv")
    df.columns = df.columns.str.replace('\n', '') 
    df[df.columns[2:]] = df[df.columns[2:]].astype(int)
    
    poblacion = pd.read_excel("poblacion_mundial.xlsx")
    poblacion_country = poblacion.loc[:, 'country']
    poblacion = poblacion.loc[:, 1990:2019]
    poblacion = pd.concat([poblacion_country, poblacion], axis=1)
    poblacion = poblacion.melt(id_vars='country', var_name='year', value_name='population')
    
    def convertir_a_enteros(valor):
        if isinstance(valor, str):
            if 'M' in valor:
                return int(float(valor.replace('M', '')) * 1_000_000)
            elif 'k' in valor:
                return int(float(valor.replace('k', '')) * 1_000)
            elif 'B' in valor:
                return int(float(valor.replace('B', '')) * 1_000_000_000)
        return valor
    
    poblacion['population'] = poblacion['population'].apply(convertir_a_enteros)
    
    df_merged = df.merge(poblacion, left_on=['Entity', 'Year'], right_on=['country', 'year'])
    df_merged = df_merged.drop(columns=['country', 'year'])
    
    return df_merged

df_merged = load_data()

# Lectura del archivo shapefile 'world'
world = gpd.read_file("C:/Users/Ana Asensio/Desktop/UNI/MIARFID/BLOQUE 2/VD/proyecto_final/110m_cultural/ne_110m_admin_0_countries.shp")

# Renombrar columna para que coincida con el DataFrame df_merged
world = world.rename(columns={'NAME': 'Entity'})

# Calcular columna total_deaths en df_merged
df_merged['total_deaths'] = df_merged.iloc[:, 2:].sum(axis=1)

# Calcular otra columna con la tasa de mortalidad dividiendo totaldeath entre población
df_merged['mortality_rate'] = df_merged['total_deaths'] / df_merged['population']

# Merge entre el GeoDataFrame world y el DataFrame df_merged
df_map = world.merge(df_merged, on='Entity')

# Creación de categorías
infectious_and_parasitic_diseases = ['Meningitis fatalities', 'Malaria fatalities', 'Tuberculosis fatalities', 'HIV/AIDS fatalities', 'Diarrheal disease fatalities', 'Measles fatalities', 'Acute hepatitis fatalities']
neurological_and_degenerative_disorders = ['Dementia fatalities', 'Parkinson s fatalities']
lifestyle_related_and_addiction_disorders = ['Drug disorder fatalities', 'Alcohol disorder fatalities', 'Self harm fatalities']
accidents_and_injuries_fatalities = ['Drowning fatalities', 'Interpersonal violence fatalities', 'Forces of nature fatalities', 'Road injury fatalities', 'Fire fatalities']
chronic_non_communicable_fatalities = ['Cardiovascular fatalities', 'Lower respiratory fatalities', 'Chronic kidney fatalities', 'Neoplasm fatalities', 'Diabetes fatalities', 'Chronic respiratory fatalities', 'Chronic liver fatalities', 'Digestive disease fatalities']
environmental_malnutrition_fatalities = ['Nutritional deficiency fatalities', 'Environmental exposure fatalities', 'Protein energy malnutrition fatalities']

df_map['Infectious and Parasitic Diseases'] = df_map[infectious_and_parasitic_diseases].sum(axis=1)
df_map['Neurological and Degenerative Disorders'] = df_map[neurological_and_degenerative_disorders].sum(axis=1)
df_map['Lifestyle-related and Addiction Disorders'] = df_map[lifestyle_related_and_addiction_disorders].sum(axis=1)
df_map['Accidents and Injuries Fatalities'] = df_map[accidents_and_injuries_fatalities].sum(axis=1)
df_map['Chronic Non-communicable Fatalities'] = df_map[chronic_non_communicable_fatalities].sum(axis=1)
df_map['Environmental and Malnutrition Fatalities'] = df_map[environmental_malnutrition_fatalities].sum(axis=1)

# Añadir selección de categoría en Streamlit
categories = [
    'Infectious and Parasitic Diseases',
    'Neurological and Degenerative Disorders',
    'Lifestyle-related and Addiction Disorders',
    'Accidents and Injuries Fatalities',
    'Chronic Non-communicable Fatalities',
    'Environmental and Malnutrition Fatalities'
]

selected_category = st.selectbox("Selecciona una categoría de enfermedad", categories)

# Mostrar el mapa global
st.write(f"## Mapa de Mortalidad Global por {selected_category} (2019)")
m = folium.Map(location=[0, 0], zoom_start=2)
folium.Choropleth(
    geo_data=df_map,
    name='choropleth',
    data=df_map,
    columns=['Entity', selected_category],
    key_on='feature.properties.Entity',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=selected_category
).add_to(m)

folium_static(m)

# Filtrar por continente
continentes = df_map['CONTINENT'].unique()
selected_continent = st.selectbox("Selecciona un continente", continentes)

# Filtrar el DataFrame por continente seleccionado
df_continent = df_map[df_map['CONTINENT'] == selected_continent]

# Filtrar por año 2019
df_continent = df_continent[df_continent['Year'] == 2019]

# Mostrar el mapa del continente seleccionado
st.write(f"## Mapa de Mortalidad en {selected_continent} por {selected_category} (2019)")
m_continent = folium.Map(location=[0, 0], zoom_start=2)
folium.Choropleth(
    geo_data=df_continent,
    name='choropleth',
    data=df_continent,
    columns=['Entity', selected_category],
    key_on='feature.properties.Entity',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=selected_category
).add_to(m_continent)

folium_static(m_continent)

# Mostrar los resultados
st.write(f"## Tasa de Mortalidad en {selected_continent} (2019)")
st.write(df_continent[['Entity', selected_category]])
