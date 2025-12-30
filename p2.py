import tkinter as tk
from tkinter import messagebox

# --- LÓGICA HAMMING (11,7) ---

def calcular_paridades(code):
    """Calcula paridades p1, p2, p3, p4 basado en un arreglo de 12 posiciones (índice 0 vacío)."""
    # p1: bits 1, 3, 5, 7, 9, 11
    p1 = code[1] ^ code[3] ^ code[5] ^ code[7] ^ code[9] ^ code[11]
    # p2: bits 2, 3, 6, 7, 10, 11
    p2 = code[2] ^ code[3] ^ code[6] ^ code[7] ^ code[10] ^ code[11]
    # p3: bits 4, 5, 6, 7
    p3 = code[4] ^ code[5] ^ code[6] ^ code[7]
    # p4: bits 8, 9, 10, 11
    p4 = code[8] ^ code[9] ^ code[10] ^ code[11]
    return p1, p2, p3, p4

def codificar_hamming(data_bits):
    """Genera el código de 11 bits a partir de 7 bits de datos."""
    if len(data_bits) != 7: raise ValueError("Se requieren 7 bits.")
    d = [int(b) for b in data_bits]
    
    # Arreglo base índice 1..11 (el 0 se ignora)
    code = [0] * 12 
    
    # Colocar datos
    code[3], code[5], code[6], code[7] = d[0], d[1], d[2], d[3]
    code[9], code[10], code[11] = d[4], d[5], d[6]
    
    # Calcular paridades (inicialmente asumiendo p=0 para el cálculo)
    # Nota: En Hamming generativo, p_i = XOR(datos que cubre).
    # Aquí usamos la propiedad: p_i ^ check(datos) = 0 => p_i = check(datos)
    # Así que el cálculo es directo sobre los datos.
    
    p1_val = code[3] ^ code[5] ^ code[7] ^ code[9] ^ code[11]
    p2_val = code[3] ^ code[6] ^ code[7] ^ code[10] ^ code[11]
    p3_val = code[5] ^ code[6] ^ code[7]
    p4_val = code[9] ^ code[10] ^ code[11]
    
    code[1], code[2], code[4], code[8] = p1_val, p2_val, p3_val, p4_val
    return code  # Retorna lista de 12 elementos

def decodificar_corregir(code_recibido):
    """Recibe lista de 12 elementos (índice 0 ignorado). Retorna (pos_error, p_calculados)."""
    # Recalculamos paridad sobre TODO el grupo (incluyendo el bit de paridad recibido)
    # Si todo está bien, el XOR de cada grupo debe dar 0.
    
    c1 = code_recibido[1] ^ code_recibido[3] ^ code_recibido[5] ^ code_recibido[7] ^ code_recibido[9] ^ code_recibido[11]
    c2 = code_recibido[2] ^ code_recibido[3] ^ code_recibido[6] ^ code_recibido[7] ^ code_recibido[10] ^ code_recibido[11]
    c3 = code_recibido[4] ^ code_recibido[5] ^ code_recibido[6] ^ code_recibido[7]
    c4 = code_recibido[8] ^ code_recibido[9] ^ code_recibido[10] ^ code_recibido[11]
    
    # El síndrome es el número binario (c4 c3 c2 c1)
    pos_error = c1 * 1 + c2 * 2 + c3 * 4 + c4 * 8
    return pos_error, (c1, c2, c3, c4)

# --- GUI ---

class HammingCompletoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Hamming (11,7) - Emisor y Receptor")
        self.root.geometry("900x600")

        # --- SECCIÓN 1: EMISOR ---
        frame_emisor = tk.LabelFrame(root, text="1. EMISOR (Generar Código)", padx=10, pady=10)
        frame_emisor.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_emisor, text="Datos (7 bits):").pack(side="left")
        self.entry_datos = tk.Entry(frame_emisor, width=10, font=("Arial", 12))
        self.entry_datos.pack(side="left", padx=5)
        self.entry_datos.insert(0, "1011001") # Ejemplo por defecto
        
        tk.Button(frame_emisor, text="Generar y Enviar", command=self.iniciar_generacion, bg="#dddddd").pack(side="left", padx=10)

        # Tabla visualización generación
        self.frame_tabla = tk.Frame(root)
        self.frame_tabla.pack(pady=5)
        self.labels_grid = []
        self.crear_rejilla_generacion()

        # --- SECCIÓN 2: CANAL Y RECEPTOR ---
        frame_receptor = tk.LabelFrame(root, text="2. CANAL CON RUIDO (Haz clic en los bits para introducir error)", padx=10, pady=10)
        frame_receptor.pack(fill="x", padx=10, pady=10)

        self.frame_bits = tk.Frame(frame_receptor)
        self.frame_bits.pack(pady=10)
        
        self.botones_bits = []
        self.bits_actuales = [0]*12 # Estado actual del canal

        self.lbl_info_canal = tk.Label(frame_receptor, text="Esperando transmisión...", fg="gray")
        self.lbl_info_canal.pack()

        self.btn_corregir = tk.Button(frame_receptor, text="Detectar y Corregir Error", state="disabled", command=self.iniciar_correccion, bg="lightblue")
        self.btn_corregir.pack(pady=5)
        
        self.lbl_resultado = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="blue")
        self.lbl_resultado.pack(pady=10)

    def crear_rejilla_generacion(self):
        headers = ["Pos", "p1", "p2", "d1", "p3", "d2", "d3", "d4", "p4", "d5", "d6", "d7"]
        for j, h in enumerate(headers):
            tk.Label(self.frame_tabla, text=h, borderwidth=1, relief="solid", width=4, bg="#f0f0f0").grid(row=0, column=j)
        
        # Fila de contenido
        self.fila_gen = []
        tk.Label(self.frame_tabla, text="Bits:", borderwidth=1, relief="solid", width=4).grid(row=1, column=0)
        for j in range(1, 12):
            l = tk.Label(self.frame_tabla, text="", borderwidth=1, relief="solid", width=4, font=("Arial", 10))
            l.grid(row=1, column=j, sticky="nsew")
            self.fila_gen.append(l)

    def iniciar_generacion(self):
        datos = self.entry_datos.get().strip()
        if len(datos) != 7 or any(c not in "01" for c in datos):
            messagebox.showerror("Error", "Deben ser 7 bits (0s y 1s).")
            return

        # 1. Calcular Hamming
        codigo_enviado = codificar_hamming(datos)
        
        # 2. Mostrar en tabla superior (visualización simple)
        for i in range(1, 12):
            es_paridad = i in [1, 2, 4, 8]
            color = "#ffebcd" if es_paridad else "white" # Beige para paridad
            self.fila_gen[i-1].config(text=str(codigo_enviado[i]), bg=color)

        # 3. Preparar el Canal (Botones)
        self.preparar_canal(codigo_enviado)

    def preparar_canal(self, codigo):
        # Limpiar botones anteriores
        for widget in self.frame_bits.winfo_children():
            widget.destroy()
        
        self.botones_bits = []
        self.bits_actuales = list(codigo) # Copia
        
        # Crear 11 botones
        for i in range(1, 12):
            # Frame para agrupar etiqueta pos y botón
            f = tk.Frame(self.frame_bits)
            f.pack(side="left", padx=2)
            
            tk.Label(f, text=f"{i}", font=("Arial", 8)).pack()
            
            btn = tk.Button(f, text=str(codigo[i]), font=("Arial", 14, "bold"), width=2,
                            command=lambda pos=i: self.toggle_bit(pos))
            # Colorear paridades diferente para identificar
            if i in [1, 2, 4, 8]:
                btn.config(relief="groove", borderwidth=3)
            
            btn.pack()
            self.botones_bits.append(btn)
        
        self.lbl_info_canal.config(text="¡Transmisión recibida! Haz clic en un bit para simular ruido (error).", fg="black")
        self.btn_corregir.config(state="normal")
        self.lbl_resultado.config(text="")

    def toggle_bit(self, pos):
        # Invertir bit en memoria
        val_actual = self.bits_actuales[pos]
        nuevo_val = 1 - val_actual
        self.bits_actuales[pos] = nuevo_val
        
        # Actualizar botón visualmente
        btn = self.botones_bits[pos-1]
        btn.config(text=str(nuevo_val), fg="red", bg="#ffcccc") # Rojo para indicar "tocado"

    def iniciar_correccion(self):
        # 1. Calcular Síndrome
        pos_error, (c1, c2, c3, c4) = decodificar_corregir(self.bits_actuales)
        
        sindrome_bin = f"{c4}{c3}{c2}{c1}" # Orden p4..p1
        
        texto_res = f"Análisis de Paridad:\n" \
                    f"C1 (grupo 1) = {c1}\n" \
                    f"C2 (grupo 2) = {c2}\n" \
                    f"C3 (grupo 4) = {c3}\n" \
                    f"C4 (grupo 8) = {c4}\n" \
                    f"--------------------\n" \
                    f"Síndrome: {sindrome_bin} (Binario) -> Posición: {pos_error}"
        
        if pos_error == 0:
            self.lbl_resultado.config(text="RESULTADO: ¡No hay errores!", fg="green")
            messagebox.showinfo("Receptor", "Transmisión correcta.\n\n" + texto_res)
        else:
            self.lbl_resultado.config(text=f"ERROR DETECTADO EN POSICIÓN {pos_error}", fg="red")
            messagebox.showwarning("Error Encontrado", f"¡Se detectó un bit corrupto!\n\n{texto_res}\n\nCorrigiendo ahora...")
            
            # Corregir visualmente
            self.animar_correccion(pos_error)

    def animar_correccion(self, pos):
        if pos < 1 or pos > 11: return # Fuera de rango (raro)
        
        # 1. Resaltar botón malo
        btn = self.botones_bits[pos-1]
        btn.config(bg="red", fg="white")
        self.root.update()
        self.root.after(1000) # Pausa dramática
        
        # 2. Corregir valor
        val_corregido = 1 - self.bits_actuales[pos]
        self.bits_actuales[pos] = val_corregido
        
        # 3. Actualizar botón a "arreglado"
        btn.config(text=str(val_corregido), bg="#90ee90", fg="black") # Verde claro
        self.lbl_resultado.config(text=f"ERROR EN POS {pos} CORREGIDO. Mensaje recuperado.", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = HammingCompletoGUI(root)
    root.mainloop()