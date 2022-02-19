import math

#Exercicio 4.1
impar = lambda a : a % 2 == 1

#Exercicio 4.2
positivo = lambda a : a >= 0

#Exercicio 4.3
comparar_modulo = lambda x,y : abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x,y : (math.sqrt(x**2+y**2), math.atan2(y,x))

#Exercicio 4.5
ex5 = lambda f,g,h: lambda x,y,z: h(f(x,y),g(y,z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if not lista:
        return True
    if not f(lista[0]):
        return False
    else:
        return quantificador_universal(lista[1:],f)

#Exercicio 4.9
def ordem(lista, f):
    if not lista:
        return None
    result = ordem(lista[1:],f)
    return lista[0] if result is None or f(lista[0], result) else result

#Exercicio 4.10
def filtrar_ordem(lista, f):
    if not lista:
        return None, []
    min,lst = filtrar_ordem(lista[1:],f)
    return (lista[0], lista[1:]) if min is None or f(lista[0],min) else (min,[lista[0]] + lst)

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if len(lista) <= 1:
        return [] if len(lista) == 0 else [ lista[0] ]
    idx = 0
    for i in range(1, len(lista)):
        if ordem(lista[i], lista[idx]):
            idx = i
    return [ lista[idx] ] + ordenar_seleccao(lista[:idx] + lista[idx+1:], ordem)
