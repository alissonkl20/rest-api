from flask import Flask, render_template
from datetime import datetime
import requests
from collections import defaultdict

app = Flask(__name__)

CATEGORIAS = [
    {"id": 1, "nome": "Bolos e Tortas"},
    {"id": 2, "nome": "Doces"},
    {"id": 3, "nome": "Salgados"},
    {"id": 4, "nome": "Paes"}
]

def agrupar_por_categoria(produtos):
    categorias = defaultdict(lambda: {"disponiveis": [], "indisponiveis": []})
    total_produtos = len(produtos)
    for produto in produtos:
        nome_categoria = produto["categoria"]["nome"]
        if produto["disponivel"]:
            categorias[nome_categoria]["disponiveis"].append(produto)
        else:
            categorias[nome_categoria]["indisponiveis"].append(produto)
    return {
        "atualizado_em": "04/08/2025",  # ou sua lógica de data
        "categorias": categorias,
        "total_produtos": total_produtos,
        "erro": None
    }

def processar_dados():
    try:
        # Troque para o endpoint que retorna todos os produtos
        resp_produtos = requests.get('http://localhost:8080/api/produtos', timeout=5)
        resp_produtos.raise_for_status()
        produtos = resp_produtos.json()
    except requests.exceptions.RequestException as e:
        return {
            'categorias': {},
            'total_produtos': 0,
            'atualizado_em': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'erro': f'Erro ao obter dados do backend: {e}'
        }

    categorias_produtos = agrupar_por_categoria(produtos)
    return {
        'categorias': categorias_produtos['categorias'],
        'total_produtos': categorias_produtos['total_produtos'],
        'atualizado_em': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'erro': categorias_produtos['erro']
    }

@app.route('/')
def dashboard():
    dados_processados = processar_dados()
    return render_template('kar.html', dados=dados_processados)

if __name__ == '__main__':
    app.run(debug=True)

