# Utilidades para cargar datos de entrada

import pandas as pd
from typing import List, Optional


def cargar_diccionario_csv(ruta_csv: str) -> List[str]:
    """
    Carga las palabras desde un archivo CSV del diccionario.
    
    Args:
        ruta_csv: Ruta al archivo CSV con las palabras
        
    Returns:
        Lista de palabras válidas ordenadas alfabéticamente
    """
    try:
        df = pd.read_csv(ruta_csv)
        
        # Obtener palabras de ambas columnas
        palabras_frecuencia = df['Frecuencia'].astype(str).str.lower().tolist()
        palabras_alfabetico = df['Alfabético'].astype(str).str.lower().tolist()
        
        # Unir ambas columnas y eliminar duplicados
        todas_palabras = list(set(palabras_frecuencia + palabras_alfabetico))
        
        # Filtrar solo palabras válidas (alfabéticas)
        palabras_validas = [p for p in todas_palabras if p.isalpha()]
        
        return sorted(palabras_validas)
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_csv}")
        return []
    except KeyError as e:
        print(f"Error: Columna no encontrada en el CSV - {e}")
        return []
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        return []


def cargar_palabras_txt(ruta_txt: str) -> List[str]:
    """
    Carga palabras desde un archivo de texto (una por línea).
    
    Args:
        ruta_txt: Ruta al archivo de texto
        
    Returns:
        Lista de palabras
    """
    try:
        with open(ruta_txt, 'r', encoding='utf-8') as f:
            palabras = [linea.strip() for linea in f if linea.strip()]
        return palabras
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_txt}")
        return []
    except Exception as e:
        print(f"Error cargando archivo: {e}")
        return []


def guardar_resultados(resultados: List[dict], ruta_salida: str) -> bool:
    """
    Guarda los resultados del análisis en un archivo de texto.
    
    Args:
        resultados: Lista de diccionarios con los resultados
        ruta_salida: Ruta del archivo de salida
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write("Palabra Original\tSeparación Silábica\tRegla(s) Aplicada(s)\n")
            f.write("=" * 70 + "\n")
            
            for r in resultados:
                f.write(f"{r['original']}\t{r['separacion']}\t{r['reglas']}\n")
        
        return True
    
    except Exception as e:
        print(f"Error guardando archivo: {e}")
        return False
