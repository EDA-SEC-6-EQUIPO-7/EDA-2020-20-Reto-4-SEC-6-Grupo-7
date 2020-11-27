"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bfs 
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import scc
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():

    citibike = {
                'stations':None,
                'startStationAge':None,
                'endStationAge':None,
                'stations location':None
                }
    
    citibike['stations'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=comparestations)
    
    citibike['startStationAge'] = newMap()
    
    citibike['endStationAge'] = newMap()

    citibike['stations location'] = newMap()
    
    return citibike

# Funciones para agregar informacion al grafo

def addConnection(citibike, origin, destination, duration):

    edge = gr.getEdge(citibike['stations'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['stations'], origin, destination, duration)
    return citibike

def addStation(citibike, stationid):

    if not gr.containsVertex(citibike ['stations'], stationid):
            gr.insertVertex(citibike ['stations'], stationid)
    return citibike

def addTrip(citibike, trip):

    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    anio = int(trip['birth year'])
    rangoAge = rangoEdad(anio)
    putMap(citibike['startStationAge'],origin)
    putMap(citibike['endStationAge'],destination)
    addAge(citibike['startStationAge'],origin, rangoAge)
    addAge(citibike['endStationAge'],destination,rangoAge)
    addLocation(citibike['stations location'],trip)
    addLocation(citibike['stations location'],trip)
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)

def addLocation(mapa, trip):
    value = (trip['start station name'], trip['start station latitude'],trip['start station longitude'])
    value2 = (trip['end station name'], trip['end station latitude'],trip['end station longitude'])
    ids = trip['start station id']
    ids2 = trip['end station id']
    if ids in mapa['table']['elements']:
        pass
    else:
        mapa['table']['elements'][ids] = value
    
    if ids2 in mapa['table']['elements']:
        pass
    else:
        mapa['table']['elements'][ids2] = value
# ==============================
# Funciones de consulta
# ==============================
def numSCC(graph):

    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def sameCC(graph, station1, station2):
    sc = scc.KosarajuSCC(graph)
    return scc.stronglyConnected(sc, station1, station2)

def numVertices(analyzer):
   
    return gr.numVertices(analyzer['stations'])

def numArcos(analyzer):
   
    return gr.numEdges(analyzer['stations'])

def sizeGraph(analyzer):

    return m.size(analyzer['stations']['vertices'])

def newMap():

    mapa = m.newMap()
    mapa['table']['elements'] = {}
    return mapa 

def VertexList(analyzer):

    return gr.vertices(analyzer['stations'])

def ArcosOut(analyzer, vertex):

    return gr.outdegree(analyzer['stations'], vertex)
    
def ArcosIn(analyzer, vertex):

    return gr.indegree(analyzer['stations'], vertex)
    
def isPresent(lst, elm):

    return lt.isPresent(lst,elm)

def getDuration(graph, va, vb):
    
    return gr.getEdge(graph,va, vb)['weight']

def getElement(lst, pos):

    return lt.getElement(lst, pos)

def djisktraCamino(graph, va, vb):
    search = djk.Dijkstra(graph, va)
    if djk.hasPathTo(search, vb):

        return djk.pathTo(search, vb)
    else:
        return 'no hay camino'
# ==============================
# TAD
# ==============================
def newList():

    return lt.newList('ARRAY_LIST')

def deleteLast(lst):

    return lt.removeLast(lst)

def deleteFirst(lst):

    return lt.removeFirst(lst)
    
def getMap(mapa, key):

    return mapa['table']['elements'][key]

def bfSearch(graph, vertice):

    return bfs.BreadhtFisrtSearch(graph, vertice)

def pathto(search, vertice):

    return bfs.pathTo(search, vertice)

def addLast(lst, elm):

    return lt.addLast(lst, elm)

def isNotNone(el):

    return el['key'] != None

def getList(busqueda):

    return busqueda['visited']['table']['elements']

def getDistance(el):

    return el['value']['distTo']

def getKey(el):

    return el['key']

def getSize(lst):

    return lst['size']

def getListmap(lst):

    return lst['table']['elements']
# ==============================
# Funciones Helper
# ==============================
def edad(anio):

    return 2020-anio

def rangoEdad(anio):
    age = edad(anio) 
    if age >= 0 and age <= 10:
        return '0-10'
    elif age >= 11 and age <= 20:
        return '11-20'
    elif age >= 21 and age <= 30:
        return '21-30'
    elif age >= 31 and age <= 40:
        return '31-40'
    elif age >= 41 and age <= 50:
        return '41-50'
    elif age >= 51 and age <= 60:
        return '51-60'
    else:
        return '+60'

def putMap(mapa, key):
    value = {'0-10':0,
            '11-20':0,
            '21-30':0,
            '31-40':0,
            '41-50':0,
            '51-60':0,
            '+60':0
            }

    if key not in mapa['table']['elements']:
        mapa['table']['elements'][key] = value

def addAge(mapa, key, edad):

    getMap(mapa, key)[edad] += 1

# ==============================
# Funciones de Comparacion
# =============================
def comparestations(station, keyvaluestation):

    code = keyvaluestation['key']
    if(station == code):
        return 0
    elif(code > code):
        return 1
    else:
        return -1

# ==============================
# Funciones de iteracion
# ==============================

def newIterator(lst):

    return it.newIterator(lst)

def hasNext(iterator):

    return it.hasNext(iterator)

def nextIterator(iterator):

    return it.next(iterator)