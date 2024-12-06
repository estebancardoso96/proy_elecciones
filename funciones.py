# Funcion limpieza (coluna porcentajes)

def limpiar_y_convertir_a_float(col):
    # Definimos una función interna para limpiar cada valor de la columna
    def limpiar_valor(valor):
        if isinstance(valor, str):  # Solo si es una cadena
            valor = valor.replace('%', '').replace(',', '.')
        return float(valor)  # Convertir a float

    # Aplicamos la función limpiar_valor a cada elemento de la columna
    return col.apply(limpiar_valor)