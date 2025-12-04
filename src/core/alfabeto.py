# Definición del alfabeto lógico para el separador silábico

# Vocales fuertes (siempre forman núcleo silábico propio)
VOCALES_FUERTES = set('aeoáéó')

# Vocales débiles (pueden unirse en diptongos o formar hiato si tienen tilde)
VOCALES_DEBILES = set('iuíú')

# Vocales débiles acentuadas (rompen diptongo = hiato)
VOCALES_DEBILES_ACENTUADAS = set('íú')

# Todas las vocales
VOCALES = VOCALES_FUERTES | VOCALES_DEBILES

# Dígrafos (se tratan como una sola consonante)
DIGRAFOS = ['ch', 'll', 'rr']

# Grupos consonánticos inseparables (la segunda es 'l' o 'r')
GRUPOS_INSEPARABLES = [
    'bl', 'br', 'cl', 'cr', 'dl', 'dr', 'fl', 'fr',
    'gl', 'gr', 'pl', 'pr', 'tl', 'tr', 'kl', 'kr'
]
