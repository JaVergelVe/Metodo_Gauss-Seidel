import tkinter as tk
from tkinter import scrolledtext

# Función que muestra el manual de usuario en una ventana emergente
def show_manual():
    """
    Muestra una ventana emergente con el manual de usuario que explica cómo usar la aplicación.
    """
    manual_text = (
        "Manual de Usuario - Solución de Sistemas de Ecuaciones 3x3 (Método Gauss-Seidel)\n\n"
        "Este programa resuelve sistemas de ecuaciones lineales de 3 variables usando el método iterativo "
        "de Gauss-Seidel. A continuación se explica paso a paso cómo utilizar la interfaz.\n\n"
        
        "1. Coeficientes de la Matriz A:\n"
        "- Ingrese los valores de los coeficientes en las casillas correspondientes.\n"
        "- Asegúrese de que los valores en la diagonal de la matriz A no sean ceros.\n\n"
        
        "2. Términos Independientes (Vector b):\n"
        "- Ingrese los valores de los términos b1, b2 y b3.\n\n"
        
        "3. Valores Iniciales (Vector x0):\n"
        "- Ingrese una aproximación inicial para las variables X, Y y Z.\n\n"
        
        "4. Tolerancia:\n"
        "- Ajuste la precisión de la solución.\n\n"
        
        "5. Botones:\n"
        "- Resolver: Calcula la solución.\n"
        "- Restablecer: Limpia los campos y resultados.\n\n"
        
        "6. Resultados:\n"
        "- Verá los valores de X, Y, Z y el número de iteraciones.\n"
        "- También verá la matriz dominante utilizada."
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