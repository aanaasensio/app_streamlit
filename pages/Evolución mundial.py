import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static # type: ignore
import streamlit as st

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
    
    # Calcular columna total_deaths en df_merged
    df_merged['total_deaths'] = df_merged.iloc[:, 2:-1].sum(axis=1)
    
    # Calcular columna mortality_rate en df_merged
    df_merged['mortality_rate'] = df_merged['total_deaths'] / df_merged['population']
    
    return df_merged

df_merged = load_data()

# Lectura del archivo shapefile 'world'
world = gpd.read_file("110m_cultural/ne_110m_admin_0_countries.shp")

# Renombrar columna para que coincida con el DataFrame df_merged
world = world.rename(columns={'NAME': 'Entity'})

# Merge entre el GeoDataFrame world y el DataFrame df_merged
df_map = world.merge(df_merged, on='Entity')

# Selección de año en Streamlit
years = df_map['Year'].unique()
selected_year = st.slider("Selecciona el año", int(years.min()), int(years.max()), int(years.min()))

# Filtrar el DataFrame por el año seleccionado
df_year = df_map[df_map['Year'] == selected_year]

# Mostrar el mapa del año seleccionado
st.write(f"## Mapa de Mortalidad Global en {selected_year}")
m = folium.Map(location=[0, 0], zoom_start=2)
folium.Choropleth(
    geo_data=df_year,
    name='choropleth',
    data=df_year,
    columns=['Entity', 'mortality_rate'],
    key_on='feature.properties.Entity',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Tasa de Mortalidad'
).add_to(m)

folium_static(m)
