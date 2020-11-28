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

def rangoEdad(anio):

    return model.rangoEdad(anio)

def caminoMasCorto(citibike, va, vb):

    return model.djisktraCamino(citibike,va,vb)
# ___________________________________________________
#  Funciones de requerimeintos 
# ___________________________________________________
#  Requerimiento 3: Estaciones críticas
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
        m1=500000
        m2=500000
        m3=500000
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
        z=float(x)+float(y)
        dct[str(j)]=z
        j=it.next(iterador)

    return Top3(dct, False)


#  Requerimiento 4: Ruta turística porresistencia
def rutaPorResistencia(citibike, idS, t):
    rutas = model.newList()
    times = model.newList()
    estaciones = model.newList()
    busqueda = model.bfSearch(citibike,idS)
    lst = model.getList(busqueda)
    for el in lst:
        if model.isNotNone(el) and model.getDistance(el)>1:
            ti = 0
            iterator = model.newIterator(model.pathto(busqueda, model.getKey(el)))
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
                if model.getSize(ruta) >= 2:
                    a = model.getSize(ruta)-1
                    b = model.getSize(ruta)
                    ti += model.getDuration(citibike,model.getElement(ruta, a),model.getElement(ruta, b))
        
            repetido = True
            
            if ti > t and model.getSize(ruta)>=2:
                model.deleteLast(ruta)
                model.deleteLast(estaciones)
                a = model.getSize(ruta)-1
                b = model.getSize(ruta)
                ti -= model.getDuration(citibike,model.getElement(ruta, a),model.getElement(ruta, b))
           
            if model.getSize(ruta)>1:
                model.addLast(rutas, ruta)
                model.addLast(times, ti)

    return rutas

#REQ 5: Recomendador de Rutas
def estacionMasUsada(lst, edad):
    max = 0
    estacion = 'Ninguna'
    listaEstaciones = model.getListmap(lst)
    for estacionId in listaEstaciones:
        if listaEstaciones[estacionId][edad] > max:
            estacion = estacionId

    return estacion

#REQ 6: Recomendador de Rutas
def distancia(lat1, long1, lat2, long2):
    if float(lat1)>float(lat2):
        a=(float(lat1)-float(lat2))**2
        b=(float(long1)-float(long2))**2
        distancia=(a+b)**(1/2)
    else:
        a=(float(lat2)-float(lat1))**2
        b=(float(long2)-float(long1))**2
        distancia=(a+b)**(1/2)
    return distancia

def RutaTuristica(citibike, tabla, latT, longT, latL, longL):
    dT=None
    stationT=None
    stationTname=None
    dL=None
    stationL=None
    stationLname=None
    ruta =None
    lst=VertexList(citibike)
    iterador=it.newIterator(lst)
    j=it.next(iterador)
    while it.hasNext(iterador):
        x= model.getMap(tabla,j)
        if dT==None:
            dT=distancia(latT, longT, x[1], x[1])
            stationT=j
            stationTname=x[0]
        elif distancia(latT, longT, x[1], x[2])<dT:
            dT=distancia(latT, longT, x[1], x[2])
            stationT=j
            stationTname=x[0]
        if dL==None:
            dL=distancia(latL, longL, x[1], x[2])
            stationL=j
            stationLname=x[0]
        elif distancia(latL, longL, x[1], x[2])<dL:
            dL=distancia(latL, longL, x[1], x[2])
            stationL=j
            stationLname=x[0]
        j=it.next(iterador)

    search=  bfs.BreadhtFisrtSearch(citibike['stations'], stationT)

    #if bfs.hasPathTo(search, stationL):
    #    ruta=bfs.pathTo(search, stationL)
    ruta = caminoMasCorto(citibike['stations'],stationL,stationT)
    a=(stationTname, stationLname, ruta)
    return a
# ___________________________________________________
#  Funciones de impresion
# ___________________________________________________
def print4(Top3Entrada, Top3Salida, Top3MenosUsadas, citibike):
    print('Las 3 estaciones a las que mas bicicletas llegan son: ')
    for i in Top3Entrada:
        print(idToName(i,citibike)) 
    print('Las 3 estaciones de las que mas bicicletas salen son: ')
    for i in Top3Salida:
        print(idToName(i,citibike))
    print('Las 3 estaciones menos utilizadas son: ')
    for i in Top3MenosUsadas:
        if i != None:
            print(idToName(i,citibike)) 

def print5(citibike, rutas, citibikes):
    j = 0
    for ruta in rutas['elements']:
        j+=1
        print('Ruta', j)
        i = 0
        while i+1 < ruta['size']:
            a = ruta['elements'][i]
            b = ruta['elements'][i+1]
            t = round(model.getDuration(citibike, a, b)/60,1)
            a = idToName(ruta['elements'][i],citibikes)
            b = idToName(ruta['elements'][i+1],citibikes)
            print(a,'--->',b, ' : ', t)
            i+=1

def print6(lst,citibike):
    iterator = model.newIterator(lst)

    while model.hasNext(iterator):
        segmento = model.nextIterator(iterator)
        a = idToName(segmento['vertexA'],citibike)
        b = idToName(segmento['vertexB'],citibike)
        t = round(segmento['weight']/60,1)
        print(a,'--->',b, ' : ', t)

def print7(requerimiento,citibike):
    print("La estacion mas cercana al turista es: ", requerimiento[0])
    print("La estacion mas cercana al sitio a visitar es: ",requerimiento[1])
    print("La ruta a usar es: ",requerimiento[2])
    #print("El tiempo estimado de dicha ruta es",tiempo)

def idToName(id, citibike):

    lst = citibike['stations location']

    return model.getMap(lst, id)[0]
