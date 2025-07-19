import streamlit as st
import pandas as pd
st.set_page_config(page_title="Finanças", layout="wide", page_icon="🍀")

st.markdown("""
 # Boas Vindas!
 ### Este é um exemplo de aplicação Streamlit para gerenciar finanças pessoais.

 """)

# Widget de upload de arquivo
uploaded_file = st.file_uploader("Faça upload do seu arquivo financeiro", type=["csv", "xlsx"])

# Verifica se um arquivo foi enviado
if uploaded_file is not None:
    
    # Lê o arquivo enviado
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df["Data"] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date

    # Exibe o conteúdo do Data  Frame
    exp1 = st.expander("Ver Dados Brutos")
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    # Exibe Instituições
    exp2 = st.expander("Ver Instituições")
    df_instituicoes = df.pivot_table(index='Data', columns='Instituição', values='Valor', aggfunc='sum')

    # Cria abas para exibir os dados
    tab_data, tab_history, tab_share = exp2.tabs(["Data", "history", "Share "])

    # Formata o índice do DataFrame    
    with tab_data:
        st.dataframe(df_instituicoes)
    
    # Exibe o histórico de transações
    with tab_history:
        st.line_chart(df_instituicoes, use_container_width=True)

    # Exibe o distribuição  de dados
    with tab_share:

      date = st.selectbox("Selecione uma data", options=df_instituicoes.index)

      # Obtem a última data de dados
      last_date = df_instituicoes.loc[date]
      # Exibe o gráfico de barras para a data selecionada
      st.bar_chart(last_date)