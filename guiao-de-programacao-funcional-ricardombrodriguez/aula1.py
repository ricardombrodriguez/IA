import math

#Exercicio 1.1
def comprimento(lista):
	if not lista:
		return 0
	return 1 + comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	if not lista:
		return 0
	return lista[0] + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
	if not lista:
		return False
	if elem == lista[0]:
		return True
	return existe(lista[1:],elem)

#Exercicio 1.4
def concat(l1, l2):
    if not l1:
        return l2
    if not l2:
        return l1
    l1.append(l2[0])
    concat(l1,l2[1:])
    return l1

#Exercicio 1.5
def inverte(lista):
	if not lista:
		return []
	return [lista[-1]] + inverte(lista[:-1]) 

#Exercicio 1.6
def capicua(lista):
    if not lista:
        return True
    if (lista[0] != lista[-1]):
        return False
    return capicua(lista[1:-1])

#Exercicio 1.7
def explode(lista):
    if not lista:
        return []
    return lista[0] + explode(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
    if not lista:
        return []
    val = novo if lista[0] == original else lista[0]
    return [val] + substitui(lista[1:],original,novo)

#Exercicio 1.9
def junta_ordenado(lista1, lista2):
    if not lista1:
        return lista2
    if not lista2:
        return lista1
    if lista1[0] < lista2[0]:
        return [lista1[0]] + junta_ordenado(lista1[1:],lista2)
    return [lista2[0]] + junta_ordenado(lista1,lista2[1:])

"""
#Exercício 1.10
def subconjuntos(list):
    if not list:
        return [[]]
    lst = subconjuntos(list[1:])
    new_lst = []
    for el in lst:
        new_lst.append([list[0]] + el)
    return new_lst + lst
"""

#Exercicio 2.1
def separar(lista):
    if not lista:
        return [],[]
    list1,list2 = separar(lista[1:])
    return ([lista[0][0]] + list1,[lista[0][1]] + list2)

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if not lista:
		return ([],0)
	lst, ocorrencias = remove_e_conta(lista[1:],elem)
	if (lista[0] == elem):
		return (lst,ocorrencias+1)
	return ([lista[0]] + lst, ocorrencias)

"""
#Exercício 2.3
def ocorrencias(lista):
    if not lista:
        return []
    lst = ocorrencias(lista[1:])
    controlo = True     
    for i in range(len(lst)):
        if (lst[i][0] == lista[0]):
            lst[i] = (lista[0],lst[i][1]+1)
            controlo = False
            break
    if controlo:
        return [(lista[0],1)] + lst
    return lst
"""

#Exercicio 3.1
def cabeca(lista):
    if not lista:
        return None
    return lista[0]

#Exercicio 3.2
def cauda(lista):
    if len(lista) < 2:
        return None
    lst = cauda(lista[:-1])
    if lst != None:
        return lst + [lista[-1]]
    else:
        return [lista[-1]]

#Exercicio 3.3
def juntar(l1, l2):
    if (len(l1) != len(l2)):
        return None
    if not l1:
        return []
    return [(l1[0],l2[0])] + juntar(l1[1:],l2[1:])

#Exercicio 3.4
def menor(lista):
    if not lista:
        return None
    result = menor(lista[1:])
    if result is None:
        return lista[0]
    return lista[0] if lista[0] < result else result

#Exercicio 3.6
def max_min(lista):
    if not lista:
        return None, None
    minval, lst = max_min(lista[1:])
    if lst is None:
        return lista[0],[]
    if lista[0] < minval:
        lst.insert(0,minval)
        minval = lista[0]
    else:
        lst.insert(0,lista[0])
    return (minval,lst)

"""
#Exercício 3.7
    if not lista:
        return None,None,[]
    firstMin,secondMin,lst = twoMinsOneList(lista[1:])
    if secondMin is None and firstMin is not None:
        if (lista[0] <= firstMin):
            secondMin = firstMin
            firstMin = lista[0]
        else:
            secondMin = lista[0]
    elif firstMin is None:
        firstMin = lista[0]
    else:
        if lista[0] > secondMin:
            lst.insert(0,lista[0])
        elif lista[0] > firstMin:
            lst.insert(0,secondMin)
            secondMin = lista[0]
        elif lista[0] <= firstMin:
            lst.insert(0,secondMin)
            secondMin = firstMin
            firstMin = lista[0]
    return (firstMin,secondMin,lst)
"""

"""
#Exercício 3.8
def mediaMediana(lista):
    if not lista:
        return None,None
    media,mediana = mediaMediana(lista[1:-1])
    if media is None:
        media = mediana = 0
    media = media * (len(lista)-2)
    if len(lista) == 2:
        media += lista[0] + lista[-1]
        mediana = (lista[0]+lista[1])/2
    elif len(lista) == 1:
        media += lista[0]
        mediana = lista[0]
    else:
        media += lista[0] + lista[-1]
    media /= len(lista)
    return (media,mediana)
"""