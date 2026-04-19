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