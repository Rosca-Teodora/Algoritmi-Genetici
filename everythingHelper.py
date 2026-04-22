import random
import individ as ind
import codificare
import mutatii
import selectie
import incrucisare

def makeIndividRandom(data):
    value = random.uniform(data['domeniu'][0], data['domeniu'][1])
    bits = codificare.codifica(value, data['domeniu'][0], codificare.findPasDiscretizare(capatStanga = data['domeniu'][0], capatDreapta = data['domeniu'][1], nrBiti=data['nrBiti']), data['nrBiti'])
    fitness = selectie.calculeazaFitness(data["coef"][0], data["coef"][1], data["coef"][2], value)
    individ = ind.Individ(bits, value, fitness)
    return individ

def initializareCromozomi(data):
    for i in range (0, data["nrCromozomi"]):
        data["listaIndivizi"].append(makeIndividRandom(data))

# random number in interval [0,1] / probabilitate; helper selectie
def makeRandomNumber():
    return round(random.uniform(0, 1), 5)

# cautarea binara pentru pozitia cromozromului in intervalele de selectie
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

# functie initiala de test
def findInterval(data, u):
    intervale = data["intervaleSiCumulare"][0]

    for i in range(0, data["nrCromozomi"]):
        if intervale[i] <= u < intervale[i + 1]:
            return i + 1

    # pt cazurile ft apropiate de 1 se ia ultimul crom.
    return data["nrCromozomi"]

# debug print
def printCromozomi(cromozomi, file):
    for i in range(0, len(cromozomi)):
        individ = cromozomi[i]
        file.write(f"{i + 1}: {''.join(individ.bits)}")
        file.write(f" x = {individ.value}")
        file.write(f" f = {individ.fitness}")
        file.write("\n")

# helpere selectare elita
def findFitnessMaxim(data):
    fMax = 0
    for individ in data["listaIndivizi"]:
        if individ.fitness > fMax:
            fMax = individ.fitness
    return fMax

def findPosEliteCromozome(data):
    fMax = findFitnessMaxim(data)
    for i in range(0, data['nrCromozomi']):
        if data['listaIndivizi'][i].fitness == fMax:
            return i 
    return -1


# fct helper pt CROSSOVER si MUTATIE
def aplicaOperatiiGenetice(cromSelectati, data):
    # avand cromozomii deja selectati si datele predefinite se face crossover-ul si mutatia 
    # INCRUCISAREA
    cromDeIncrucisat = []
    
    for i in range(0, len(cromSelectati)):
        individ = cromSelectati[i]
        u = makeRandomNumber()
        if u < data["probIncrucisare"]:
            cromDeIncrucisat.append([individ, i])
    
    i = 0
    while i < len(cromDeIncrucisat) - 1:
        pctRupere = int(random.uniform(1, data["nrBiti"] - 1))
        
        crom1 = cromDeIncrucisat[i][0]
        crom2 = cromDeIncrucisat[i + 1][0]
        pozitie1 = cromDeIncrucisat[i][1]
        pozitie2 = cromDeIncrucisat[i + 1][1]
        
        rez = incrucisare.incruciseaza(crom1, crom2, pctRupere)
        crom1.bits = rez[0]
        crom2.bits = rez[1]
        
        crom1.update(data)
        crom2.update(data)
        
        cromSelectati[pozitie1] = crom1
        cromSelectati[pozitie2] = crom2
        
        i = i + 2
    
    # MUTATII
    for i in range(0, len(cromSelectati)):
        for j in range(0, data['nrBiti']):
            u = makeRandomNumber()
            if u <= data["probMutatie"]:
                cromSelectati[i].bits[j] = mutatii.mutate(cromSelectati[i].bits[j])
    
    # recalc fitness dupa mutatii
    for i in range(0, len(cromSelectati)):
        cromSelectati[i].update(data)
    
    return cromSelectati
