import codificare
import selectie

class Individ:
    def __init__(self, bits, value, fitness):
        self.bits = bits
        self.value = value
        self.fitness = fitness

    # dupa procesurile de selectie, incrucisare si mutatie trebuie modificati bitii si recalculat fitness-ul
    def update(self, data):
        d = codificare.findPasDiscretizare(data['domeniu'][0], data['domeniu'][1], data['nrBiti'])
        self.value = codificare.decodifica(self.bits, data['domeniu'][0], d)
        self.fitness = selectie.calculeazaFitness(data['coef'][0], data['coef'][1], data['coef'][2], self.value)