import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import math
import random
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Cálculos: mínimos cuadrados y correlación
# ---------------------------------------------------------
def calcular_parametros_xy(xs, ys):
    n = len(xs)
    if n == 0:
        return None, None, None

    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_x2 = sum(x * x for x in xs)
    sum_y2 = sum(y * y for y in ys)
    sum_xy = sum(x * y for x, y in zip(xs, ys))

    num_a = n * sum_xy - sum_x * sum_y
    den_a = n * sum_x2 - (sum_x ** 2)
    if den_a == 0:
        return None, None, None

    a = num_a / den_a
    b = (sum_y - a * sum_x) / n

    # --- fórmula corregida de r ---
    num_r = n * sum_xy - sum_x * sum_y
    den_r = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
    r = num_r / den_r if den_r != 0 else None
    return a, b, r


def porcentaje_error(vr, vc):
    if vr == 0:
        return None
    return (vc / vr) * 100.0


# ---------------------------------------------------------
# Funciones de interfaz
# ---------------------------------------------------------
xs = []
ys = []

def generar_datos():
    xs.clear()
    ys.clear()

    # Genera datos con correlación alta (r entre 0.9 y 1)
    while True:
        xs[:] = [i for i in range(1, 51)]
        pendiente_real = random.uniform(0.5, 2.0)
        inter_real = random.uniform(2, 10)
        ys[:] = [pendiente_real * x + inter_real + random.uniform(-2, 2) for x in xs]

        a, b, r = calcular_parametros_xy(xs, ys)
        if r is not None and 0.9 <= abs(r) <= 1.0:
            break

    # Actualiza la tabla
    filas = tabla.get_children()
    for i, item in enumerate(filas):
        if i < len(xs):
            tabla.item(item, values=(i + 1, round(xs[i], 2), round(ys[i], 2)))
        else:
            tabla.item(item, values=(i + 1, "", ""))

    messagebox.showinfo("Datos generados", f"Se generaron 50 datos con r = {r:.3f}")
    lbl_resultado.config(text=f"a = {a:.3f}   |   b = {b:.3f}   |   r = {r:.3f}")

def cargar_csv():
    ruta = filedialog.askopenfilename(
        title="Selecciona archivo CSV",
        filetypes=(("Archivos CSV", ".csv"), ("Todos los archivos", ".*"))
    )
    if not ruta:
        return

    xs.clear()
    ys.clear()

    try:
        with open(ruta, newline='', encoding="utf-8") as f:
            lector = csv.reader(f)
            next(lector)  # salta encabezado si lo tiene
            for row in lector:
                if len(row) < 2:
                    continue
                try:
                    x_val = float(row[0])
                    y_val = float(row[1])
                except ValueError:
                    continue
                xs.append(x_val)
                ys.append(y_val)
                if len(xs) == 50:
                    break

        filas = tabla.get_children()
        for i, item in enumerate(filas):
            if i < len(xs):
                tabla.item(item, values=(i + 1, xs[i], ys[i]))
            else:
                tabla.item(item, values=(i + 1, "", ""))

        messagebox.showinfo("CSV", "Datos cargados correctamente.")
        lbl_resultado.config(text="")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")


def graficar():
    if not xs or not ys:
        messagebox.showwarning("Aviso", "Primero carga o genera datos.")
        return

    a, b, r = calcular_parametros_xy(xs, ys)
    if a is None:
        messagebox.showerror("Error", "No se pudieron calcular a, b y r.")
        return

    x_ord = sorted(xs)
    y_recta = [a * x + b for x in x_ord]

    plt.figure()
    plt.scatter(xs, ys, label="Datos", color="#FFB6C1")
    plt.plot(x_ord, y_recta, label=f"Recta: y = {a:.3f}x + {b:.3f}", color="#7EC8E3")
    plt.title(f"Método de mínimos cuadrados (r = {r:.3f})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()

    lbl_resultado.config(
        text=f"a = {a:.3f}   |   b = {b:.3f}   |   r = {r:.3f}"
    )


def mostrar_error():
    if not xs or not ys:
        messagebox.showwarning("Aviso", "Primero carga o genera datos.")
        return

    a, b, r = calcular_parametros_xy(xs, ys)
    if a is None:
        messagebox.showerror("Error", "No se pudieron calcular parámetros.")
        return

    y_real_prom = sum(ys) / len(ys)
    y_calc = [a * x + b for x in xs]
    y_calc_prom = sum(y_calc) / len(y_calc)
    per = porcentaje_error(y_real_prom, y_calc_prom)

    msg = (
        f"V_r (promedio real)  = {y_real_prom:.3f}\n"
        f"V_c (promedio calc.) = {y_calc_prom:.3f}\n"
        f"r = {r:.3f}\n"
        f"%err = (V_c / V_r) × 100 = {per:.2f} %"
    )
    messagebox.showinfo("Error porcentual", msg)
    lbl_resultado.config(
        text=f"a = {a:.3f}   |   b = {b:.3f}   |   r = {r:.3f}   |   Error = {per:.2f} %"
    )


# ---------------------------------------------------------
# INTERFAZ GRÁFICA PASTEL
# ---------------------------------------------------------
root = tk.Tk()
root.title("Coeficiente de correlación y regresión lineal")

# Colores pastel
color_fondo = "#FDF6FF"
color_tabla = "#F3FBFF"
color_encabezado = "#FFEFD5"

root.configure(bg=color_fondo)

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Pastel.Treeview",
    background=color_tabla,
    fieldbackground=color_tabla,
    foreground="black",
    font=("Arial", 10),
    rowheight=24
)
style.configure(
    "Pastel.Treeview.Heading",
    background=color_encabezado,
    foreground="black",
    font=("Arial", 10, "bold")
)

# Frame tabla
frame_tabla = ttk.Frame(root)
frame_tabla.pack(padx=10, pady=10)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("n", "x", "y"),
    show="headings",
    height=18,
    style="Pastel.Treeview"
)

tabla.heading("n", text="n", anchor="center")
tabla.heading("x", text="x", anchor="center")
tabla.heading("y", text="y", anchor="center")

tabla.column("n", width=40, anchor="center")
tabla.column("x", width=100, anchor="center")
tabla.column("y", width=100, anchor="center")

tabla.pack(side="left")

scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
scroll_y.pack(side="right", fill="y")
tabla.configure(yscrollcommand=scroll_y.set)

for i in range(1, 51):
    tabla.insert("", "end", values=(i, "", ""))

# Botones
frame_botones = ttk.Frame(root)
frame_botones.pack(pady=10)

style.configure("Pastel.TButton", font=("Arial", 10))

btn_generar = ttk.Button(frame_botones, text="Generar Datos", style="Pastel.TButton", command=generar_datos)
btn_generar.grid(row=0, column=0, padx=8)

btn_cargar = ttk.Button(frame_botones, text="Cargar CSV", style="Pastel.TButton", command=cargar_csv)
btn_cargar.grid(row=0, column=1, padx=8)

btn_graficar = ttk.Button(frame_botones, text="Graficar", style="Pastel.TButton", command=graficar)
btn_graficar.grid(row=0, column=2, padx=8)

btn_error = ttk.Button(frame_botones, text="Error", style="Pastel.TButton", command=mostrar_error)
btn_error.grid(row=0, column=3, padx=8)

# Resultado
lbl_resultado = tk.Label(root, text="", bg=color_fondo, fg="black", font=("Arial", 11, "bold"))
lbl_resultado.pack(pady=8)

root.mainloop()