import tkinter as tk
from tkinter import ttk, messagebox
from gauss_seidel import gauss_seidel, is_strictly_diagonally_dominant, validate_inputs
from manual import show_manual

# Crear la tabla para mostrar las iteraciones
def create_table(main_frame):
    """
    Crea una tabla en la interfaz para mostrar las iteraciones, X, Y, Z, y el error.
    También agrega una barra de desplazamiento.
    """
    # Crear el Treeview con 5 columnas: Iteración, X, Y, Z, Error
    columns = ("Iteración", "X", "Y", "Z", "Error")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    
    # Definir el encabezado para cada columna
    tree.heading("Iteración", text="Iteración")
    tree.heading("X", text="X")
    tree.heading("Y", text="Y")
    tree.heading("Z", text="Z")
    tree.heading("Error", text="Error (%)")
    
    # Configurar el ancho de las columnas
    tree.column("Iteración", width=80, anchor="center")
    tree.column("X", width=80, anchor="center")
    tree.column("Y", width=80, anchor="center")
    tree.column("Z", width=80, anchor="center")
    tree.column("Error", width=80, anchor="center")
    
    # Crear una barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Colocar la tabla y la barra de desplazamiento en la interfaz
    tree.grid(row=13, column=0, columnspan=3, pady=10, sticky="nsew")  # Expandir la tabla con `sticky`
    scrollbar.grid(row=13, column=3, sticky="ns")  # Colocar la barra de scroll a la derecha de la tabla
    
    return tree

# Función para actualizar la tabla con los resultados de cada iteración
def update_table(tree, results):
    """
    Actualiza la tabla con los resultados de cada iteración, mostrando solo 4 decimales.
    """
    # Limpiar la tabla antes de actualizar
    for row in tree.get_children():
        tree.delete(row)
    
    # Insertar los resultados en la tabla, redondeados a 4 decimales
    for result in results:
        # Formatear los valores de la iteración, X, Y, Z, Error a 4 decimales
        formatted_result = (
            result[0],  # Iteración (no necesita formateo)
            f"{result[1]:.4f}",  # X con 4 decimales
            f"{result[2]:.4f}",  # Y con 4 decimales
            f"{result[3]:.4f}",  # Z con 4 decimales
            f"{result[4]:.4f}"   # Error con 4 decimales
        )
        tree.insert("", tk.END, values=formatted_result)

# Función para restablecer todos los campos y limpiar la tabla
def reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree):
    """
    Restablece todos los campos de entrada a su valor original.
    Limpia la matriz A, el vector b, el vector x0, la tolerancia, el resultado, y la tabla.
    """
    # Limpiar las entradas de la matriz A, el vector b, y el vector x0
    for i in range(3):
        for j in range(3):
            entries[i][j].delete(0, tk.END)  # Limpiar cada casilla de la matriz A
        entries_b[i].delete(0, tk.END)  # Limpiar cada casilla del vector b
        entries_x0[i].delete(0, tk.END)  # Limpiar cada casilla del vector x0
    
    # Restablecer el vector x0 a sus valores predeterminados (0, 0, 0)
    for entry in entries_x0:
        entry.insert(0, "0")

    # Restablecer la tolerancia al valor predeterminado
    tol_entry.delete(0, tk.END)
    tol_entry.insert(0, "1e-4")  # Valor predeterminado de la tolerancia

    # Restablecer la etiqueta de resultados
    result_label.config(text="Solución:")  # Limpiar la etiqueta de solución

    # Limpiar la tabla
    for row in tree.get_children():
        tree.delete(row)

# Función para resolver el sistema y actualizar la tabla
def solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree):
    """
    Resuelve el sistema de ecuaciones ingresado y actualiza la tabla.
    Muestra la solución en el formato solicitado.
    """
    # Validar los datos de entrada
    A, b, x0, tol = validate_inputs(entries, entries_b, entries_x0, tol_entry)
    if A is None:
        return  # Si hay un error en los datos, no hacer nada
    
    # Verificar si la matriz es estrictamente diagonalmente dominante
    if not is_strictly_diagonally_dominant(A):
        result_label.config(text="La ecuación no es estrictamente diagonalmente dominante, no se puede solucionar.")
        return
    
    try:
        # Llamar al método de Gauss-Seidel y obtener los resultados de cada iteración
        results = gauss_seidel(A, b, x0, tol)
        
        # Mostrar los resultados de todas las iteraciones en la tabla
        update_table(tree, results)
        
        # Obtener los valores finales de X, Y, Z y el error en X
        final_result = results[-1]  # Última iteración
        iteracion_final, X_final, Y_final, Z_final, error_x = final_result
        
        # Formatear el mensaje final
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
root.geometry("")  # Ajustar el tamaño automáticamente
root.resizable(True, True)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Entradas para matriz A, vector b, x0, tolerancia
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

# Frame para botones
button_frame = tk.Frame(main_frame)
button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 10))

# Crear tabla para mostrar resultados
tree = create_table(main_frame)

# Etiqueta para mostrar el resultado final
result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

solve_button = tk.Button(button_frame, text="Resolver", command=lambda: solve_system(entries, entries_b, entries_x0, tol_entry, result_label, tree), width=10)
solve_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Restablecer", command=lambda: reset_fields(entries, entries_b, entries_x0, tol_entry, result_label, tree), width=10)
reset_button.grid(row=0, column=1, padx=5)

manual_button = tk.Button(button_frame, text="Manual de Usuario", command=show_manual, width=15)
manual_button.grid(row=0, column=2, padx=5)

root.mainloop()