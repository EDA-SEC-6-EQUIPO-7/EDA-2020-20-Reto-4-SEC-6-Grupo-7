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

import config as cf
from App import model
from DISClib.DataStructures import linkedlistiterator as it
from DISClib.DataStructures import probehashtable as h
from DISClib.Algorithms.Graphs import bfs
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def newAnalyzer():

    citibike = model.newAnalyzer()

    return citibike
# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadFile(citibike, tripfile):
    i = 0
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
        i+=1
    citibike['size'] = i
    return citibike

def loadTrips(citibike, filename):

    #for filename in os.listdir(cf.data_dir):
    #    if filename.endswith('.csv'):
    print('Cargando archivo: ' + filename)
    citibike = loadFile(citibike, filename)
    print('No. viajes:',citibike['size'])
    print('No. de Vertices:',model.numVertices(citibike))
    print('No. de Arcos:',model.numArcos(citibike))
    print('No de componentes fuertemente conectados:',model.numSCC(citibike['stations']))
    return citibike


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def numCluster(citibike):
    
    return model.numSCC(citibike['stations'])

def mismoCluster(citibike, id1, id2):

    return model.sameCC(citibike['stations'], id1, id2)

def VertexList(citibike):
    
    return model.VertexList(citibike)

def Top3(dct, MasUsada):
    if MasUsada==True:
        Station=None
        top3={}
        m1=0
        m2=0
        m3=0
        for i in dct:
            if dct[i]>m1:
                Station=i
                m1=dct[i]
        top3[Station]=m1
        for i in dct:
            if dct[i]>m2 and not(i in top3):
                Station=i
                m2=dct[i]
        top3[Station]=m2
        for i in dct:
            if dct[i]>m3 and not(i in top3):
                Station=i
                m3=dct[i]
        top3[Station]=m3
        return top3
    else:
        Station=None
        min3={}
        m1=0
        m2=0
        m3=0
        for i in dct:
            if dct[i]<m1:
                Station=i
                m1=dct[i]
        min3[Station]=m1
        for i in dct:
            if dct[i]<m2 and not(i in min3):
                Station=i
                m2=dct[i]
        min3[Station]=m2
        for i in dct:
            if dct[i]<m3 and not(i in min3):
                Station=i
                m3=dct[i]
        min3[Station]=m3
        return min3


def topSalida(citibike):
    dct={}
    lst=VertexList(citibike)
    iterador=it.newIterator(lst)
    j=it.next(iterador)
    while it.hasNext(iterador):
        x=model.ArcosOut(citibike, str(j))
        dct[str(j)]=x
        j=it.next(iterador)
    return Top3(dct, True)

def topEntrada(citibike):
    dct={}
    lst=VertexList(citibike)
    iterador=it.newIterator(lst)
    j=it.next(iterador)
    while it.hasNext(iterador):
        x=model.ArcosIn(citibike, str(j))
        dct[str(j)]=x
        j=it.next(iterador)
    return Top3(dct, True)

def MenosUsado(citibike):
    dct={}
    lst=VertexList(citibike)
    iterador=it.newIterator(lst)
    j=it.next(iterador)
    while it.hasNext(iterador):
        x=model.ArcosOut(citibike, str(j))
        y=model.ArcosIn(citibike, str(j))
        z=int(x)+int(y)
        dct[str(j)]=z
        j=it.next(iterador)
    return Top3(dct, False)

def distancia(lat1, long1, lat2, long2):
    if int(lat1)>int(lat2):
        a=(int(lat1)-int(lat2))**2
        b=(int(long1)-int(long2))**2
        distancia=(a+b)**(1/2)
    else:
        a=(int(lat2)-int(lat1))**2
        b=(int(long2)-int(long1))**2
        distancia=(a+b)**(1/2)
    return distancia

def RutaTuristica(citibike, tabla, latT, longT, latL, longL):
    dT=None
    stationT=None
    stationTname=None
    dL=None
    stationL=None
    stationLname=None
    lst=VertexList(citibike)
    iterador=it.newIterator(lst)
    j=it.next(iterador)
    while it.hasNext(iterador):
        x=h.get(tabla, j)
        if dT==None:
            dT=distancia(latT, longT, x[0], x[1])
            stationT=j
            stationTname=x[2]
        elif distancia(latT, longT, x[0], x[1])<dT:
            dT=distancia(latT, longT, x[0], x[1])
            stationT=j
            stationTname=x[2]
        if dL==None:
            dL=distancia(latL, longL, x[0], x[1])
            stationL=j
            stationLname=x[2]
        elif distancia(latL, longL, x[0], x[1])<dL:
            dL=distancia(latL, longL, x[0], x[1])
            stationL=j
            stationLname=x[2]
        j=it.next(iterador)

    search= bfs.BreadhtFisrtSearch(citibike, stationT)
    if bfs.hasPathTo(search, stationL):
        ruta=bfs.pathTo(search, stationL)
    a=(stationTname, stationLname, ruta)
    return a

