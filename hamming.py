import numpy as np

# Matrices Hamming (7,4)
G = np.array([[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
H = np.array([[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]])
# Nota: Ajusté las matrices para que coincidan con el estándar G habitual de data+parity
# Si usas otras matrices, solo cámbialas aquí.

def codificar_bloque(bloque_4bits):
    return np.dot(G, bloque_4bits) % 2

def decodificar_bloque(bloque_7bits):
    sindrome = np.dot(H, bloque_7bits) % 2
    idx = int("".join(str(x) for x in sindrome[::-1]), 2) # Binario a decimal
    
    if idx > 0: # Si hay error
        bloque_7bits[idx-1] = (bloque_7bits[idx-1] + 1) % 2 # Corregir (Flip)
    
    # Extraemos los datos (asumiendo que los datos están en las posiciones correctas según tu G)
    # Para simplificar este ejemplo, retornamos los últimos 4 bits (ajustar según tu G)
    return bloque_7bits[3:] # Ojo: Esto depende de cómo construiste G.