import numpy as np
import matplotlib.pyplot as plt
from hamming import codificar_bloque, decodificar_bloque
from canal import aplicar_ruido
from utils import cargar_imagen_a_bits, bits_a_imagen # <--- Importamos lo nuevo

def main():
    print("--- SISTEMA DE TRANSMISIÓN CON HAMMING (7,4) ---")
    
    # A. CARGAR IMAGEN REAL
    # Asegúrate de tener una imagen llamada 'test.jpg' en la carpeta
    try:
        bits_mensaje, dimensiones = cargar_imagen_a_bits('perro.jpg')
    except FileNotFoundError:
        print("ERROR: No se encontró 'test.jpg'. Asegúrate de poner una imagen en la carpeta.")
        return

    # Relleno (Padding) para que sea divisible por 4
    padding = 0
    while len(bits_mensaje) % 4 != 0:
        bits_mensaje = np.append(bits_mensaje, 0)
        padding += 1
        
    bloques_4 = bits_mensaje.reshape(-1, 4)
    print(f"Imagen cargada: {dimensiones[0]}x{dimensiones[1]} pixeles.")
    print(f"Total de bloques a transmitir: {len(bloques_4)}")

    # B. CODIFICACIÓN
    print("Codificando...")
    bloques_codificados = np.array([codificar_bloque(b) for b in bloques_4])
    
    # C. CANAL CON RUIDO
    print("Enviando a través del canal ruidoso...")
    # Probabilidad 0.15 es un buen equilibrio para ver errores pero poder corregirlos
    bloques_recibidos, num_errores = aplicar_ruido(bloques_codificados, probabilidad=0.15)
    print(f"--> Se inyectaron {num_errores} errores en la transmisión.")

    # D. DECODIFICACIÓN
    print("Decodificando y corrigiendo...")
    bits_corregidos = []
    bits_sin_corregir = []
    
    for i in range(len(bloques_recibidos)):
        # Con Hamming
        recuperado = decodificar_bloque(bloques_recibidos[i].copy())
        bits_corregidos.extend(recuperado)
        
        # Sin Hamming (Simulación: tomamos los últimos 4 bits tal cual llegaron)
        bits_sin_corregir.extend(bloques_recibidos[i][3:]) 

    # E. VISUALIZACIÓN
    img_original = bits_a_imagen(bits_mensaje, dimensiones)
    img_ruidosa = bits_a_imagen(bits_sin_corregir, dimensiones)
    img_corregida = bits_a_imagen(bits_corregidos, dimensiones)

    fig, axs = plt.subplots(1, 3, figsize=(12, 5))
    axs[0].imshow(img_original, cmap='gray'); axs[0].set_title("Original")
    axs[1].imshow(img_ruidosa, cmap='gray'); axs[1].set_title(f"Sin Corrección\n(~{num_errores} errores)")
    axs[2].imshow(img_corregida, cmap='gray'); axs[2].set_title("Con Hamming (Corregida)")
    plt.show()

if __name__ == "__main__":
    main()