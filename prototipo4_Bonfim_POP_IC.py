import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados da planilha
file_path = "dados_agrupados_unido.xlsx"
df = pd.read_excel(file_path)

# Converter colunas de decimal para porcentagem
colunas_percentuais = ["PROP_LIXO/DOM", "PROP_SANEAMENTO/DOM", "PROP_AGUA/DOM"]
for coluna in colunas_percentuais:
    if coluna in df.columns:
        df[coluna] = df[coluna] * 100
        df[coluna] = df[coluna].map(lambda x: f"{x:.2f}%")

# Arredondar colunas específicas
if "GRAU_ENVELHECIMENTO" in df.columns:
    df["GRAU_ENVELHECIMENTO"] = df["GRAU_ENVELHECIMENTO"].round().astype(int)

if "DENSIDADE" in df.columns:
    df["DENSIDADE"] = df["DENSIDADE"].round().astype(int)

dom_pizza_cols = ["DOM_1_MORADOR", "DOM_2_4_MORADORES", "DOM_5_6_MORADORES", "DOM_ACIMA_7_MORADORES"]
resp_renda_cols = [ 'RESP_RENDA_0_2_SM', 'RESP_RENDA_2_5_SM', 'RESP_RENDA_5_10_SM', 'RESP_RENDA_10_20_SM', 'RESP_RENDA_20_MAIS_SM', 'RESP_SEM_RENDIMENTO']

# Título do aplicativo
st.title("📊 Dados dos Bairros")

# Filtro para selecionar o bairro
bairro_selecionado = "Bonfim"
df_bairro_selecionado = df[df["NOME_BAIRRO"] == bairro_selecionado]

# Função para formatar os rótulos das colunas
def formatar_rotulo(rotulo):
    return " ".join(palavra.capitalize() for palavra in rotulo.split("_"))

# Menu na barra lateral para navegação entre páginas
page = "População"

# Função para a página 1
def page_1():
    
    # Barra lateral para selecionar gráficos
    st.sidebar.header("🔽 Selecione os gráficos")
    mostrar_pop_total = st.sidebar.checkbox("População por sexo", True)
    mostrar_pop_total_bairro = st.sidebar.checkbox("População por bairros", True)
    mostrar_faixa_etaria = st.sidebar.checkbox("População por grupos de idade", True)
    mostrar_grau = st.sidebar.checkbox("Grau de envelhecimento", True)
    mostrar_cor = st.sidebar.checkbox("População por cor/raça", True)
    mostrar_densidade = st.sidebar.checkbox("Densidade demográfica", True)
    mostrar_analfabetismo = st.sidebar.checkbox("População não alfabetizada", True)
    
    # Exibir gráficos conforme seleção do usuário
    if mostrar_pop_total:
        valores_bairro = {
            "Homens": df_bairro_selecionado["POP_TOTAL_HOMEM"].iloc[0],
            "Mulheres": df_bairro_selecionado["POP_TOTAL_MULHER"].iloc[0]
        }
        
        st.write("### 📊 Distribuição percentual da população residente, por sexo, segundo os bairros de Salvador, 2010")
        st.write(f"##### {bairro_selecionado}")
        
        fig_pizza = px.pie(
            names=list(valores_bairro.keys()), 
            values=list(valores_bairro.values()),
            color=list(valores_bairro.keys()),  # Define as cores por categoria
            color_discrete_map={"Homens": "blue", "Mulheres": "pink"}  # Mapeia cores específicas
        )
        
        st.plotly_chart(fig_pizza)

        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_pop_total_bairro:
        st.write('### 📊 População residente segundo os bairros de Salvador, 2010')
        
        #Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")

        #Filtro de ordenação
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao_pop = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Residente (Crescente)": ("POP_TOTAL_RESIDENTE", True),
            "Residente (Decrescente)": ("POP_TOTAL_RESIDENTE", False),
        }   

        criterio_ordenacao_pop = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao_pop.keys()))

        #Aplicar ordenação ao DataFrame
        coluna_ordenacao_pop, ordem_crescente = opcoes_ordenacao_pop[criterio_ordenacao_pop]
        df_ordenado = df.sort_values(by=coluna_ordenacao_pop, ascending=ordem_crescente)

        #Ordenar os dados para manter a ordem original dos bairros
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()

        fig_pop_total = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="POP_TOTAL_RESIDENTE", 
            labels={'POP_TOTAL_RESIDENTE': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        #Remover a legenda
        fig_pop_total.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")

        st.plotly_chart(fig_pop_total)

        pop_total_bairro = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
        pop_total_geral = df["POP_TOTAL_RESIDENTE"].sum()
        percentual_bairro = (pop_total_bairro / pop_total_geral) * 100

        st.markdown(f"📌 **Nota:** A população residente deste bairro representa {percentual_bairro:.2f}% da população de Salvador.")

        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")
    
    if mostrar_faixa_etaria:
        idade_cols = [col for col in df.columns if "IDADE_" in col]
        if idade_cols:
            
            faixa_etaria = {
            "Entre 0 a 6 Anos": df_bairro_selecionado["IDADE_0_6_ANOS"].iloc[0],
            "Entre 7 a 14 Anos": df_bairro_selecionado["IDADE_7_14_ANOS"].iloc[0],
            "Entre 15 a 18 Anos": df_bairro_selecionado["IDADE_15_18_ANOS"].iloc[0],
            "Entre 19 a 24 Anos": df_bairro_selecionado["IDADE_19_24_ANOS"].iloc[0],
            "Entre 25 a 49 Anos": df_bairro_selecionado["IDADE_25_49_ANOS"].iloc[0],
            "Entre 50 a 64 Anos": df_bairro_selecionado["IDADE_50_64_ANOS"].iloc[0],
            "Entre 65 ou mais Anos": df_bairro_selecionado["IDADE_65_MAIS"].iloc[0],
            }
            
            st.write("### 📊 Distribuição da população residente, por grupos de idade, segundo os bairros de Salvador, 2010")
            st.write(f"##### {bairro_selecionado}")
            
            fig_barras = px.bar(
                x=list(faixa_etaria.keys()), 
                y=list(faixa_etaria.values()),
                labels= {"x" : "Grupos de idade", 'y' : ' '},
                text_auto=True
            )

            # Posicionar os números acima das colunas
            fig_barras.update_traces(textposition="outside")

            #Remover a legenda, e editar o grafico
            fig_barras.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
            
            st.plotly_chart(fig_barras)

            #Espaçamento entre os graficos
            st.write(" ")
            st.write(" ")
            st.write(" ")

    if mostrar_grau:
            
        st.write('### 📊 Grau de envelhecimento da população residente segundo os bairros de Salvador, 2010')
            
        #Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")

        #Filtro de ordenação
        st.write("##### 🔽 Ordenação dos Dados")
        
        opcoes_ordenacao_grau = {
           "Alfabética": ("NOME_BAIRRO", True),
           "Salvador (Crescente)": ('GRAU_ENVELHECIMENTO', True),
            "Salvador (Decrescente)": ('GRAU_ENVELHECIMENTO', False),
        }   

        criterio_ordenacao_grau = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao_grau.keys()))

        #Aplicar ordenação ao DataFrame
        coluna_ordenacao_grau, ordem_crescente = opcoes_ordenacao_grau[criterio_ordenacao_grau]
        df_ordenado = df.sort_values(by=coluna_ordenacao_grau, ascending=ordem_crescente)

        #Ordenar os dados para manter a ordem original dos bairros
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()

        fig_grau = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y='GRAU_ENVELHECIMENTO', 
            labels={'GRAU_ENVELHECIMENTO': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        #Remover a legenda
        fig_grau.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")

        st.plotly_chart(fig_grau)

        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_cor:
        cor_cols = [col for col in df.columns if "COR_" in col]
        if cor_cols:

            cor_values = {
            "Parda": df_bairro_selecionado["COR_PARDA"].iloc[0],
            "Preta": df_bairro_selecionado["COR_PRETA"].iloc[0],
            "Branca": df_bairro_selecionado["COR_BRANCA"].iloc[0],
            "Amarela": df_bairro_selecionado["COR_AMARELA"].iloc[0],
            "Indigena": df_bairro_selecionado["COR_INDIGENA"].iloc[0],
            }
            
            st.write(f'### 📊 Distribuição percentual da população residente, por cor/raça, segundo os bairros de Salvador, 2010')
            st.write(f'##### {bairro_selecionado}')
            
            fig_cor = px.pie(
                names=list(cor_values.keys()), 
                values=list(cor_values.values()),
                color=list(cor_values.keys()),  # Define as cores por categoria
                color_discrete_map={"Parda": "brown", "Preta": "black", "Branca": "off-white", 'Amarela': 'yellow', 'Indigena': 'Green'}  # Mapeia cores específicas
                )
            
            st.plotly_chart(fig_cor)
            
            #Espaçamento entre os graficos
            st.write(" ")
            st.write(" ")
            st.write(" ")

    # Exibir gráficos conforme seleção do usuário
    if mostrar_densidade:
        # Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        
        st.write('### 📊 Densidade demográfica segundo os bairros de Salvador, 2010')

        # Filtro de ordenação
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Densidade (Crescente)": ("DENSIDADE", True),
            "Densidade (Decrescente)": ("DENSIDADE", False),
        }   

        criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))

        # Aplicar ordenação ao DataFrame
        coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
        df_ordenado = df.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)

        # Ordenar os dados para manter a ordem original dos bairros
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()

        fig_densidade = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="DENSIDADE", 
            labels={'DENSIDADE': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        # Remover a legenda
        fig_densidade.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")

        st.plotly_chart(fig_densidade)

        st.markdown("📌 **Nota:** Densidade demográfica - Habitantes/Km²")
        
        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")

    # Exibir gráficos conforme seleção do usuário
    if mostrar_analfabetismo:
        # Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        
        st.write('### 📊 População residente acima de 15 anos não alfabetizada segundo os bairros de Salvador, 2010')
    
        # Filtro de ordenação
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Taxa de Analfabetismo (Crescente)": ("EDUC_ANALFABETISMO", True),
            "Taxa de Analfabetismo (Decrescente)": ("EDUC_ANALFABETISMO", False),
        }

        criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))

        # Aplicar ordenação ao DataFrame
        coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
        df_ordenado = df.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)

        # Ordenar os dados para manter a ordem original dos bairros
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()

        fig_analfabetismo = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="EDUC_ANALFABETISMO", 
            labels={'EDUC_ANALFABETISMO': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        # Remover a legenda
        fig_analfabetismo.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")

        st.plotly_chart(fig_analfabetismo)

if page == "População":
    page_1()
