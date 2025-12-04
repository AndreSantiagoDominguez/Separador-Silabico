# Algoritmo principal de separación silábica (DFA)

from typing import Tuple, List
from .alfabeto import DIGRAFOS
from .clasificador import (
    es_vocal, es_consonante, es_diptongo,
    es_digrafo, es_grupo_inseparable
)


def separar_silabas(palabra: str) -> Tuple[str, List[str]]:
    """
    Separa una palabra en sílabas siguiendo las reglas de la RAE.
    Simula el comportamiento de un Autómata Finito Determinista (DFA).
    
    Args:
        palabra: La palabra a separar en sílabas
        
    Returns:
        Tupla con (palabra_separada, lista_reglas_aplicadas)
    """
    palabra = palabra.lower().strip()
    
    if not palabra or not palabra.isalpha():
        return palabra, ["Palabra inválida"]
    
    n = len(palabra)
    silabas = []
    silaba_actual = ""
    reglas = []
    i = 0
    
    while i < n:
        c = palabra[i]
        
        # Verificar si es parte de un dígrafo
        if i + 1 < n and es_digrafo(c, palabra[i + 1]):
            silaba_actual += c + palabra[i + 1]
            i += 2
            continue
        
        silaba_actual += c
        
        # Si es consonante, seguir acumulando
        if es_consonante(c):
            i += 1
            continue
        
        # Es vocal - analizar lo que viene después
        if i + 1 >= n:
            # Última letra, terminar sílaba
            i += 1
            continue
        
        siguiente = palabra[i + 1]
        
        # CASO 1: Siguiente es vocal
        if es_vocal(siguiente):
            if es_diptongo(c, siguiente):
                # Diptongo: no separar, agregar a sílaba actual
                reglas.append(f"Diptongo ({c}{siguiente})")
                i += 1
                continue
            else:
                # Hiato: separar aquí
                reglas.append(f"Hiato ({c}-{siguiente})")
                silabas.append(silaba_actual)
                silaba_actual = ""
                i += 1
                continue
        
        if es_consonante(siguiente):
            # Contar consonantes consecutivas
            consonantes = ""
            j = i + 1
            while j < n and es_consonante(palabra[j]):
                # Verificar dígrafos
                if j + 1 < n and es_digrafo(palabra[j], palabra[j + 1]):
                    consonantes += palabra[j] + palabra[j + 1]
                    j += 2
                else:
                    consonantes += palabra[j]
                    j += 1
            
            # Verificar si hay vocal después de las consonantes
            if j >= n:
                # No hay más vocales, todas las consonantes van con esta sílaba
                silaba_actual += consonantes
                i = j
                continue
            
            # Hay vocal después - aplicar reglas de separación consonántica
            num_cons = len(consonantes)
            
            if num_cons == 1:
                # Una consonante entre vocales: va con la siguiente vocal (V-CV)
                reglas.append("V-C-V")
                silabas.append(silaba_actual)
                silaba_actual = ""
                i += 1
                continue
            
            elif num_cons == 2:
                # Verificar si es dígrafo
                if consonantes.lower() in DIGRAFOS:
                    # Dígrafo: va completo con la siguiente vocal
                    reglas.append(f"Dígrafo ({consonantes})")
                    silabas.append(silaba_actual)
                    silaba_actual = ""
                    i += 1
                    continue
                
                # Verificar si es grupo inseparable
                if es_grupo_inseparable(consonantes[0], consonantes[1]):
                    # Grupo inseparable: va completo con la siguiente vocal
                    reglas.append(f"Grupo inseparable ({consonantes})")
                    silabas.append(silaba_actual)
                    silaba_actual = ""
                    i += 1
                    continue
                
                # Dos consonantes separables: primera con vocal anterior, segunda con siguiente
                reglas.append("C-C")
                silaba_actual += consonantes[0]
                silabas.append(silaba_actual)
                silaba_actual = ""
                i += 2
                continue
            
            elif num_cons >= 3:
                # Tres o más consonantes
                # Verificar si las últimas dos forman grupo inseparable
                if es_grupo_inseparable(consonantes[-2], consonantes[-1]):
                    # Las primeras van con vocal anterior, grupo inseparable con siguiente
                    reglas.append(f"C-C + Grupo ({consonantes[-2:]})") 
                    silaba_actual += consonantes[:-2]
                    silabas.append(silaba_actual)
                    silaba_actual = ""
                    i += 1 + len(consonantes) - 2
                    continue
                elif len(consonantes) >= 2 and consonantes[-2:].lower() in DIGRAFOS:
                    # Las primeras van con vocal anterior, dígrafo con siguiente
                    reglas.append(f"C + Dígrafo ({consonantes[-2:]})")
                    silaba_actual += consonantes[:-2]
                    silabas.append(silaba_actual)
                    silaba_actual = ""
                    i += 1 + len(consonantes) - 2
                    continue
                else:
                    # Separar: todas menos la última van con vocal anterior
                    reglas.append("C-C-C")
                    silaba_actual += consonantes[:-1]
                    silabas.append(silaba_actual)
                    silaba_actual = ""
                    i += len(consonantes)
                    continue
        
        i += 1
    
    # Agregar última sílaba si existe
    if silaba_actual:
        silabas.append(silaba_actual)
    
    # Unir sílabas con guión
    resultado = "-".join(silabas)
    
    # Si no se aplicaron reglas específicas
    if not reglas:
        reglas = ["Palabra simple"]
    
    return resultado, list(set(reglas))


def procesar_lista_palabras(palabras: List[str]) -> List[dict]:
    """
    Procesa una lista de palabras y retorna los resultados.
    
    Args:
        palabras: Lista de palabras a procesar
        
    Returns:
        Lista de diccionarios con 'original', 'separacion' y 'reglas'
    """
    resultados = []
    
    for palabra in palabras:
        palabra = palabra.strip()
        if palabra:
            separacion, reglas = separar_silabas(palabra)
            resultados.append({
                'original': palabra,
                'separacion': separacion,
                'reglas': ", ".join(reglas)
            })
    
    return resultados
