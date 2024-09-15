from tkinter import messagebox
import itertools

def is_strictly_diagonally_dominant(A):
    """
    Verifica si la matriz A es estrictamente diagonalmente dominante.
    
    :param A: Matriz cuadrada de coeficientes.
    :return: True si la matriz es estrictamente diagonalmente dominante, False en caso contrario.
    """
    n = len(A)
    for i in range(n):
        # Suma de los valores absolutos de la fila, excluyendo el valor diagonal
        sum_row = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) <= sum_row:
            return False
    return True

def reorder_to_dominant(A, b):
    """
    Reordena las filas de la matriz A para hacerla estrictamente diagonalmente dominante si es posible.
    
    :param A: Matriz cuadrada de coeficientes.
    :param b: Vector de términos independientes.
    :return: Una tupla (A_reordenada, b_reordenado) si es posible, o (None, None) si no se puede.
    """
    n = len(A)
    
    # Probar todas las permutaciones posibles de las filas de A
    for perm in itertools.permutations(range(n)):
        A_permuted = [A[i] for i in perm]
        b_permuted = [b[i] for i in perm]
        
        if is_strictly_diagonally_dominant(A_permuted):
            return A_permuted, b_permuted  # Devolver matriz reordenada si es dominante
    
    # Si no se puede hacer dominante, devolver None
    return None, None

def gauss_seidel(A, b, x0, tol=1e-4, max_iterations=1000):
    """
    Aplica el método iterativo de Gauss-Seidel para resolver el sistema de ecuaciones Ax = b.
    
    :param A: Matriz cuadrada de coeficientes.
    :param b: Vector de términos independientes.
    :param x0: Vector inicial de aproximación.
    :param tol: Tolerancia para la convergencia.
    :param max_iterations: Máximo número de iteraciones permitido.
    :return: Una lista de tuplas con los resultados de cada iteración y el error aproximado.
    """
    n = len(A)
    x = x0[:]  # Copia del vector inicial
    results = []  # Almacenar los resultados de cada iteración

    for iteration in range(max_iterations):
        x_new = x[:]  # Copiar el estado previo de x

        # Actualizar cada componente de x usando la fórmula de Gauss-Seidel
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))  # Suma de los términos a la izquierda
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))  # Suma de los términos a la derecha
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]

        # Calcular el error aproximado en x[0]
        error_x = abs(((x_new[0] - x[0]) / x_new[0]) * 100) if x_new[0] != 0 else 0
        
        # Almacenar los resultados de esta iteración: iteración, valores de x y error en x
        results.append((iteration, *x_new, error_x))

        # Comprobar si la diferencia entre iteraciones es menor que la tolerancia
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            break  # Si se cumple la tolerancia, detener las iteraciones

        x = x_new[:]  # Actualizar la solución para la próxima iteración
    
    return results

def validate_inputs(entries, entries_b, entries_x0, tol_entry):
    """
    Valida los datos de entrada del sistema de ecuaciones y asegura que sean numéricos y válidos.
    
    :param entries: Entradas de la matriz A.
    :param entries_b: Entradas del vector b.
    :param entries_x0: Entradas del vector inicial x0.
    :param tol_entry: Entrada de la tolerancia.
    :return: Una tupla (A, b, x0, tol) si los datos son válidos, o (None, None, None, None) si no lo son.
    """
    try:
        # Convertir las entradas a flotantes
        A = [[float(entries[i][j].get()) for j in range(3)] for i in range(3)]
        b = [float(entries_b[i].get()) for i in range(3)]
        x0 = [float(entries_x0[i].get()) for i in range(3)]
        
        # Verificar que no haya ceros en la diagonal de A
        for i in range(3):
            if A[i][i] == 0:
                messagebox.showerror("Error en la matriz A", f"El elemento A[{i+1}][{i+1}] no debe ser cero.")
                return None, None, None, None
        
        # Validar la tolerancia
        tol = float(tol_entry.get())
        if tol <= 0:
            messagebox.showerror("Error en la tolerancia", "La tolerancia debe ser un número positivo mayor que 0.")
            return None, None, None, None
        
        return A, b, x0, tol
    
    except ValueError:
        messagebox.showerror("Error en las entradas", "Asegúrate de que todos los campos contengan números válidos.")
        return None, None, None, None