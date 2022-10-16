from array import array
from math import comb
import numpy as np
import itertools as it
import warnings

def incidToConectMatrix(matrix, vector_conf):
    initial_matrix = np.zeros([len(matrix[:,0]),len(matrix[:,0])], dtype=int)
    for i in range(0,len(matrix[0,:])):
        indexes = np.where(matrix[:,i] == 1)[0]
        # print(indexes)
        initial_matrix[indexes[0]][indexes[1]] = i+1
        initial_matrix[indexes[1]][indexes[0]] = i+1
    
    print("Matrix de conectividad")
    print(initial_matrix)
    return initial_matrix;

def getNumbers(array):
    aux = []
    i = 0
    while(i < len(array)-1):
        if(array[i] != 0):
            aux.append(array[i])
        i+=1
    return aux
            
def getCombination(matrix):
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

def deleteCombination(matrix, combinations):
  
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
        if(len(combinations[i])>len(delete2)):
            break;
        equals = (delete2 == combinations[i]).all()
        if(equals):
            # print("Es igual en la posición ", i , "del array de combinaciones")
            del copyCombinations[i]
            
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
                    
    # for i in range(0,len(delete1)):
    #     for j in range(0,len(combinations)):
    #         if(j < len(combinations)):
    #             aux1 = [delete1[i]]
    #             aux2 = combinations[j]
    #             if(aux1 == aux2):
    #                 # print("Es igual en la posición ", j , "del array de combinaciones")
    #                 del copyCombinations[j]
    return copyCombinations


def ignoreWarning():
    return warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 
    

def getMCS(matrix,combinations):
    matrixInicial = matrix
    final_mcs = []
    # for i in range(3,4):
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
        
        
        print("MCS")
        print(array_mcs)
        final_mcs.append(array_mcs)
        
    return final_mcs # VA FALTANDO IR GUARDANDO LOS MCS JUNTO CON LA COMBINACION ASOCIADA Y RETORNARLO (SERÁ NECESARIO PONER LA COMBINACION ASOCIADA?)
        

incid_matrix = np.genfromtxt('matrix_incid_5_8.csv', delimiter=',', dtype=int)
vector_conf = np.genfromtxt('vector_conf_5_8.csv', delimiter=',')
matrix = incidToConectMatrix(incid_matrix,vector_conf)

mcs_array = []
# Aquí obtengo los MCS de la primera y ultima fila 
if(len(matrix)>=2):
    first_column = matrix[:,0]
    last_column = matrix[:,len(matrix)-1]
    mcs_array.append(getNumbers(first_column))
    mcs_array.append(getNumbers(last_column))
else:
    first_column = matrix[:,0]
    mcs_array.append(getNumbers(first_column))


ignoreWarning() #Para eliminar los "warnings" que me salian por consola por algunas librerias

print("MCS iniciales",mcs_array)
arrayCombinations = getCombination(matrix)
print("Combinaciones antes de eliminar",arrayCombinations)
arrayCombinations = deleteCombination(matrix,arrayCombinations) #Aquí paso las combinaciones totales y me las entrega eliminando las que no correspondan
print("Combinaciones despues de eliminar",arrayCombinations)

mcs_array.append(getMCS(matrix,arrayCombinations))
print(mcs_array)




