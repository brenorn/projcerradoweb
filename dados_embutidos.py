# -*- coding: utf-8 -*-
"""Arquivo com dados embutidos para evitar acesso ao sistema de arquivos na Vercel."""

from etl_municipios import _slugify as slugify

DADOS_PROFESSORES = [
    {
        "nome": "Cybele Bueno de Faria",
        "foto": "cybele-bueno-faria.jpg",
        "resumo": "Coordenadora do projeto, especialista em Planejamento Urbano e Regional."
    },
    {
        "nome": "Manuel Eduardo Ferreira",
        "foto": "manuel-ferreira.jpg",
        "resumo": "Vice-coordenador, especialista em Geoprocessamento e Análise de Dados."
    }
]

DADOS_GESTAO = [
    {
        "nome": "Ana Clara Ribeiro",
        "foto": "ana-clara.jpg",
        "resumo": "Gerente de Projeto, responsável pela articulação e entregas."
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
