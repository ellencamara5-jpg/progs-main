import streamlit as st
import Servico as s

# título da página (H1)
st.title("Cadastro de Pessoas")

# ----------------------
# formulário de cadastro 
# ----------------------

# agrupar em formulário
# após submeter, limpa os campos
with st.form("meu_formulario", clear_on_submit=True):
    
    # insere os campos na tela
    nome = st.text_input("Pessoa: ")
    email = st.text_input("Email: ")
    telefone = st.text_input("Telefone: ")

    # ao clicar no botão de Adicionar...
    if st.form_submit_button("Adicionar"):

        # se o nome não foi preenchido
        if nome == "":
            # mostre uma mensagem de advertência!
            st.warning("Preencha pelo menos o nome!!!")
        else:
            # adiciona a pessoa
            s.inserir_pessoa(nome, email, telefone)

# --------------------
# listagem das pessoas
# --------------------

# obter dados das pessoas em formato para tabela
dados = s.retornar_pessoas_formato_tabela()

# exibir!!
st.dataframe(dados)

# --------
# exclusão
# --------

st.subheader("Excluir pessoa")

# cria um dicionário vazio
opcoes = {}

# percorre os nomes e emails das pessoas
for nome, email in zip(dados["Nome"], dados["Email"]):
    # a chave é o texto exibido; o valor é o email usado para remover
    opcoes[f"{nome} ({email})"] = email

# se houver pessoas...
if opcoes:
    # mostra as pessoas para serem excluídas
    escolha = st.selectbox("Selecione a pessoa", list(opcoes.keys()))

    # se for clicado o botão Excluir...
    if st.button("Excluir"):
        # remove a pessoa pelo email
        s.remover_pessoa(opcoes[escolha])
        # atualiza a página
        st.rerun()
else:
    st.info("Não há pessoas cadastradas para excluir.")