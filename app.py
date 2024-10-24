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
        background-color: #1a1a1a; /* Cor de fundo da div específica */
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

# Carregar todos os DataFrames de todas as sheets
# Carregar os DataFrames de cada arquivo e sheet
# Carregar os DataFrames de cada arquivo e sheet
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
    nomes_selecionados = st.multiselect("Selecione o(s) Nome(s) para filtrar", options=nomes_para_filtrar)

    arquivos_disponiveis = ["Todos"] + list(excel_files.keys())
    arquivos_selecionados = st.multiselect(
        "Selecione o(s) Arquivo(s) para filtrar",
        options=arquivos_disponiveis
        #default=list(excel_files.keys())  # Seleciona todos por padrão
    )
    
    # Filtro de sheets com base nos arquivos selecionados
    sheets_disponiveis = []
    for arquivo in arquivos_selecionados:
        sheets_disponiveis.extend(dataframes[arquivo].keys())
    sheets_disponiveis = ["Todos"] + sheets_disponiveis  # Adiciona a opção "Todos" no início
    
    sheets_selecionadas = st.multiselect(
        "Selecione a(s) Sheets para filtrar", 
        options=sheets_disponiveis
    )
    
    anos_selecionados = st.multiselect(
        "Selecione os anos para filtrar", 
        options=anos_para_filtrar, 
        default="Todos"
    )

# Filtrar os DataFrames com base nos nomes, arquivos, anos e sheets selecionados
dados_filtrados = {}
for file_name, sheets in dataframes.items():
    if file_name in arquivos_selecionados:  # Filtra pelos arquivos selecionados
        dados_filtrados[file_name] = {}
        for sheet_name, df in sheets.items():
            # Verifica se a opção "Todos" está selecionada ou se a sheet está na lista de selecionadas
            if "Todos" in sheets_selecionadas or sheet_name in sheets_selecionadas:
                # Filtrar pelo nome
                if nomes_selecionados and "Todos" not in nomes_selecionados:
                    df = df[df['Nome Completo'].isin(nomes_selecionados)]
                
                # Filtrar pelo ano
                if 'Ano' in df.columns and anos_selecionados and "Todos" not in anos_selecionados:
                    df = df[df['Ano'].isin(anos_selecionados)]
                
                dados_filtrados[file_name][sheet_name] = df














