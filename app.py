import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    h1 {
        color: #ffffff;
        text-align: center;
    }
    h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    .stSidebar {
        background-color: #1a1a1a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("DashBoard PPGHIS (Professores)")
st.sidebar.header("Menu Lateral")
st.sidebar.write("Aqui estão alguns filtros e opções.")

# Lista de nomes para filtrar
nomes_para_filtrar = [
    "Todos", "Andréa Casa Nova Maia", "Andrea Daher", "Antonio Carlos Jucá de Sampaio", 
    "Beatriz Catão Cruz Santos", "Carlos Ziller Camenietzki", "Cláudio Costa Pinheiro", 
    "Deivid Valério Gaia", "Felipe Charbel Teixeira", "Fernando Luiz Vale Castro", 
    "Flávio dos Santos Gomes", "Gabriel de Carvalho Godoy Castanho", "Hanna Sonkajärvi", 
    "Henrique Buarque de Gusmão", "Isabele de Matos Pereira de Mello", "Jacqueline Hermann", 
    "João Rodolfo Munhoz Ohara", "Jorge Victor de Araújo Souza", "Jose Augusto Padua", 
    "Joao Luis Ribeiro Fragoso", "Lise Fernanda Sedrez", "Lorena Lopes da Costa", 
    "Luiza Larangeira da Silva Mello", "Marcos Luiz Bretas da Fonseca", 
    "Maria Paula Nascimento Araujo", "Marieta de Moraes Ferreira", 
    "Marta Mega de Andrade", "Michel Gherman", "Monica Grin", "Mônica Lima e Souza", 
    "Murilo Sebe Bon Meihy", "Nuno Carlos de Fragoso Vidal", 
    "Paulo Roberto Ribeiro Fontes", "Renato Luis do Couto Neto e Lemos", 
    "Roberto Guedes Ferreira", "Silvia Regina Liebel", 
    "Vinícius Aurélio Liebel", "Vitor Izecksohn", "William de Souza Martins"
]

# Anos para filtrar
anos_para_filtrar = ["Todos", "2021", "2022", "2023", "2024"]

# Carregar os arquivos Excel
excel_files = {
    "Produção Bibliográfica": pd.ExcelFile("data/Producao_Bibliografica.xlsx"),
    "Produção Técnica": pd.ExcelFile("data/Producao_tecnica.xlsx"),
    "Produção Cultural": pd.ExcelFile("data/Producao_cultural.xlsx"),
    "Bancas": pd.ExcelFile("data/Bancas.xlsx"),
    "Eventos": pd.ExcelFile("data/Eventos.xlsx"),
    "Orientações": pd.ExcelFile("data/orientações.xlsx")
}

# Processar os DataFrames
dataframes = {}
for file_name, excel_file in excel_files.items():
    dataframes[file_name] = {sheet: excel_file.parse(sheet) for sheet in excel_file.sheet_names}

# Função para filtrar e contar as linhas
def contar_linhas(df, nomes, anos):
    if "Todos" not in nomes:
        df = df[df['Nome Completo'].isin(nomes)]
    if "Todos" not in anos:
        df = df[df['Ano'].isin(anos)]
    return len(df)

# Interface do usuário
nomes_selecionados = st.sidebar.multiselect("Selecione os Nomes", options=nomes_para_filtrar, default="Todos")
anos_selecionados = st.sidebar.multiselect("Selecione os Anos", options=anos_para_filtrar, default="Todos")

# Filtrar os dados
contagens = {arquivo: sum(contar_linhas(df, nomes_selecionados, anos_selecionados) for df in sheets.values()) for arquivo, sheets in dataframes.items()}

# Exibir o gráfico de pizza
fig_pie = px.pie(names=list(contagens.keys()), values=list(contagens.values()), title="Distribuição por Categoria")
st.plotly_chart(fig_pie)

# Filtrar os anos selecionados
if "Todos" in anos_selecionados or not anos_selecionados:
    anos_filtrados = ["2021", "2022", "2023", "2024"]
else:
    anos_filtrados = anos_selecionados

# Contagem de linhas por ano filtrado
contagens_por_ano = {ano: 0 for ano in anos_filtrados}
for sheets in dataframes.values():
    for df in sheets.values():
        for ano in contagens_por_ano.keys():
            contagens_por_ano[ano] += len(df[df['Ano'] == int(ano)])

# Gráfico de barras atualizado com os anos filtrados
fig_bar = px.bar(x=list(contagens_por_ano.keys()), y=list(contagens_por_ano.values()), title="Total por Ano")
st.plotly_chart(fig_bar)
















