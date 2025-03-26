import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados da planilha
file_path = "dados_agrupadosV2.xlsx"
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
st.title("📊 Projeto de Disponibilidade de Dados")

# Filtro para selecionar o bairro
bairro_selecionado = st.selectbox("Selecione o Bairro", df["NOME_BAIRRO"].unique())
df_bairro_selecionado = df[df["NOME_BAIRRO"] == bairro_selecionado]

# Função para formatar os rótulos das colunas
def formatar_rotulo(rotulo):
    return " ".join(palavra.capitalize() for palavra in rotulo.split("_"))

# Função para a página 1
def page_1():
    
    # Barra lateral para selecionar gráficos
    st.sidebar.header("🔽 Selecione os Gráficos")
    mostrar_pop_total = st.sidebar.checkbox("Homens x Mulheres", True)
    mostrar_faixa_etaria = st.sidebar.checkbox("Gráfico de Faixa Etária", True)
    mostrar_cor = st.sidebar.checkbox("Gráfico de Cor", True)
    mostrar_densidade = st.sidebar.checkbox("Densidade Populacional", True)
    mostrar_analfabetismo = st.sidebar.checkbox("Taxa de Analfabetismo", True)
    
    # Exibir gráficos conforme seleção do usuário
    if mostrar_pop_total:
        valores_bairro = {
            "Homens": df_bairro_selecionado["POP_TOTAL_HOMEM"].iloc[0],
            "Mulheres": df_bairro_selecionado["POP_TOTAL_MULHER"].iloc[0]
            }
        
        st.write(f"### 📊Percentual da População total residente, por sexo, segundo os bairros do município de Salvador, 2010 : {bairro_selecionado}")
        
        fig_pizza = px.pie(
            names=list(valores_bairro.keys()), 
            values=list(valores_bairro.values()),
            )
        
        st.plotly_chart(fig_pizza)
    
        pop_total_bairro = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
        pop_total_geral = df["POP_TOTAL_RESIDENTE"].sum()
        percentual_bairro = (pop_total_bairro / pop_total_geral) * 100
    
        st.write(f"### População Total de Residentes no Bairro {bairro_selecionado}: {pop_total_bairro}")
        st.write(f"### O bairro {bairro_selecionado} representa {percentual_bairro:.2f}% da população total.")

    if mostrar_faixa_etaria:
        idade_cols = [col for col in df.columns if "IDADE_" in col]
        if idade_cols:
            
            faixa_etaria = {
            "Entre 0 a 6 Anos": df_bairro_selecionado["IDADE_0_6_ANOS"].iloc[0],
            "Entre 17 a 14 Anos": df_bairro_selecionado["IDADE_7_14_ANOS"].iloc[0],
            "Entre 15 a 18 Anos": df_bairro_selecionado["IDADE_15_18_ANOS"].iloc[0],
            "Entre 19 a 24 Anos": df_bairro_selecionado["IDADE_19_24_ANOS"].iloc[0],
            "Entre 25 a 49 Anos": df_bairro_selecionado["IDADE_25_49_ANOS"].iloc[0],
            "Entre 50 a 64 Anos": df_bairro_selecionado["IDADE_50_64_ANOS"].iloc[0],
            "Entre 65 ou mais Anos": df_bairro_selecionado["IDADE_65_MAIS"].iloc[0],
            }
            
            st.write(f"### 📊População total residente por faixas etárias segundo os bairros do município de Salvador, 2010 : {bairro_selecionado}")
            
            fig_barras = px.bar(
                x=list(faixa_etaria.keys()), 
                y=list(faixa_etaria.values()),
                labels= {"x" : "Idades", 'y' : 'População'},
                text_auto=True)
            
            st.plotly_chart(fig_barras)
            st.write(f"### Grau de Envelhecimento no Bairro {bairro_selecionado}: {df_bairro_selecionado['GRAU_ENVELHECIMENTO'].iloc[0]}")

    if mostrar_cor:
        cor_cols = [col for col in df.columns if "COR_" in col]
        if cor_cols:
            
            st.write(f'### 📊Percentual da população total residente por cor/raça segundo os bairros do município de Salvador, 2010 :  {bairro_selecionado}')
            
            cor_values = {formatar_rotulo(col): df_bairro_selecionado[col].iloc[0] for col in cor_cols}
            fig_cor = px.pie(
                names=list(cor_values.keys()), 
                values=list(cor_values.values()), 
                )
            
            st.plotly_chart(fig_cor)

    # Exibir gráficos conforme seleção do usuário
    if mostrar_densidade:
        # Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        
        st.write('### 📊Densidade demográfica, segundo os bairros do município de Salvador, 2010')

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
            labels={'DENSIDADE': 'Densidade Populacional', 'NOME_BAIRRO' : 'Bairro de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        # Remover a legenda
        fig_densidade.update_layout(showlegend=False)

        st.plotly_chart(fig_densidade)

    # Exibir gráficos conforme seleção do usuário
    if mostrar_analfabetismo:
        # Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        
        st.write('### 📊População total residente acima de 15 anos, não alfabetizada, por sexo, segundo os bairros do município de Salvador, 2010')
    
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
            labels={'EDUC_ANALFABETISMO': 'Taxa de Analfabetismo', 'NOME_BAIRRO' : 'Bairro de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        # Remover a legenda
        fig_analfabetismo.update_layout(showlegend=False)

        st.plotly_chart(fig_analfabetismo)

# Função para a página 2
def page_2():
    # Barra lateral para selecionar gráficos
    st.sidebar.header("🔽 Selecione os Gráficos")
    mostrar_domicilios = st.sidebar.checkbox("Gráfico de Domicílios", True)
    mostrar_moradores  = st.sidebar.checkbox("Gráfico de Moradores", True)
    mostrar_proporcao = st.sidebar.checkbox("Gráfico de Proporções", True)
    mostrar_resp = st.sidebar.checkbox("Responsaveis dos Domicilio", True)
    mostrar_renda_sexo = st.sidebar.checkbox("Renda de Homens e Mulheres", True)
    mostrar_salario = st.sidebar.checkbox("Renda dos Responsaveis dos Domicilios", True)
    mostrar_renda = st.sidebar.checkbox("Média de Renda", True)

    if mostrar_domicilios:
        dom_cols = [col for col in df.columns if "DOM_" in col]

        if dom_cols:
            
            dom_values = {
            "Domicilios de Casa": df_bairro_selecionado["DOM_PART_PERM_CASA"].iloc[0],
            "Domicilios de Casa em Vilas": df_bairro_selecionado["DOM_PART_PERM_CASA_VILA"].iloc[0],
            "Domicilios em Apartamentos": df_bairro_selecionado["DOM_PART_PERM_CASA_APART"].iloc[0],
            }
            
            st.write(f'### 📊Total de domicílios particulares permanentes por tipo de infraestrutura urbana, segundo os bairros do município de Salvador, 2010: {bairro_selecionado}')
            
            fig_dom = px.bar(
                x=list(dom_values.keys()), 
                y=list(dom_values.values()),
                labels= {"x" : "Domicilios", 'y' : 'Quantidade'},
                )
            st.plotly_chart(fig_dom)
            
            dom_totais = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
    
            st.write(f"### Total de Domicilios no Bairro {bairro_selecionado}: {dom_totais}")
    
    if mostrar_moradores:
        
        dom_pizza_values = {
        "Domicilios com 1 Morador": df_bairro_selecionado["DOM_1_MORADOR"].iloc[0],
        "Domicilios com 2 a 4 Moradores": df_bairro_selecionado["DOM_2_4_MORADORES"].iloc[0],
        "Domicilios com 5 a 6 Moradores ": df_bairro_selecionado["DOM_5_6_MORADORES"].iloc[0],
        "Domicilios com 7 ou mais Moradores": df_bairro_selecionado["DOM_ACIMA_7_MORADORES"].iloc[0],
        }
        
        st.write(f'### 📊Distribuição de Moradores por Domicílio: {bairro_selecionado}')
            
        fig_dom_pizza = px.pie(
            names=list(dom_pizza_values.keys()), 
            values=list(dom_pizza_values.values()),
            category_orders={"names": [
             "Domicilios com 1 Morador",
             "Domicilios com 2 a 4 Moradores",
             "Domicilios com 5 a 6 Moradores",
             "Domicilios com 7 ou mais Moradores"
            ]}
        )
        st.plotly_chart(fig_dom_pizza)

    if mostrar_proporcao:
        prop_cols = [col for col in df.columns if "PROP_" in col]
        if prop_cols:
            
            prop_values = {
            "Lixo por Domicilio": df_bairro_selecionado["PROP_LIXO/DOM"].iloc[0],
            "Saneamento por Domicilio": df_bairro_selecionado["PROP_SANEAMENTO/DOM"].iloc[0],
            "Água por Domicilio": df_bairro_selecionado["PROP_AGUA/DOM"].iloc[0],
            }
                     
            st.write(f'### 📊Percentual de domicílios particulares permanentes por tipo de infraestrutura urbana, segundo os bairros do município de Salvador, 2010: {bairro_selecionado}')
            
            fig_prop = px.bar(
                x=list(prop_values.keys()), 
                y=list(prop_values.values()),
                labels={'x' : 'Proporção', 'y' : 'Porcentagem (%)'}
                )
            st.plotly_chart(fig_prop)
    
    if mostrar_resp:        
        # Verificar se as colunas existem antes de criar o gráfico
        if all(col in df.columns for col in ["RESP_MULHER", "RESP_IDOSOS", "RESP_TOTAL"]):
            # Filtrar os dados apenas para o bairro selecionado
            df_bairro = df[df["NOME_BAIRRO"] == bairro_selecionado]
            
            st.write(f'### 📊Distribuição de Responsáveis pelo Domicílio: {bairro_selecionado}')

            # Calcular a nova variável RESP_HOMEM_JOVEM
            resp_mulher = df_bairro["RESP_MULHER"].values[0]
            resp_idosos = df_bairro["RESP_IDOSOS"].values[0]
            resp_total = df_bairro["RESP_TOTAL"].values[0]
            resp_homem_jovem = resp_total - (resp_mulher + resp_idosos)

            # Criar um DataFrame para o gráfico de pizza
            df_pizza = pd.DataFrame({
                "Categoria": [
                    "Mulheres Responsáveis pelo Domicílio", 
                    "Idosos Responsáveis pelo Domicílio", 
                    "Homens Jovens Responsáveis pelo Domicílio"
                ],
                "Quantidade": [resp_mulher, resp_idosos, resp_homem_jovem]
            })

            # Criar gráfico de pizza
            fig_pizza = px.pie(
                df_pizza, 
                names="Categoria", 
                values="Quantidade", 
                color="Categoria",
                color_discrete_map={
                    "Mulheres Responsáveis pelo Domicílio": "pink",
                    "Idosos Responsáveis pelo Domicílio": "gray",
                    "Homens Jovens Responsáveis pelo Domicílio": "blue"
                }
            )

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig_pizza)

    if mostrar_renda_sexo:
        # Verificar se as colunas existem antes de criar o gráfico
        if "RESP_RENDA_MEDIA_HOMEM" in df.columns and "RESP_RENDA_MEDIA_MULHER" in df.columns:
            # Filtrar os dados apenas para o bairro selecionado
            df_bairro = df[df["NOME_BAIRRO"] == bairro_selecionado]
            
            st.write(f"### 📊 Renda Média por Gênero no Bairro: {bairro_selecionado}")

            # Criar um DataFrame para o gráfico
            df_renda_genero = pd.DataFrame({
                "Gênero": ["Homens", "Mulheres"],
                "Renda Média": [df_bairro["RESP_RENDA_MEDIA_HOMEM"].values[0], df_bairro["RESP_RENDA_MEDIA_MULHER"].values[0]]
            })

            # Criar gráfico de barras
            fig_renda_genero = px.bar(
                df_renda_genero, 
                x="Gênero", 
                y="Renda Média", 
                labels={"Renda Média": "Renda Média (R$)"},
                color="Gênero", 
                color_discrete_map={"Homens": "blue", "Mulheres": "pink"}
            )

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig_renda_genero)
    
    if mostrar_salario:
                
        resp_pizza_values = {
        "0 a 2 Salarios Minimos": df_bairro_selecionado["RESP_RENDA_0_2_SM"].iloc[0],
        "2 a 5 Salarios Minimos": df_bairro_selecionado["RESP_RENDA_2_5_SM"].iloc[0],
        "5 a 10 Salarios Minimos": df_bairro_selecionado["RESP_RENDA_5_10_SM"].iloc[0],
        "10 a 20 Salarios Minimos": df_bairro_selecionado["RESP_RENDA_10_20_SM"].iloc[0],
        "20 ou mais Salarios Minimos": df_bairro_selecionado["RESP_RENDA_20_MAIS_SM"].iloc[0],
        "Sem Rendimento": df_bairro_selecionado["RESP_SEM_RENDIMENTO"].iloc[0],
        }
        
        #RESP_RENDA_0_2_SM	RESP_RENDA_2_5_SM	RESP_RENDA_5_10_SM	RESP_RENDA_10_20_SM	RESP_RENDA_20_MAIS_SM	RESP_SEM_RENDIMENTO
        
        st.write(f'### 📊Renda dos Resposaveis dos Domicilios em Salarios Minimos: {bairro_selecionado}')
        
        fig_resp_pizza = px.pie(
            names=list(resp_pizza_values.keys()),
            values=list(resp_pizza_values.values()),
            category_orders={"names": [
             "0 a 2 Salarios Minimos",
             "2 a 5 Salarios Minimos",
             "5 a 10 Salarios Minimos",
             "10 a 20 Salarios Minimos",
             "20 ou mais Salarios Minimos",
             'Sem Rendimento',
            ]}
        )
            
        st.plotly_chart(fig_resp_pizza)
            
        resp_total_bairro = df_bairro_selecionado["RESP_TOTAL"].iloc[0]
        st.write(f"### População Total de Responsaveis no Bairro {bairro_selecionado}: {resp_total_bairro}")
    
    if mostrar_renda:
        # Exibir gráficos conforme seleção do usuário
        # Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        
        st.write('### 📊Rendimento médio dos responsáveis por domicílios particulares permanentes, segundo os bairros do município de Salvador, 2010')
    
        # Filtro de ordenação
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Renda Média (Crescente)": ("RESP_RENDA_MEDIA", True),
            "Renda Média (Decrescente)": ("RESP_RENDA_MEDIA", False),
        }

        criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))

        # Aplicar ordenação ao DataFrame
        coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
        df_ordenado = df.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)

        # Ordenar os dados para manter a ordem original dos bairros
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()

        fig_renda = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="RESP_RENDA_MEDIA", 
            labels={'RESP_RENDA_MEDIA': 'Média de Renda (R$)', 'NOME_BAIRRO' : 'Bairro de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        # Remover a legenda
        fig_renda.update_layout(showlegend=False)
        
        st.plotly_chart(fig_renda)
        
# Menu na barra lateral para navegação entre páginas
page = st.sidebar.radio("Escolha a página", ["Graficos de População", "Graficos de Domicilios"])

if page == "Graficos de População":
    page_1()
elif page == "Graficos de Domicilios":
    page_2()
