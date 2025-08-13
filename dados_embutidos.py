# -*- coding: utf-8 -*-
"""Arquivo com dados embutidos para evitar acesso ao sistema de arquivos na Vercel."""

from etl_municipios import _slugify as slugify

DADOS_PROFESSORES = [
  {
    "nome": "Mauro Eloi Nappo",
    "bio": "Engenheiro Florestal pela UFV (1993), especialista em Proteção de Plantas (ABeAS/UFV, 1995), mestre em Engenharia Florestal pela UFLA (1999) e doutor em Ciência Florestal pela UFV (2002). Pesquisa regeneração natural e silvicultura com foco em áreas mineradas e sub-bosques de espécies nativas. Atuou no IEF-MG, consultoria privada e como professor substituto na UFU antes de ingressar na UnB (EFL/FT) em 2007. Na UnB, atua em silvicultura, recuperação de áreas degradadas, biodiversidade e perícia ambiental.",
    "lattes": "http://lattes.cnpq.br/4038904353437470",
    "areas": ["Silvicultura", "Recuperação de Áreas Degradadas", "Biodiversidade", "Perícia Ambiental"],
    "foto": "/static/imagens/professores/mauro-eloi-nappo.jpg"
  },
  {
    "nome": "Ricardo Tezini Minoti",
    "bio": "Biólogo (UFSCar), mestre (1999) e doutor (2006) em Ciências da Engenharia Ambiental pela EESC/USP, com foco em monitoramento da qualidade da água e modelagem hidrológica/erosiva. Realizou pós-doutorado na Universidade de Adelaide (2013–2014) aplicando algoritmos genéticos à previsão de florações de cianobactérias. Professor do ENC/UnB e do PTARH-UnB, atuou também em comitês e GTs de bacias hidrográficas no DF. Áreas de atuação: limnologia, monitoramento de sistemas hídricos, métodos e modelos para recursos hídricos e políticas públicas ambientais.",
    "lattes": "http://lattes.cnpq.br/4058939299213448",
    "areas": ["Recursos Hídricos", "Limnologia", "Modelagem Hidrológica", "Gestão Ambiental", "Políticas Públicas"],
    "foto": "/static/imagens/professores/ricardo-tezini-minoti.jpg"
  },
  {
    "nome": "Eraldo Aparecido Trondoli Matricardi",
    "bio": "Engenheiro Florestal (UFMT), especialista em aerofotos (UFSM), mestre e doutor em Geografia pela Michigan State University, com ênfase em Sensoriamento Remoto e Geoprocessamento. Atuou na iniciativa privada, governo de Rondônia, Nações Unidas e na própria MSU. Professor Associado na UnB, consultor Ad-hoc da NSF, CAPES e MMA/ARPA e Editor Associado da Remote Sensing of Earth System Science (Springer). Pesquisa mudanças climáticas, geoprocessamento, sensoriamento remoto, degradação florestal, incêndios, análises ambientais e uso e cobertura da terra.",
    "lattes": "http://lattes.cnpq.br/3238397066723847",
    "areas": ["Geoprocessamento", "Sensoriamento Remoto", "Mudanças Climáticas", "Uso e Cobertura da Terra", "Análises Ambientais"],
    "foto": "/static/imagens/professores/eraldo-matricardi.jpg"
  },
  {
    "nome": "Leonardo Jobi Biali",
    "bio": "Engenheiro Florestal (UFSM), com mestrado e doutorado em Engenharia Florestal pela UFSM e pós-doutorado na UFES. Professor adjunto do Departamento de Engenharia Florestal da UnB. Atua nas áreas de Administração Florestal e Política Florestal, com interesse em gestão e governança do setor. Desenvolve atividades de ensino, pesquisa e extensão voltadas à sustentabilidade do uso de recursos florestais.",
    "lattes": "http://lattes.cnpq.br/3216800651211677",
    "areas": ["Administração Florestal", "Política Florestal", "Gestão Ambiental"],
    "foto": "/static/imagens/professores/leonardo-jobi-biali.jpg"
  },
  {
    "nome": "Ariuska Karla Barbosa Amorim",
    "bio": "Engenheira Química (UFPB), mestre (1995) e doutora (2000) em Engenharia Civil – Hidráulica e Saneamento (EESC/USP), com estágio pós-doutoral (2013) na Universidade de Adelaide em Bionanotecnologia. Professora do Departamento de Engenharia Civil e Ambiental da UnB. Experiência em processos biológicos de tratamento de efluentes, produção de metano em processos anaeróbios e remoção biológica de nutrientes. Pesquisa aplicações de nanopartículas magnéticas e microplásticos em ETEs e tecnologias emergentes para saneamento.",
    "lattes": "http://lattes.cnpq.br/2034414130213796",
    "areas": ["Saneamento", "Tratamento de Efluentes", "Bioprocessos", "Remoção de Nutrientes", "Microplásticos"],
    "foto": "/static/imagens/professores/ariuska-karla-barbosa-amorim.jpg"
  },
  {
    "nome": "Paulo Celso dos Reis Gomes",
    "bio": "Engenheiro Civil e Engenheiro de Segurança do Trabalho, mestre em Tecnologia Ambiental e Recursos Hídricos e doutor em Desenvolvimento Sustentável. Professor da UnB desde 1998, coordena o Laboratório de Segurança Ambiental (FT/UnB) e a Pós-Graduação em Engenharia de Segurança do Trabalho. Exerceu cargos de direção na UnB e no Governo do DF, incluindo SLU e Subsecretaria de Meio Ambiente/Resíduos Sólidos. Atuação em gestão pública ambiental, resíduos sólidos, segurança do trabalho e ordenamento territorial.",
    "lattes": "http://lattes.cnpq.br/8405120104436318",
    "areas": ["Desenvolvimento Sustentável", "Gestão Ambiental", "Resíduos Sólidos", "Segurança do Trabalho", "Políticas Públicas"],
    "foto": "/static/imagens/professores/paulo-celso-dos-reis-gomes.jpg"
  },
  {
    "nome": "Cláudio Henrique de Almeida Feitosa Pereira",
    "bio": "Engenheiro Civil (UnP), mestre em Engenharia Civil (UFG) e doutor em Estruturas e Construção Civil (UnB). Professor adjunto do Curso de Engenharia Civil e Ambiental da UnB, com atuação no Laboratório de Materiais de Construção Civil (LEM/UnB). Trabalha com materiais e componentes de construção, desempenho e inovação em sistemas construtivos. Desenvolve atividades de ensino, pesquisa e extensão na área de Engenharia Civil.",
    "lattes": "http://lattes.cnpq.br/5457613006182121",
    "areas": ["Materiais de Construção", "Estruturas", "Construção Civil"],
    "foto": "/static/imagens/professores/claudio-henrique-feitosa-pereira.jpg"
  }
]

DADOS_GESTAO = [
  {
    "nome": "Cybele Bueno Rocha Rodrigues de Faria",
    "papel": "Pesquisa, Desenvolvimento e Inovação (PD&I) A / Vice-Coordenadora",
    "bio": "Mestrado em Governança e Inovação (UnB). MBA em Gestão da Inovação, Tecnologia e Empreendedorismo. Pós-graduações em Direito e Gestão Pública. Coordenadora e pesquisadora em projetos estratégicos da UnB (PDI_PISAC, Observatório de Práticas Integrativas). Experiência em gestão de projetos, recursos, finanças públicas e inovação.",
    "lattes": "http://lattes.cnpq.br/3678187057033895",
    "foto": "/static/imagens/professores/cybele-bueno-faria.jpg"
  },
  {
    "nome": "Márcio Antônio Pereira de Alcântara",
    "papel": "Apoio Técnico (PD&I) A",
    "bio": "Graduação em Sistemas de Informação. Experiência em gestão administrativa e orçamentária na Direção da FT/UnB, incluindo emissão de passagens/diárias, execução de processos com recursos de diversas pró-reitorias, controle orçamentário e ordenação de despesas.",
    "lattes": None,
    "foto": "/static/imagens/professores/marcio-antonio-alcantara.jpg"
  }
]

# Dados extraídos dos JSONs e do banco para embutir no código
DADOS_MUNICIPIOS = [
    {
        'nome': 'Cavalcante',
        'uf': 'GO',
        'codigo_ibge': '5205304',
        'slug': slugify('Cavalcante-GO'),
        'area_km2': 6953.65,
        'bioma': 'Cerrado',
        'populacao': 9993,
        'idhm': 0.563,
        'pib_per_capita_reais': 15674.88,
        'plano_diretor': True,
    },
    {
        'nome': 'Cidade Ocidental',
        'uf': 'GO',
        'codigo_ibge': '5205494',
        'slug': slugify('Cidade Ocidental-GO'),
        'area_km2': 393.35,
        'bioma': 'Cerrado',
        'populacao': 72890,
        'idhm': 0.704,
        'pib_per_capita_reais': 18431.54,
        'plano_diretor': True,
    },
    {
        'nome': 'Monte Alegre de Goiás',
        'uf': 'GO',
        'codigo_ibge': '5213506',
        'slug': slugify('Monte Alegre de Goiás-GO'),
        'area_km2': 3119.8,
        'bioma': 'Cerrado',
        'populacao': 6866,
        'idhm': 0.57,
        'pib_per_capita_reais': 14876.98,
        'plano_diretor': False,
    },
    {
        'nome': 'Teresina de Goiás',
        'uf': 'GO',
        'codigo_ibge': '5221301',
        'slug': slugify('Teresina de Goiás-GO'),
        'area_km2': 774.64,
        'bioma': 'Cerrado',
        'populacao': 3345,
        'idhm': 0.59,
        'pib_per_capita_reais': 13543.21,
        'plano_diretor': True,
    }
]
