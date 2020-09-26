from scipy.optimize import linprog  #Librería para optimización
from copy import deepcopy           #Librería para copiar nodos
import random                       #Librería para operaciones aleatorias
import math                         #Librería para operaciones matemáticas

hojas = []                          #Vector de hojas

#Definición de la clase nodo
class node():
    #Metodo constructor para objeto tipo nodo
    def __init__(self, z, c, A, b, entero = False, factible = False, res = None):
        self.left = None          #Rama izquierda
        self.right = None         #Rama derecha
        self.z = z.capitalize()   #Variable que define si el problema es de Maximización o Minimización
        self.c = c                 #Lista de Coeficientes de funcion objetivo
        self.A = A                 #Lista de Coeficientes de restricciones
        self.b = b                 #Lista de Lados derechos
        self.res = res             #Lista con la solución encontrada del problema
        self.entero = entero       #Variable que define si el problema encontrado es entero o no
        self.factible = factible   #Variable que define si el problema encontrado es factible o no
        
    #Método que regresa todos los atributos de un objeto en una lista
    def toList(self):
        return [self.z, self.c, self.A, self.b, self.entero, self.factible, self.res]
    
    #Método para imprimir la solucion
    def printSolucion(self):
        print("\nZ* = ", self.res.fun)
        for i, x in enumerate(self.res.x):
            print("X_", i, "*= ", x)

#Definicion de la clase árbol
class arbol():
    #Metodo constructor para objeto tipo arbol
    def __init__(self):
        self.root = None      #Root es la raíz del árbol

    def insertRoot(self, nodo, z, c, A, b ):  #Este es para la raiz del arbol
        if nodo == None:               #Si no existe, 
            nodo = node(z, c, A, b)     #declaramos la raiz con el problema
        return nodo           

    def insertar(self, nodo, bNueva, i, direccion): #Este es para las ramas del arbol
        nuevo = deepcopy(nodo)      
        ANueva = []                             #Definimos la nueva restriccion que vamos a meter
        for indice in range(len(nodo.c)):    
            if(indice == i):
                if(direccion == 'izquierda'): #Si metes el nodo a la izquierda es restriccion <= y la variable toma el valor de 1 
                    ANueva.append(1.0)         
                else:
                    ANueva.append(-1.0) #Si lo metes a la derecha es restriccion de >= y la variable toma el valor de -1 
            else:                              
                ANueva.append(0.0)  #Donde no este la variable pone un 0
                
        nuevo.A.append(ANueva)      #Se guarda la nueva restriccion
        
        if(direccion == 'izquierda'):  #Agregamos el nuevo nodo izquierdo o derecho y agregamos el nuevo lado derecho
            nuevo.b.append(bNueva)     #Si es la lado izquierdo no se cambia el signo por el <=
            nodo.left = nuevo          
        else:
            nuevo.b.append(-bNueva)     #Si es al lado derecho se cambia el signo por el >=
            nodo.right = nuevo

def initProblem():
    
    arch = open(r"Data.txt", "r")     #Se abre el archivo Datos para lectura
    z = "Max"                                       #Es un problema de maximizar
    n = float(arch.readline())                      #Se lee el numero de objetos a guardar en la mochila
    c = []                                          #Se declara el vector de coeficientes de funcion objetivo(Beneficios)
    for number in arch.readline().split(','):       #Lee la linea de beneficios y agarra los valores separados por comas
        c.append(-float(number))                    #Guarda los valores en el vector (Negativo porque es Maximizar)
    A = []                                          #Se declara el vector de coeficientes de cada restriccion
    for number in arch.readline().split(','):       #Lee la linea de pesos y agarra los valores separados por comas
        A.append(float(number))                     #Guarda los valores en el vector
    if len(c) != n or len(A) != n:
        print("Error en lectura de datos. Revisar Datos.txt")
        return None
    A = [A]                                         #Vector de restricciones(Solo hay 1 restriccion en este caso)
    b = [float(arch.readline())]                    #Se lee la capacidad máxima de la mochila
    arch.close()                                    #Se cierra el archivo Datos
    
    return tree.insertRoot(tree.root, z, c, A, b)  #Se inserta el nodo raiz con el problema principal relajado

def resolverProblema(nodo):
    nodo.res = linprog(nodo.c, nodo.A, nodo.b, None, None, (0,None), method='simplex') #Me da el valor optimo, si es factible y el valor de cada X
    if nodo.z == "Max":                           
        nodo.res.fun = nodo.res.fun*-1      #Como la libreria tiene solo para Minimizar, multiplicamos por -1 para que sea de Maximizar
    
def subProblema(nodo):
    ran = [nodo.res.x[i] if not nodo.res.x[i].is_integer() else 0 for i in range(len(nodo.c))] #Hacemos un nuevo arreglo con las varibales que no sean enteras, si es entera pone un 0 , si no lo es pone el valor
    i = 0
    bNueva = 0
    while bNueva == 0:
        i = random.randrange(0, len(ran))  #Toma una varibale random de las que no son enteras
        bNueva = ran[i]   #Nuevo lado derecho
    
    tree.insertar(nodo, math.floor(bNueva), i, 'izquierda') #Lado izquiero le estamos mandando el piso
    bab(nodo.left) #Funcion recursiva para resolver la rama izquierda
    tree.insertar(nodo, math.ceil(bNueva), i, 'derecha') #Lado derecho le estoy mandando el techo
    bab(nodo.right) #Funcion recursiva para resolver la rama derecha
       
def bab(nodo):
    resolverProblema(nodo)           #Se resuelve el problema en el nodo
    nodo.factible = nodo.res.success #Checar si es factible o no
        
    #Checamos si es entero o no
    if (not nodo.res.fun.is_integer() or True in [not x.is_integer() for x in nodo.res.x]) and nodo.factible:
        subProblema(nodo) #Si no es entero empezamos la ramificacion
    elif nodo.factible:     #Si todos son enteros y el problema es factible entonces
        nodo.entero = True #Define el problema como entero
        nodo.printSolucion()            #Se imprime la solucion del problema en el nodo
        hojas.append(nodo.res)          #Se agrega la hoja al arreglo de hojas
    else:
        nodo = None
    
tree = arbol() #Declaro una variable tree de tipo de arbol
tree.root = initProblem()    #  Defino el nodo principal, la raiz del arbol

if tree.root != None:       #Si la lectura de datos no tuvo problemas

    print("\nHojas: ")
    
    bab(tree.root)          #Inicio del algoritmo
    
    mayor = 0               #Variable auxiliar que contiene la funcion objetivo mayor 
    variables = []          #Vector auxiliar que contendrá la solucion óptima
    for res in hojas:       #Se recorre el arreglo de hojas
        if res.fun > mayor:             #Si la funcion objetivo de la hoja es mayor a la mayor entonces
            mayor = res.fun             #El mayor ahora es el valor de la funcion objetivo
            variables = list(res.x)     #Se guardan las variables en el vector auxiliar
            
    print("\nSolución Óptima")
    print("Z* = ", mayor)                   #Se imprime el valor de la función objetivo
    for i,j in enumerate(variables):        #Se imprimen las variables de la solución óptima
        print("X_", i, "*= ", j)
