import tkinter as tk

def show_manual():
    """
    Muestra el manual de usuario en una ventana emergente.
    Explica cómo funciona la interfaz y cómo utilizar el programa.
    """
    manual_text = (
        "Manual de Usuario - Solución de Sistemas de Ecuaciones 3x3 por Gauss-Seidel\n\n"
        
        "Introducción:\n"
        "Este programa resuelve sistemas de ecuaciones lineales con tres incógnitas (X, Y, Z) "
        "utilizando el método numérico de Gauss-Seidel. A continuación, se detalla cómo utilizar "
        "la interfaz de usuario para ingresar datos, ejecutar los cálculos y comprender los resultados.\n\n"
        
        "Secciones de la Interfaz:\n\n"
        
        "1. Entradas de Datos para las Ecuaciones:\n"
        "- En esta sección, ingresarás los coeficientes de cada una de las tres ecuaciones que componen tu sistema.\n"
        "  a. En la 'Matriz A', ingresa los coeficientes de las incógnitas X, Y y Z para cada ecuación.\n"
        "  b. En el 'Vector b', ingresa el valor numérico del término independiente de cada ecuación.\n"
        "  c. En el 'Vector x0', puedes ingresar los valores iniciales de X, Y y Z. Si no tienes valores estimados, "
        "deja los valores predeterminados (0).\n"
        "  d. La 'Tolerancia' define el nivel de precisión deseado. Un valor más pequeño ofrece mayor precisión, "
        "pero puede requerir más iteraciones.\n\n"
        
        "2. Despejes de las Ecuaciones:\n"
        "Después de ingresar los datos, la aplicación te mostrará cómo queda despejada cada ecuación con respecto a "
        "una incógnita. Verás el despeje de:\n"
        "  - X en función de Y y Z.\n"
        "  - Y en función de X y Z.\n"
        "  - Z en función de X y Y.\n\n"
        
        "3. Matriz Reordenada:\n"
        "Si la matriz ingresada no es estrictamente diagonalmente dominante, el programa intentará reordenar las filas "
        "de la matriz para mejorar la convergencia del método de Gauss-Seidel. Si esto ocurre, se mostrará la nueva "
        "matriz reordenada en esta sección.\n\n"
        
        "4. Tabla de Resultados Iterativos:\n"
        "La tabla muestra los resultados de cada iteración del método de Gauss-Seidel. Cada columna contiene:\n"
        "  - 'Iteración': El número de iteración.\n"
        "  - 'X', 'Y', 'Z': Los valores calculados de las incógnitas en cada iteración.\n"
        "  - 'Error': El error relativo en el valor de X.\n"
        "La tabla te permite ver cómo los valores de X, Y y Z se van ajustando a lo largo de las iteraciones.\n\n"
        
        "5. Resultado Final:\n"
        "Una vez que el cálculo haya alcanzado la precisión definida por la tolerancia, se mostrará el valor final de "
        "X, Y y Z en la parte inferior de la pantalla, junto con el error en X.\n\n"
        
        "Botones:\n"
        "- 'Resolver': Ejecuta el cálculo del sistema de ecuaciones usando los valores ingresados.\n"
        "- 'Restablecer': Limpia todos los campos de entrada y resultados para comenzar de nuevo.\n"
        "- 'Manual de Usuario': Abre este manual.\n\n"
        
        "Notas Técnicas:\n"
        "1. Asegúrate de que los coeficientes de la matriz A no tengan ceros en la diagonal principal, ya que esto "
        "puede causar errores durante los cálculos.\n"
        "2. Este programa está diseñado para resolver sistemas de ecuaciones lineales con tres incógnitas.\n\n"
        
        "¡Gracias por utilizar la aplicación! Si tienes alguna duda, consulta este manual en cualquier momento."
    )

    # Crear la ventana emergente para mostrar el manual
    manual_window = tk.Toplevel()
    manual_window.title("Manual de Usuario")
    manual_window.geometry("600x500")

    # Widget de texto para mostrar el contenido del manual
    text_widget = tk.Text(manual_window, wrap="word", padx=10, pady=10)
    text_widget.insert(tk.END, manual_text)
    text_widget.config(state=tk.DISABLED)  # Deshabilitar edición para que sea solo lectura
    text_widget.pack(expand=True, fill="both")

    # Botón para cerrar la ventana del manual
    close_button = tk.Button(manual_window, text="Cerrar", command=manual_window.destroy)
    close_button.pack(pady=10)