import tkinter as tk
from tkinter import ttk, messagebox
from gauss_seidel import gauss_seidel, is_strictly_diagonally_dominant, reorder_to_dominant, validate_inputs
from manual import show_manual

def create_table(main_frame):
    """
    Crea y configura la tabla para mostrar los resultados de las iteraciones.
    """
    columns = ("Iteración", "X", "Y", "Z", "Error")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    
    # Configuración de encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=80, anchor="center")

    # Configuración de scroll vertical
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Posicionar la tabla y el scroll
    tree.grid(row=13, column=0, columnspan=3, pady=10, sticky="nsew")
    scrollbar.grid(row=13, column=3, sticky="ns")
    
    return tree

def update_table(tree, results):
    """
    Actualiza la tabla con los resultados obtenidos en las iteraciones.
    
    :param tree: Widget de la tabla.
    :param results: Lista de resultados de las iteraciones.
    """
    # Limpiar los resultados anteriores
    tree.delete(*tree.get_children())
    
    # Insertar los nuevos resultados en la tabla
    for result in results:
        formatted_result = [f"{val:.4f}" for val in result]
        tree.insert("", tk.END, values=formatted_result)

def show_reordered_matrix(matrix, reordered_label):
    """
    Muestra la matriz reordenada de forma clara en la interfaz.
    
    :param matrix: Matriz reordenada.
    :param reordered_label: Widget Label para mostrar la matriz.
    """
    matrix_text = "Matriz reordenada:\n" + "\n".join(
        " | ".join(f"{val:.4f}" for val in row) for row in matrix
    )
    reordered_label.config(text=matrix_text)

def reset_entries(entries, entries_b, entries_x0):
    """
    Restablece los campos de entrada a sus valores predeterminados.
    
    :param entries: Lista de entradas para la matriz A.
    :param entries_b: Entradas del vector b.
    :param entries_x0: Entradas del vector inicial x0.
    """
    # Restablecer entradas de la matriz A y el vector b
    for i in range(3):
        for j in range(3):
            entries[i][j].delete(0, tk.END)
        entries_b[i].delete(0, tk.END)

    # Restablecer entradas de x0 a 0
    for entry in entries_x0:
        entry.delete(0, tk.END)
        entry.insert(0, "0")

def reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label):
    """
    Restablece todos los campos de entrada y limpia los resultados mostrados.
    
    :param entries: Entradas de la matriz A.
    :param entries_b: Entradas del vector b.
    :param entries_x0: Entradas del vector inicial x0.
    :param tol_entry: Entrada de la tolerancia.
    :param result_label: Widget para mostrar los resultados.
    :param tree: Widget de la tabla de resultados.
    :param reordered_label: Widget para mostrar la matriz reordenada.
    """
    reset_entries(entries, entries_b, entries_x0)
    tol_entry.delete(0, tk.END)
    tol_entry.insert(0, "1e-4")
    result_label.config(text="Solución:")
    reordered_label.config(text="")
    tree.delete(*tree.get_children())  # Limpiar tabla

def solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label):
    """
    Resuelve el sistema de ecuaciones usando Gauss-Seidel y actualiza la interfaz.
    
    :param entries: Entradas de la matriz A.
    :param entries_b: Entradas del vector b.
    :param entries_x0: Entradas del vector inicial x0.
    :param tol_entry: Entrada de la tolerancia.
    :param result_label: Widget para mostrar los resultados.
    :param tree: Widget de la tabla de resultados.
    :param reordered_label: Widget para mostrar la matriz reordenada.
    """
    # Validar y obtener las entradas
    A, b, x0, tol = validate_inputs(entries, entries_b, entries_x0, tol_entry)
    if A is None:
        return  # Salir si hay un error en las entradas

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
        result_label.config(text=(
            f"Solución:\n"
            f"X = {final_result[1]:.4f}, Y = {final_result[2]:.4f}, Z = {final_result[3]:.4f}\n"
            f"Error en X: {final_result[4]:.4f}%"
        ))

    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")

# Configuración de la interfaz gráfica
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

# Botones
button_frame = tk.Frame(main_frame)
button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 10))

solve_button = tk.Button(button_frame, text="Resolver", command=lambda: solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label), width=10)
solve_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Restablecer", command=lambda: reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label), width=10)
reset_button.grid(row=0, column=1, padx=5)

manual_button = tk.Button(button_frame, text="Manual de Usuario", command=show_manual, width=15)
manual_button.grid(row=0, column=2, padx=5)

# Etiqueta para mostrar la matriz reordenada
reordered_label = tk.Label(main_frame, text="", font=("Arial", 10, "bold"), anchor="center", justify="center")
reordered_label.grid(row=11, column=0, columnspan=3, pady=10)

# Etiqueta para mostrar el resultado final
result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

# Crear tabla para mostrar resultados
tree = create_table(main_frame)

root.mainloop()