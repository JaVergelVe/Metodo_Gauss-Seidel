import tkinter as tk
from tkinter import messagebox, scrolledtext

def show_manual():
    """
    Muestra una ventana emergente con un manual detallado de usuario.
    """
    manual_text = (
        "Manual de Usuario - Solución de Sistemas de Ecuaciones 3x3 (Método Gauss-Seidel)\n\n"
        "Este programa resuelve sistemas de ecuaciones lineales de 3 variables usando el método iterativo "
        "de Gauss-Seidel. A continuación se explica paso a paso cómo utilizar la interfaz.\n\n"
        
        "1. **Coeficientes de la Matriz A**:\n"
        "- La matriz A es una matriz de coeficientes de 3x3 que representa el sistema de ecuaciones.\n"
        "- Ingrese los valores de los coeficientes en las casillas correspondientes. Por ejemplo, para la "
        "primera ecuación del sistema (a11 * X + a12 * Y + a13 * Z = b1), debe ingresar los valores de a11, a12 y a13.\n"
        "- Es importante que los valores en la diagonal de la matriz A (a11, a22, a33) no sean ceros.\n\n"
        
        "2. **Términos Independientes (Vector b)**:\n"
        "- El vector b contiene los términos independientes de cada una de las 3 ecuaciones del sistema.\n"
        "- Ingrese los valores de los términos b1, b2 y b3, que corresponden a los resultados de cada ecuación.\n"
        "- Ejemplo: Si tiene la ecuación 3X + 2Y + Z = 4, el valor de b1 es 4.\n\n"
        
        "3. **Valores Iniciales (Vector x0)**:\n"
        "- El método de Gauss-Seidel es un método iterativo, lo que significa que empieza desde un valor inicial "
        "para encontrar la solución. Estos son los valores iniciales de X, Y y Z.\n"
        "- Ingrese una aproximación inicial en las casillas correspondientes para cada una de las variables.\n"
        "- Ejemplo: Puede comenzar con X = 0, Y = 0, Z = 0, o con cualquier otro valor.\n\n"
        
        "4. **Tolerancia**:\n"
        "- La tolerancia determina cuán precisa debe ser la solución final. Un valor más bajo implica mayor precisión.\n"
        "- El valor predeterminado es 0.0001 (1e-4), lo cual es adecuado para la mayoría de los casos. Si desea mayor "
        "o menor precisión, puede ajustar este valor.\n\n"
        
        "5. **Botones**:\n"
        "- **Resolver**: Presione este botón para calcular la solución del sistema de ecuaciones utilizando "
        "el método de Gauss-Seidel. El resultado aparecerá en la sección de 'Solución'.\n"
        "- **Restablecer**: Presione este botón para limpiar todos los campos y restablecer la interfaz. Útil si "
        "desea comenzar de nuevo o cambiar los valores ingresados.\n\n"
        
        "6. **Resultados**:\n"
        "- Después de presionar 'Resolver', el programa mostrará los valores de X, Y y Z que son la solución del sistema.\n"
        "- También verá cuántas iteraciones fueron necesarias para alcanzar esa solución.\n"
        "- Además, la 'Matriz Dominante' que se usa en el cálculo se mostrará en la parte inferior de la interfaz.\n\n"
        
        "¡Eso es todo! Ahora puedes usar el programa para resolver tus sistemas de ecuaciones lineales 3x3 con facilidad."
    )
    
    # Crear una ventana emergente para mostrar el manual
    manual_window = tk.Toplevel(root)
    manual_window.title("Manual de Usuario")
    manual_window.geometry("500x500")  # Ajustar el tamaño de la ventana
    
    # Crear un cuadro de texto con desplazamiento para el manual de usuario
    manual_textbox = scrolledtext.ScrolledText(manual_window, wrap=tk.WORD, padx=10, pady=10, font=("Arial", 10))
    manual_textbox.insert(tk.END, manual_text)
    manual_textbox.config(state=tk.DISABLED)  # Desactivar la edición
    manual_textbox.pack(fill="both", expand=True)

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

def validate_inputs():
    try:
        A = [[float(entries[i][j].get()) for j in range(3)] for i in range(3)]
        b = [float(entries_b[i].get()) for i in range(3)]
        x0 = [float(entries_x0[i].get()) for i in range(3)]
        
        for i in range(3):
            if A[i][i] == 0:
                messagebox.showerror("Error en la matriz A", f"El elemento en la posición A[{i+1}][{i+1}] no debe ser cero.")
                return None, None, None, None
        
        if all(all(A[i][j] == 0 for j in range(3)) for i in range(3)):
            messagebox.showerror("Error en la matriz A", "La matriz A no puede estar compuesta solo de ceros. Ingresa al menos un valor distinto de cero.")
            return None, None, None, None
        
        tol = float(tol_entry.get())
        if tol <= 0:
            messagebox.showerror("Error en la tolerancia", "La tolerancia debe ser un número positivo. Ingresa un valor mayor que 0.")
            return None, None, None, None
        
        return A, b, x0, tol
    
    except ValueError:
        messagebox.showerror("Error en las entradas", "Asegúrate de que todos los campos contengan números válidos.")
        return None, None, None, None

def solve_system():
    A, b, x0, tol = validate_inputs()
    if A is None:
        return
    
    try:
        A_dominant, b_dominant = make_strictly_diagonally_dominant(A, b)
        
        matrix_dominant_text = "\n".join([f"[{A_dominant[i][0]:.4f}, {A_dominant[i][1]:.4f}, {A_dominant[i][2]:.4f}] = [{b_dominant[i]:.4f}]" for i in range(3)])
        dominant_matrix_label.config(text=f'Matriz Dominante:\n{matrix_dominant_text}')
        
        solution, iterations = gauss_seidel(A_dominant, b_dominant, x0, tol=tol)
        
        result_text = f"X = {solution[0]:.4f}\nY = {solution[1]:.4f}\nZ = {solution[2]:.4f}"
        iterations_text = f'Número de iteraciones: {iterations}'
        result_label.config(text=f'Solución:\n{result_text}\n\n{iterations_text}')
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la solución: {e}")

def reset_fields():
    for i in range(3):
        for j in range(3):
            entries[i][j].delete(0, tk.END)
        entries_b[i].delete(0, tk.END)
        entries_x0[i].delete(0, tk.END)
    
    tol_entry.delete(0, tk.END)
    tol_entry.insert(0, "1e-4")
    
    dominant_matrix_label.config(text="Matriz Dominante:")
    result_label.config(text="Solución:")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Solución de Sistemas de Ecuaciones 3x3 - Gauss-Seidel")
root.geometry("")
root.resizable(True, True)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

entries = [[tk.Entry(main_frame, width=5, justify="center") for _ in range(3)] for _ in range(3)]
entries_b = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
entries_x0 = [tk.Entry(main_frame, width=5, justify="center") for _ in range(3)]
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

solve_button = tk.Button(button_frame, text="Resolver", command=solve_system, width=10)
solve_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Restablecer", command=reset_fields, width=10)
reset_button.grid(row=0, column=1, padx=5)

manual_button = tk.Button(main_frame, text="Manual de Usuario", command=show_manual, width=15)
manual_button.grid(row=11, column=0, columnspan=3, pady=10)

dominant_matrix_label = tk.Label(main_frame, text="Matriz Dominante:", font=("Arial", 10, "bold"), anchor="center", justify="center")
dominant_matrix_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

result_label = tk.Label(main_frame, text="Solución:", font=("Arial", 10, "bold"), anchor="center", justify="center")
result_label.grid(row=13, column=0, columnspan=3, pady=(10, 0))

root.mainloop()