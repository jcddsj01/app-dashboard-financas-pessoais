import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Finanças Pessoais", layout="wide")

# Leitura e preparação dos dados
df = pd.read_csv("finances.csv")
df.drop(columns=["ID"], inplace=True)

# Converte a coluna 'Data' para datetime
df["Data"] = pd.to_datetime(df["Data"])

# Cria a coluna 'Mês' no formato "MM/YYYY"
df["Mês"] = df["Data"].dt.strftime("%m/%Y")

# Remove entradas da categoria 'Receitas'
df = df[df["Categoria"] != "Receitas"]

# Função para filtrar os dados
def filter_data(df, mes, selected_categories):
    df_filtered = df[df['Mês'] == mes]
    if selected_categories:
        df_filtered = df_filtered[df_filtered['Categoria'].isin(selected_categories)]
    return df_filtered

# Título do app
st.title("Dashboard de Finanças Pessoais com IAs")

# Sidebar com seleção de mês e categorias
mes = st.sidebar.selectbox("Selecione o Mês", df["Mês"].unique())
categories = df["Categoria"].unique().tolist()
selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

# Filtragem dos dados
df_filtered = filter_data(df, mes, selected_categories)

# Criação do gráfico de pizza
category_distribution = df_filtered.groupby("Categoria")["Valor"].sum().reset_index()
fig = px.pie(category_distribution, values="Valor", names="Categoria", title="Distribuição por Categoria", hole=0.3)

# Preparação da tabela para exibição
df_display = df_filtered.copy()
df_display["Data"] = df_display["Data"].dt.strftime("%d/%m/%Y")
df_display["Valor"] = df_display["Valor"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

# Layout com colunas
c1, c2 = st.columns([0.5, 0.5])
c1.dataframe(df_display)
c2.plotly_chart(fig, use_container_width=True)
