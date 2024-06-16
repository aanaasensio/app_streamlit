# code2.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

def analyze_data(df):
    # Primer análisis exploratorio
    summary = df.describe()
    summary_max = summary.iloc[:,1:].T
    summary_max = summary_max.sort_values(by='max', ascending=False)
    summary_top10 = summary_max.head(10)

    fig, ax = plt.subplots()
    ax.bar(summary_top10.index, summary_top10['max'], color='red')
    ax.set_xticklabels([label.replace('fatalities', '') for label in summary_top10.index], rotation=90)
    ax.set_title('Top 10 causas de muerte')
    ax.set_ylabel('Muertes')
    st.pyplot(fig)

    summary_min = summary.iloc[:,1:].T
    summary_min = summary_min.sort_values(by='mean', ascending=True)
    summary_top10 = summary_min.head(10)

    fig, ax = plt.subplots()
    ax.bar(summary_top10.index, summary_top10['mean'], color='yellow')
    ax.set_xticklabels(summary_top10.index, rotation=90)
    ax.set_title('Top 10 causas de muerte más leves')
    ax.set_ylabel('Muertes')
    st.pyplot(fig)

    a = df.describe()
    total_row = a.loc['count'] * a.loc['mean']

    a.loc['total'] = total_row

    total_row = a.loc['total', a.columns[1:]]
    percentage_row = np.round((total_row / total_row.sum()) * 100, 2)
    percentage_row['Year'] = 0
    a[a.columns[:]] = a[a.columns[:]].astype(int)
    a.loc['percentage'] = percentage_row

    fig, ax = plt.subplots()
    ax.bar(a.columns[1:], a.loc['percentage'].values[1:])
    ax.set_xticklabels(a.columns[1:], rotation=90)
    ax.set_title('Porcentaje de muertes por causa')
    ax.set_ylabel('Porcentaje')
    st.pyplot(fig)

    deaths_by_cause = df.drop(columns=['Entity', 'Code', 'Year']).groupby(level=0).sum()
    deaths_by_cause = deaths_by_cause.sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = sns.color_palette("RdYlBu", len(deaths_by_cause))
    deaths_by_cause.plot(kind='barh', color=colors, ax=ax)
    ax.set_title('Número total de enfermedades en el mundo por causa', fontsize=16)
    ax.set_xlabel('Número de enfermedades', fontsize=14)
    ax.set_ylabel('Causa de muerte', fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)

    cardiovascular_df = df[['Entity', 'Year', 'Cardiovascular fatalities']]
    cardiovascular_by_country_year = cardiovascular_df.groupby(['Entity', 'Year']).sum().reset_index()
    top_10_countries = cardiovascular_by_country_year.groupby('Entity')['Cardiovascular fatalities'].sum().nlargest(10).index
    top_10_data = cardiovascular_by_country_year[cardiovascular_by_country_year['Entity'].isin(top_10_countries)]

    fig, ax = plt.subplots(figsize=(10, 6))
    for country, group in top_10_data.groupby('Entity'):
        ax.plot(group['Year'], group['Cardiovascular fatalities'], label=country)
    ax.set_title('Top 10 países con enfermedades cardiovasculares')
    ax.set_xlabel('Año')
    ax.set_ylabel('Número de casos')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

    return " "