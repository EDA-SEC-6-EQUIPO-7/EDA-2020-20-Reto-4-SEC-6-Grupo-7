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


# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print('----------------------------')
    print('NAME RETO')
    print('BIENVENID@')
    print('1- Inicializar Analizador')
    print('2- Cargar Dato')
    print('3- (Req. 1)')
    print('4- (Req. 2)')
    print('5- (Req. 3)')
    print('6- (Req. 4)')
    print('7- (Req. 5)')
    print('8- (Req. 6)')
    print('9- (Req. 7)')
    print('10- (Req. 8)')
    print('0- Exit')
    print('----------------------------')
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opcion\n')

    if int(inputs[0]) == 1:
        citibike = controller.newAnalyzer()

    elif int(inputs[0]) == 2:
        
        citinike = controller.loadTrips(citibike)

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass
    
    elif int(inputs[0]) == 5:
        pass
    
    elif int(inputs[0]) == 6:
        pass
    
    elif int(inputs[0]) == 7:
        pass

    elif int(inputs[0]) == 8:
        pass
    
    elif int(inputs[0]) == 9:
        pass

    elif int(inputs[0]) == 10:
        pass

    else:
        sys.exit(0)
sys.exit(0)