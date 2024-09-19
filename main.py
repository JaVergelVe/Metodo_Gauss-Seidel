import tkinter as tk
from tkinter import ttk, messagebox
from gauss_seidel import gauss_seidel, is_strictly_diagonally_dominant, reorder_to_dominant, validate_inputs
from manual import show_manual

# Función para crear la tabla de resultados
def create_table(main_frame):
    columns = ("Iteración", "X", "Y", "Z", "Error")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    
    # Configuración de encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=80, anchor="center")

    # Scroll vertical
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.grid(row=14, column=0, columnspan=3, pady=10, sticky="nsew")
    scrollbar.grid(row=14, column=3, sticky="ns")
    
    return tree

# Función para actualizar la tabla con los resultados de cada iteración
def update_table(tree, results):
    tree.delete(*tree.get_children())  # Limpiar la tabla existente
    
    for result in results:
        formatted_result = [f"{val:.4f}" for val in result]
        tree.insert("", tk.END, values=formatted_result)

# Función para mostrar la matriz reordenada
def show_reordered_matrix(matrix, reordered_label):
    matrix_text = "Matriz reordenada:\n" + "\n".join(
        " | ".join(f"{val:.4f}" for val in row) for row in matrix
    )
    reordered_label.config(text=matrix_text)

# Función para mostrar cómo quedan despejadas las ecuaciones
def show_equation_despejes(A, b, despeje_label):
    despeje_text = (
        f"Despejes de las ecuaciones:\n"
        f"X = ({b[0]} - ({A[0][1]}*Y + {A[0][2]}*Z)) / {A[0][0]}\n"
        f"Y = ({b[1]} - ({A[1][0]}*X + {A[1][2]}*Z)) / {A[1][1]}\n"
        f"Z = ({b[2]} - ({A[2][0]}*X + {A[2][1]}*Y)) / {A[2][2]}"
    )
    despeje_label.config(text=despeje_text)

# Función para restablecer todos los campos y limpiar los resultados
def reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label, despeje_label):
    for i in range(3):
        for j in range(3):
            entries[i][j].delete(0, tk.END)
        entries_b[i].delete(0, tk.END)
        entries_x0[i].delete(0, tk.END)
        entries_x0[i].insert(0, "0")

    tol_entry.delete(0, tk.END)
    tol_entry.insert(0, "1e-4")
    result_label.config(text="Solución:")
    reordered_label.config(text="")
    despeje_label.config(text="")
    tree.delete(*tree.get_children())  # Limpiar la tabla

# Función para resolver el sistema y actualizar la interfaz
def solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label, despeje_label):
    # Validar y obtener las entradas
    A, b, x0, tol = validate_inputs(entries, entries_b, entries_x0, tol_entry)
    if A is None:
        return  # Salir si hay un error en las entradas

    # Mostrar los despejes de las ecuaciones
    show_equation_despejes(A, b, despeje_label)

    # Verificar si la matriz es diagonalmente dominante
    if not is_strictly_diagonally_dominant(A):
        A_reordered, b_reordered = reorder_to_dominant(A, b)
        if A_reordered is None:
            result_label.config(text="La ecuación no es diagonalmente dominante y no se puede reordenar.")
            return
        else:
            A, b = A_reordered, b_reordered
            show_reordered_matrix(A, reordered_label)  # Mostrar la matriz reordenada

    try:
        # Resolver el sistema usando Gauss-Seidel
        results = gauss_seidel(A, b, x0, tol)

        # Actualizar la tabla con los resultados de las iteraciones
        update_table(tree, results)
        
        # Mostrar los resultados finales en la interfaz
        final_result = results[-1]
        result_text = (
            f"Solución Final:\n"
            f"Los valores aproximados para las variables son\n"
            f"X = {final_result[1]:.4f}, Y = {final_result[2]:.4f}, Z = {final_result[3]:.4f}\n"
            f"Error en X: {final_result[4]:.4f}%"
        )
        result_label.config(text=result_text)  # Mostrar resultado final

    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Solución de Sistemas de Ecuaciones 3x3 - Gauss-Seidel")
root.geometry("")
root.resizable(True, True)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Entradas para la matriz A, vector b y vector inicial x0
entries = [[tk.Entry(main_frame, width=5, justify="center") for _ in range(3)] for _ in range(3)]
entries_b = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
entries_x0 = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
for entry in entries_x0:
    entry.insert(0, "0")

tol_entry = tk.Entry(main_frame, width=5, justify="center")
tol_entry.insert(0, "1e-4")

# Etiquetas para las entradas
tk.Label(main_frame, text="Coeficientes de la matriz A:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))
for i in range(3):
    for j in range(3):
        entries[i][j].grid(row=i+1, column=j, padx=5, pady=5)

tk.Label(main_frame, text="Términos independientes (vector b):", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=3, pady=(10, 0))
for i in range(3):
    entries_b[i].grid(row=5, column=i, padx=5, pady=5)

tk.Label(main_frame, text="Valores iniciales (vector x0):", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=3, pady=(10, 0))
for i in range(3):
    entries_x0[i].grid(row=7, column=i, padx=5, pady=5)

tk.Label(main_frame, text="Tolerancia:", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=3, pady=(10, 0))
tol_entry.grid(row=9, column=0, columnspan=3, pady=5)

# Sección de botones
button_frame = tk.Frame(main_frame)
button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 10))

solve_button = tk.Button(button_frame, text="Resolver", command=lambda: solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label, despeje_label), width=10)
solve_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Restablecer", command=lambda: reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label, despeje_label), width=10)
reset_button.grid(row=0, column=1, padx=5)

manual_button = tk.Button(button_frame, text="Manual de Usuario", command=show_manual, width=15)
manual_button.grid(row=0, column=2, padx=5)

# Etiqueta para mostrar el despeje de las ecuaciones
despeje_label = tk.Label(main_frame, text="", font=("Arial", 10, "bold"), anchor="center", justify="center")
despeje_label.grid(row=11, column=0, columnspan=3, pady=10)

# Etiqueta para mostrar la matriz reordenada
reordered_label = tk.Label(main_frame, text="", font=("Arial", 10, "bold"), anchor="center", justify="center")
reordered_label.grid(row=12, column=0, columnspan=3, pady=10)

# Etiqueta para mostrar el resultado final
result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=13, column=0, columnspan=3, pady=(10, 0))

# Crear tabla para mostrar resultados
tree = create_table(main_frame)

root.mainloop()