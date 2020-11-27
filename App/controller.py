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
        origin = trip['start station id']
        destination = trip['end station id']
        anio = int(trip['birth year'])
        rangoEdad = model.rangoEdad(anio)
        model.putMap(citibike['startStationAge'],origin)
        model.putMap(citibike['endStationAge'],destination)
        model.addAge(citibike['startStationAge'],origin, rangoEdad)
        model.addAge(citibike['endStationAge'],destination,rangoEdad)
        model.addLocation(citibike['stations location'],trip)
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
    #print(type(model.bfSearch(citibike['stations'],'72')['visited']['table']['elements']))
    #print(type(model.adjacents(citibike['stations'],'72')))
    
    return citibike            

def rutaPorResistencia(citibike, idS, t):
    rutas = model.newList()
    times = model.newList()
    estaciones = model.newList()
    busqueda = model.bfSearch(citibike,idS)
    lst = busqueda['visited']['table']['elements']
    for el in lst:
        if el['key'] != None and el['value']['distTo']>1:
            ti = 0
            iterator = model.newIterator(model.pathto(busqueda, el['key']))
            ruta = model.newList()
            repetido =True
            while model.hasNext(iterator) and ti <= t and repetido:
                estacion = model.nextIterator(iterator)   
                if estacion == idS:
                    model.addLast(ruta,estacion)
                elif estacion not in estaciones['elements']:
                    model.addLast(estaciones, estacion)
                    model.addLast(ruta, estacion)
                else:
                    repetido = False
                if ruta['size'] >= 2:
                    a = ruta['size']-1
                    b = ruta['size']
                    ti += model.getDuration(citibike,model.getElement(ruta, a),model.getElement(ruta, b))
            repetido = True
            
            if ti > t:
                a = ruta['size']-1
                b = ruta['size']
                ti -= model.getDuration(citibike,model.getElement(ruta, a),model.getElement(ruta, b))
                model.deleteLast(ruta)

            
            if ruta['size']>1:
                model.addLast(rutas, ruta)
                model.addLast(times, ti)
  
    return rutas

def estacionMasUsada(lst, edad):
    max = 0
    estacion = 'Ninguna'
    listaEstaciones = lst['table']['elements']
    for estacionId in listaEstaciones:
        if listaEstaciones[estacionId][edad] > max:
            estacion = estacionId
    
    return estacion

def rangoEdad(anio):
    return model.rangoEdad(anio)

def caminoMasCorto(citibike, va, vb):

    return model.djisktraCamino(citibike,va,vb)


def print6(citibike, rutas):
    j = 0
    for ruta in rutas['elements']:
        j+=1
        print('Ruta', j)
        i = 0
        while i+1 < ruta['size']:
            a = ruta['elements'][i]
            b = ruta['elements'][i+1]
            t = round(model.getDuration(citibike, a, b)/60,1)
            print(a,'--->',b, ' : ', t)
            i+=1
def print7(lst):
    iterator = model.newIterator(lst)

    while model.hasNext(iterator):
        segmento = model.nextIterator(iterator)
        a = segmento['vertexA']
        b = segmento['vertexB']
        t = round(segmento['weight']/60,1)
        print(a,'--->',b, ' : ', t)

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def numCluster(citibike):
    
    return model.numSCC(citibike['stations'])

def mismoCluster(citibike, id1, id2):

    return model.sameCC(citibike['stations'], id1, id2)

def test2(grf):
    print(model.getDuration(grf,'72','3533'))

def test(grf):
    rutas = model.newList()
    busqueda = model.bfSearch(grf,'72')
    lst = busqueda['visited']['table']['elements']
    for el in lst:
        
        if el['key'] != None:
            print('-----------------------')
            print(el)
            ti = 0
            iterator = model.newIterator(model.pathto(busqueda, el['key']))
            ruta = model.newList()
            while model.hasNext(iterator) and ti <= 5400:
                model.addLast(ruta,model.nextIterator(iterator))
                if ruta['size'] >= 2:
                    a = ruta['size']-1
                    b = ruta['size']
                    ti += model.getDuration(grf,model.getElement(ruta, a),model.getElement(ruta, b))
            print(ruta['elements'])
            print(ti)
            print('::::::::::::::::::::::::')
            if ti> 5400:
                a = ruta['size']-1
                b = ruta['size']
                ti -= model.getDuration(grf,model.getElement(ruta, a),model.getElement(ruta, b))
                model.deleteLast(ruta)
            print(ruta['elements'])
            print(ti)
            model.addLast(rutas, ruta)

    #bus = model.bfSearch(grf,'72')
    #lst = bus['visited']['table']['elements']
    #for el in lst:
        #if el['key'] != None:
            #print(el['key'])
         #   iterator = model.newIterator(model.pathto(bus, el['key']))
        #    while model.hasNext(iterator):
       #         while model.hasNext(iterator) and ti <= t:
      #          model.addLast(ruta, model.nextIterator(iterator))
     #           if len(ruta) > 2:
    #                ti += model.getDuration(citibike,ruta[len(ruta)-1],ruta[len(ruta)])
        #print(el['key'])
    #print(iterator)
    #while model.hasNext(iterator):
        #print(iterator['iterable_lst']['first']['info'])
        #print(model.nextIterator(iterator))
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

