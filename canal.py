import numpy as np
import random

def aplicar_ruido(trama, probabilidad=0.1):
    trama_ruidosa = trama.copy()
    # Recorremos cada bloque de 7 bits
    filas, cols = trama.shape
    errores_totales = 0
    
    for i in range(filas):
        if random.random() < probabilidad:
            bit_a_cambiar = random.randint(0, 6)
            trama_ruidosa[i][bit_a_cambiar] = (trama_ruidosa[i][bit_a_cambiar] + 1) % 2
            errores_totales += 1
            
    return trama_ruidosa, errores_totales
