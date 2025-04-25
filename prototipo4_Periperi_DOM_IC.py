import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados da planilha
file_path = "prototipo_4\\dados_agrupados_unido.xlsx"
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
bairro_selecionado = "Periperi"
df_bairro_selecionado = df[df["NOME_BAIRRO"] == bairro_selecionado]

# Função para formatar os rótulos das colunas
def formatar_rotulo(rotulo):
    return " ".join(palavra.capitalize() for palavra in rotulo.split("_"))

# Menu na barra lateral para navegação entre páginas
page = "Domicílios"

# Função para a página 2
def page_2():
    # Barra lateral para selecionar gráficos
    st.sidebar.header("🔽 Selecione os gráficos")
    mostrar_domicilios = st.sidebar.checkbox("Domicílios por tipo", True)
    mostrar_moradores  = st.sidebar.checkbox("Domicílios por número de moradores", True)
    mostrar_proporcao = st.sidebar.checkbox("Domicílios por tipo de infraestrutura urbana", True)
    #mostrar_resp = st.sidebar.checkbox("Responsaveis dos Domicílio", True)
    mostrar_renda_sexo = st.sidebar.checkbox("Rendimento médio dos responsáveis por sexo", True)
    mostrar_salario = st.sidebar.checkbox("Rendimento em salários mínimos dos responsáveis", True)
    mostrar_renda = st.sidebar.checkbox("Rendimento médio dos responsáveis", True)

    if mostrar_domicilios:
        dom_cols = [col for col in df.columns if "DOM_" in col]

        if dom_cols:
            
            dom_values = {
                "Casa": df_bairro_selecionado["DOM_PART_PERM_CASA"].iloc[0],
                "Casa em vilas": df_bairro_selecionado["DOM_PART_PERM_CASA_VILA"].iloc[0],
                "Apartamentos": df_bairro_selecionado["DOM_PART_PERM_CASA_APART"].iloc[0],
            }
    
            st.write(f'### 📊 Total de domicílios particulares permanentes, por tipo, segundo os bairros de Salvador, 2010')
            st.write(f'##### {bairro_selecionado}')
    
            fig_dom = px.bar(
                x=list(dom_values.keys()), 
                y=list(dom_values.values()),
                labels={"x": "Tipo de domicílio", "y": " "},
                text_auto=True  # Mostra os valores automaticamente
            )

            # Posicionar os números acima das colunas
            fig_dom.update_traces(textposition="outside")

            # Remover a legenda e ajustar o layout
            fig_dom.update_layout(
                yaxis_showticklabels=False, 
                showlegend=False, 
                yaxis_showgrid=False, 
                yaxis_tickformat="."
            )
    
            st.plotly_chart(fig_dom)
            
            dom_totais = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
    
            st.markdown(f"📌 **Nota:** Total de domicilios no bairro de {bairro_selecionado}: {dom_totais}")

        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")
    
    if mostrar_moradores:
        
        dom_pizza_values = {
            "1 morador": df_bairro_selecionado["DOM_1_MORADOR"].iloc[0],
            "2 a 4 moradores": df_bairro_selecionado["DOM_2_4_MORADORES"].iloc[0],
            "5 a 6 moradores": df_bairro_selecionado["DOM_5_6_MORADORES"].iloc[0],
            "7 ou mais moradores": df_bairro_selecionado["DOM_ACIMA_7_MORADORES"].iloc[0],
        }
    
        st.write(f'### 📊 Distribuição percentual dos domicílios particulares permanentes, por número de moradores, segundo os bairros de Salvador, 2010')
        st.write(f'##### {bairro_selecionado}')
        
        # Criando DataFrame para garantir a ordem correta
        df_pizza = pd.DataFrame({
            "Categoria": list(dom_pizza_values.keys()),
            "Valor": list(dom_pizza_values.values())
        })

        # Definir a ordem correta explicitamente
        ordem_categorias = [
            "1 morador",
            "2 a 4 moradores",
            "5 a 6 moradores",
            "7 ou mais moradores"
        ]

        #Ordena os dados para garantir a sequência correta no gráfico
        df_pizza["Categoria"] = pd.Categorical(df_pizza["Categoria"], categories=ordem_categorias, ordered=True)
        df_pizza = df_pizza.sort_values("Categoria", ascending=True)

        # Criando o gráfico de pizza
        fig_dom_pizza = px.pie(
            df_pizza,
            names="Categoria", 
            values="Valor",
        )

        # Garantindo que os segmentos e a legenda sigam a ordem correta
        fig_dom_pizza.update_traces(sort=False)  

        fig_dom_pizza.update_layout(
            legend=dict(traceorder="normal")  # Exibe na mesma ordem dos dados
        )

        st.plotly_chart(fig_dom_pizza)

    if mostrar_proporcao:
        prop_cols = [col for col in df.columns if "PROP_" in col]
        if prop_cols:
            
            prop_values = {
            "Lixo coletado": df_bairro_selecionado["PROP_LIXO/DOM"].iloc[0],
            "Esgotamento sanitário ligado a rede geral": df_bairro_selecionado["PROP_SANEAMENTO/DOM"].iloc[0],
            "Abastecimento de água ligado a rede geral": df_bairro_selecionado["PROP_AGUA/DOM"].iloc[0],
            }
                     
            st.write(f'### 📊 Distribuição percentual dos domicílios particulares permanentes, por tipo de infraestrutura urbada segundo os bairros de Salvador, 2010')
            st.write(f'##### {bairro_selecionado}')
            
            fig_prop = px.bar(
                x=list(prop_values.keys()), 
                y=list(prop_values.values()),
                labels={'x' : 'Tipo de infraestrutura urbana', 'y' : ' '}
            )

            # Remover a legenda
            fig_prop.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
            
            st.plotly_chart(fig_prop)

            #Espaçamento entre os graficos
            st.write(" ")
            st.write(" ")
            st.write(" ")
    
    #if mostrar_resp:        
        # Verificar se as colunas existem antes de criar o gráfico
    #    if all(col in df.columns for col in ["RESP_MULHER", "RESP_IDOSOS", "RESP_TOTAL"]):
            # Filtrar os dados apenas para o bairro selecionado
    #        df_bairro = df[df["NOME_BAIRRO"] == bairro_selecionado]
            
    #        st.write(f'### 📊 Distribuição percentual dos responsaveis pelos domicílios particulares permanentes segundo os bairros de Salvador, 2010 ')
    #        st.write(f'##### {bairro_selecionado}')

            # Calcular a nova variável RESP_HOMEM_JOVEM
    #        resp_mulher = df_bairro["RESP_MULHER"].values[0]
    #        resp_idosos = df_bairro["RESP_IDOSOS"].values[0]
    #        resp_total = df_bairro["RESP_TOTAL"].values[0]
    #        resp_homem_jovem = resp_total - (resp_mulher + resp_idosos)

            # Criar um DataFrame para o gráfico de pizza
    #        df_pizza = pd.DataFrame({
    #            "Categoria": [
    #                "Mulheres", 
    #                "Idosos", 
    #                "Homens"
    #            ],
    #            "Quantidade": [resp_mulher, resp_idosos, resp_homem_jovem]
    #        })

            # Criar gráfico de pizza
    #        fig_pizza = px.pie(
    #            df_pizza, 
    #            names="Categoria", 
    #            values="Quantidade", 
    #            color="Categoria",
    #            color_discrete_map={
    #                "Mulheres": "pink",
    #                "Idosos": "gray",
    #                "Homens": "blue"
    #            }
    #        )

            # Exibir o gráfico no Streamlit
     #     st.plotly_chart(fig_pizza)

        #Espaçamento entre os graficos
     #   st.write(" ")
     #   st.write(" ")
     #   st.write(" ")

    if mostrar_renda_sexo:
        # Verificar se as colunas existem antes de criar o gráfico
        if "RESP_RENDA_MEDIA_HOMEM" in df.columns and "RESP_RENDA_MEDIA_MULHER" in df.columns:
            # Filtrar os dados apenas para o bairro selecionado
            df_bairro = df[df["NOME_BAIRRO"] == bairro_selecionado]
            
            st.write(f'### 📊 Rendimento médio dos responsáveis pelos domicílios particulares permanentes, por sexo, segundo os bairros de Salvador, 2010 ')
            st.write(f'##### {bairro_selecionado}')

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
                labels={"Renda Média": " ", "Gênero": "Sexo"},
                color="Gênero", 
                color_discrete_map={"Homens": "blue", "Mulheres": "pink"},
                text_auto=True,  # Mostra os valores automaticamente
            )

            # Posicionar os números acima das colunas
            fig_renda_genero.update_traces(textposition="outside")
            
            

            # Remover a legenda
            fig_renda_genero.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig_renda_genero)

        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")
    
    if mostrar_salario:
                
        resp_pizza_values = {
        "0 a 2 Salários mínimos": df_bairro_selecionado["RESP_RENDA_0_2_SM"].iloc[0],
        "mais de 2 a 5 Salários mínimos": df_bairro_selecionado["RESP_RENDA_2_5_SM"].iloc[0],
        "mais de 5 a 10 Salários mínimos": df_bairro_selecionado["RESP_RENDA_5_10_SM"].iloc[0],
        "mais de 10 a 20 Salários mínimos": df_bairro_selecionado["RESP_RENDA_10_20_SM"].iloc[0],
        "mais de 20 Salários mínimos": df_bairro_selecionado["RESP_RENDA_20_MAIS_SM"].iloc[0],
        "Sem rendimento": df_bairro_selecionado["RESP_SEM_RENDIMENTO"].iloc[0],
        }
        
        st.write(f'### 📊 Rendimento em salários mínimos dos responsáveis pelos domicílios particulares permanentes segundo os bairros de Salvador, 2010')
        st.write(f'##### {bairro_selecionado}')
        
        fig_resp_pizza = px.pie(
            names=list(resp_pizza_values.keys()),
            values=list(resp_pizza_values.values()),
            category_orders={"names": [
             "0 a 2 Salários mínimos",
             "mais de 2 a 5 Salários mínimos",
             "mais de 5 a 10 Salários mínimos",
             "mais de 10 a 20 Salários mínimos",
             "mais de 20 Salários mínimos",
             'Sem rendimento',
            ]}
        )
            
        st.plotly_chart(fig_resp_pizza)
            
        resp_total_bairro = df_bairro_selecionado["RESP_TOTAL"].iloc[0]
        st.write(f"##### População Total de Responsaveis no Bairro {bairro_selecionado}: {resp_total_bairro}")

        #Espaçamento entre os graficos
        st.write(" ")
        st.write(" ")
        st.write(" ")
    
    if mostrar_renda:
        # Exibir gráficos conforme seleção do usuário
        # Adicionar a coluna de cor, sem alterar a ordem dos bairros
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        
        st.write('### 📊 Rendimento médio dos responsáveis por domicílios particulares permanentes segundo os bairros de Salvador, 2010')
    
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
            labels={'RESP_RENDA_MEDIA': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}  # Garantir a ordem original
        )

        # Remover a legenda
        fig_renda.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        
        st.plotly_chart(fig_renda)

if page == "Domicílios":
    page_2()