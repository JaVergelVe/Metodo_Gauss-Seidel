import tkinter as tk
from tkinter import messagebox

# Función que verifica si la matriz ya es estrictamente diagonalmente dominante
def is_strictly_diagonally_dominant(A):
    """
    Verifica si la matriz A ya es estrictamente diagonalmente dominante.
    Una matriz es estrictamente diagonalmente dominante si para cada fila,
    el valor absoluto del elemento diagonal es mayor que la suma de los
    valores absolutos de los otros elementos de la fila.
    """
    n = len(A)
    for i in range(n):
        sum_non_diag = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) <= sum_non_diag:
            return False  # La matriz no es estrictamente diagonalmente dominante
    return True  # La matriz es estrictamente diagonalmente dominante

# Función que transforma la matriz A en estrictamente diagonalmente dominante
def make_strictly_diagonally_dominant(A, b):
    """
    Intenta transformar la matriz A en estrictamente diagonalmente dominante
    solo intercambiando filas si es necesario. No se alteran los valores numéricos
    de la matriz ni del vector b. Si no es posible hacer la matriz dominante,
    devuelve la matriz sin cambios.
    """
    n = len(A)
    A_dominant = [row[:] for row in A]  # Crear una copia de la matriz A
    b_dominant = b[:]  # Crear una copia del vector b

    for i in range(n):
        sum_non_diag = sum(abs(A_dominant[i][j]) for j in range(n) if j != i)

        # Verificar si el elemento diagonal no es dominante
        if abs(A_dominant[i][i]) <= sum_non_diag:
            swapped = False
            # Intentar encontrar una fila para intercambiar
            for k in range(i + 1, n):
                sum_non_diag_k = sum(abs(A_dominant[k][j]) for j in range(n) if j != k)
                # Verificar si al intercambiar se hace dominante
                if abs(A_dominant[k][k]) > sum_non_diag_k and abs(A_dominant[k][i]) > sum_non_diag:
                    # Intercambiar filas i y k
                    A_dominant[i], A_dominant[k] = A_dominant[k], A_dominant[i]
                    b_dominant[i], b_dominant[k] = b_dominant[k], b_dominant[i]
                    swapped = True
                    break

            # Si no se pudo hacer la matriz dominante intercambiando filas, continuar sin cambiar valores
            if not swapped:
                continue

    # Después de intentar hacer la matriz dominante, verificar si es dominante
    if is_strictly_diagonally_dominant(A_dominant):
        return A_dominant, b_dominant  # La matriz fue modificada y ahora es dominante
    else:
        return A, b  # No se logró la dominancia, devolver la matriz original sin cambios

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
        
        # Verificar que la matriz A no sea nula (toda de ceros)
        if all(all(A[i][j] == 0 for j in range(3)) for i in range(3)):
            messagebox.showerror("Error en la matriz A", "La matriz A no puede estar compuesta solo de ceros. Ingresa al menos un valor distinto de cero.")
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
def solve_system(entries, entries_b, entries_x0, tol_entry, dominant_matrix_label, result_label):
    """
    Resuelve el sistema usando Gauss-Seidel y muestra los resultados en la interfaz.
    """
    # Validar los datos de entrada
    A, b, x0, tol = validate_inputs(entries, entries_b, entries_x0, tol_entry)
    if A is None:
        return  # Si hay un error en los datos, no hacer nada
    
    try:
        # Hacer que la matriz A sea diagonalmente dominante
        A_dominant, b_dominant = make_strictly_diagonally_dominant(A, b)
        
        # Mostrar la matriz dominante en la interfaz
        matrix_dominant_text = "\n".join([f"[{A_dominant[i][0]:.4f}, {A_dominant[i][1]:.4f}, {A_dominant[i][2]:.4f}] = [{b_dominant[i]:.4f}]" for i in range(3)])
        dominant_matrix_label.config(text=f'Matriz Dominante:\n{matrix_dominant_text}')
        
        # Resolver el sistema con el método de Gauss-Seidel
        solution, iterations = gauss_seidel(A_dominant, b_dominant, x0, tol=tol)
        
        # Mostrar la solución en la interfaz
        result_text = f"X = {solution[0]:.4f}\nY = {solution[1]:.4f}\nZ = {solution[2]:.4f}"
        iterations_text = f'Número de iteraciones: {iterations}'
        result_label.config(text=f'Solución:\n{result_text}\n\n{iterations_text}')
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")