# Función que restablece todos los campos de la interfaz a su valor original
def reset_fields(entries, entries_b, entries_x0, tol_entry, dominant_matrix_label, result_label):
    """
    Limpia todos los campos de entrada y restablece las etiquetas de matriz dominante y solución.
    """
    # Limpiar las entradas de la matriz A, vector b y vector x0
    for i in range(3):
        for j in range(3):
            entries[i][j].delete(0, 'end')
        entries_b[i].delete(0, 'end')
        entries_x0[i].delete(0, 'end')
    
    # Restablecer la tolerancia a su valor predeterminado
    tol_entry.delete(0, 'end')
    tol_entry.insert(0, "1e-4")
    
    # Restablecer las etiquetas de la matriz dominante y la solución
    dominant_matrix_label.config(text="Matriz Dominante:")
    result_label.config(text="Solución:")