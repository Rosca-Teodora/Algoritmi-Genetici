import random
import individ as ind
import codificare
import selectie

def makeIndividRandom(data):
    value = random.uniform(data['domeniu'][0], data['domeniu'][1])
    bits = codificare.codifica(value, data['domeniu'][0], codificare.findPasDiscretizare(capatStanga = data['domeniu'][0], capatDreapta = data['domeniu'][1], nrBiti=data['nrBiti']), data['nrBiti'])
    fitness = selectie.calculeazaFitness(data["coef"][0], data["coef"][1], data["coef"][2], value)
    individ = ind.Individ(bits, value, fitness)
    return individ

def initializareCromozomi(data):
    for i in range (0, data["nrCromozomi"]):
        data["listaIndivizi"].append(makeIndividRandom(data))

# random number in interval; hlper selectie
def makeRandomNumber():
    return round(random.uniform(0, 1), 5)

def binarySearch(data, u):
    intervale = data["intervaleSiCumulare"][0]
    left = 0
    right = data["nrCromozomi"]

    # cel mai mare i pt care intervale[i] <= u
    # indexul cromozomului este i + 1.
    while left < right:
        mid = (left + right + 1) // 2
        if intervale[mid] <= u:
            left = mid
        else:
            right = mid - 1

    return min(left + 1, data["nrCromozomi"])

def findInterval(data, u):
    intervale = data["intervaleSiCumulare"][0]

    for i in range(0, data["nrCromozomi"]):
        if intervale[i] <= u < intervale[i + 1]:
            return i + 1

    # pt cazurile ft apropiate de 1 se ia ultimul crom.
    return data["nrCromozomi"]