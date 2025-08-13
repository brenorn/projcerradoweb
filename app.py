import os
import json
from pathlib import Path
from flask import Flask, render_template, abort, jsonify
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import gzip
from io import BytesIO
from sqlalchemy import func
from etl_municipios import _slugify as slugify  # reuse lightweight slugify

# Dados embutidos para contornar o sistema de arquivos da Vercel
from dados_embutidos import DADOS_MUNICIPIOS, DADOS_PROFESSORES, DADOS_GESTAO


app = Flask(__name__)

#     def __repr__(self):
#         return f'<Noticia {self.titulo}>'

# class CamadaGeoespacial(db.Model):
#     __tablename__ = 'camadas_geo'
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False, unique=True)
#     descricao = db.Column(db.Text)
#     categoria = db.Column(db.String(100)) # Ex: 'Uso do Solo', 'Hidrografia'
#     fonte = db.Column(db.String(150))
    
#     def __repr__(self):
#         return f'<CamadaGeoespacial {self.nome}>'


# Rota para a página inicial
@app.route('/')
def home():
    # Home agora herda de base.html para padronizar o menu/cabeçalho
    return render_template('home.html')

# Rota para a página do Geoportal
@app.route('/geoportal')
def geoportal():
    return render_template('geoportal.html')

# Rota para a trilha de Gestão Pública
@app.route('/gestao-publica')
def gestao_publica():
    return render_template('gestao-publica.html')

# Rota para a trilha de Desenvolvimento Sustentável
@app.route('/desenvolvimento-sustentavel')
def desenvolvimento_sustentavel():
    return render_template('desenvolvimento-sustentavel.html')

# Rota para a trilha de Análise de Dados
@app.route('/analise-dados')
def analise_dados():
    return render_template('analise-dados.html')

# Rota para o Dashboard RIDE-DF
@app.route('/dashboard')
def dashboard():
    # Agora usa template que estende base.html para padronizar o layout
    return render_template('dashboard_base.html')

# Bloqueia URL antiga '/sobre' (não existe mais página própria)
@app.route('/sobre')
def sobre_legacy():
    abort(404)

# ------------------
# Novas rotas (estrutura do plano)
# ------------------

# Hub de Municípios
@app.route('/municipios')
def municipios():
    # Usa dados embutidos para garantir funcionamento na Vercel
    return render_template('municipios.html', municipios=DADOS_MUNICIPIOS)


@app.route('/municipios/<slug>')
def municipio_detalhe(slug: str):
    """Página de detalhe do município. Busca nos dados embutidos.
    """
    ctx = None
    for municipio in DADOS_MUNICIPIOS:
        if municipio.get('slug') == slug:
            ctx = municipio
            break
    
    if not ctx:
        abort(404)

    return render_template('municipio.html', **ctx)


# ------------------
# Piloto: municipio_teste
# ------------------
@app.route('/municipio_teste/<int:codigo_ibge>')
def municipio_teste(codigo_ibge: int):
    """Página simples para testar integração com IBGE Localidades."""
    return render_template('municipio_teste.html', codigo_ibge=str(codigo_ibge))


@app.route('/api/municipio_ibge/<int:codigo_ibge>')
def api_municipio_ibge(codigo_ibge: int):
    """Consulta o IBGE Localidades para obter metadados básicos do município.
    Fonte: https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{codigo}
    """
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{codigo_ibge}"
    req = Request(
        url,
        headers={
            "User-Agent": "ProjetoCerrado/1.0",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        },
    )
    try:
        with urlopen(req, timeout=15) as resp:
            raw = resp.read()
            enc = (resp.headers.get('Content-Encoding') or '').lower()
            # Alguns endpoints do IBGE retornam gzip mesmo sem pedir
            if enc == 'gzip' or (len(raw) > 2 and raw[0] == 0x1F and raw[1] == 0x8B):
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    # fallback via BytesIO
                    raw = gzip.GzipFile(fileobj=BytesIO(raw)).read()
            data = json.loads(raw.decode('utf-8'))
    except HTTPError as e:
        return jsonify({"error": f"HTTP {e.code} ao consultar IBGE Localidades"}), 502
    except URLError as e:
        return jsonify({"error": f"Falha de conexão ao IBGE: {e.reason}"}), 502
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

    # Normaliza campos principais
    nome = data.get('nome')
    uf = None
    try:
        uf = data['microrregiao']['mesorregiao']['UF']['sigla']
    except Exception:
        pass

    payload = {
        "codigo_ibge": str(codigo_ibge),
        "nome": nome,
        "uf": uf,
        "fonte": "IBGE Localidades",
        # Espaço reservado: próximos passos para acoplar SIDRA (população, área, etc.)
        "indicadores": {
            "populacao": None,
            "area_km2": None,
            "densidade": None
        }
    }
    return jsonify(payload)

 

# Índice de Temas
@app.route('/temas')
def temas():
    return render_template('temas.html')

# Temas específicos
@app.route('/temas/saneamento')
def tema_saneamento():
    return render_template('tema-saneamento.html')

@app.route('/temas/recursos-hidricos')
def tema_recursos_hidricos():
    return render_template('tema-recursos-hidricos.html')

@app.route('/temas/uso-da-terra')
def tema_uso_terra():
    return render_template('tema-uso-terra.html')

@app.route('/temas/bens-servicos-ambientais')
def tema_bsa():
    return render_template('tema-bsa.html')



# Cursos e capacitações
@app.route('/cursos')
def cursos():
    return render_template('cursos.html')



# Equipe (professores por JSON e equipe de gestão por JSON)
@app.route('/equipe')
def equipe():
    # Usa dados embutidos para garantir funcionamento na Vercel
    return render_template('equipe.html', professores=DADOS_PROFESSORES, gestao=DADOS_GESTAO)

# Página 404 simples
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Desenvolvimento: recarregar templates e evitar cache de estáticos
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
