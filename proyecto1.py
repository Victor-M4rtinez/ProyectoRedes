import tkinter as tk
from tkinter import messagebox

# --- Lógica Hamming (11,7) paridad par ---

def calcular_hamming_11_7(data_bits):
    # data_bits: string de 7 bits d1..d7
    if len(data_bits) != 7 or any(c not in "01" for c in data_bits):
        raise ValueError("Se requieren exactamente 7 bits (0/1).")

    d1, d2, d3, d4, d5, d6, d7 = map(int, data_bits)

    # Posiciones: 1:p1, 2:p2, 3:d1, 4:p3, 5:d2, 6:d3, 7:d4, 8:p4, 9:d5, 10:d6, 11:d7
    code = [None] * 12  # índice 1..11
    code[3] = d1
    code[5] = d2
    code[6] = d3
    code[7] = d4
    code[9] = d5
    code[10] = d6
    code[11] = d7

    # Paridades (paridad par, conjuntos típicos Hamming 11,7)
    p1 = (code[3] ^ code[5] ^ code[7] ^ code[9] ^ code[11])
    p2 = (code[3] ^ code[6] ^ code[7] ^ code[10] ^ code[11])
    p3 = (code[5] ^ code[6] ^ code[7])
    p4 = (code[9] ^ code[10] ^ code[11])

    code[1] = p1
    code[2] = p2
    code[4] = p3
    code[8] = p4

    return code[1:], (p1, p2, p3, p4)

# --- GUI ---

class HammingTablaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming (11,7) visual")

        tk.Label(root, text="Datos (7 bits, d1..d7):").grid(row=0, column=0, sticky="w")
        self.entry = tk.Entry(root, width=10)
        self.entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Animar", command=self.iniciar_animacion).grid(row=0, column=2, padx=5)

        # Cabeceras columnas
        headers = ["", "p1", "p2", "d1", "p3", "d2", "d3", "d4", "p4", "d5", "d6", "d7"]
        self.labels = []  # matriz de labels [fila][col]

        for j, h in enumerate(headers):
            lbl = tk.Label(root, text=h, borderwidth=1, relief="solid", width=4)
            lbl.grid(row=1, column=j, sticky="nsew")

        filas_texto = [
            "Palabra de datos (sin paridad):",
            "p1",
            "p2",
            "p3",
            "p4",
            "Palabra de datos (con paridad):"
        ]

        for i, txt in enumerate(filas_texto):
            fila_labels = []
            # Col 0: título fila
            lbl_t = tk.Label(root, text=txt, borderwidth=1, relief="solid", width=25, anchor="w")
            lbl_t.grid(row=2 + i, column=0, sticky="nsew")
            fila_labels.append(lbl_t)
            # Resto celdas vacías
            for j in range(1, 12):
                lbl = tk.Label(root, text="", borderwidth=1, relief="solid", width=4)
                lbl.grid(row=2 + i, column=j, sticky="nsew")
                fila_labels.append(lbl)
            self.labels.append(fila_labels)

        self.pasos = []
        self.indice_paso = 0
        self.intervalo = 200
        self.codigo_final = None
        self.paridades = None

    def limpiar_tabla(self):
        for fila in self.labels:
            for lbl in fila[1:]:
                lbl.config(text="", bg="white")

    def iniciar_animacion(self):
        datos = self.entry.get().strip()
        try:
            codigo, paridades = calcular_hamming_11_7(datos)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.codigo_final = codigo
        self.paridades = paridades

        self.limpiar_tabla()
        self.pasos = []
        self.indice_paso = 0

        # Paso 1-2: colocar palabra sin paridad (solo d1..d7)
        # Fila 0 de self.labels = "sin paridad"
        d_map = list(map(int, datos))  # d1..d7
        pos_to_data = {
            3: d_map[0],
            5: d_map[1],
            6: d_map[2],
            7: d_map[3],
            9: d_map[4],
            10: d_map[5],
            11: d_map[6]
        }
        for pos in range(1, 12):
            if pos in pos_to_data:
                col = pos
                self.pasos.append(("set", 0, col, str(pos_to_data[pos])))

        # Paso 3-6: marcar qué bits usa cada paridad (color)
        # Fila 1..4 de self.labels = p1..p4
        conjuntos = {
            1: [3, 5, 7, 9, 11],   # p1
            2: [3, 6, 7, 10, 11],  # p2
            3: [5, 6, 7],          # p3
            4: [9, 10, 11]         # p4
        }
        colores = {
            1: "lightblue",
            2: "lightgreen",
            3: "khaki",
            4: "lightpink"
        }
        for i_paridad in range(1, 5):
            fila = i_paridad  # fila 1..4
            for pos in conjuntos[i_paridad]:
                self.pasos.append(("mark", fila, pos, colores[i_paridad]))

        # Paso 7-8: rellenar fila final con código completo
        # Fila 5 = "con paridad"
        for pos in range(1, 12):
            self.pasos.append(("set", 5, pos, str(codigo[pos - 1])))

        # Duración total ~8 s
        duracion_total_ms = 8000
        if len(self.pasos) == 0:
            return
        self.intervalo = max(100, duracion_total_ms // len(self.pasos))

        self.ejecutar_siguiente_paso()

    def ejecutar_siguiente_paso(self):
        if self.indice_paso >= len(self.pasos):
            # Animación terminada -> mostrar ventana de resultado
            self.mostrar_ventana_resultado()
            return

        accion, fila, col, valor = self.pasos[self.indice_paso]
        lbl = self.labels[fila][col]

        if accion == "set":
            lbl.config(text=valor, bg="white")
        elif accion == "mark":
            lbl.config(bg=valor)

        self.indice_paso += 1
        self.root.after(self.intervalo, self.ejecutar_siguiente_paso)

    def mostrar_ventana_resultado(self):
        if not self.codigo_final or not self.paridades:
            return

        p1, p2, p3, p4 = self.paridades
        codigo_str = "".join(str(b) for b in self.codigo_final)

        win = tk.Toplevel(self.root)
        win.title("Resultado del código Hamming")
        win.geometry("480x280")

        tk.Label(
            win,
            text="Código Hamming (11,7) generado:",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        tk.Label(
            win,
            text=codigo_str,
            font=("Consolas", 16, "bold")
        ).pack(pady=5)

        texto = (
            "Se usó un código Hamming (11,7) con paridad par.\n"
            "Las posiciones 1, 2, 4 y 8 son bits de paridad (p1, p2, p3, p4).\n"
            "Las demás posiciones (3, 5, 6, 7, 9, 10, 11) son bits de datos (d1..d7).\n\n"
            "Valores de paridad calculados:\n"
            f"  p1 (pos 1)  = {p1}\n"
            f"  p2 (pos 2)  = {p2}\n"
            f"  p3 (pos 4)  = {p3}\n"
            f"  p4 (pos 8)  = {p4}\n\n"
            "Cada bit de paridad se calcula para que el número total de unos\n"
            "en las posiciones que controla sea par (paridad par)."
        )

        lbl_texto = tk.Label(
            win,
            text=texto,
            justify="left",
            font=("Arial", 10)
        )
        lbl_texto.pack(padx=10, pady=5, fill="both", expand=True)

        tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)
        win.grab_set()  # hace la ventana modal


if __name__ == "__main__":
    root = tk.Tk()
    app = HammingTablaGUI(root)
    root.mainloop()
