from array import array
from calendar import c
from math import comb
import numpy as np
import itertools as it
import warnings


matrix_incid = np.genfromtxt('matrix_incid_6_9.csv', delimiter=',', dtype=int)
vector_conf = np.genfromtxt('vector_conf_6_9.csv', delimiter=',')

# Elimina paralelos
def deleteParalels():
    global matrix_incid, vector_conf # Se define que estas variables son "globales" para así tener acceso a ellas desde la función
    i=0
    j=0
    while(i<matrix_incid[0,:].size and len(vector_conf)>1): # si i es menor que la cantidad de filas y el largo del vector de confiabilidad es > 1 se continua el ciclo hasta que alguna no se cumpla
        j=0     
        actual_col = matrix_incid[:,i] # La columna la cual se está comparando con todas las demás actualmente
        while(j<len(vector_conf)-1):
            check_col = matrix_incid[:,j] # Esta es la columna que va iterando
            if(np.dot(actual_col,check_col) == 2 and i!=j): # Si el producto punto es = 2 y no es la misma columna (i!=j)
                matrix_incid = np.delete(matrix_incid, j ,1) # Se elimina la columna que se encontró que era igual a la actual (actual_col)
                vector_conf[i] = (1-(1-vector_conf[i])*(1-vector_conf[j])) # Se aplica la funcion de estructura y se guarda en la posicion de la primera columna (i) del vector de confiabilidad
                vector_conf = np.delete(vector_conf,j,0) # Se elimina la posicion del vector de confiabilidad (j)
                j=0
            else: # Si el producto punto no es = 2 o es la misma columna (i==j)
                j+=1    
            if(j>=len(vector_conf)-1): # Mientras j sea mayor que el largo del vector de confiabilidad se itera i
                i+=1

          

# Elimina series  
def deleteSeries():
    global matrix_incid, vector_conf # Se define que estas variables son "globales" para así tener acceso a ellas desde la función
    i=0
    while(i<matrix_incid[:,0].size): # Mientras i sea menor que la cantidad de columnas
        actual_row = matrix_incid[i,:] # Fila actual que se tiene seleccionada
        if(sum(actual_row) == 2 and i!= 0 and i!= matrix_incid[:,0].size -1):  # Si la suma de la fila actual da igual a 2 significa que ese nodo está entre dos nodos más por lo tanto se encuentran en serie
        # if(sum(actual_row) == 2 ):  # Si la suma de la fila actual da igual a 2 significa que ese nodo está entre dos nodos más por lo tanto se encuentran en serie
            indexes = np.where(actual_row == 1) # Aqui se obtienen los indices de los 1 dentro de la fila actual
            matrix_incid  = np.delete(matrix_incid, i, 0) # Aqui se elimina la fila actual (la cúal sumó 2)
            matrix_incid[:,indexes[0][0]] = matrix_incid[:,indexes[0][0]] + matrix_incid[:,indexes[0][1]] # Aquí se suma las columnas de los indices donde se encontraron los 1 ( que se guardaron en la variable "indexes") y el resultado se guarda en la posición del primer 1 encontrado
            matrix_incid = np.delete(matrix_incid, indexes[0][1], 1) # Se elimina la columna del ultimo uno encontrado dentro de la fila 
            vector_conf[indexes[0][0]] = vector_conf[indexes[0][0]] * vector_conf[indexes[0][1]] # Se aplica la función de estructura y se guardan el resultado en la primera posición
            vector_conf = np.delete(vector_conf, indexes[0][1] , 0 ) # Se elimina la ultima posición de las 2 encontradas dentro del vector de confiabilidad
            deleteParalels() # Se ejecuta la función de eliminar paralelos debido a posibles paralelos que pueden aparecer al eliminar enlaces en serie
            i=0
        # 
        i+=1

        
def incidToConectMatrix(matrix): # Esta función genera la matriz de conectividad a partir de la matriz de incidencia ,  recibe cómo parámetro la matriz de incidencia 
    initial_matrix = np.zeros([len(matrix[:,0]),len(matrix[:,0])], dtype=int)
    for i in range(0,len(matrix[0,:])):
        indexes = np.where(matrix[:,i] == 1)[0]
        # print(indexes)
        initial_matrix[indexes[0]][indexes[1]] = i+1
        initial_matrix[indexes[1]][indexes[0]] = i+1
    # print("Matrix de conectividad")
    # print(initial_matrix)
    return initial_matrix;

def getNumbers(array): # Esta función retorna los números distintos de 0 en un array , recibe cómo parametro un array de números
    aux = []
    i = 0
    while(i < len(array)-1):
        if(array[i] != 0):
            aux.append(array[i])
        i+=1
    return aux
    
def getCombination(matrix): # Obtiene todas las combinaciones posibles , recibe cómo parámetro la matriz de conectividad 
    aux = []
    i = 1
    possible_combinations = list(range(1,len(matrix)-1))
    if(len(matrix)>=4):
        order = len(matrix)-2
    else:
        order = len(matrix)
        
    while(i < order):
        combination = list(it.combinations(possible_combinations,i))
        for j in range(0,len(combination)):
            aux.append(list(combination[j]))
        i+=1
    return aux

def deleteCombination(matrix, combinations): # Esta función elimina todas las combinaciones que no son un MCS , recibe cómo parámetro la matriz de conectividad y un array con las combinaciones
  
    #El vector "delete1" obtiene las combinaciones a eliminar debido a que la primera fila es 0 (entonces obtiene los indices a eliminar)
    delete1 = matrix[0,:] 
    delete1 = np.delete(delete1,0)
    delete1 = np.delete(delete1,len(delete1)-1)
    #El vector "delete2" obtiene las combinaciones a eliminar debido a que la ultima columna es distinta de 0 (entonces obtiene los indices a eliminar)
    delete2 = matrix[:,len(matrix)-1]
    delete2 = np.delete(delete2,0)
    delete2 = np.delete(delete2,len(delete2)-1)
    
    
    delete1 = np.where(delete1 == 0)
    delete2 = np.where(delete2 != 0)
    
    delete1 = [x+1 for x in delete1]
    delete2 = [x+1 for x in delete2]

    delete1 = delete1[0]
    delete2 = delete2[0]
    
    
    copyCombinations = np.copy(combinations).tolist() #Creo la copia porqe estoy eliminando elementos , así no tengo problemas al usar el len(combinations)
    
    #Aquí elimino las combinaciones exclusivamente en las que la ultima columna era != 0
    for i in range(0,len(combinations)): 
        equals = (delete2 == combinations[i]).all()
        if(equals):
            # print("Es igual en la posición ", i , "del array de combinaciones")
            del copyCombinations[i]
            break;
            
    #Aquí elimino las combinaciones en las cuales la primera fila era 0
    i=0
    j=0
    while i < len(delete1):
        while j < len(copyCombinations):
            if(j < len(copyCombinations)):
                aux1 = [delete1[i]]
                aux2 = combinations[j]
                if(aux1 == aux2):
                    # print("Es igual en la posición ", j , "del array de combinaciones")
                    del copyCombinations[j]
            j+=1
        i+=1
                    
    return copyCombinations


def ignoreWarning():
    return warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 
    
def getConfiability(mcs): # Esta función calcula la confiabilidad de la red , obtiene cómo parámetro un array con los MCS de la red

    numbers = np.arange(len(mcs))
    # print(mcs)
    # print(numbers)
    subsets = []
    combinations = []
    
    for x in range(len(mcs) + 1):
        for subset in it.combinations(numbers, x):
            subsets.append(list(subset))
    subsets.remove([])
    # print("Subsets")
    # print(subsets)
    

    for i in range(0,len(subsets)):
        aux = []
        for j in subsets[i]:
            for k in range(0,len(mcs[j])):
                if mcs[j][k] not in aux:
                    aux.append(mcs[j][k])
        combinations.append(aux)
    # print("Combinations")
    # print(combinations)
    
    confiability = 0
    resta = False
    subsetAnterior = subsets[0]
    cotas = 1
    for i in range(0,len(combinations)):
        times = 1
        if(len(subsets[i]) != len(subsetAnterior)):
            resta = not resta
            if(cotas < 5):
                print('Cota ', cotas)
                print(1-confiability)
                cotas+=1
        combiActual = combinations[i]
        for j in combinations[i]:
            times*=(1-vector_conf[j-1])
        if(resta):
            confiability-=(times)
        else:
            confiability+=(times)
            
        subsetAnterior =  subsets[i] 
    
    print("Confiabilidad final")
    print(1-confiability)
    
def getMCS(matrix,combinations): # Esta función obtiene todos los MCS recibe cómo parametros la matriz de conectividad y un array con las combinaciones 
    matrixInicial = matrix
    final_mcs = []
    
    # Aquí obtengo los MCS de la primera y ultima fila 
    if(len(matrix)>=2):
        first_column = matrix[:,0]
        last_column = matrix[:,len(matrix)-1]
        final_mcs.append(getNumbers(first_column))
        final_mcs.append(getNumbers(last_column))
    else:
        first_column = matrix[:,0]
        final_mcs.append(getNumbers(first_column))
    
    for i in range(0,len(combinations)):
        aux = np.copy(matrixInicial)
        array_mcs = []
        for j in range(0,len(combinations[i])):
            index_actual = combinations[i][j]
            aux[:,index_actual] = -1
        aux[:,0] = -1 # Hace la primera columna -1
        
        firstRow = True
        for k in combinations[i]:
            for l in range(0,len(matrix)):
                if(firstRow):
                    if(aux[0][l]!=-1 and aux[0][l]!=0):
                        array_mcs.append(aux[0][l])
                if(aux[k][l]!=-1 and aux[k][l]!=0):
                    array_mcs.append(aux[k][l])
            
            firstRow = False
        
        
        # print("MCS")
        # print(array_mcs)
        final_mcs.append(array_mcs)
        
    if [] in final_mcs:
        final_mcs.remove([])   
    return final_mcs 
        


print("------------------------")
# Eliminaciones serie paralelo
print("Cantidad de nodos pre SP")
print(len(matrix_incid[:,0]))
print("Cantidad de enlaces pre SP")
print(len(matrix_incid[0,:]))
print("------------------------")
deleteParalels() 
deleteSeries()
matrix = incidToConectMatrix(matrix_incid) # Transformo matriz de incidencia a matriz de conectividad
print("Cantidad de nodos post SP")
print(len(matrix_incid[:,0]))
print("Cantidad de enlaces post SP")
print(len(matrix_incid[0,:]))

ignoreWarning() #Para eliminar los "warnings" que me salian por consola por algunas librerias

print("------------------------")
arrayCombinations = getCombination(matrix) #Aquí obtengo todas las combinaciones posibles 
print("Combinaciones antes de eliminar",arrayCombinations)
arrayCombinations = deleteCombination(matrix,arrayCombinations) #Aquí paso las combinaciones totales y me las entrega eliminando las que no correspondan
print("Combinaciones despues de eliminar",arrayCombinations)
print("------------------------")
mcs_array = getMCS(matrix,arrayCombinations) # Aquí obtengo los MCS finales
print("Minimal cut sets finales")
print(mcs_array)
print("------------------------")

getConfiability(mcs_array) # Esta función me printea y calcula los valores de confiabilidad de la red junto con sus cotas (primeras 4 cotas)




