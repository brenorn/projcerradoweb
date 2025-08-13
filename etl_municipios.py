from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

# Try to import python-slugify; fallback to a minimal implementation
try:
    from slugify import slugify as _slugify  # type: ignore
except Exception:  # pragma: no cover
    import re

    def _slugify(value: str | None) -> str:
        s = (value or "").lower()
        # remove accents and non-alphanum basic (simple fallback)
        s = re.sub(r"[^a-z0-9\s-]", "", s, flags=re.I)
        s = re.sub(r"\s+", "-", s).strip("-")
        s = re.sub(r"-+", "-", s)
        return s

from sqlalchemy.orm import Session

from db import get_session
from models import (
    AgroCenso,
    CoberturaUsoSoloClasse,
    CoberturaUsoSoloResumo,
    Demografia,
    Fonte,
    Geografia,
    Governanca,
    Municipio,
    Socioeconomia,
    Conflito,
)


def get_or_create_fonte(session: Session, nome: Optional[str], url: Optional[str]) -> Optional[int]:
    if not nome and not url:
        return None
    q = session.query(Fonte)
    if nome:
        q = q.filter(Fonte.nome == nome)
    if url:
        q = q.filter(Fonte.url == url)
    fonte = q.one_or_none()
    if not fonte:
        fonte = Fonte(nome=nome or "", url=url)
        session.add(fonte)
        session.flush()
    return fonte.id


def upsert_municipio(session: Session, nome: str, uf: str, codigo_ibge: str) -> Municipio:
    m = session.query(Municipio).filter_by(codigo_ibge=codigo_ibge).one_or_none()
    if not m:
        m = Municipio(slug=_slugify(f"{nome}-{uf}"), nome=nome, uf=uf, codigo_ibge=codigo_ibge)
        session.add(m)
        session.flush()
    return m


def load_json_file(session: Session, path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    ident = data.get("identificacao", {})
    m = upsert_municipio(
        session,
        ident.get("nome_municipio"),
        ident.get("uf"),
        str(ident.get("codigo_ibge")),
    )

    # Geografia
    geo = data.get("geografia_territorio", {})
    if isinstance(geo, dict):
        area = geo.get("area_territorial_km2")
        bioma = geo.get("bioma", {}).get("valor") if isinstance(geo.get("bioma"), dict) else None
        if isinstance(area, dict):
            fonte_id = get_or_create_fonte(session, area.get("fonte_nome"), area.get("fonte_url"))
            session.merge(
                Geografia(
                    municipio_id=m.id,
                    ano_referencia=area.get("ano_referencia"),
                    area_km2=area.get("valor"),
                    bioma=bioma,
                    fonte_id=fonte_id,
                )
            )

    # Demografia
    dem = data.get("demografia", {})
    if isinstance(dem, dict):
        densidade = dem.get("densidade_demografica_hab_km2", {})
        densidade_valor = densidade.get("valor") if isinstance(densidade, dict) else None
        for key in ("populacao_censo_2022", "populacao_censo_2010"):
            d = dem.get(key)
            if isinstance(d, dict) and d.get("ano_referencia"):
                fonte_id = get_or_create_fonte(session, d.get("fonte_nome"), d.get("fonte_url"))
                session.merge(
                    Demografia(
                        municipio_id=m.id,
                        ano=d.get("ano_referencia"),
                        populacao=d.get("valor"),
                        densidade_hab_km2=densidade_valor,
                        fonte_id=fonte_id,
                    )
                )

    # Socioeconomia
    soc = data.get("socioeconomia", {})
    if isinstance(soc, dict):
        if isinstance(soc.get("idhm_2010"), dict):
            s = soc["idhm_2010"]
            fonte_id = get_or_create_fonte(session, s.get("fonte_nome"), s.get("fonte_url"))
            session.merge(
                Socioeconomia(
                    municipio_id=m.id,
                    ano=s.get("ano_referencia"),
                    idhm=s.get("valor"),
                    fonte_id=fonte_id,
                )
            )
        if isinstance(soc.get("pib_per_capita_reais"), dict):
            p = soc["pib_per_capita_reais"]
            fonte_id = get_or_create_fonte(session, p.get("fonte_nome"), p.get("fonte_url"))
            session.merge(
                Socioeconomia(
                    municipio_id=m.id,
                    ano=p.get("ano_referencia"),
                    pib_per_capita_reais=p.get("valor"),
                    fonte_id=fonte_id,
                )
            )
        if isinstance(soc.get("censo_agropecuario_2017"), dict):
            a = soc["censo_agropecuario_2017"]
            fonte_id = get_or_create_fonte(session, a.get("fonte_nome"), a.get("fonte_url"))
            session.merge(
                AgroCenso(
                    municipio_id=m.id,
                    ano=2017,
                    numero_estabelecimentos=a.get("numero_estabelecimentos"),
                    area_total_estabelecimentos_ha=a.get("area_total_estabelecimentos_ha"),
                    pessoal_ocupado=a.get("pessoal_ocupado"),
                    area_lavouras_ha=a.get("area_lavouras_ha"),
                    area_pastagens_ha=a.get("area_pastagens_ha"),
                    fonte_id=fonte_id,
                )
            )

    # Cobertura uso do solo
    cub = data.get("cobertura_uso_solo")
    if isinstance(cub, dict):
        dg = cub.get("dados_gerais", {}) if isinstance(cub.get("dados_gerais"), dict) else {}
        fonte_id = get_or_create_fonte(session, dg.get("fonte_nome"), dg.get("fonte_url"))
        resumo = CoberturaUsoSoloResumo(
            municipio_id=m.id,
            ano_referencia=dg.get("ano_referencia"),
            fonte_id=fonte_id,
        )
        session.add(resumo)
        session.flush()
        classes = cub.get("classes")
        if not isinstance(classes, list):
            classes = []
        for c in classes:
            session.add(
                CoberturaUsoSoloClasse(
                    cobertura_id=resumo.id,
                    classe=c.get("classe"),
                    area_km2=c.get("area_km2"),
                    percentual=c.get("percentual"),
                )
            )

    # Governança
    gov = data.get("governanca_planejamento", {}).get("plano_diretor")
    if isinstance(gov, dict):
        fonte_id = get_or_create_fonte(session, gov.get("fonte_nome"), gov.get("fonte_url"))
        session.merge(
            Governanca(
                municipio_id=m.id,
                possui_plano_diretor=gov.get("existe"),
                lei_referencia=gov.get("lei_referencia"),
                observacao=gov.get("observacao"),
                fonte_id=fonte_id,
            )
        )

    # Conflitos
    confs = data.get("conflitos_pressoes", {})
    if isinstance(confs, dict):
        for tipo, obj in confs.items():
            if isinstance(obj, dict):
                fonte_id = get_or_create_fonte(session, obj.get("fonte_nome"), obj.get("fonte_url"))
                session.add(
                    # múltiplos registros por tipo são permitidos; se quiser de-duplicar, usar unique hash
                    Conflito(municipio_id=m.id, tipo=tipo, descricao=obj.get("descricao"), fonte_id=fonte_id)
                )


def load_dir(json_dir: Path) -> None:
    """Carrega apenas JSONs de municípios (com chave 'identificacao' e 'codigo_ibge').
    Isola transações por arquivo para evitar que um erro contamine os demais.
    """
    for path in json_dir.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERRO JSON em {path.name}: {e}")
            continue

        # Filtrar somente arquivos de município
        if not isinstance(data, dict):
            print(f"IGNORADO (não é dict): {path.name}")
            continue
        ident = data.get("identificacao")
        if not isinstance(ident, dict) or not ident.get("codigo_ibge"):
            print(f"IGNORADO (sem identificacao/codigo_ibge): {path.name}")
            continue

        # Transação isolada por arquivo
        try:
            with get_session() as session:
                # reaproveita o parser por arquivo usando a mesma lógica
                # mas evitando reabrir o arquivo (já temos data)
                # Reutilizamos load_json_file para manter comportamento
                load_json_file(session, path)
            print(f"OK: {path.name}")
        except Exception as e:
            print(f"ERRO ao importar {path.name}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Importa JSONs de municípios para o banco")
    parser.add_argument("json_dir", type=str, help="Diretório contendo arquivos .json")
    args = parser.parse_args()

    load_dir(Path(args.json_dir))
