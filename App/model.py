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
                'stations':None
                }
    
    citibike['stations'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=1000,
                                        comparefunction=comparestations)
    
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
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)

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

def siseGraph(analyzer):

    return m.size(analyzer['stations']['vertices'])
# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def comparestations(station, keyvaluestation):

    code = keyvaluestation['key']
    if(station == code):
        return 0
    elif(code > code):
        return 1
    else:
        return -1