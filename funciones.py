import plotly.express as px

# color segunda vuelta

color_balotaje = {
    "Partido Nacional": "#87CEEB",  # Celeste
    "Partido Colorado": "#d62728",  # Rojo (colorado)
    "Frente Amplio": "#2ca02c", # verde
    "Partido Nacional - Coalición Multicolor": "#6A0DAD"   # morado
    # Agrega aquí todos los partidos que quieras
}

# colores de los partidos

color_map = {
    "Partido Nacional": "#87CEEB",  # Celeste
    "Partido Colorado": "#d62728",  # Rojo (colorado)
    "Frente Amplio": "#2ca02c", # verde
    "Partido Independiente": "#6A0DAD",   # morado
    "Partido Socialista":"#FFD700",
    "Cabilo Abierto":"#556B2F",
    "Nuevo Espacio":"#8A2BE2"
    # Agrega aquí todos los partidos que quieras
}

# Funcion limpieza (coluna porcentajes)

def limpiar_y_convertir_a_float(col):
    # Definimos una función interna para limpiar cada valor de la columna
    def limpiar_valor(valor):
        if isinstance(valor, str):  # Solo si es una cadena
            valor = valor.replace('%', '').replace(',', '.')
        return float(valor)  # Convertir a float

    # Aplicamos la función limpiar_valor a cada elemento de la columna
    return col.apply(limpiar_valor)


# Función gráfica

def graficar_histograma_por_anio(df, anio):
    # Filtrar el DataFrame por el año especificado
    df_filtrado = df[df["Año"] == anio]
    
    # Crear el histograma usando Plotly Express
    fig = px.histogram(df_filtrado, x='Partido', y='Porcentaje', color='Partido',color_discrete_map=color_map,
                       title=f"Resultados de las elecciones en {anio}",
                       labels={'Partido': 'Partido Político', 'Porcentaje': 'Porcentaje de Votos'},
                       text_auto=True)

    # Ajustar el diseño del gráfico
    fig.update_layout(bargap=0.2, template="plotly_white")
    return fig
