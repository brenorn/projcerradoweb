# -*- coding: utf-8 -*-
"""Função utilitária para criar 'slugs' a partir de strings."""

# Try to import python-slugify; fallback to a minimal implementation
try:
    # A dependência 'python-slugify' deve estar no requirements.txt
    from slugify import slugify as _slugify  # type: ignore
except ImportError:
    import re

    def _slugify(value: str | None) -> str:
        """Implementação simples de slugify caso a biblioteca não esteja instalada."""
        s = (value or "").lower()
        # Remove acentos e caracteres não alfa-numéricos (abordagem simples)
        s = re.sub(r'[^a-z0-9\s-]', '', s, flags=re.I)
        s = re.sub(r'\s+', '-', s).strip('-')
        s = re.sub(r'-+', '-', s)
        return s
