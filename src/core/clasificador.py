# Funciones para clasificar caracteres según el alfabeto lógico

from .alfabeto import (
    VOCALES, VOCALES_FUERTES, VOCALES_DEBILES, 
    VOCALES_DEBILES_ACENTUADAS, DIGRAFOS, GRUPOS_INSEPARABLES
)


def es_vocal(c: str) -> bool:
    """Determina si un carácter es vocal."""
    return c.lower() in VOCALES


def es_vocal_fuerte(c: str) -> bool:
    """Determina si un carácter es vocal fuerte."""
    return c.lower() in VOCALES_FUERTES


def es_vocal_debil(c: str) -> bool:
    """Determina si un carácter es vocal débil."""
    return c.lower() in VOCALES_DEBILES


def es_vocal_debil_acentuada(c: str) -> bool:
    """Determina si es vocal débil con tilde (rompe diptongo)."""
    return c.lower() in VOCALES_DEBILES_ACENTUADAS


def es_consonante(c: str) -> bool:
    """Determina si un carácter es consonante."""
    return c.isalpha() and not es_vocal(c)


def clasificar_caracter(c: str) -> str:
    """
    Clasifica un carácter según el alfabeto lógico.
    
    Retorna:
        'VF'  - Vocal fuerte
        'VD'  - Vocal débil
        'VDA' - Vocal débil acentuada
        'C'   - Consonante
        'X'   - Carácter no alfabético
    """
    c = c.lower()
    if c in VOCALES_DEBILES_ACENTUADAS:
        return 'VDA'
    elif c in VOCALES_DEBILES:
        return 'VD'
    elif c in VOCALES_FUERTES:
        return 'VF'
    elif c.isalpha():
        return 'C'
    return 'X'


def es_diptongo(v1: str, v2: str) -> bool:
    """
    Determina si dos vocales forman diptongo (NO se separan).
    
    Diptongo: VF+VD, VD+VF, VD+VD (sin tilde en la débil)
    """
    tipo1 = clasificar_caracter(v1)
    tipo2 = clasificar_caracter(v2)
    
    # Si alguna vocal débil tiene tilde, es HIATO (se separa)
    if tipo1 == 'VDA' or tipo2 == 'VDA':
        return False
    
    # VF + VD = Diptongo
    if tipo1 == 'VF' and tipo2 == 'VD':
        return True
    
    # VD + VF = Diptongo
    if tipo1 == 'VD' and tipo2 == 'VF':
        return True
    
    # VD + VD = Diptongo
    if tipo1 == 'VD' and tipo2 == 'VD':
        return True
    
    # VF + VF = Hiato 
    return False


def es_hiato(v1: str, v2: str) -> bool:
    """
    Determina si dos vocales forman hiato (SE separan).
    
    Hiato: VF+VF, o cualquier combinación con VD acentuada
    """
    return not es_diptongo(v1, v2)


def es_digrafo(c1: str, c2: str) -> bool:
    """Determina si dos caracteres forman un dígrafo (ch, ll, rr)."""
    return (c1 + c2).lower() in DIGRAFOS


def es_grupo_inseparable(c1: str, c2: str) -> bool:
    """Determina si dos consonantes forman un grupo inseparable (bl, br, cl, etc.)."""
    return (c1 + c2).lower() in GRUPOS_INSEPARABLES
