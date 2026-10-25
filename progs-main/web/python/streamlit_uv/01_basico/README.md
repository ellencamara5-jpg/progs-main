# CRUD Escolar com Streamlit

Aplicação simples de gerenciamento de alunos com banco SQLite e interface web em Streamlit.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) instalado no sistema

## Executando a aplicação

Dentro do diretório, rode:

```bash
uv run streamlit run main.py
```

A aplicação será iniciada e o Streamlit abrirá a interface em um navegador, normalmente em:

```text
http://localhost:8501
```

## Estrutura principal

- `main.py` - código da aplicação Streamlit e do banco SQLite
- `alunos.db` - banco de dados SQLite gerado ao iniciar a aplicação
- `pyproject.toml` - definição do projeto e dependências

## Funcionalidades

- Adicionar aluno
- Listar alunos cadastrados
- Remover aluno