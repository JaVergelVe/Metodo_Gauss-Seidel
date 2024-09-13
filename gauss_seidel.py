import tkinter as tk
from tkinter import messagebox

# Función que valida si la matriz es estrictamente diagonalmente dominante
def is_strictly_diagonally_dominant(A, tolerance=1e-10):
    """
    Verifica si la matriz A es estrictamente diagonalmente dominante.
    
    Args:
        A: Matriz cuadrada.
        tolerance: Tolerancia numérica para las comparaciones.

    Returns:
        True si la matriz es estrictamente dominante, False en caso contrario.
    """

    n = len(A)
    
    for i in range(n):
        sum_non_diag = 0
        for j in range(n):
            if i != j:
                sum_non_diag += abs(A[i][j])
        
        # Usar una tolerancia para evitar problemas de precisión numérica
        if abs(A[i][i]) <= sum_non_diag + tolerance:
            return False
    
    return True

# Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales
def gauss_seidel(A, b, x0, tol=1e-4, max_iterations=1000):
    """
    Implementa el método iterativo de Gauss-Seidel para resolver el sistema de ecuaciones Ax = b.
    """
    n = len(A)
    x = x0[:]  # Inicializar el vector de soluciones con los valores iniciales
    
    # Iterar hasta que la solución converja o se alcance el número máximo de iteraciones
    for iteration in range(max_iterations):
        x_new = x[:]  # Crear una copia de la solución anterior
        
        # Actualizar cada valor de x_i según la fórmula del método Gauss-Seidel
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))  # Parte izquierda
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))  # Parte derecha
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        # Verificar si la diferencia entre iteraciones es menor que la tolerancia
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return x_new, iteration + 1  # Devolver la solución y el número de iteraciones
        
        x = x_new[:]  # Actualizar la solución

    return x, max_iterations  # Devolver la solución final después de todas las iteraciones

# Función que valida las entradas antes de resolver el sistema
def validate_inputs(entries, entries_b, entries_x0, tol_entry):
    """
    Valida los datos de entrada para asegurar que sean correctos y numéricos.
    Retorna la matriz A, el vector b, el vector x0, y la tolerancia.
    Si los datos no son válidos, muestra un mensaje de error.
    """
    try:
        # Obtener los valores ingresados en la matriz A, vector b y x0
        A = [[float(entries[i][j].get()) for j in range(3)] for i in range(3)]
        b = [float(entries_b[i].get()) for i in range(3)]
        x0 = [float(entries_x0[i].get()) for i in range(3)]
        
        # Verificar que la diagonal de la matriz A no contenga ceros
        for i in range(3):
            if A[i][i] == 0:
                messagebox.showerror("Error en la matriz A", f"El elemento en la posición A[{i+1}][{i+1}] no debe ser cero.")
                return None, None, None, None
        
        # Validar que la tolerancia sea un número positivo
        tol = float(tol_entry.get())
        if tol <= 0:
            messagebox.showerror("Error en la tolerancia", "La tolerancia debe ser un número positivo. Ingresa un valor mayor que 0.")
            return None, None, None, None
        
        return A, b, x0, tol
    
    except ValueError:
        messagebox.showerror("Error en las entradas", "Asegúrate de que todos los campos contengan números válidos.")
        return None, None, None, None

# Función que resuelve el sistema de ecuaciones y actualiza los resultados en la interfaz
def solve_system(entries, entries_b, entries_x0, tol_entry, result_label):
    """
    Resuelve el sistema de ecuaciones ingresado solo si la matriz es estrictamente
    diagonalmente dominante. Si no lo es, muestra un mensaje de error en lugar de la solución.
    """
    # Validar los datos de entrada
    A, b, x0, tol = validate_inputs(entries, entries_b, entries_x0, tol_entry)
    if A is None:
        return  # Si hay un error en los datos, no hacer nada
    
    # Verificar si la matriz es estrictamente diagonalmente dominante
    if not is_strictly_diagonally_dominant(A):
        # Mostrar un mensaje de error en la etiqueta de la solución
        result_label.config(text="La ecuación no es estrictamente diagonalmente dominante, no se puede solucionar.")
        return
    
    # Si la matriz es estrictamente diagonalmente dominante, proceder a resolver
    try:
        solution, iterations = gauss_seidel(A, b, x0, tol=tol)
        
        # Mostrar la solución en la interfaz
        result_text = f"X = {solution[0]:.4f}\nY = {solution[1]:.4f}\nZ = {solution[2]:.4f}"
        iterations_text = f'Número de iteraciones: {iterations}'
        result_label.config(text=f'Solución:\n{result_text}\n\n{iterations_text}')
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")