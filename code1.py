# code1.py
import pandas as pd

def read_and_clean_data():
    # Lectura de datos
    df_annual_deaths = pd.read_csv("Annual cause death numbers new.csv")
    
    # Limpieza y transformación
    paises_eliminar = ['SouthEast Asia Region who', 'World Bank High Income', 'African Region who', 'G20', 'North America wb', 'World', 'Europe & Central Asia wb', 'Western Pacific Region who', 'World Bank Lower Middle Income', 'World Bank Low Income', 'Eastern Mediterranean Region who', 'OECD Countries', 'European Region who', 'South Asia wb', 'Region of the Americas who', 'East Asia & Pacific wb', 'Middle East & North Africa wb', 'World Bank Upper Middle Income']
    
    df = df_annual_deaths[~df_annual_deaths['Entity'].isin(paises_eliminar)]
    df.columns = df.columns.str.replace('\n', '') 
    df[df.columns[2:]] = df[df.columns[2:]].astype(int)

    return df

def data_summary(df):
    summary = df.describe()
    return summary
