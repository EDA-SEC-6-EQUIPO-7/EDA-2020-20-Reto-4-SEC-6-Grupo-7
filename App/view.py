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


import sys
import config
from App import controller
from App import model
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________
filename = '201801-1-citibike-tripdata.csv'
#filename = '201801-2-citibike-tripdata.csv'
#filename = '201801-3-citibike-tripdata.csv'
#filename = '201801-4-citibike-tripdata.csv'
# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print('----------------------------')
    print('NAME RETO')
    print('BIENVENID@')
    print('1- Inicializar Analizador')
    print('2- Cargar Dato')
    print('3- Cantidad de Clusteres de viaje (Req. 1)')
    print('5- (Req. 3)')
    print('6- Ruta turística por resistencia (Req. 4)')
    print('7- Recomendador de Rutas (Req. 5)')
    print('8- Ruta de interés turístico (Req. 6)')
    print('9- (Req. 7)')
    print('10- (Req. 8)')
    print('0- Exit')
    print('----------------------------')
"""
Menu principal
"""
def option3():
    id1 = input('Ingrese el id de la estacion 1:\n')
    id2 = input('Ingrese el id de la estacion 2:\n')
    cluster = controller.numCluster(citibike)
    stations = controller.mismoCluster(citibike,id1,id2)
    print('El numero de clusters en el grafo es:',cluster)
    print('Las dos estaciones pertenecen al mismo cluster:',stations)

def option6():
    idStation = input('Ingrese el id de la estacion de inicio:\n')
    tmax = int(input('Ingrese el tiempo maximo que desea montar (en minutos):\n'))*60
    rutas = controller.rutaPorResistencia(citibike['stations'],idStation,tmax)
    controller.print6(citibike['stations'],rutas)  
def option5():
    Top3Entrada=controller.topEntrada(citibike)
    Top3Salida=controller.topSalida(citibike)
    Top3MenosUsadas=controller.MenosUsado(citibike)
    print('Las 3 estaciones a las que mas bicicletas llegan son ', Top3Entrada)
    print('Las 3 estaciones de las que mas bicicletas salen son', Top3Salida)
    print('Las 3 estaciones menos utilizadas son', Top3MenosUsadas)

def option8():
    latT=input("Ingrese la latitud del turista: ")
    longT=input("Ingrese la longitud del turista: ")
    latL=input("Ingrese la latitud del sitio a visitar: ")
    longL=input("Ingrese la longitud del sitio a visitar: ")
    requerimiento=controller.RutaTuristica(citibike, tabla, latT, longT, latL, longL)
    print("La estacion mas cercana al turista es: ",requerimiento[0])
    print("La estacion mas cercana al sitio a visitar es: ",requerimiento[1])
    print("La ruta a usar es: ",requerimiento[2])
    #print("El tiempo estimado de dicha ruta es",tiempo)

while True:
    printMenu()
    inputs = input('Seleccione una opcion\n')

    if int(inputs[0]) == 1:
        citibike = controller.newAnalyzer()

    elif int(inputs[0]) == 2:
        
        citibike = controller.loadTrips(citibike,filename)
        #controller.test(citibike['stations'])
        print(citibike['stations location'])
    elif int(inputs[0]) == 3:
        time = timeit.timeit(option3, number=1)
        print('El tiempo de ejecucion es de:',time)

    elif int(inputs[0]) == 4:
        pass
    
    elif int(inputs[0]) == 5:
        time = timeit.timeit(option5, number=1)
        print('El tiempo de ejecucion es de:',time)
    
    elif int(inputs[0]) == 6: #REQ 4

        option6()
    
    elif int(inputs[0]) == 7:
        anioNacimiento = int(input('Ingrese su año de nacimiento: \n'))
        edad = controller.rangoEdad(anioNacimiento)
        origin = controller.estacionMasUsada(citibike['startStationAge'],edad)
        print('Estacion inicial:',origin)
        destination = controller.estacionMasUsada(citibike['endStationAge'],edad)
        print('Estacion final',destination)
        path = controller.caminoMasCorto(citibike['stations'],origin,destination)
        controller.print7(path)

    elif int(inputs[0]) == 8:
        time = timeit.timeit(option8, number=1)
        print('El tiempo de ejecucion es de:',time)
    
    elif int(inputs[0]) == 9:
        pass

    elif int(inputs[0]) == 10:
        pass

    else:
        sys.exit(0)
sys.exit(0)