import tkinter as tk

def reset_fields(entries, entries_b, entries_x0, tol_entry, result_label):
    """
    Restablece todos los campos de entrada a su valor original.
    Limpia la matriz A, el vector b, el vector x0, la tolerancia, y la etiqueta de solución.
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