from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

app = Flask(__name__)
CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
    ],
    supports_credentials=True,
)

BASE_DIR = Path(__file__).resolve().parent
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'maquiagem.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
load_dotenv(BASE_DIR / ".env")

class Maquiagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tom_cor = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "marca": self.marca,
            "categoria": self.categoria,
            "preco": self.preco,
            "tom_cor": self.tom_cor
        }

with app.app_context():
    db.create_all()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Catálogo de Maquiagem</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #fce4ec; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card { border-radius: 15px; border: none; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn-pink { background-color: #d81b60; color: white; border-radius: 20px; }
        .btn-pink:hover { background-color: #ad1457; color: white; }
        .table-custom { background: white; border-radius: 10px; overflow: hidden; }
        h1 { color: #880e4f; font-weight: bold; }
    </style>
</head>
<body class="py-5">
    <div class="container">
        <h1 class="text-center mb-4">💄 Catálogo de Maquiagens</h1>
        
        <div class="row">
            <!-- FORMULÁRIO -->
            <div class="col-md-5 mb-4">
                <div class="card p-4">
                    <h4 class="mb-3" style="color: #ad1457;">Cadastrar Produto</h4>
                    <form id="formMaquiagem">
                        <div class="mb-2">
                            <label class="form-label">Nome do Produto</label>
                            <input type="text" id="nome" class="form-control" placeholder="Ex: Batom Matte" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Marca</label>
                            <input type="text" id="marca" class="form-control" placeholder="Ex: Vult" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Categoria</label>
                            <input type="text" id="categoria" class="form-control" placeholder="Ex: Lábios, Rosto" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Preço (R$)</label>
                            <input type="number" step="0.01" id="preco" class="form-control" placeholder="35.90" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tom / Cor</label>
                            <input type="text" id="tom_cor" class="form-control" placeholder="Ex: Vermelho Intenso" required>
                        </div>
                        <button type="submit" class="btn btn-pink w-100">Salvar Maquiagem</button>
                    </form>
                </div>
            </div>

            <!-- TABELA -->
            <div class="col-md-7">
                <div class="card p-4">
                    <h4 class="mb-3" style="color: #ad1457;">Produtos Cadastrados</h4>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>ID</th>
                                    <th>Nome</th>
                                    <th>Marca</th>
                                    <th>Categoria</th>
                                    <th>Preço</th>
                                    <th>Tom/Cor</th>
                                </tr>
                            </thead>
                            <tbody id="tabelaMaquiagens"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function carregarMaquiagens() {
            const res = await fetch('/api/maquiagens');
            const lista = await res.json();
            const tbody = document.getElementById('tabelaMaquiagens');
            tbody.innerHTML = '';
            lista.forEach(m => {
                tbody.innerHTML += `
                    <tr>
                        <td><b>#${m.id}</b></td>
                        <td>${m.nome}</td>
                        <td>${m.marca}</td>
                        <td><span class="badge bg-secondary">${m.categoria}</span></td>
                        <td>R$ ${m.preco.toFixed(2)}</td>
                        <td>${m.tom_cor}</td>
                    </tr>
                `;
            });
        }

        document.getElementById('formMaquiagem').addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                nome: document.getElementById('nome').value,
                marca: document.getElementById('marca').value,
                categoria: document.getElementById('categoria').value,
                preco: parseFloat(document.getElementById('preco').value),
                tom_cor: document.getElementById('tom_cor').value
            };

            await fetch('/api/maquiagem', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            document.getElementById('formMaquiagem').reset();
            carregarMaquiagens();
        });

        carregarMaquiagens();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/maquiagens", methods=["GET"])
def listar_maquiagens():
    maquiagens = Maquiagem.query.all()
    return jsonify([m.to_dict() for m in maquiagens]), 200

@app.route("/api/maquiagem", methods=["POST"])
def adicionar_maquiagem():
    data = request.get_json()
    try:
        nova = Maquiagem(
            nome=data.get("nome"),
            marca=data.get("marca"),
            categoria=data.get("categoria"),
            preco=float(data.get("preco", 0)),
            tom_cor=data.get("tom_cor")
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({"message": "Sucesso", "maquiagem": nova.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)