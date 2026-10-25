from Modelo import Pessoa

pessoas_interno = [
        Pessoa("Ana", "a@gmail.com", "47 91234567"), 
        Pessoa("Bruno", "bru@gmail.com", "47 98765432"), 
        Pessoa("Carlos", "ca@gmail.com", "47 91324354")
            ]

# esta função retorna a lista de pessoas
# em um formato a ser exibido pela tabela do streamlit
# está armazenada na lista interna
def retornar_pessoas_formato_tabela():
    dados_no_formato = {
        "Nome": [p.nome for p in pessoas_interno],
        "Email": [p.email for p in pessoas_interno],
        "Telefone": [p.telefone for p in pessoas_interno]
    }
    return dados_no_formato

# esta função insere uma pessoa
def inserir_pessoa(nome : str, email : str, telefone : str):
    # cria uma pessoa
    nova = Pessoa(nome, email, telefone)
    # adiciona no cadastro interno
    pessoas_interno.append(nova)

# esta função remove uma pessoa, tendo
# como chave de busca o email
def remover_pessoa(email : str):
    # percorre as pessoas
    for p in pessoas_interno:
        # se achou
        if p.email == email:
            # remove :-)
            pessoas_interno.remove(p)
    