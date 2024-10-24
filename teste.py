import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    h1 {
        color: #ffffff;
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

st.title("Meu Aplicativo")
st.sidebar.header("Menu Lateral")
st.sidebar.write("Aqui estão alguns filtros e opções.")

# Lista de nomes para filtrar
nomes_para_filtrar = [
    "Andréa Casa Nova Maia", "Andrea Daher", "Antonio Carlos Jucá de Sampaio", 
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

# Adicionar a opção "Todos"
nomes_para_filtrar = ["Todos"] + nomes_para_filtrar

anos_para_filtrar = ["Todos", "2021", "2022", "2023", "2024"]

# Carregar os arquivos Excel usando pd.ExcelFile
excel_producao_bibliografica = pd.ExcelFile("data/Producao_Bibliografica.xlsx")
excel_producao_tecnica = pd.ExcelFile("data/Producao_tecnica.xlsx")
excel_producao_cultural = pd.ExcelFile("data/Producao_cultural.xlsx")
excel_bancas = pd.ExcelFile("data/Bancas.xlsx")
excel_eventos = pd.ExcelFile("data/Eventos.xlsx")
excel_orientacoes = pd.ExcelFile("data/orientações.xlsx")

# Dicionário para mapear os arquivos com suas sheets
excel_files = {
    "Produção Bibliográfica": excel_producao_bibliografica,
    "Produção Técnica": excel_producao_tecnica,
    "Produção Cultural": excel_producao_cultural,
    "Bancas": excel_bancas,
    "Eventos": excel_eventos,
    "Orientações": excel_orientacoes
}

dataframes = {}
for file_name, excel_file in excel_files.items():
    dataframes[file_name] = {}
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        # Converter a coluna 'Ano' para string, se existir
        if 'Ano' in df.columns:
            df['Ano'] = df['Ano'].astype(str)
        dataframes[file_name][sheet_name] = df

# Criar os filtros na barra lateral
with st.sidebar:
    nomes_selecionados = st.multiselect("Selecione o(s) Nome(s) para filtrar", options=nomes_para_filtrar, default="Todos")

    arquivos_disponiveis = ["Todos"] + list(excel_files.keys())
    arquivos_selecionados = st.multiselect(
        "Selecione o(s) Arquivo(s) para filtrar",
        options=arquivos_disponiveis,
        default="Todos"
    )
    
    sheets_disponiveis = []
    for arquivo in arquivos_selecionados:
        if arquivo != "Todos":
            sheets_disponiveis.extend(dataframes[arquivo].keys())
        else:
            for all_sheets in dataframes.values():
                sheets_disponiveis.extend(all_sheets.keys())
    sheets_disponiveis = ["Todos"] + sheets_disponiveis
    
    sheets_selecionadas = st.multiselect(
        "Selecione a(s) Sheets para filtrar", 
        options=sheets_disponiveis,
        default="Todos"
    )
    
    anos_selecionados = st.multiselect(
        "Selecione os anos para filtrar", 
        options=anos_para_filtrar, 
        default="Todos"
    )

# Função para contar as linhas de acordo com os filtros
def contar_linhas(df, nomes_selecionados, anos_selecionados):
    if "Todos" not in nomes_selecionados:
        df = df[df['Nome Completo'].isin(nomes_selecionados)]
    if "Todos" not in anos_selecionados:
        df = df[df['Ano'].isin(anos_selecionados)]
    return len(df)

# Contagem das linhas para o gráfico
contagens = {}
for arquivo in arquivos_selecionados:
    if arquivo == "Todos":
        for nome_arquivo, sheets in dataframes.items():
            total_linhas = 0
            for sheet, df in sheets.items():
                total_linhas += contar_linhas(df, nomes_selecionados, anos_selecionados)
            contagens[nome_arquivo] = total_linhas
    else:
        total_linhas = 0
        for sheet, df in dataframes[arquivo].items():
            total_linhas += contar_linhas(df, nomes_selecionados, anos_selecionados)
        contagens[arquivo] = total_linhas

# Exibir o gráfico de pizza
fig = px.pie(
    names=list(contagens.keys()), 
    values=list(contagens.values()), 
    title="Distribuição por Categoria"
)
st.plotly_chart(fig)




