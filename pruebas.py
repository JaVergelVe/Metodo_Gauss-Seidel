import tkinter as tk
from tkinter import messagebox

def make_strictly_diagonally_dominant(A, b):
    n = len(A)
    A_dominant = [row[:] for row in A]
    b_dominant = b[:]
    
    for i in range(n):
        if abs(A_dominant[i][i]) <= sum(abs(A_dominant[i][j]) for j in range(n) if j != i):
            for k in range(i + 1, n):
                if abs(A_dominant[k][i]) > sum(abs(A_dominant[k][j]) for j in range(n) if j != i):
                    A_dominant[i], A_dominant[k] = A_dominant[k], A_dominant[i]
                    b_dominant[i], b_dominant[k] = b_dominant[k], b_dominant[i]
                    break
            
            if abs(A_dominant[i][i]) <= sum(abs(A_dominant[i][j]) for j in range(n) if j != i):
                A_dominant[i][i] = sum(abs(A_dominant[i][j]) for j in range(n) if j != i) + 1

    return A_dominant, b_dominant

def gauss_seidel(A, b, x0, tol=1e-4, max_iterations=1000):
    n = len(A)
    x = x0[:]
    
    for iteration in range(max_iterations):
        x_new = x[:]
        
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return x_new, iteration + 1
        
        x = x_new[:]
    
    return x, max_iterations

def solve_system():
    try:
        A = [[float(entries[i][j].get()) for j in range(3)] for i in range(3)]
        b = [float(entries_b[i].get()) for i in range(3)]
        x0 = [float(entries_x0[i].get()) for i in range(3)]
        tol = float(tol_entry.get())
        
        A_dominant, b_dominant = make_strictly_diagonally_dominant(A, b)
        
        matrix_dominant_text = "\n".join([f"[{A_dominant[i][0]:.4f}, {A_dominant[i][1]:.4f}, {A_dominant[i][2]:.4f}] = [{b_dominant[i]:.4f}]" for i in range(3)])
        dominant_matrix_label.config(text=f'Matriz Dominante:\n{matrix_dominant_text}')
        
        solution, iterations = gauss_seidel(A_dominant, b_dominant, x0, tol=tol)
        
        result_text = f"X = {solution[0]:.4f}\nY = {solution[1]:.4f}\nZ = {solution[2]:.4f}"
        iterations_text = f'Iteraciones: {iterations}'
        result_label.config(text=f'Solución:\n{result_text}\n\n{iterations_text}')
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")

def reset_fields():
    for widgets in entries + entries_b + entries_x0:
        for widget in widgets:
            widget.delete(0, tk.END)
    
    tol_entry.delete(0, tk.END)
    tol_entry.insert(0, "1e-4")
    dominant_matrix_label.config(text="Matriz Dominante:")
    result_label.config(text="Solución:")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Solución de Sistemas de Ecuaciones 3x3 - Gauss-Seidel")

# Frame principal centrado
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Crear las entradas de coeficientes y términos independientes
entries = [[tk.Entry(main_frame, width=5, justify="center") for _ in range(3)] for _ in range(3)]
entries_b = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
entries_x0 = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
tol_entry = tk.Entry(main_frame, width=5, justify="center")
tol_entry.insert(0, "1e-4")

# Etiqueta y matriz A
tk.Label(main_frame, text="Coeficientes de la matriz A:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))
for i in range(3):
    for j in range(3):
        entries[i][j].grid(row=i+1, column=j, padx=5, pady=5)

# Etiqueta y vector b
tk.Label(main_frame, text="Términos independientes (vector b):", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=3, pady=(10, 0))
for i in range(3):
    entries_b[i].grid(row=5, column=i, padx=5, pady=5)

# Etiqueta y vector x0
tk.Label(main_frame, text="Valores iniciales (vector x0):", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=3, pady=(10, 0))
for i in range(3):
    entries_x0[i].grid(row=7, column=i, padx=5, pady=5)

# Etiqueta y entrada de tolerancia
tk.Label(main_frame, text="Tolerancia:", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=3, pady=(10, 0))
tol_entry.grid(row=9, column=0, columnspan=3, pady=5)

# Botones para resolver y restablecer
button_frame = tk.Frame(main_frame)
button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 10))

solve_button = tk.Button(button_frame, text="Resolver", command=solve_system, width=10)
solve_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Restablecer", command=reset_fields, width=10)
reset_button.grid(row=0, column=1, padx=5)

# Etiqueta para mostrar la matriz dominante
dominant_matrix_label = tk.Label(main_frame, text="Matriz Dominante:", font=("Arial", 10, "bold"), anchor="center", justify="center")
dominant_matrix_label.grid(row=11, column=0, columnspan=3, pady=(10, 0))

# Etiqueta para mostrar el resultado
result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

root.mainloop()
