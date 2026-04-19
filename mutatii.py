# helper returneaza "opusul" unui singur cromozom
def mutate(chr):
    if chr == '1':
        return '0'
    return '1'

# cromozom = lista de char
def getMutatedCrom(cromozom, pozMutatii):
    # pastrez intr-un dictionar ca sa verific rapid pozitiile mutatiilor
    dictPozitii = {}

    for i in pozMutatii:
        if int(i) not in dictPozitii:
            dictPozitii[int(i)] = 1
        else:
            dictPozitii[int(i)] = dictPozitii[int(i)] + 1

    for i in range (0, l):
        if i in dictPozitii:
            if (dictPozitii[i] % 2 == 1):
                cromozom[i] = mutate(c[i])

    return cromozom

if __name__ == "__main__":
    file = open("Inputs/inputMutatii.in", "r")

    input = file.readline().strip().split()
    l = int(input[0]) # nr de biti ai unui cromozom
    k = int(input[1]) # nr de mutatii ce urmeaza sa fie aplicate cromozomului 
    c = file.readline().strip() # cromozomul
    pozMutatii = file.readline().strip().split() # pozitiile mutatiilor pastrate intr-un array

    file.close()

    #print(l, k, c)
    c = list(c) # pastrat in forma de lista pentru ca e mai usor si eficient (String imutable)
    print(getMutatedCrom(pozMutatii=pozMutatii, cromozom=c))