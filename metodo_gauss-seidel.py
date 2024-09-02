import tkinter as tk
from tkinter import messagebox

def make_strictly_diagonally_dominant(A, b):
    """
    Ajusta la matriz A para que sea estrictamente diagonalmente dominante,
    reordenando las filas si es necesario.
    
    Parámetros:
    A: matriz de coeficientes (3x3)
    b: vector de términos independientes (3x1)
    
    Retorna:
    A_dominant: matriz A ajustada para ser estrictamente diagonalmente dominante.
    b_dominant: vector b ajustado correspondiente.
    """
    n = len(A)
    A_dominant = [row[:] for row in A]
    b_dominant = b[:]
    
    for i in range(n):
        # Verificar si la fila actual ya es dominante
        if abs(A_dominant[i][i]) <= sum(abs(A_dominant[i][j]) for j in range(n) if j != i):
            # Intentar encontrar una fila para intercambiar
            for k in range(i + 1, n):
                if abs(A_dominant[k][i]) > sum(abs(A_dominant[k][j]) for j in range(n) if j != i):
                    # Intercambiar las filas i y k
                    A_dominant[i], A_dominant[k] = A_dominant[k], A_dominant[i]
                    b_dominant[i], b_dominant[k] = b_dominant[k], b_dominant[i]
                    break
            
            # Si no se encontró una fila para intercambiar, incrementar el valor en la diagonal
            if abs(A_dominant[i][i]) <= sum(abs(A_dominant[i][j]) for j in range(n) if j != i):
                A_dominant[i][i] = sum(abs(A_dominant[i][j]) for j in range(n) if j != i) + 1

    return A_dominant, b_dominant

def gauss_seidel(A, b, x0, tol=1e-10, max_iterations=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Gauss-Seidel.
    
    Parámetros:
    A: matriz de coeficientes (3x3)
    b: vector de términos independientes (3x1)
    x0: vector inicial (3x1)
    tol: tolerancia para la convergencia
    max_iterations: número máximo de iteraciones permitidas
    
    Retorna:
    x: la solución aproximada (3x1)
    iterations: el número de iteraciones realizadas
    """
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
        # Capturar entradas de la GUI
        A = [[float(entries[i][j].get()) for j in range(3)] for i in range(3)]
        b = [float(entries_b[i].get()) for i in range(3)]
        x0 = [float(entries_x0[i].get()) for i in range(3)]
        
        # Hacer la matriz estrictamente diagonalmente dominante
        A_dominant, b_dominant = make_strictly_diagonally_dominant(A, b)
        
        # Mostrar la matriz dominante en la GUI
        matrix_dominant_text = "\n".join([f"[{A_dominant[i][0]:.4f}, {A_dominant[i][1]:.4f}, {A_dominant[i][2]:.4f}]" for i in range(3)])
        dominant_matrix_label.config(text=f'Matriz Dominante:\n{matrix_dominant_text}')
        
        # Resolver el sistema con la matriz dominante
        solution, iterations = gauss_seidel(A_dominant, b_dominant, x0)
        
        # Mostrar resultado con 4 decimales sin redondeo
        result_text = f'Solución: X = {solution[0]:.4f}, Y = {solution[1]:.4f}, Z = {solution[2]:.4f}'
        iterations_text = f'Número de iteraciones: {iterations}'
        result_label.config(text=f'{result_text}\n{iterations_text}')
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Solución de Sistemas de Ecuaciones 3x3 - Gauss-Seidel")

# Crear las entradas de coeficientes y términos independientes
entries = [[tk.Entry(root, width=5) for _ in range(3)] for _ in range(3)]
entries_b = [tk.Entry(root, width=5) for _ in range(3)]
entries_x0 = [tk.Entry(root, width=5) for _ in range(3)]

# Ubicar las etiquetas y entradas en la cuadrícula
tk.Label(root, text="Coeficientes de la matriz A:").grid(row=0, column=0, columnspan=3)
for i in range(3):
    for j in range(3):
        entries[i][j].grid(row=i+1, column=j)

tk.Label(root, text="Términos independientes (vector b):").grid(row=4, column=0, columnspan=3)
for i in range(3):
    entries_b[i].grid(row=5, column=i)

tk.Label(root, text="Valores iniciales (vector x0):").grid(row=6, column=0, columnspan=3)
for i in range(3):
    entries_x0[i].grid(row=7, column=i)

# Botón para resolver el sistema
solve_button = tk.Button(root, text="Resolver", command=solve_system)
solve_button.grid(row=8, column=0, columnspan=3)

# Etiqueta para mostrar la matriz dominante
dominant_matrix_label = tk.Label(root, text="Matriz Dominante: ")
dominant_matrix_label.grid(row=9, column=0, columnspan=3)

# Etiqueta para mostrar el resultado
result_label = tk.Label(root, text="Solución: ")
result_label.grid(row=10, column=0, columnspan=3)

root.mainloop()