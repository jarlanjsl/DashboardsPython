import streamlit as st
import pandas as pd
import numpy as np

st.title("💡 Demonstração Básica do Streamlit")
st.subheader("Widgets, Tabelas e Gráficos Interativos")

# Texto e Markdown
st.markdown("Este é um exemplo de como usar **Streamlit** no modo interativo.")

# Entrada de texto
nome = st.text_input("Digite seu nome:")
if nome:
    st.success(f"Olá, {nome}!")

# Slider
idade = st.slider("Selecione sua idade", 0, 100, 25)
st.write(f"Idade selecionada: {idade}")

# Checkbox
if st.checkbox("Mostrar tabela aleatória"):
    df = pd.DataFrame(np.random.randn(10, 3), columns=["A", "B", "C"])
    st.write(df)

# Gráfico
st.subheader("Gráfico de Linhas")
dados = pd.DataFrame(np.random.randn(50, 3), columns=["X", "Y", "Z"])
st.line_chart(dados)

# Selectbox
opcao = st.selectbox("Escolha uma opção", ["Opção 1", "Opção 2", "Opção 3"])
st.write(f"Você selecionou: {opcao}")

# Botão
if st.button("Clique aqui"):
    st.balloons()
