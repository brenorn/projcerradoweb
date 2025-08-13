from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Fonte(Base):
    __tablename__ = "fontes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # reverse relationships
    geografias: Mapped[List["Geografia"]] = relationship(back_populates="fonte")
    demografias: Mapped[List["Demografia"]] = relationship(back_populates="fonte")
    socioeconomias: Mapped[List["Socioeconomia"]] = relationship(back_populates="fonte")
    agro_censos: Mapped[List["AgroCenso"]] = relationship(back_populates="fonte")
    cobertura_resumos: Mapped[List["CoberturaUsoSoloResumo"]] = relationship(
        back_populates="fonte"
    )
    governancas: Mapped[List["Governanca"]] = relationship(back_populates="fonte")
    conflitos: Mapped[List["Conflito"]] = relationship(back_populates="fonte")


class Municipio(Base):
    __tablename__ = "municipios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    uf: Mapped[str] = mapped_column(String(2), nullable=False)
    codigo_ibge: Mapped[str] = mapped_column(String(7), unique=True, nullable=False)
    observacoes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    geografias: Mapped[List["Geografia"]] = relationship(
        back_populates="municipio", cascade="all, delete-orphan"
    )
    demografias: Mapped[List["Demografia"]] = relationship(
        back_populates="municipio", cascade="all, delete-orphan"
    )
    socioeconomias: Mapped[List["Socioeconomia"]] = relationship(
        back_populates="municipio", cascade="all, delete-orphan"
    )
    agro_censos: Mapped[List["AgroCenso"]] = relationship(
        back_populates="municipio", cascade="all, delete-orphan"
    )
    cobertura_resumos: Mapped[List["CoberturaUsoSoloResumo"]] = relationship(
        back_populates="municipio", cascade="all, delete-orphan"
    )
    governanca: Mapped[Optional["Governanca"]] = relationship(
        back_populates="municipio", uselist=False, cascade="all, delete-orphan"
    )
    conflitos: Mapped[List["Conflito"]] = relationship(
        back_populates="municipio", cascade="all, delete-orphan"
    )


class Geografia(Base):
    __tablename__ = "geografias"
    __table_args__ = (UniqueConstraint("municipio_id", "ano_referencia"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    ano_referencia: Mapped[int] = mapped_column(Integer, nullable=False)
    area_km2: Mapped[Optional[float]] = mapped_column(Numeric(12, 3))
    bioma: Mapped[Optional[str]] = mapped_column(Text)
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="geografias")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="geografias")


class Demografia(Base):
    __tablename__ = "demografias"
    __table_args__ = (UniqueConstraint("municipio_id", "ano"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    populacao: Mapped[Optional[int]] = mapped_column(BigInteger)
    densidade_hab_km2: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="demografias")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="demografias")


class Socioeconomia(Base):
    __tablename__ = "socioeconomias"
    __table_args__ = (UniqueConstraint("municipio_id", "ano"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    idhm: Mapped[Optional[float]] = mapped_column(Numeric(5, 3))
    pib_total_mil_reais: Mapped[Optional[float]] = mapped_column(Numeric(16, 2))
    pib_per_capita_reais: Mapped[Optional[float]] = mapped_column(Numeric(16, 2))
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="socioeconomias")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="socioeconomias")


class AgroCenso(Base):
    __tablename__ = "agro_censo"
    __table_args__ = (UniqueConstraint("municipio_id", "ano"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    numero_estabelecimentos: Mapped[Optional[int]] = mapped_column(Integer)
    area_total_estabelecimentos_ha: Mapped[Optional[float]] = mapped_column(
        Numeric(16, 2)
    )
    pessoal_ocupado: Mapped[Optional[int]] = mapped_column(Integer)
    area_lavouras_ha: Mapped[Optional[float]] = mapped_column(Numeric(16, 2))
    area_pastagens_ha: Mapped[Optional[float]] = mapped_column(Numeric(16, 2))
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="agro_censos")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="agro_censos")


class CoberturaUsoSoloResumo(Base):
    __tablename__ = "cobertura_uso_solo_resumo"
    __table_args__ = (UniqueConstraint("municipio_id", "ano_referencia"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    ano_referencia: Mapped[int] = mapped_column(Integer, nullable=False)
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="cobertura_resumos")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="cobertura_resumos")
    classes: Mapped[List["CoberturaUsoSoloClasse"]] = relationship(
        back_populates="cobertura", cascade="all, delete-orphan"
    )


class CoberturaUsoSoloClasse(Base):
    __tablename__ = "cobertura_uso_solo_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cobertura_id: Mapped[int] = mapped_column(
        ForeignKey("cobertura_uso_solo_resumo.id", ondelete="CASCADE"), nullable=False
    )
    classe: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # ex: Vegetação Nativa, Pastagem, Agricultura, Corpos Hídricos, Área Urbana
    area_km2: Mapped[Optional[float]] = mapped_column(Numeric(16, 2))
    percentual: Mapped[Optional[float]] = mapped_column(Numeric(6, 2))

    cobertura: Mapped[CoberturaUsoSoloResumo] = relationship(back_populates="classes")


class Governanca(Base):
    __tablename__ = "governancas"
    __table_args__ = (UniqueConstraint("municipio_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    possui_plano_diretor: Mapped[Optional[bool]] = mapped_column(Boolean)
    lei_referencia: Mapped[Optional[str]] = mapped_column(Text)
    observacao: Mapped[Optional[str]] = mapped_column(Text)
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="governanca")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="governancas")


class Conflito(Base):
    __tablename__ = "conflitos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.id", ondelete="CASCADE"), nullable=False
    )
    tipo: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # ex: crescimento_desordenado, situacao_fundiaria, desmatamento, mineracao, etc.
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    fonte_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fontes.id"))

    municipio: Mapped[Municipio] = relationship(back_populates="conflitos")
    fonte: Mapped[Optional[Fonte]] = relationship(back_populates="conflitos")
