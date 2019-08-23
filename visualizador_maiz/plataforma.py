#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:57:30 2019

@author: datalab
"""

# Bibliotecas necesarias para utilizar 'dash'
import dash # Biblioteca principal, para crear la app en geneal
import dash_core_components as dcc # Contiene elementos como 'Dropdows', Botones y demás
import dash_html_components as html # Contiene todo lo que existe en HTML, como 'divs', headers y demás
from dash.dependencies import Input, Output # Se tratan de las funciones para generar 'callbacks'
from dash.exceptions import PreventUpdate # Función que ayuda a evitar errores al inicializar la aplicación

# Biblioteca para otras funcionalidades
import math # Se utilizan las funciones de raíz, potencia y logaritmo de la biblioteca
import pandas as pd # Para importar archivos tipo .csv
import geopandas as gpd # Para importar datos espaciales (e.g. .geojson)
import plotly.graph_objs as go # Para facilitar la escritura de algunos componentes de las gráficas y mapas

# Las siguientes dos líneas siempre se incluyen dentro de toda aplicación de 'dash'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# ¡Importante! Todos los archivos deben de contenerse dentro de una carpeta llamada 'assests', ubicada en el mismo lugar que el código

# ============================== VARIABLES INICIALES ================================================================================================

# Características del mapa que aparece al iniciar la aplicación
layout_inicial = dict(mapbox=dict(accesstoken = 'pk.eyJ1IjoicGxhYmxvMDkiLCJhIjoiLVdaOHJ5cyJ9.J3n95xgPc2yjnm6QyLuMYQ', # Token para acceso a Mapbox
                             center = dict(lat=23.6254,lon=-102.0054), # Coordenadas donde se ubica el centro del mapa
                             zoom = 4, # Nivel de acercamiento al mapa; mientras más grande, mayor acercamiento
                             # 'layers' es una lista de diccionarios, siendo cada diccionario una capa diferente
                             layers = [dict(sourcetype ='geojson', # También se pueden importar archivos .shp ('vector') o ráster ('raster')
                                            source = 'assets/estados.json', # Archivo dentro de la carpeta 'assets' a importar
                                            type = 'fill', # Siempre especificar para polígonos (fill) y líneas (line)
                                            opacity = 0.75, # Siempre especificar, pues por defecto es completa opacidad (1)
                                            )],
                            ))

# Secuencia de comandos para generar los elementos del 'Dropdown' donde se seleccionarán los estados ('menu_estados')
# Importar a través de GeoPandas
estados = gpd.read_file('assets/estados.json', dtype={'cve_ent':str}).sort_values('cve_ent')
# Generar lista con dos listas dentro, una de nombes y otra de claves
tmp_estados = [list(estados['estados'].unique()),list(estados['cve_ent'].unique())]
# Crear diccionario tipo Nombre:Clave a partir de listas anteriores
# Por emeplo, para la CDMX se tiene 'Ciudad de México':'09'
lista_estados = [{'label':a , 'value':b} for a,b in zip(tmp_estados[0],tmp_estados[1])]


# Importar GeoJSON de municipios a través de GeoPandas (Archivo aún muy pesado; pero, al simplificar más, se pierde mucho detalle)
municipios = gpd.read_file('assets/municipios.geojson', dtype={'cve_ent':str, 'cve_mun':str, 'csv_tipos':str}).sort_values('cve_mun')

# Importar .csv con Lista de Tipos de Maíz. A cada tipo también se le ha asignado una clave, existente en la columna 'clave'
maiz = pd.read_csv('assets/maiz.csv', dtype={'clave':str}).sort_values('raza')

# ======================================== APARIENCIA DE LA APLICACIÓN =====================================================================================

# 'app.layout' contiene todo sobre la apariencia de la aplicación. Sólo aquí se utiliza todo lo de las bibliotecas 'html' y 'dcc'
# Tradicionalmente, todos los elementos de la aplicación se conservan dentro de un 'Div', por lo que siempre se crea primero
app.layout = html.Div(children=[
        # Primer título de la página
        html.H1(children='Visualizador de Tipos de Maíz en México'),
        # Gráfica donde se contiene el mapa. Importante asignar un 'id' para poder modificar su contenido a través de los 'callbacks'
        # Las especificaciones dentro de 'style' permiten su visualización lado a lado con el siguiente elemento que se cree
        # El argumento clave de 'dcc.Graph' es 'figure', que será el que se modifique a través de los 'callbacks'; recordar que es un diccionario
        dcc.Graph(id = 'mapa', style={'width':'60%','display':'inline-block','height':'700px'}, figure={
                # 'figure' siempre contiene dos elementos; 'data' define qué tipo de gráfica se desea. Todas las existentes en 'plotly' pueden colocarse
                # Una de las gráficas que permiten mapas es 'scattermapbox', razón por la que se selecciona. Debido a que sólo se desea el mapa, se deja vacío.
                'data' : [go.Scattermapbox()],
                # 'layout' contiene todos los detalles estéticos de la gráfica, incluido el mapa. Se coloca la variable creada anteriormente.
                'layout' : go.Layout(layout_inicial),
                }),
        # Las especificaciones de 'style' permiten mostrar este 'div' y su contenido lado a lado con el elemento anterior.
        html.Div(style={'width':'30%','display':'inline-block','float':'right'}, children=[
                # Cada 'dropdown' se encuentra contenido dentro del 'div', y todos tienen su título gracias a los elementos 'H4'
                html.H4(children='Selecciona un estado...'),
                # Cada 'dropdown' también posee un 'id', para poder modificarlo a través de los 'callbacks'.
                dcc.Dropdown(id ='menu_estados',
                             # Define cuáles son los elementos que se mostrarán en el 'dropdown'. Se trata de un diccionario tipo label:value
                             # Donde 'label' es la etiqueta que se mostrará en la selección, y 'value' el valor con el que el código trabajará.
                             options = lista_estados,
                             # 'multi' define si se pueden seleccionar múltiples opciones a la vez
                             multi = False,
                             ),
                html.H4(children='Selecciona un municipio...'),
                dcc.Dropdown(id='menu_municipios',
                             options = [],
                             # 'disabled' determina si es posible interactuar con el menú o no. Se mantiene en 'True' para evitar interacciones no deseadas.
                             disabled = True,
                             multi = False
                             ),
                html.H4(children='Selecciona una especie de maíz...'),
                dcc.Dropdown(id='menu_maiz',
                             options = [],
                             disabled = True,
                             multi = False
                             ),
                ]),
        ])

# ==================================================== FUNCIONES TIPO CALLBACK (INTERACCIONES) =======================================================

# Es recomendable tener un único Output para cada callback. Si se seleccionan varios, es recomendable que pertenezcan al mismo elemento.
# Después de '@app.callback' se definen, primero, los 'Output', que son los elementos que resultarán modificados por esta función.
# Después, se definen los 'Input', que son las variables que se utilizarán dentro de la función
# Cada uno se define dentro de una lista, para poder incluir múltiples elementos si es necesario

# ================== PRIMERA FUNCIÓN
@app.callback(
        # En cada 'Output' se coloca primero el 'id' del elemento a modificar, y después cuáles de sus argumentos se modificará. Estos fueron creados anteriormente.
        # En este caso, del elemento 'mapa' se va a modificar su argumento 'figure'. Nosotros definimos el 'id'.
        [Output('mapa', 'figure')],
        # Los inputs siguen la misma lógica; en este caso, del elemento 'menu_estados' se utilizará su argumento 'value'
        [Input('menu_estados', 'value'), Input('menu_municipios', 'value'), Input('menu_maiz', 'value')],
        )
# Nótese que el orden de las variables de la función corresponde exactamente al orden en que se colocaron los elementos tipo 'Input'
# Puede decirse que aquí únicamente se les asigna nombre. Por ejemplo, a lo que 'Input('menu_estados', 'values')' haya arrojado se le dará el nombre 'cve_ent'
# La función 'zoom' se encarga de definir el posicionamiento en el mapa para determinar algún estado o municipio.
def zoom(cve_ent, cve_mun, cve_maiz):
    # ¡Nota Importante! ¿Qué contienen estas variables?
    # Como se mencionó anteriormente, a cada 'dropdown' se le asigna en su argumento 'options' un diccionario de tipo label:value, siendo 'value' con lo que
    # trabajará el código. En nuestro caso, el diccionario asignado fue de tipo Nombre:ClaveEntidad; por ende, si en el menú se selecciona la CDMX, el argumento
    # 'value' será '09'. Como tal, debido a que 'cve_ent' toma lo que haya en 'value', entonces para el ejemplo anterior cve_ent = '09'
    
    # Al inicializar la aplicación, 'dash' intenta ejecutar todas las funciones desde un inicio
    # Debido a que el menú de entidades comienza sin alguna selección, estas dos líneas evitan que el callback se ejecute y, por ende, evitan un error inicial.
    if cve_ent is None:
        raise PreventUpdate
    
    # El siguiente conjunto de comandos define si el acercamiento se hará a algún estado o a algún municipio
    # Si no se ha seleccionado ningún municipio, entonces el acercamiento será a un estado
    if cve_mun is None:
        lugar = estados.loc[estados['cve_ent']==cve_ent]
    # Si ya se ha seleccionado un estado y un municipio, y después se cambia de estado, esta línea permite reenfocar el mapa al nuevo estado
    # Aquí se compara la Clave del Estado con los primeros dos elementos de la Clave de Municipio
    elif cve_ent != cve_mun[:2]:
        lugar = estados.loc[estados['cve_ent']==cve_ent]
    # Si ya hay un municipio seleccionado, y corresponde al estado seleccionado, entonces se hará un acercamiento al municipio.
    else:
        lugar = municipios.loc[municipios['cve_mun']==cve_mun]
    
    # Para el cálculo del acercamiento y el lugar donde se posicionará el mapa, se necesita saber, primero, las coordenadas de su centroide.
    # Debido a que se importó un GeoJSON a través de GeoPandas, la misma librería puede utilizarse para obtenerlas
    x = lugar['geometry'].centroid.x.values[0]
    y = lugar['geometry'].centroid.y.values[0]
    
    # El cálculo también necesita conocer la longitud en metros de la diagonal de su 'Bounding Box'
    # Se transforma el Sistema de Coordenadas de Referencia a uno métrico para asegurar este resultado.
    lugar = lugar.to_crs(epsg = 6362)
    # La diagonal se calcula a través de la forma tradicional de calcular la distancia entre dos puntos √((x2-x1)² + (y2-y1)²)
    diagonal = math.sqrt(math.pow((lugar['geometry'].bounds['maxx'].values[0])-(lugar['geometry'].bounds['minx'].values[0]),2)+math.pow((lugar['geometry'].bounds['miny'].values[0])-(lugar['geometry'].bounds['maxy'].values[0]),2))
    
    # Fórmula para obtener zoom derivada de la utilizapor OpenStreetMaps (https://wiki.openstreetmap.org/wiki/Zoom_levels)
    zoom = math.log((4.0075*math.pow(10,7))*((math.cos(math.radians(y)))/(diagonal)),2)
    
    # Como se mencionó anteriormente, a un 'mapbox' pueden agregarse capas de datos vectoriales a través de su argumento 'layers'
    # Éste es una lista de diccionarios; como tal, se asigna primero.
    layers = []
    # Sin importar el tipo de zoom, siempre se colocará una capa de municipios de algún estado. Como tal,
    # se añade ésta capa, en función de cual estado se haya seleccionado.
    layers.append(dict(sourcetype ='geojson',
                       # 'mapbox' únicamente puede colocar capas que carga de forma local. No posee capacidad de utilizar un GeoDataFrame o similar
                       # Como tal, existe una carpeta que contiene un GeoJSON para cada uno de los estados del país, llamados a partir de la Clave de Entidad.
                       # Cuál se llama depende del valor de 'cve_ent'
                       source = 'assets/municipios/'+str(cve_ent)+'.geojson',
                       type = 'fill',
                       opacity = 0.75,
            ))
    
    # Una capa de tipo de maíz se asignará únicamente si existe algún tipo de maíz seleccionado. Este comando realiza el filtro.
    if not (cve_maiz is None or cve_maiz == '00'):
        layers.append(dict(sourcetype ='geojson',
                           # Al igual que con los municipios, cuál capa de maíz se coloque depende de la 'cve_maiz' asignada.
                           # Gracias a que a cada maíz tiene una clave asignada, es posible llamar a las capas de forma similar que a los municipios.
                           source = 'assets/maiz/'+str(cve_maiz)+'.geojson',
                           type = 'fill',
                           opacity = 0.75,
                           # El color con el que se llama a la capa.
                           color = 'red',
                ))
        
        
    
    # Dentro de 'return' se colocan todo lo que se colocará en lo que se ha definido como 'Output'
    # En este caso, debido aquí se coloca lo que se asignará al argumento 'figure' del elemento con el id 'mapa'
    # Como tal, el resultado debe de seguir exactamente la misma lógica de lo que se colocaría en este argumento 'figure'
    # Puede observarse que es muy similar a los valores que se tenían para el mapa inicial, únicamente asignando los calculados en la función.
    return [{
            'data': [go.Scattermapbox()],
            'layout': go.Layout(mapbox=dict(
                    accesstoken = 'pk.eyJ1IjoicGxhYmxvMDkiLCJhIjoiLVdaOHJ5cyJ9.J3n95xgPc2yjnm6QyLuMYQ',
                    center = dict(lat=y,lon=x),
                    zoom = zoom,
                    layers = layers,
                    ))
            }]

# ================ SEGUNDA FUNCIÓN
# Aquí se actualizan los elementos mostrados en el Menú de Municipios, en función del estado que se tenga seleccionado    
@app.callback(
        # Aunque se tienen múltiples 'Output', todos corresponden a un mismo elemento, evitando así algún posible error.
        [Output('menu_municipios', 'options'), Output('menu_municipios','disabled'), Output('menu_municipios','value')],
        [Input('menu_estados', 'value')]
        )
def opciones_municipios(cve_ent):
    # AL igual que con la función anterior, estas dos líneas permiten evitar un error al inicializar la aplicación.
    if cve_ent is None:
        raise PreventUpdate
    
    # Primero, se seleccionan todos los municipios del GeoDataFrame que pertenezcan al estado seleccionado.
    tmp1 = municipios[municipios['cve_ent'] == cve_ent]
    # Al igual que como se hizo con los estados en las variables iniciales, se crea una lista con dos listas en su interior: una con nombres y otra con claves.
    tmp2 = [list(tmp1['municipios'].unique()),list(tmp1['cve_mun'].unique())]
    # NUevamente, se crea el diccionario label:value con el que trabajará el menú de municipios, creándose de tipo Nombre:ClaveMunicipio
    # Por ejemplo, para el municipio de Aguascalientes 'Aguascalientes':'01001'
    lista_municipios = [{'label':a , 'value':b} for a,b in zip(tmp2[0],tmp2[1])]
    
    # El orden de los elementos que regresa la función es idéntico al orden en que se definieron los 'Output'
    # Primero, se regresa el diccionario definido anteriormente, para definir el contenido del menú
    # Después, se regresa 'False' para redefinir el argumento 'displayed' del menú, y se pueda interactuar con él
    # Finalmente, 'None' se asigna para que, siempre que se redefina la lista de municipios, no permanezca alguno incorrecto seleccionado.
    return lista_municipios, False, None


# =================== TERCERA FUNCIÓN
# Aquí se actualizan los elementos mostrados en el Menú de Tipos de Maíz, en función del estado y el muncipio seleccionado
@app.callback(
        [Output('menu_maiz', 'options'), Output('menu_maiz','disabled'), Output('menu_maiz','value')],
        [Input('menu_estados', 'value'), Input('menu_municipios', 'value')]
        )
# El orden de los 'Input' define el orden de las variables con las que se trabaja en la función
def opciones_maiz(cve_ent, cve_mun):
    # Nuevamente, estas dos líneas permiten evitar errores al inicializar la aplicación
    if cve_mun is None:
        raise PreventUpdate
        
    # En caso de que se haya seleccionado algún municipio y tipo de maíz, y se cambie de estado
    # Las siguientes líneas permiten reiniciar el contenido del menú de tipos de maíz, e inhabilitarlo hasta que se seleccione un nuevo municipio.
    if cve_ent != cve_mun[:2]:
        opciones_maiz = []
        disabled = True
        
    # Si ya se tiene un municipio, y corresponde al estado seleccionado, entonces puede definirse los tipos de maíz que aparecerán en el menú
    else:
        # ¡Nota Importante! ¿Cómo se sabe cuáles tipos de maíz se encuentran en cada municipio?
        # Debido tanto los tipos de maíz y los municipios se encuentran en formato espacial, fácilmente podría realizarse un cálculo de intersección para
        # responder la pregunta anterior; sin embargo, el número de municipios y tipos de maíz hacen que ésta sea una labor muy tardada en la aplicación.
        # Como tal, esto ha sido definido con anterioridad; en el GEoDataFrame 'municipios' existe una columna llamada 'csv_tipos' que contiene una serie
        # de números, los cuales aprovechan el hecho de que a cada maíz se le ha asignado una clave.
        # Por ejemplo, si un municipio posee en esta columna '01001', significa que el municipio posee los tipos de maíz con las claves '02' y '05'.
        # El código anterior posee una extensión de 47 caracteres, en línea con los 47 tipos de maíz registrados.
        
        # Se almacena el municipio de interés
        tmp1 = municipios.loc[municipios['cve_mun']==cve_mun]
        # Se guarda su código que define los tipos de maíz que posee el municipio.
        a = tmp1['csv_tipos'].values[0]
        # Esta lista guardará la clave en formato '00' de los tipos de maíz que posee el municipio
        b = []
        # El bucle analiza cada uno de los caracteres del código y, si en la posición #15 encuentra el número '1', entonces asignará el código '15', por ejemplo.
        for i in range(48):
            if a[i] == '1':
                if i < 9:
                    # La suma compensa el hecho de que Python comienza sus conteos desde el cero
                    # Esta línea en particular permite escribir códigos como '01', '02', '03', etc.
                    b.append('0'+str(i+1))
                else:
                    b.append(str(i+1))
        
        # En caso de que no exista ningún tipo de maíz en el municipio, se regresa el siguiente diccionario que define esto.
        if not b:
            opciones_maiz = [{'label':'El municipio no posee variedades de maíz', 'value': '00'}]
        else:
            # Para cada una de las claves de tipo de maíz en la lista 'b' se identifica el nombre que tienen asignado.
            for i in b:
                # Se encuentra el tipo de maíz en el archivo .csv cargado bajo el nombre 'maiz'
                tmp2 = maiz.loc[maiz['clave']==str(i)]
                # En caso de ser el primer elemento de la lista 'b', se crea la lista que contiene las otras dos listas de 'raza' y 'claves'
                # Ésta es la misma lógica utilizada con las entidades y los municipios.
                if i == b[0]:
                    c = [list(tmp2['raza'].unique()),list(tmp2['clave'].unique())]
                else:
                    c[0].append(tmp2['raza'].values[0])
                    c[1].append(tmp2['clave'].values[0])
            
            # Nuevamente, se crea el diccionario tipo label:value, esta vez siendo Raza:ClaveTipoMaíz
            opciones_maiz = [{'label':a , 'value':b} for a,b in zip(c[0],c[1])]
        disabled = False
    
    # El orden de lo que regresa la función corresponde exactamente con el que se definieron los 'Output' de la función
    # Primero, se regresa el diccionario con el que trabajará el menú de tipos de maíz
    # Después, se regresa lo que corresponde al argumento 'disabled' del menú, que define si se puede interactuar con él o no
    # Por último, 'None' permite que siempre se deseleccionar cualquier selección anterior cuando se redefina la lista de tipos de maíz
    return opciones_maiz , disabled, None
    

# Toda aplicación de 'dash' siempre se cierra con estas líneas
if __name__ == '__main__':
    app.run_server(debug=True) # 'debug=True' permite que la página se actualice al cambiar el código; hay que cambiar a 'False' al publicar