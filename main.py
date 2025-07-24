# main.py
# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd

# Configurações do Streamlit
def calc_general_stats(df: pd.DataFrame):
    df_data = df.groupby(by="Data")[["Valor"]].sum()
    df_data["lag1"] = df_data["Valor"].shift(1)
    df_data["Diferença Mensal"] = df_data["Valor"] - df_data["lag1"]
    df_data["Média 6M Diferença Mensal"] = df_data["Diferença Mensal"].rolling(window=6).mean()
    df_data["Média 12M Diferença Mensal"] = df_data["Valor"].rolling(window=12).mean()
    df_data["Média 24M Diferença Mensal"] = df_data["Valor"].rolling(window=24).mean()
    df_data["Diferença Mensal Relativa"] = df_data["Valor"] / df_data["lag1"] - 1
    df_data["Evolução em 6M Total"] = df_data["Valor"].rolling(6).apply(lambda x: (x[-1] - x[0]))
    df_data["Evolução em 6M Relativa"] = df_data["Valor"].rolling(6).apply(lambda x: (x[-1] / x[0])-1)
    df_data["Evolução em 12M Total"] = df_data["Valor"].rolling(12).apply(lambda x: (x[-1] - x[0]))
    df_data["Evolução em 12M Relativa"] = df_data["Valor"].rolling(12).apply(lambda x: (x[-1] / x[0])-1)
    df_data["Evolução em 24M Total"] = df_data["Valor"].rolling(24).apply(lambda x: (x[-1] - x[0]))
    df_data["Evolução em 24M Relativa"] = df_data["Valor"].rolling(24).apply(lambda x: (x[-1] / x[0])-1)

    df_data = df_data.drop(columns=["lag1"])

    return df_data



# Configuração da página
st.set_page_config(page_title="Finanças", layout="wide", page_icon="🍀")

# Título da aplicação
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
        df = pd.read_csv(uploaded_file, encoding='latin1')
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

    # Calcula as estatísticas gerais
    exp3 = st.expander("Ver Estatísticas Gerais")

    df_stats = calc_general_stats(df)

    # Formata o DataFrame de estatísticas gerais
    columns_config = {
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "Diferença Mensal": st.column_config.NumberColumn("Diferença Mensal", format="R$ %.2f"),
        "Média 6M Diferença Mensal": st.column_config.NumberColumn("Média 6M Diferença Mensal", format="R$ %.2f"),
        "Média 12M Diferença Mensal": st.column_config.NumberColumn("Média 12M Diferença Mensal", format="R$ %.2f"),
        "Média 24M Diferença Mensal": st.column_config.NumberColumn("Média 24M Diferença Mensal", format="R$ %.2f"),
        "Evolução em 6M Total": st.column_config.NumberColumn("Evolução em 6M Total", format="R$ %.2f"),
        "Evolução em 6M Relativa": st.column_config.NumberColumn("Evolução em 6M Relativa", format="percent"),
        "Evolução em 12M Total": st.column_config.NumberColumn("Evolução em 12M Total", format="R$ %.2f"),
        "Evolução em 12M Relativa": st.column_config.NumberColumn("Evolução em 12M Relativa", format="percent"),
        "Evolução em 24M Total": st.column_config.NumberColumn("Evolução em 24M Total", format="R$ %.2f"),
        "Evolução em 24M Relativa": st.column_config.NumberColumn("Evolução em 24M Relativa", format="percent"),
        "Diferença Mensal Relativa": st.column_config.NumberColumn("Diferença Mensal Relativa", format="percent"),
    }

    # Cria abas para exibir as estatísticas gerais
    tab_stats, tabs_abs, tabs_rel = exp3.tabs(tabs=["Dados", "Histórico de Evolução", "Crescimento Relativo"])

    # Exibe o DataFrame de estatísticas gerais
    with tab_stats:
        st.dataframe(df_stats, column_config=columns_config, use_container_width=True)

    # Exibe o gráfico de evolução mensal
    with tabs_abs:
        abs_cols = [
            "Diferença Mensal", 
            "Média 6M Diferença Mensal",
            "Média 12M Diferença Mensal", 
            "Média 24M Diferença Mensal",
        ]
        st.line_chart(data=df_stats[abs_cols])

    # Exibe o gráfico de crescimento relativo
    with tabs_rel:
        rel_cols = [
            "Diferença Mensal Relativa",
            "Evolução em 6M Relativa",
            "Evolução em 12M Relativa",
            "Evolução em 24M Relativa",
        ]
        st.line_chart(data=df_stats[rel_cols])
    
    # Exibe o DataFrame de estatísticas gerais
    #exp3.dataframe(df_stats, column_config=columns_config, use_container_width=True)

    # Cria um expander para metas
    with st.expander("Metas"):

        # Cria colunas para os widgets de entrada
        col1, col2 = st.columns(2)

        # Widget para entrada de nome da meta
        data_inicio_meta = col1.date_input("Data de Início da Meta",  max_value=df_stats.index.max())
        # Filtra o DataFrame de estatísticas gerais para obter o valor inicial da meta
        data_filtered = df_stats.index[df_stats.index <= data_inicio_meta][-1]
        
        # Widget para entrada do nome da meta
        custos_fixo = col1.number_input("Custos Fixos", min_value=0.0, format="%.2f", key="custos_fixo")

        # Widget para entrada do nome da meta
        salario_bruto = col2.number_input("Salário Bruto", min_value=0.0, format="%.2f", key="salario_bruto")
        salario_liquido = col2.number_input("Salário Líquido", min_value=0.0, format="%.2f", key="salario_liquido")
       
         
        # Obtém o valor inicial da meta
        valor_inicio = df_stats.loc[data_filtered]["Valor"]
        col1.markdown(f"**Patrimônio no Início da Meta:** R$ {valor_inicio:.2f}")

        # Exibe o valor inicial da meta
        col1_pot, col2_pot = st.columns(2)
        mensal = salario_liquido - custos_fixo
        anual = mensal * 12

        # Exibe o potencial de arrecadação mensal
        with col1_pot.container(border=True):
            st.markdown(f"""**Potencial Arrecadação Mensal**:\n\n R$ {mensal:.2f}""")

        # Exibe o potencial de arrecadação anual
        with col2_pot.container(border=True):    
            st.markdown(f"""**Potencial Arrecadação Anual**:\n\n R$ {anual:.2f}""")

        # Exibe o patrimônio final estimado
        with st.container(border=True):
            col1_meta, col2meta = st.columns(2)
            with col1_meta:
                meta_estipulda = st.number_input("Meta Estipulada", min_value=-9999999.0, format="%.2f", value=anual)

            with col2meta:
                patrimonio_final = meta_estipulda + valor_inicio
                st.markdown(f"**Patrimônio Final Estimado:**\n\n R$ {patrimonio_final:.2f}")


    