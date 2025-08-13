import os
import json
from pathlib import Path
from flask import Flask, render_template, abort, jsonify
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import gzip
from io import BytesIO
from sqlalchemy import func
from db import get_session
from etl_municipios import _slugify as slugify  # reuse lightweight slugify
from models import (
    Municipio,
    Geografia,
    Demografia,
    Socioeconomia,
    CoberturaUsoSoloResumo,
    CoberturaUsoSoloClasse,
    Governanca,
    Conflito,
)


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
    # Lista dinâmica dos municípios cadastrados
    with get_session() as session:
        lista = (
            session.query(Municipio)
            .order_by(Municipio.nome.asc())
            .all()
        )
        # Fallback: se estiver vazio, lê diretamente os JSONs (sem gravar no banco)
        if not lista:
            try:
                # diretório relativo ao projeto
                json_dir = Path(__file__).resolve().parent / "planejamento"
                if json_dir.exists():
                    print(f"[municipios] Banco vazio; carregando JSONs somente para exibição: {json_dir}")
                    temp = []
                    for path in sorted(json_dir.glob('*.json')):
                        try:
                            data = json.loads(path.read_text(encoding='utf-8'))
                        except Exception:
                            continue
                        ident = data.get('identificacao') if isinstance(data, dict) else None
                        if not isinstance(ident, dict):
                            continue
                        nome = ident.get('nome_municipio')
                        uf = ident.get('uf')
                        codigo = str(ident.get('codigo_ibge')) if ident.get('codigo_ibge') is not None else None
                        if not (nome and uf and codigo):
                            continue
                        # indicadores (opcionais)
                        geo = data.get('geografia_territorio') if isinstance(data.get('geografia_territorio'), dict) else {}
                        area = None
                        bioma = None
                        if isinstance(geo, dict):
                            a = geo.get('area_territorial_km2')
                            if isinstance(a, dict):
                                area = a.get('valor')
                            b = geo.get('bioma')
                            if isinstance(b, dict):
                                bioma = b.get('valor')

                        dem = data.get('demografia') if isinstance(data.get('demografia'), dict) else {}
                        pop = None
                        if isinstance(dem, dict):
                            c22 = dem.get('populacao_censo_2022')
                            c10 = dem.get('populacao_censo_2010')
                            if isinstance(c22, dict) and c22.get('valor') is not None:
                                pop = c22.get('valor')
                            elif isinstance(c10, dict) and c10.get('valor') is not None:
                                pop = c10.get('valor')

                        soc = data.get('socioeconomia') if isinstance(data.get('socioeconomia'), dict) else {}
                        idhm = None
                        pib_pc = None
                        if isinstance(soc, dict):
                            i = soc.get('idhm_2010')
                            if isinstance(i, dict):
                                idhm = i.get('valor')
                            p = soc.get('pib_per_capita_reais')
                            if isinstance(p, dict):
                                pib_pc = p.get('valor')

                        gov = data.get('governanca_planejamento')
                        plano = None
                        if isinstance(gov, dict):
                            pd = gov.get('plano_diretor')
                            if isinstance(pd, dict):
                                plano = pd.get('existe')

                        temp.append({
                            'nome': nome,
                            'uf': uf,
                            'codigo_ibge': codigo,
                            'slug': slugify(f"{nome}-{uf}"),
                            'area_km2': area,
                            'bioma': bioma,
                            'populacao': pop,
                            'idhm': idhm,
                            'pib_per_capita_reais': pib_pc,
                            'plano_diretor': plano,
                        })
                    # Passa a lista simples (dicts) para o template
                    lista = temp
            except Exception:
                # Se falhar, segue vazio e a UI mostrará a orientação
                pass
    return render_template('municipios.html', municipios=lista)


@app.route('/municipios/<slug>')
def municipio_detalhe(slug: str):
    """Página de detalhe do município. Busca no DB e faz fallback para JSONs.
    """
    # Tenta encontrar no DB
    with get_session() as session:
        m = (
            session.query(Municipio)
            .filter(func.lower(Municipio.slug) == func.lower(slug))
            .one_or_none()
        )

        if m:
            ctx = {
                'slug': m.slug,
                'nome': m.nome,
                'uf': m.uf,
                'codigo_ibge': m.codigo_ibge,
            }
        else:
            # Fallback: procurar JSON que gere o mesmo slug
            ctx = None
            try:
                json_dir = Path(__file__).resolve().parent / "planejamento"
                for path in json_dir.glob('*.json'):
                    try:
                        data = json.loads(path.read_text(encoding='utf-8'))
                    except Exception:
                        continue
                    ident = data.get('identificacao') if isinstance(data, dict) else None
                    if not isinstance(ident, dict):
                        continue
                    nome = ident.get('nome_municipio')
                    uf = ident.get('uf')
                    if not (nome and uf):
                        continue
                    if slugify(f"{nome}-{uf}") == slug:
                        # indicadores básicos
                        codigo = str(ident.get('codigo_ibge')) if ident.get('codigo_ibge') is not None else None
                        geo = data.get('geografia_territorio') if isinstance(data.get('geografia_territorio'), dict) else {}
                        dem = data.get('demografia') if isinstance(data.get('demografia'), dict) else {}
                        soc = data.get('socioeconomia') if isinstance(data.get('socioeconomia'), dict) else {}

                        area = geo.get('area_territorial_km2', {}).get('valor') if isinstance(geo.get('area_territorial_km2'), dict) else None
                        bioma = geo.get('bioma', {}).get('valor') if isinstance(geo.get('bioma'), dict) else None
                        pop = dem.get('populacao_censo_2022', {}).get('valor') if isinstance(dem.get('populacao_censo_2022'), dict) else None
                        if pop is None:
                            pop = dem.get('populacao_censo_2010', {}).get('valor') if isinstance(dem.get('populacao_censo_2010'), dict) else None
                        idhm = soc.get('idhm_2010', {}).get('valor') if isinstance(soc.get('idhm_2010'), dict) else None

                        ctx = {
                            'slug': slug,
                            'nome': nome,
                            'uf': uf,
                            'codigo_ibge': codigo,
                            'area_km2': area,
                            'bioma': bioma,
                            'populacao': pop,
                            'idhm': idhm,
                        }
                        break
            except Exception:
                pass

    if not (m or ctx):
        abort(404)

    # Normaliza contexto para o template
    if m and not ctx:
        ctx = {
            'slug': m.slug,
            'nome': m.nome,
            'uf': m.uf,
            'codigo_ibge': m.codigo_ibge,
        }

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
    # Professores: lidos de JSON para facilitar manutenção
    # Define o caminho base para os arquivos de dados
    data_dir = Path(__file__).resolve().parent / "planejamento"
    profs_json_path = data_dir / "professores.json"
    professores = []
    try:
        if profs_json_path.exists():
            with open(profs_json_path, 'r', encoding='utf-8') as f:
                professores = json.load(f)
    except Exception:
        professores = []
    # Equipe de gestão (opcional)
    gestao_json_path = data_dir / "gestao.json"
    gestao = []
    try:
        if gestao_json_path.exists():
            with open(gestao_json_path, 'r', encoding='utf-8') as f:
                gestao = json.load(f)
    except Exception:
        gestao = []

    return render_template('equipe.html', professores=professores, gestao=gestao)

# Página 404 simples
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Desenvolvimento: recarregar templates e evitar cache de estáticos
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
