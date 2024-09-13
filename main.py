import tkinter as tk
from gauss_seidel import solve_system
from manual import show_manual
from utils import reset_fields

# Configuración de la ventana principal de la aplicación
root = tk.Tk()
root.title("Solución de Sistemas de Ecuaciones 3x3 - Gauss-Seidel")  # Título de la ventana
root.geometry("")  # Ajusta automáticamente el tamaño de la ventana al contenido
root.resizable(True, True)  # Permitir que la ventana se pueda redimensionar

# Crear un frame principal con padding para colocar los widgets centrados
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Crear las entradas para la matriz A (coeficientes de las ecuaciones)
entries = [[tk.Entry(main_frame, width=5, justify="center") for _ in range(3)] for _ in range(3)]
# Crear las entradas para el vector b (términos independientes)
entries_b = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
# Crear las entradas para los valores iniciales (vector x0)
entries_x0 = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
# Crear la entrada para la tolerancia
tol_entry = tk.Entry(main_frame, width=5, justify="center")
tol_entry.insert(0, "1e-4")  # Establecer el valor predeterminado para la tolerancia

# Etiqueta para la matriz A (coeficientes)
tk.Label(main_frame, text="Coeficientes de la matriz A:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))
# Colocar las entradas de la matriz A en la interfaz
for i in range(3):
    for j in range(3):
        entries[i][j].grid(row=i+1, column=j, padx=5, pady=5)

# Etiqueta para el vector b
tk.Label(main_frame, text="Términos independientes (vector b):", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=3, pady=(10, 0))
# Colocar las entradas del vector b en la interfaz
for i in range(3):
    entries_b[i].grid(row=5, column=i, padx=5, pady=5)

# Etiqueta para los valores iniciales (vector x0)
tk.Label(main_frame, text="Valores iniciales (vector x0):", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=3, pady=(10, 0))
# Colocar las entradas de los valores iniciales (vector x0)
for i in range(3):
    entries_x0[i].grid(row=7, column=i, padx=5, pady=5)

# Etiqueta para la tolerancia
tk.Label(main_frame, text="Tolerancia:", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=3, pady=(10, 0))
# Colocar la entrada de tolerancia
tol_entry.grid(row=9, column=0, columnspan=3, pady=5)

# Frame para colocar los botones (Resolver y Restablecer) alineados
button_frame = tk.Frame(main_frame)
button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 10))

# Etiqueta para mostrar la matriz dominante resultante
dominant_matrix_label = tk.Label(main_frame, text="Matriz Dominante:", font=("Arial", 10, "bold"), anchor="center", justify="center")
dominant_matrix_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

# Etiqueta para mostrar el resultado de la solución
result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=13, column=0, columnspan=3, pady=(10, 0))

# Botón para resolver el sistema de ecuaciones
solve_button = tk.Button(button_frame, text="Resolver", command=lambda: solve_system(entries, entries_b, entries_x0, tol_entry, dominant_matrix_label, result_label), width=10)
solve_button.grid(row=0, column=0, padx=5)

# Botón para restablecer todos los campos
reset_button = tk.Button(button_frame, text="Restablecer", command=lambda: reset_fields(entries, entries_b, entries_x0, tol_entry, dominant_matrix_label, result_label), width=10)
reset_button.grid(row=0, column=1, padx=5)

# Botón para mostrar el manual de usuario
manual_button = tk.Button(main_frame, text="Manual de Usuario", command=show_manual, width=15)
manual_button.grid(row=11, column=0, columnspan=3, pady=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()