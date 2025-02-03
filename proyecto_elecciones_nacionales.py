import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
pd.options.plotting.backend = 'plotly' # cambio el backend, lo hago interactivo con plotly
import os
import datetime
import re
# Desactiva advertencias
pd.options.mode.chained_assignment = None


# Scrapeo a wikipedia de las elecciones que faltan

from funciones import limpiar_y_convertir_a_float

# Eleecciones del 1962

e_p_1962 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_1962')

e_p_1962 = e_p_1962[2]

e_p_1962 = e_p_1962[['Partido político', 'Porcentaje']].iloc[0:18,]
e_p_1962['Año'] = 1962
e_p_1962 = e_p_1962.drop_duplicates()
# Identifica caracteres invisibles
print(repr(e_p_1962['Partido político'].unique()))
e_p_1962['Partido político'] = e_p_1962['Partido político'].replace({'Frente Izquierda de Liberación[n 1]\u200b':'Frente Izquierda de Liberacion'})
e_p_1962['Partido político'] = e_p_1962['Partido político'].replace({'Unión Popular[n 2]\u200b':'Union Popular'})
diccio = {'Partido Nacional':'PN', 'Frente Amplio' : 'FA', 'Partido Colorado': 'PC'}
e_p_1962['Sigla'] = e_p_1962['Partido político'].map(diccio)
e_p_1962['Porcentaje'] = limpiar_y_convertir_a_float(e_p_1962['Porcentaje'])

# Eleecciones del 1958
e_p_1958 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_1958')
e_p_1958 = e_p_1958[2]
e_p_1958 = e_p_1958[['Partido político', 'Porcentaje']].iloc[0:18,]
e_p_1958['Año'] = 1958
e_p_1958 = e_p_1958.drop_duplicates()
e_p_1958['Sigla'] = e_p_1958['Partido político'].map(diccio)
e_p_1958['Porcentaje'] = limpiar_y_convertir_a_float(e_p_1958['Porcentaje'])

e_p_1958.rename(columns = {'Partido político':'Partido'}, inplace=True)
e_p_1962.rename(columns = {'Partido político':'Partido'}, inplace=True)

# Eleecciones del 1926
#e_p_1926 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_1926')
#e_p_1926 = e_p_1926[1]
#e_p_1926['Año'] = 1926
#e_p_1926 = e_p_1958[['Partido político', 'Porcentaje']]
#e_p_1926 = e_p_1926.drop_duplicates()
#e_p_1926['Sigla'] = e_p_1926['Partido político'].map(diccio)
#e_p_1926['Porcentaje'] = limpiar_y_convertir_a_float(e_p_1926['Porcentaje'])

# df = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_2024') # WIKIPEDIA
base = pd.read_html('https://umad-fcs.github.io/data_politica_uy/') # UMAD, base de datos con todas las elecciones
e_p_1984 = base[11] # elecciones 1984
e_p_1989 = base[12] # elecciones 1989
e_p_1994 = base[13] # elecciones 1994
e_p_1999 = base[14] # elecciones 1999
e_p_2004 = base[15] # elecciones 2004
e_p_2009 = base[16] # elecciones 2009
e_p_2014 = base[17] # elecciones 2014
e_p_2019 = base[18] # elecciones 2019
from funciones import limpiar_y_convertir_a_float
df = pd.concat([e_p_1984,e_p_1989,e_p_1994,e_p_1999,e_p_2004,e_p_2009,e_p_2014, e_p_2019], axis = 0) # unifico
df['Porcentaje'] = limpiar_y_convertir_a_float(df['Porcentaje'])
df['Fecha']= pd.to_datetime(df['Fecha'])
df['Año'] = df['Fecha'].dt.year
vb_va = df.query('Sigla == "VA" or Sigla == "VB"')
vb_va['Porcentaje_suma'] = vb_va.groupby('Año')['Porcentaje'].transform(sum)
vb_va['Suma'] = 'VA + VB' 
df['Partidos aliados'] = df['Partido'].replace({'Partido Nacional': 'Partidos fundacionales y aliados', 'Partido Colorado': 'Partidos fundacionales y aliados', 'Frente Amplio': 'Frente Amplio y aliados',
                                       'Nuevo Espacio':'Frente Amplio y aliados', 'Cabildo Abierto':'Partidos fundacionales y aliados', 'Partido Independiente':'Partidos fundacionales y aliados'})

df2 = df.query('Sigla in ("PC", "PN", "CA", "FA", "PI", "NE")').groupby(['Partidos aliados', 'Año'], as_index=False).sum(numeric_only=True).sort_values(by = ['Año', 'Partidos aliados'])

# Pre dictadura (faltan las elecciones del 1926, 1958 y 1962)

e_p_1971 = base[10] # elecciones 1971
e_p_1966 = base[9] # elecciones 1966
# faltan las del 1958 y 1962
e_p_1954 = base[7] # elecciones 1954 
e_p_1950 = base[6] # elecciones 1950
e_p_1946 = base[5] # elecciones 1946
e_p_1942 = base[4] # elecciones 1942
e_p_1938 = base[3] # elecciones 1938
e_p_1930 = base[2] # elecciones 1930
e_p_1926 = base[1] # elecciones 1926
e_p_1922 = base[0] # elecciones 1922
from funciones import limpiar_y_convertir_a_float
df_0 = pd.concat([e_p_1971,e_p_1966,e_p_1954,e_p_1950,e_p_1946,e_p_1942,e_p_1938, e_p_1930, e_p_1926, e_p_1922], axis = 0) # unifico
df_0['Porcentaje'] = limpiar_y_convertir_a_float(df_0['Porcentaje'])
df_0['Fecha']= pd.to_datetime(df_0['Fecha'])
df_0['Año'] = df_0['Fecha'].dt.year
df_0_0 = pd.concat([e_p_1962,e_p_1958], axis = 0)
df_0_0['Porcentaje'] = limpiar_y_convertir_a_float(df_0_0['Porcentaje'])
df_0 = pd.concat([df_0,df_0_0], axis = 0)
df_0 = df_0.sort_values(by = 'Año', ascending=False)

# Segundas vueltas

s_v_1999 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_1999')
s_v_2009 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_2009')
s_v_2014 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_2014')
s_v_2019 = pd.read_html('https://es.wikipedia.org/wiki/Elecciones_generales_de_Uruguay_de_2019')

s_v_1999 = s_v_1999[9]
s_v_2009 = s_v_2009[12]
s_v_2014 = s_v_2014[15]
s_v_2019 = s_v_2019[18]

s_v_1999 = s_v_1999[['Partido político / Coalición', 'Fórmula presidencial', 'Porcentaje de votos válidos']]
s_v_1999['Año'] = 1999
s_v_2009 = s_v_2009[['Partido político / Coalición', 'Fórmula presidencial', 'Porcentaje de votos válidos']]
s_v_2009['Año'] = 2009
s_v_2014 = s_v_2014[['Partido político / Coalición', 'Fórmula presidencial', 'Porcentaje de votos válidos']]
s_v_2014['Año'] = 2014
s_v_2019 = s_v_2019.rename(columns = {'Partido político':'Partido político / Coalición'})
s_v_2019 = s_v_2019[['Partido político / Coalición', 'Fórmula presidencial', 'Porcentaje de votos válidos']]
s_v_2019['Año'] = 2019

df_3 = pd.concat([s_v_1999, s_v_2009, s_v_2014, s_v_2019], axis = 0)
df_3 = df_3.rename(columns = {'Porcentaje de votos válidos':'Porcentaje'})
df_3['Porcentaje'] = df_3['Porcentaje'].replace('-','0')
df_3['Porcentaje'] = df_3['Porcentaje'].str.replace('%','')
df_3 = df_3.reset_index(drop = True).drop(index = 32)
segunda_vuelta = df_3[df_3['Porcentaje'].notna() & df_3['Porcentaje'].str.match(r'^.{6}$')]
segunda_vuelta['Porcentaje']= limpiar_y_convertir_a_float(segunda_vuelta['Porcentaje'])
segunda_vuelta['Porcentaje'] = segunda_vuelta['Porcentaje'].astype(float)
segunda_vuelta = segunda_vuelta.rename(columns={'Partido político / Coalición':'Partido político'})
segunda_vuelta['Partido político'] = segunda_vuelta['Partido político'].replace('Partido Socialista - Frente Amplio','Frente Amplio')

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

import dash
import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Configuración de la hoja de estilos de Bootstrap

# Configuración de Dash con Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL]) 

# Configuración de la plantilla de Plotly: opciones 'plotly', 'seaborn' (muy buena), simple_white (media)
pio.templates.default = "seaborn"

#Generamos gráficos

fig0 = df_0.query('Sigla in ("PN", "PC", "FA")').plot(x='Año', y='Porcentaje', color='Partido',color_discrete_map=color_map,
 title = 'Desempeño de los partidos en las elecciones Nacionales').update_xaxes(
    tickvals=[1922,1926,1930,1938, 1942, 1946, 1950, 1954, 1958,1962,1966, 1971]
).update_layout(
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.2,  # Posición en la ventana
            showarrow=False,
            text="Nota: Rige la regla del Doble Voto Simultáneo, en una vuelta sola se vota al legislativo y al ejecutivo.",
            font=dict(size=12, color="gray")
        )
    ]
)


fig1 = df.query('Sigla in ("PN", "PC", "FA","NE","CA")').plot(x='Año', y='Porcentaje', color='Partido',color_discrete_map=color_map,
title = 'Desempeño de los partidos en las elecciones Nacionales').update_xaxes(
    tickvals=[1984,1989, 1994, 1999, 2004, 2009, 2014, 2019]
).update_layout(
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.2,  # Posición en la ventana
            showarrow=False,
            text="Nota: A partir de 1999, las elecciones en Uruguay comenzaron a incluir una segunda vuelta.",
            font=dict(size=12, color="gray")
        )
    ]
)

segunda_vuelta = px.bar(segunda_vuelta, x="Año", y="Porcentaje", color="Partido político", barmode="group",color_discrete_map=color_balotaje,
    title="Elecciones Nacionales - Segunda Vuelta", hover_data=["Fórmula presidencial"]).update_xaxes(
    tickvals=[1999,2004, 2009, 2014, 2019]).update_layout(
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.2,  # Posición en la ventana
            showarrow=False,
            text="Nota: En el año 2004 el Frente Amplio gana en primera vuelta con más del 50% + 1 de los votos.",
            font=dict(size=12, color="gray")
        )
    ]
)

fig1_2 = df2.plot(x = 'Año', y ='Porcentaje', color = 'Partidos aliados').update_xaxes(
    tickvals=[1984,1989, 1994, 1999, 2004, 2009, 2014, 2019])

fig0_0=graficar_histograma_por_anio(df_0, 1922)
fig0_1=graficar_histograma_por_anio(df_0, 1926)
fig0_2=graficar_histograma_por_anio(df_0, 1930)
fig0_3=graficar_histograma_por_anio(df_0, 1938)
fig0_4=graficar_histograma_por_anio(df_0, 1942)
fig0_5=graficar_histograma_por_anio(df_0, 1946)
fig0_6=graficar_histograma_por_anio(df_0, 1950)
fig0_7=graficar_histograma_por_anio(df_0, 1954)
fig0_8=graficar_histograma_por_anio(df_0, 1958)
fig0_9=graficar_histograma_por_anio(df_0, 1962)
fig0_10=graficar_histograma_por_anio(df_0, 1966)
fig0_11=graficar_histograma_por_anio(df_0, 1971)

fig2_0=graficar_histograma_por_anio(df, 1984)
fig2_1=graficar_histograma_por_anio(df, 1989)
fig2_2=graficar_histograma_por_anio(df, 1994)
fig2_3=graficar_histograma_por_anio(df, 1999)
fig2_4=graficar_histograma_por_anio(df, 2004)
fig2_5=graficar_histograma_por_anio(df, 2009)
fig2_6=graficar_histograma_por_anio(df, 2014)
fig2_7=graficar_histograma_por_anio(df, 2019)
fig3 = df.plot(x='Año', y='Porcentaje', color='Partido')
fig_edad_masc = df.plot(x='Año', y='Porcentaje', color='Partido')
fig_edad_fem =df.plot(x='Año', y='Porcentaje', color='Partido')

fig_4 = px.line(
    vb_va,
    x='Año',
    y='Porcentaje',
    color='Partido',  # Variable categórica para el color
    markers=True,     # Mostrar los puntos además de las líneas
    labels={'Año': 'Año', 'Porcentaje': 'Porcentaje'},
    title='Evolución de los votos anulados y en blanco (1984-2019)'
).add_scatter(   # Añadir la segunda métrica en el mismo gráfico
    x=vb_va['Año'],
    y=vb_va['Porcentaje_suma'],  
    mode='lines',  # Solo puntos
    name='Porcentaje Suma',
    marker=dict(symbol='circle', color='black')  # Opcional: Estilo de marcador
).update_xaxes(
    tickvals=[1984, 1989, 1994, 1999, 2004, 2009, 2014, 2019])

# Creación de la aplicación Dash

tab_0 = [dbc.Row([
dbc.Col(dcc.Graph(figure=fig0), md=12),
])]

tab_1 = [dbc.Row([
dbc.Col(dcc.Graph(figure=fig1), md=12),
])]


tab_1_1 =[dbc.Row([
  dbc.Col(dcc.Graph(figure = segunda_vuelta), md=12),
])]

tab_2 =[html.Br(),
                                  html.H3("Desempeño electoral estático"),
                                  dbc.Row([
                                      dbc.Col(
                                            dcc.Dropdown(id="dropdown_eleccion", options=[
                                              {"label": "1922", "value": "Resultados de las elecciones de 1922"},
                                              {"label": "1926", "value": "Resultados de las elecciones de 1926"},
                                              {"label": "1930", "value": "Resultados de las elecciones de 1930"},
                                              {"label": "1938", "value": "Resultados de las elecciones de 1938"},
                                              {"label": "1942", "value": "Resultados de las elecciones de 1942"},
                                              {"label": "1946", "value": "Resultados de las elecciones de 1946"},
                                              {"label": "1950", "value": "Resultados de las elecciones de 1950"},
                                              {"label": "1954", "value": "Resultados de las elecciones de 1954"},
                                              {"label": "1958", "value": "Resultados de las elecciones de 1958"},
                                              {"label": "1962", "value": "Resultados de las elecciones de 1962"},
                                              {"label": "1966", "value": "Resultados de las elecciones de 1966"},
                                              {"label": "1971", "value": "Resultados de las elecciones de 1971"},
                                              {"label": "1994", "value": "Resultados de las elecciones de 1994"},
                                              {"label": "1999", "value": "Resultados de las elecciones de 1999"},
                                              {"label": "2004", "value": "Resultados de las elecciones de 2004"},
                                              {"label": "2009", "value": "Resultados de las elecciones de 2009"},
                                              {"label": "2014", "value": "Resultados de las elecciones de 2014"},
                                              {"label": "2019", "value": "Resultados de las elecciones de 2019"}]

                                   ,placeholder="Seleccionar año de la elección"), width=6)]),
                                   dbc.Row([dbc.Col(dcc.Graph(id="graph_tipo")),])]

## guia analoga

tab_3 = [dbc.Row([
dbc.Col(dcc.Graph(figure=fig1_2), md=12),
])]

tab_4 = [dbc.Row([
dbc.Col(dcc.Graph(figure=fig_4), md=12),
])]

# Diseño general de la aplicación

app.layout = dbc.Container([
    html.H1(
        "Visualizador de datos de las Elecciones Nacionales en el Uruguay", 
        style={"font-size": "3rem", "text-align": "center", "color": "#333"}  # Personalización del estilo
    ),
    html.Br(),

    # Tarjeta que muestra los  datos en forma de tabla
    #dbc.Card([
    #    dbc.CardHeader(html.H5("General")),  # Encabezado de la tarjeta
    #    dbc.CardBody(
    #        dbc.Table.from_dataframe(tabla, striped=True, hover=True, bordered=True, responsive=True)
    #    )  # Cuerpo de la tarjeta que contiene la tabla
    #], color="primary", outline=True),  # Estilo y borde de la tarjeta

    html.Br(),  # Salto de línea

    # Pestañas que contienen los gráficos definidos previamente en 'tab_1', 'tab_2'
    dbc.Tabs([
        dbc.Tab(tab_0, label="Elecciones nacionales generales (1922-1971)", className = 'text-dark'), # etiquetas
        dbc.Tab(tab_1, label="Elecciones nacionales generales (1984-2019)"), 
        dbc.Tab(tab_1_1, label="Balotaje (Segunda vuelta)"),  # etiqueta titulo de primer tab 
        dbc.Tab(tab_2, label="Desempeño por elección histórico"), # etiqueta de segundo
        dbc.Tab(tab_3, label="Desempeño electoral de los bloques aliados (1984-2019)"),
        dbc.Tab(tab_4, label="Votos en blanco y anulado (1984-2019)")
          # Pestaña para visualizar pruebas
    ])
], fluid=True, style={'color': 'black'})


# Llamar al Callback y funcion de la pestana 2
@app.callback( Output('graph_tipo', 'figure'),[Input('dropdown_eleccion', 'value')])
def crear_grafico_pestana_2(value):
    if value == "Resultados de las elecciones de 1922":
      return fig0_0
    elif value == "Resultados de las elecciones de 1926":
      return fig0_1
    elif value == "Resultados de las elecciones de 1930":
      return fig0_2
    elif value == "Resultados de las elecciones de 1938":
      return fig0_3
    elif value == "Resultados de las elecciones de 1942":
      return fig0_4
    elif value == "Resultados de las elecciones de 1946":
      return fig0_5
    elif value == "Resultados de las elecciones de 1950":
      return fig0_6
    elif value == "Resultados de las elecciones de 1954":
      return fig0_7
    elif value == "Resultados de las elecciones de 1958":
      return fig0_8
    elif value == "Resultados de las elecciones de 1962":
      return fig0_9
    elif value == "Resultados de las elecciones de 1966":
      return fig0_10
    elif value == "Resultados de las elecciones de 1971":
      return fig0_11   
    elif value == "Resultados de las elecciones de 1984":
      return fig2_0
    elif value == "Resultados de las elecciones de 1989":
      return fig2_1
    elif value == "Resultados de las elecciones de 1994":
      return fig2_2
    elif value == "Resultados de las elecciones de 1999":
      return fig2_3
    elif value == "Resultados de las elecciones de 2004":
      return fig2_4
    elif value == "Resultados de las elecciones de 2009":
      return fig2_5
    elif value == "Resultados de las elecciones de 2014":
      return fig2_6
    elif value == "Resultados de las elecciones de 2019":
      return fig2_7
    else:
      return{}

# Llamar al callback y funcion de la pestana 3 (como la pestana 3 no tiene nada interactivo entonces no tiene ningun callback)

# Llamar al callback de la pestana 4 (IDEM)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render asigna el puerto
    app.run_server(host="0.0.0.0", port=port)


