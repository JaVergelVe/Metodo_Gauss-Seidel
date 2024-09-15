import tkinter as tk
from tkinter import ttk, messagebox
from gauss_seidel import gauss_seidel, is_strictly_diagonally_dominant, reorder_to_dominant, validate_inputs
from manual import show_manual

# Función para crear la tabla
def create_table(main_frame):
    columns = ("Iteración", "X", "Y", "Z", "Error")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    
    tree.heading("Iteración", text="Iteración")
    tree.heading("X", text="X")
    tree.heading("Y", text="Y")
    tree.heading("Z", text="Z")
    tree.heading("Error", text="Error (%)")
    
    tree.column("Iteración", width=80, anchor="center")
    tree.column("X", width=80, anchor="center")
    tree.column("Y", width=80, anchor="center")
    tree.column("Z", width=80, anchor="center")
    tree.column("Error", width=80, anchor="center")
    
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.grid(row=13, column=0, columnspan=3, pady=10, sticky="nsew")
    scrollbar.grid(row=13, column=3, sticky="ns")
    
    return tree

# Función para actualizar la tabla con los resultados de cada iteración
def update_table(tree, results):
    for row in tree.get_children():
        tree.delete(row)
    
    for result in results:
        formatted_result = (
            result[0], 
            f"{result[1]:.4f}",
            f"{result[2]:.4f}",
            f"{result[3]:.4f}",
            f"{result[4]:.4f}"
        )
        tree.insert("", tk.END, values=formatted_result)

# Función para mostrar la matriz reordenada
def show_reordered_matrix(matrix, reordered_label):
    """
    Muestra la matriz reordenada en la interfaz.
    """
    matrix_text = "Matriz reordenada:\n"
    for row in matrix:
        matrix_text += "   ".join(f"{val:.4f}" for val in row) + "\n"
    
    reordered_label.config(text=matrix_text)

# Función para restablecer todos los campos y limpiar la tabla
def reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label):
    for i in range(3):
        for j in range(3):
            entries[i][j].delete(0, tk.END)
        entries_b[i].delete(0, tk.END)
        entries_x0[i].delete(0, tk.END)
    
    for entry in entries_x0:
        entry.insert(0, "0")

    tol_entry.delete(0, tk.END)
    tol_entry.insert(0, "1e-4")
    result_label.config(text="Solución:")
    reordered_label.config(text="")  # Limpiar el texto de la matriz reordenada
    
    for row in tree.get_children():
        tree.delete(row)

# Función para resolver el sistema y actualizar la tabla
def solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label):
    """
    Resuelve el sistema de ecuaciones ingresado y actualiza la tabla.
    Intenta reordenar las filas de la matriz si no es dominante.
    """
    # Validar los datos de entrada
    A, b, x0, tol = validate_inputs(entries, entries_b, entries_x0, tol_entry)
    if A is None:
        return  # Si hay un error en los datos, no hacer nada
    
    # Verificar si la matriz es estrictamente diagonalmente dominante
    if not is_strictly_diagonally_dominant(A):
        # Intentar reordenar la matriz para que sea dominante
        A_reordered, b_reordered = reorder_to_dominant(A, b)
        
        if A_reordered is None:
            # Si no se puede hacer que la matriz sea dominante, mostrar mensaje
            result_label.config(text="La ecuación no es estrictamente diagonalmente dominante y no se puede reordenar.")
            return
        else:
            # Usar la matriz reordenada
            A, b = A_reordered, b_reordered
            show_reordered_matrix(A, reordered_label)  # Mostrar la matriz reordenada en la interfaz
    
    try:
        # Llamar al método de Gauss-Seidel y obtener los resultados de cada iteración
        results = gauss_seidel(A, b, x0, tol=tol)
        
        # Mostrar los resultados de todas las iteraciones en la tabla
        update_table(tree, results)
        
        # Obtener los valores finales de X, Y, Z y el error en X
        final_result = results[-1]  # Última iteración
        iteracion_final, X_final, Y_final, Z_final, error_x = final_result
        
        # Formatear el mensaje final sin quitar "Solución"
        result_text = (
            f"Solución:\n"
            f"Los valores aproximados para las variables son:\n"
            f"X = {X_final:.4f}    Y = {Y_final:.4f}    Z = {Z_final:.4f}\n"
            f"Para un error en X del {error_x:.4f}%"
        )
        
        # Actualizar la etiqueta de resultados
        result_label.config(text=result_text)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")

# Crear la interfaz gráfica (resto de la interfaz...)
root = tk.Tk()
root.title("Solución de Sistemas de Ecuaciones 3x3 - Gauss-Seidel")
root.geometry("")
root.resizable(True, True)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

entries = [[tk.Entry(main_frame, width=5, justify="center") for _ in range(3)] for _ in range(3)]
entries_b = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
entries_x0 = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
for entry in entries_x0:
    entry.insert(0, "0")

tol_entry = tk.Entry(main_frame, width=5, justify="center")
tol_entry.insert(0, "1e-4")

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

button_frame = tk.Frame(main_frame)
button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 10))

# Crear tabla para mostrar resultados
tree = create_table(main_frame)

# Etiqueta para mostrar el resultado final
result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

# Etiqueta para mostrar la matriz reordenada
reordered_label = tk.Label(main_frame, text="", font=("Arial", 10), anchor="center", justify="center")
reordered_label.grid(row=11, column=0, columnspan=3, pady=(10, 0))

solve_button = tk.Button(button_frame, text="Resolver", command=lambda: solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label), width=10)
solve_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Restablecer", command=lambda: reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree, reordered_label), width=10)
reset_button.grid(row=0, column=1, padx=5)

manual_button = tk.Button(button_frame, text="Manual de Usuario", command=show_manual, width=15)
manual_button.grid(row=0, column=2, padx=5)

root.mainloop()