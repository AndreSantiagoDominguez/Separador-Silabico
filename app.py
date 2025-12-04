# app.py
# Interfaz de usuario con Streamlit para el Separador Silábico

import streamlit as st
import pandas as pd
import re
from collections import Counter

# Importar módulos del proyecto
from src.core import separar_silabas, procesar_lista_palabras
from src.utils import cargar_diccionario_csv


st.set_page_config(
    page_title="Separador Silábico",
    page_icon="📝",
    layout="wide"
)


st.title("Separador Silábico en Español")
st.write("**Práctica 3** - Lenguajes y Autómatas")
st.write("Simulación de un Autómata Finito Determinista (DFA)")

st.divider()



tab1, tab2, tab3, tab4 = st.tabs([
    " Palabra Individual", 
    " Lista Manual", 
    " Diccionario CSV",
    " Oraciones"
])

with tab1:
    st.subheader("Analizar una palabra")
    
    palabra_input = st.text_input("Escribe una palabra:", key="palabra_individual")
    
    if st.button(" Separar", key="btn_individual"):
        if palabra_input.strip():
            separacion, reglas = separar_silabas(palabra_input)
            
            st.success(f"**Resultado:** {separacion}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Palabra Original", palabra_input.lower())
            with col2:
                st.metric("Número de Sílabas", len(separacion.split('-')))
            
            st.write("**Reglas aplicadas:**")
            for regla in reglas:
                st.write(f"• {regla}")
        else:
            st.warning(" Ingresa una palabra para separar.")


with tab2:
    st.subheader("Procesar lista de palabras")
    st.write("Ingresa una palabra por línea:")
    
    ejemplo = """autonomia
murcielago
teatro
ahorro
computadora
ciencia
cancion"""
    
    texto_input = st.text_area("Lista de palabras:", value=ejemplo, height=200)
    
    if st.button("Procesar Lista", key="btn_lista"):
        if texto_input.strip():
            palabras = texto_input.strip().split('\n')
            resultados = procesar_lista_palabras(palabras)
            
            st.subheader(f"Resultados ({len(resultados)} palabras):")
            
            # Crear DataFrame
            df = pd.DataFrame(resultados)
            df.columns = ['Palabra Original', 'Separación Silábica', 'Reglas Aplicadas']
            st.dataframe(df, use_container_width=True)
            
            # Generar archivo de salida
            salida_txt = "Palabra Original\tSeparación Silábica\tRegla(s) Aplicada(s)\n"
            salida_txt += "=" * 60 + "\n"
            for r in resultados:
                salida_txt += f"{r['original']}\t{r['separacion']}\t{r['reglas']}\n"
            
            st.download_button(
                label="Descargar tokens_salida.txt",
                data=salida_txt,
                file_name="tokens_salida.txt",
                mime="text/plain"
            )
        else:
            st.warning("Ingresa al menos una palabra.")


with tab3:
    st.subheader("Procesar diccionario CSV")
    st.write("Procesa las palabras del diccionario español (1000+ palabras)")
    
    ruta_csv = "data/diccionario_espanol.csv"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        num_palabras = st.slider(
            "Número de palabras a procesar:", 
            min_value=10, 
            max_value=500, 
            value=50, 
            step=10
        )
    
    if st.button(" Procesar Diccionario", key="btn_csv"):
        palabras = cargar_diccionario_csv(ruta_csv)
        
        if palabras:
            st.success(f" Se cargaron {len(palabras)} palabras del diccionario")
            
            palabras_a_procesar = palabras[:num_palabras]
            resultados = []
            
            progress_bar = st.progress(0)
            for i, palabra in enumerate(palabras_a_procesar):
                separacion, reglas = separar_silabas(palabra)
                resultados.append({
                    'original': palabra,
                    'separacion': separacion,
                    'reglas': ", ".join(reglas)
                })
                progress_bar.progress((i + 1) / len(palabras_a_procesar))
            
            st.subheader(f" Resultados ({len(resultados)} palabras):")
            
            df_resultados = pd.DataFrame(resultados)
            df_resultados.columns = ['Palabra Original', 'Separación Silábica', 'Reglas Aplicadas']
            st.dataframe(df_resultados, use_container_width=True, height=400)
            
            # Generar archivo de salida
            salida_txt = "Palabra Original\tSeparación Silábica\tRegla(s) Aplicada(s)\n"
            salida_txt += "=" * 70 + "\n"
            for r in resultados:
                salida_txt += f"{r['original']}\t{r['separacion']}\t{r['reglas']}\n"
            
            st.download_button(
                label=" Descargar tokens_salida.txt",
                data=salida_txt,
                file_name="tokens_salida.txt",
                mime="text/plain",
                key="download_csv"
            )
            
            # Estadísticas
            st.subheader(" Estadísticas:")
            
            todas_reglas = []
            for r in resultados:
                todas_reglas.extend(r['reglas'].split(", "))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total palabras", len(resultados))
            with col2:
                st.metric("Diptongos", sum(1 for r in todas_reglas if "Diptongo" in r))
            with col3:
                st.metric("Hiatos", sum(1 for r in todas_reglas if "Hiato" in r))
        else:
            st.error(" No se pudieron cargar las palabras del CSV. Verifica que el archivo exista en data/")


with tab4:
    st.subheader("Analizar oraciones completas")
    st.write("Escribe una oración y se separarán las sílabas de cada palabra:")
    
    oracion_ejemplo = "Hola buenas tardes como están todos"
    oracion_input = st.text_area(
        "Escribe una oración:", 
        value=oracion_ejemplo, 
        height=100, 
        key="oracion"
    )
    
    if st.button(" Analizar Oración", key="btn_oracion"):
        if oracion_input.strip():
            # Extraer solo palabras (eliminar puntuación)
            palabras_oracion = re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+', oracion_input)
            
            if palabras_oracion:
                resultados = []
                oracion_separada = []
                
                for palabra in palabras_oracion:
                    separacion, reglas = separar_silabas(palabra)
                    oracion_separada.append(separacion)
                    resultados.append({
                        'original': palabra.lower(),
                        'separacion': separacion,
                        'reglas': ", ".join(reglas)
                    })
                
                # Mostrar oración completa separada
                st.success(f"**Oración separada:** {' | '.join(oracion_separada)}")
                
                st.write("")
                
                # Mostrar tabla detallada
                df = pd.DataFrame(resultados)
                df.columns = ['Palabra', 'Separación', 'Reglas']
                st.dataframe(df, use_container_width=True)
                
                # Generar archivo de salida
                salida_txt = f"Oración original: {oracion_input}\n"
                salida_txt += f"Oración separada: {' | '.join(oracion_separada)}\n"
                salida_txt += "=" * 60 + "\n"
                salida_txt += "Palabra\tSeparación\tReglas\n"
                salida_txt += "-" * 60 + "\n"
                for r in resultados:
                    salida_txt += f"{r['original']}\t{r['separacion']}\t{r['reglas']}\n"
                
                st.download_button(
                    label=" Descargar análisis",
                    data=salida_txt,
                    file_name="oracion_analizada.txt",
                    mime="text/plain",
                    key="download_oracion"
                )
            else:
                st.warning(" No se encontraron palabras válidas en la oración.")
        else:
            st.warning(" Escribe una oración para analizar.")


st.divider()

# Sección informativa
with st.expander("ℹ️ Información sobre las reglas silábicas"):
    st.markdown("""
    ### Alfabeto Lógico
    - **Vocales Fuertes (VF):** a, e, o, á, é, ó
    - **Vocales Débiles (VD):** i, u, í, ú
    - **Dígrafos:** ch, ll, rr (se tratan como una consonante)
    - **Grupos Inseparables:** bl, br, cl, cr, dr, fl, fr, gl, gr, pl, pr, tr, etc.
    
    ### Reglas de Separación
    
    **Vocálicas (Diptongos e Hiatos):**
    - VF + VD → Diptongo (NO se separa): *ai-re*
    - VD + VF → Diptongo (NO se separa): *pue-blo*
    - VD + VD → Diptongo (NO se separa): *cui-dar*
    - VF + VF → Hiato (SE separa): *te-a-tro*
    - VD acentuada → Hiato (SE separa): *ma-rí-a*
    
    **Consonánticas:**
    - V-C-V → La consonante va con la segunda vocal: *ca-sa*
    - V-CC-V → Se separan: *can-to*
    - Grupos inseparables (bl, br, cl, etc.) → NO se separan: *a-bril*
    - Dígrafos (ch, ll, rr) → NO se separan: *a-rro-z*
    """)

st.divider()
st.caption("UP Chiapas · Práctica 3 · Lenguajes y Autómatas")
