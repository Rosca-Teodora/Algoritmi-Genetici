import random
import codificare
import selectie
import incrucisare
import mutatii
import everythingHelper
import individ as id

file = open("Inputs/inputMain.in", "r")

# dictionar in care se pastreaza tot pt a putea trimite datele catre functii helper
data = {}

# CITIRE & INITIALIZARE DATE
data["nrCromozomi"] = int(file.readline().strip()) # dimensiunea populatiei
data["domeniu"] = [int(x) for x in file.readline().strip().split()] # capetele intervalului inchis
data["coef"] = [float(x) for x in file.readline().strip().split()] # parametrii functiei/ coef polinomului de grad 2
data["prec"] = int(file.readline().strip()) # precizia cu care se discretizeaza intervalul
data["probIncrucisare"] = int(file.readline().strip()) / 100 # probabilitatea de crossover/ incrucisare
data["probMutatie"] = int(file.readline().strip()) / 100 # prob de mutatie 
data["nrEtape"] = int(file.readline().strip()) # nr de etape ale alg
data["nrBiti"] = codificare.findNrBiti(data["domeniu"][0], data["domeniu"][1], data["prec"]) # aflare l dupa formula facuta la lab pastrata in helper function
data["listaIndivizi"] = [] # lista initial nula populata la initializarea populatiei

file.close() # inchide file read
file = open("output.out", "w") # deschide file write

# INITIALIZAREA PUPULATIEI
# genereaza cromozomii initiali prin nr aleatoare in intervalul si cu precizia ceruta

file.write("Populatie Initiala:\n")

everythingHelper.initializareCromozomi(data)
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    file.write(f"{i + 1}: {''.join(individ.bits)}")
    file.write(f" x = {individ.value}")
    file.write(f" f = {individ.fitness}")
    file.write("\n")

# SELECTIE
# start prin a updata data a.i. sa apara fitnesul si intervalele de selectie
a = data["coef"][0]
b = data["coef"][1]
c = data["coef"][2]
data["listaFitness"] = selectie.getListaFitnessIndividualServiciu(a, b, c, data["listaIndivizi"], data["nrCromozomi"])
data["fitnessTotal"] = selectie.findFitnessTotal(data["listaFitness"])
data["intervaleSiCumulare"] = selectie.detProbAndCumulate(data["listaFitness"], data["fitnessTotal"], data["nrCromozomi"])

file.write("\nProbabilitati de Selectie:\n")
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    p = float(selectie.calculeazaFitness(a, b, c, individ.value) / data["fitnessTotal"])
    file.write(f"cromozom {i + 1} probabilitate: {p}\n")

file.write(f"\nIntervale Probabilitati Selectie:\n {data["intervaleSiCumulare"][0]}\n\n")

cromSelectati = []

# selectez doar 19 indivizi din cei pastrati pentru a putea pastra elita
for i in range(0, data["nrCromozomi"] - 1): 
    u = everythingHelper.makeRandomNumber()
    cromSelectat = everythingHelper.binarySearch(data, u) # cromSelectat = INDICELE cromozomului selectat 
    file.write(f"u = {u} -> selectam cromozomul {cromSelectat}\n")
    cromSelectati.append(data["listaIndivizi"][cromSelectat - 1]) # cromSelectat - 1 deoarece sunt indexati de la zero in lista de indivizi, nu de la 1

# calcul elita ce va trece direct in generatia urmatoare
posElita = everythingHelper.findPosEliteCromozome(data)

print(len(cromSelectati))

# INCRUCISAREA cromozomilor tocmai selectati

cromDeIncrucisat = []

file.write(f"\nProbabilitatea de incrucisare: {data['probIncrucisare']}\n")
for i in range(0, len(cromDeIncrucisat)):
    individ = cromSelectati[i]
    u = everythingHelper.makeRandomNumber()
    file.write(f"{i}: {''.join(individ.bits)} u = {u}")
    if u < data["probIncrucisare"]: 
        cromDeIncrucisat.append([individ, i]) # pastrez bitii individului si pozitia lui initiala
        file.write(f" < {data['probIncrucisare']} participa")
    file.write(f"\n")

# debug print 
#everythingHelper.printCromozomi(data, file)

i = 0
while i <  len(cromDeIncrucisat) - 1:
    pctRupere = int(random.uniform(1, data["nrBiti"] - 1))

    crom1 = cromDeIncrucisat[i][0]
    crom2 = cromDeIncrucisat[i + 1][0]
    pozitie1 = cromDeIncrucisat[i][1]
    pozitie2 = cromDeIncrucisat[i + 1][1]
    
    file.write(f'Recombinarea dintre cromozomul {pozitie1 + 2} si {pozitie2 + 1}\n')
    file.write(f'{''.join(crom1.bits)} {''.join(crom2.bits)} punct {pctRupere}\n')

    rez = incrucisare.incruciseaza(crom1, crom2, pctRupere)
    crom1.bits = rez[0]
    crom2.bits = rez[1]
    file.write(f'Rezultat: {''.join(crom1.bits)} {''.join(crom2.bits)}\n')

    # tb salvate schimbarile in cromSelectati
    cromSelectati[pozitie1] = crom1
    cromSelectati[pozitie2] = crom2

    i = i + 2

file.write('\nDupa Recombinare:\n')
everythingHelper.printCromozomi(cromSelectati, file)


# MUTATII 
# pastrez intr-un dictionar ca sa nu printez indexul de mai multe ori: 
# perechi de tipul: (cheie = index initial : cromozom.bits)
dictCromCuMutatii = {}

file.write(f'\nProbabilitatea de mutatie pentru fiecare gena: {data['probMutatie']}\n')
file.write('Au fost modificati cromozomii:\n')
for i in range(0, len(cromSelectati)):
    cromozom = cromSelectati[i].bits

    for i in range(0, data['nrBiti']): 
        u = everythingHelper.makeRandomNumber()
        if u <= data["probMutatie"]:
            if i not in dictCromCuMutatii: 
                file.write(f'{i + 1}\n')

            cromozom[i] = mutatii.mutate(cromozom[i])
            dictCromCuMutatii[i] = cromozom

# salvarea mutatiilor in lista de selectie             
    
             
# adaugare elita direct in generatia urmatoare (fara a trece prin selectie, incrucisare sau mutatie)
cromSelectati.append(data["listaIndivizi"][posElita - 1])