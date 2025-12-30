import numpy as np
import matplotlib.pyplot as plt
from PIL import Image # Requiere: pip install pillow

def cargar_imagen_a_bits(ruta_imagen):
    """
    Carga una imagen, la convierte a escala de grises, luego a blanco y negro,
    y finalmente retorna un array de bits (0s y 1s) y las dimensiones originales.
    """
    # 1. Abrir imagen y convertir a escala de grises (L)
    img = Image.open(ruta_imagen).convert('L')
    
    # 2. Redimensionar para que la simulación no sea eterna (Recomendado 50x50 o 60x60)
    img = img.resize((50, 50)) 
    
    # 3. Convertir a numpy array y binarizar (Umbral 128)
    img_array = np.array(img)
    bits_array = (img_array > 128).astype(int) # True/False a 1/0
    
    # 4. Aplanar a una lista de bits
    bits_planos = bits_array.flatten()
    
    return bits_planos, bits_array.shape

def bits_a_imagen(bits, forma, titulo="Imagen Reconstruida"):
    """
    Toma los bits, los reacomoda en la forma original y muestra la imagen.
    """
    # Aseguramos que la cantidad de bits coincida con la forma (recortando sobras de relleno)
    total_pixeles = forma[0] * forma[1]
    bits_limpios = bits[:total_pixeles]
    
    img_reconstruida = np.array(bits_limpios).reshape(forma)
    
    return img_reconstruida