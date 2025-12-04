# Módulo principal del separador silábico

from .alfabeto import (
    VOCALES_FUERTES,
    VOCALES_DEBILES,
    VOCALES_DEBILES_ACENTUADAS,
    VOCALES,
    DIGRAFOS,
    GRUPOS_INSEPARABLES
)

from .clasificador import (
    es_vocal,
    es_vocal_fuerte,
    es_vocal_debil,
    es_vocal_debil_acentuada,
    es_consonante,
    clasificar_caracter,
    es_diptongo,
    es_hiato,
    es_digrafo,
    es_grupo_inseparable
)

from .separador import (
    separar_silabas,
    procesar_lista_palabras
)

__all__ = [
    # Alfabeto
    'VOCALES_FUERTES',
    'VOCALES_DEBILES', 
    'VOCALES_DEBILES_ACENTUADAS',
    'VOCALES',
    'DIGRAFOS',
    'GRUPOS_INSEPARABLES',
    # Clasificador
    'es_vocal',
    'es_vocal_fuerte',
    'es_vocal_debil',
    'es_vocal_debil_acentuada',
    'es_consonante',
    'clasificar_caracter',
    'es_diptongo',
    'es_hiato',
    'es_digrafo',
    'es_grupo_inseparable',
    # Separador
    'separar_silabas',
    'procesar_lista_palabras'
]
