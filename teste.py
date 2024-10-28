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
st.sidebar.header("Menu de Filtragem: ")
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
    nomes_selecionados = st.multiselect("Selecione o(s) Nome(s) para filtrar", options=nomes_para_filtrar)

    arquivos_disponiveis = ["Todos"] + list(excel_files.keys())
    arquivos_selecionados = st.multiselect(
        "Selecione o(s) Arquivo(s) para filtrar",
        options=arquivos_disponiveis
    )

    # Se nenhum arquivo for selecionado, considera como "Todos"
    if not arquivos_selecionados or "Todos" in arquivos_selecionados:
        arquivos_selecionados = list(excel_files.keys())

    sheets_disponiveis = []
    for arquivo in arquivos_selecionados:
        sheets_disponiveis.extend(dataframes[arquivo].keys())

    sheets_disponiveis = ["Todos"] + list(set(sheets_disponiveis))  # Remover duplicatas

    sheets_selecionadas = st.multiselect(
        "Selecione a(s) Sheets para filtrar", 
        options=sheets_disponiveis
    )

    # Se nenhuma sheet for selecionada, considera como "Todos"
    if not sheets_selecionadas or "Todos" in sheets_selecionadas:
        sheets_selecionadas = list(set(sheets_disponiveis[1:]))
    
    anos_selecionados = st.multiselect(
        "Selecione os anos para filtrar", 
        options=anos_para_filtrar
    )

st.subheader("Distribuição por Categoria: ")

# Função para contar as linhas de acordo com os filtros de forma dinâmica
def contar_linhas(df, nomes_selecionados, anos_selecionados):
    # Aplicar filtro de nomes apenas se não for vazio
    if nomes_selecionados:
        df = df[df['Nome Completo'].isin(nomes_selecionados)]
    # Aplicar filtro de anos apenas se não for vazio
    if anos_selecionados:
        df = df[df['Ano'].isin(anos_selecionados)]
    return len(df)

# Inicializar dicionário para contagens e definir arquivos e sheets a contar
arquivos_para_contar = list(excel_files.keys()) if "Todos" in arquivos_selecionados or not arquivos_selecionados else arquivos_selecionados
sheets_para_contar = None if "Todos" in sheets_selecionadas or not sheets_selecionadas else sheets_selecionadas
cores = ['#FF5733', '#33FF57', '#3357FF'] 

contagens = {}
total_contagens = 0  # Para armazenar o total geral

# Realizar contagem com base nos filtros aplicados
for arquivo in arquivos_para_contar:
    total_linhas = 0
    sheets = dataframes[arquivo]
    for sheet, df in sheets.items():
        # Verifica se deve filtrar as sheets ou contar todas
        if not sheets_para_contar or sheet in sheets_para_contar:
            linhas_contadas = contar_linhas(df, nomes_selecionados, anos_selecionados)
            total_linhas += linhas_contadas
            total_contagens += linhas_contadas  # Acumula no total geral
    contagens[arquivo] = total_linhas

# Exibir o gráfico de pizza atualizado
fig = px.pie(
    names=list(contagens.keys()), 
    values=list(contagens.values()),
    color_discrete_sequence=cores
)
st.plotly_chart(fig)

# Exibir o total de linhas no centro do layout
st.markdown(
    f"<h2 style='text-align: center; color: white;'>O Total é: {total_contagens}</h2>",
    unsafe_allow_html=True
)


st.subheader("Total por ANO: ")


# Filtrar os anos selecionados
if "Todos" in anos_selecionados or not anos_selecionados:
    anos_filtrados = ["2021", "2022", "2023", "2024"]
else:
    anos_filtrados = anos_selecionados

# Filtrar os nomes selecionados
if "Todos" in nomes_selecionados or not nomes_selecionados:
    nomes_filtrados = nomes_para_filtrar[1:]  # Exclui "Todos" para contagem real
else:
    nomes_filtrados = nomes_selecionados

# Filtrar os arquivos selecionados
if "Todos" in arquivos_selecionados or not arquivos_selecionados:
    arquivos_filtrados = list(dataframes.keys())
else:
    arquivos_filtrados = arquivos_selecionados

# Filtrar as sheets selecionadas
sheets_filtradas = []
if "Todos" in sheets_selecionadas or not sheets_selecionadas:
    sheets_filtradas = None  # Marca para incluir todas as sheets dentro dos arquivos filtrados
else:
    sheets_filtradas = sheets_selecionadas

# Contagem de linhas por ano, nome, arquivo e sheet selecionados
contagens_por_ano = {ano: 0 for ano in anos_filtrados}
for arquivo, sheets in dataframes.items():
    if arquivo in arquivos_filtrados:  # Aplica filtro de arquivos
        for sheet, df in sheets.items():
            # Aplica o filtro de sheets, se não for "Todos"
            if sheets_filtradas is None or sheet in sheets_filtradas:
                # Aplica os filtros de ano e nome no DataFrame e conta as linhas correspondentes
                for ano in contagens_por_ano.keys():
                    if "Ano" in df.columns and "Nome Completo" in df.columns:
                        # Filtra o DataFrame usando todos os critérios
                        contagens_por_ano[ano] += len(df[(df['Ano'] == ano) & (df['Nome Completo'].isin(nomes_filtrados))])



# Gráfico de barras atualizado com todos os filtros
fig_bar = px.bar(
    x=list(contagens_por_ano.keys()),
    y=list(contagens_por_ano.values())
)

# Define o eixo x como categórico
fig_bar.update_xaxes(type='category')

# Adiciona os rótulos de dados nas barras
fig_bar.update_traces(text=list(contagens_por_ano.values()), textposition='outside')

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_bar)

# Exibir a tabela da primeira sheet selecionada, se houver
if sheets_selecionadas:
    sheet_selecionada = sheets_selecionadas[0]  # Pega apenas a primeira sheet selecionada
    for arquivo in arquivos_selecionados:
        if sheet_selecionada in dataframes[arquivo]:
            df_sheet = dataframes[arquivo][sheet_selecionada]

            # Aplicar filtros de nome e ano, se selecionados
            if nomes_selecionados and "Todos" not in nomes_selecionados:
                df_sheet = df_sheet[df_sheet['Nome Completo'].isin(nomes_selecionados)]
            if anos_selecionados and "Todos" not in anos_selecionados:
                df_sheet = df_sheet[df_sheet['Ano'].isin(anos_selecionados)]

            # Ordenar pela coluna "Ano" se ela estiver presente
            if 'Ano' in df_sheet.columns:
                df_sheet = df_sheet.sort_values(by='Ano', ascending=True)

            # Exibir a tabela no Streamlit com barra de rolagem
            st.subheader(f"Tabela de Dados: {sheet_selecionada} - {arquivo}")

            # Gerar HTML da tabela e aplicar estilo
            tabela_html = df_sheet.to_html(index=False)  # Converte DataFrame para HTML sem índice
            st.markdown(
                f"""
                <div style="overflow-x: auto;">
                    {tabela_html}
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.subheader("Nenhuma sheet selecionada para exibir")












