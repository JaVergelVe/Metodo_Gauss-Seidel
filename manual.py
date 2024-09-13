import tkinter as tk
from tkinter import scrolledtext

def show_manual():
    """
    Muestra una ventana emergente con el manual de usuario actualizado, explicando cómo usar
    el programa para resolver sistemas de ecuaciones lineales 3x3 usando el método de Gauss-Seidel.
    """
    manual_text = (
        "Manual de Usuario - Solución de Sistemas de Ecuaciones 3x3 (Método Gauss-Seidel)\n\n"
        "Este programa resuelve sistemas de ecuaciones lineales de 3 variables usando el método iterativo "
        "de Gauss-Seidel. A continuación se explica paso a paso cómo utilizar la interfaz:\n\n"
        
        "1. **Coeficientes de la Matriz A**:\n"
        "- Ingrese los valores de los coeficientes en las casillas correspondientes de la matriz A.\n"
        "- Asegúrese de que los valores en la diagonal de la matriz A no sean ceros.\n"
        "- El programa validará si la matriz es diagonalmente dominante antes de resolverla.\n\n"
        
        "2. **Términos Independientes (Vector b)**:\n"
        "- Ingrese los valores de los términos independientes en las casillas del vector b.\n"
        "- Estos son los resultados de las ecuaciones, por ejemplo, si tiene la ecuación 3X + 2Y + Z = 4, "
        "el valor de b1 es 4.\n\n"
        
        "3. **Valores Iniciales (Vector x0)**:\n"
        "- Ingrese una aproximación inicial para las variables X, Y y Z en las casillas correspondientes.\n"
        "- Si no tiene una aproximación inicial específica. Por defecto, es 0,0,0.\n\n"
        
        "4. **Tolerancia**:\n"
        "- Ingrese un valor de tolerancia para definir la precisión del cálculo. Por defecto, es 0.0001 (1e-4).\n"
        "- Un valor de tolerancia más pequeño dará una mayor precisión pero puede requerir más iteraciones.\n\n"
        
        "5. **Botones**:\n"
        "- **Resolver**: Presione este botón para calcular la solución del sistema de ecuaciones. "
        "El programa mostrará los valores de X, Y, Z si la matriz es diagonalmente dominante. "
        "Si la matriz no es diagonalmente dominante, verá un mensaje de error.\n"
        "- **Restablecer**: Presione este botón para limpiar todos los campos de entrada y restablecer la interfaz "
        "a su estado original."
    )
    
    # Crear una ventana emergente para mostrar el manual
    manual_window = tk.Toplevel()
    manual_window.title("Manual de Usuario")
    manual_window.geometry("500x500")  # Ajustar el tamaño de la ventana
    
    # Crear un cuadro de texto con desplazamiento para el manual de usuario
    manual_textbox = scrolledtext.ScrolledText(manual_window, wrap=tk.WORD, padx=10, pady=10, font=("Arial", 10))
    manual_textbox.insert(tk.END, manual_text)  # Insertar el texto del manual
    manual_textbox.config(state=tk.DISABLED)  # Desactivar la edición
    manual_textbox.pack(fill="both", expand=True)  # Colocar el cuadro de texto en la ventana