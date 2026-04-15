import operator
from functools import reduce

print('map')
lista = [[1, 2, 3], [4, 5, 6], [7, 8, 9] ]
lista2 = list(map(max, lista))
print(lista2)

print('reduce')
lista = [1, 2, 3]
lista2 = reduce(operator.add, lista)
print(lista2)