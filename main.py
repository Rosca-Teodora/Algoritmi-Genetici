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

# citire data
data["nrCromozomi"] = int(file.readline().strip()) # dimensiunea populatiei
data["domeniu"] = [int(x) for x in file.readline().strip().split()] # capetele intervalului inchis
data["coef"] = [float(x) for x in file.readline().strip().split()] # parametrii functiei/ coef polinomului de grad 2
data["prec"] = int(file.readline().strip()) # precizia cu care se discretizeaza intervalul
data["probIncrucisare"] = int(file.readline().strip()) # probabilitatea de crossover/ incrucisare
data["probMutatie"] = int(file.readline().strip()) # prob de mutatie 
data["nrEtape"] = int(file.readline().strip()) # nr de etape ale alg

print(data["domeniu"])

file.close()

# aflare l dupa formula facuta la lab pastrata in helper function
data["nrBiti"] = codificare.findNrBiti(data["domeniu"][0], data["domeniu"][1], data["prec"])
data["listaIndivizi"] = []

file = open("output.out", "w")

# genereaza cromozomii initiali prin nr aleatoare in intervalul si cu precizia ceruta

file.write("Populatie Initiala:\n")

everythingHelper.initializareCromozomi(data)
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    file.write(f"{i + 1}: {individ.bits}")
    file.write(f" x = {individ.value}")
    file.write(f" f = {individ.fitness}")
    file.write("\n")

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

for i in range(0, data["nrCromozomi"]):
    u = everythingHelper.makeRandomNumber()
    cromSelectat = everythingHelper.binarySearch(data, u)
    file.write(f"u = {u} -> selectam cromozomul {cromSelectat}\n")

cromDeIncrucisat = []
sizeIncrucisare = 0

file.write(f"\nProbabilitatea de incrucisare: {data['probIncrucisare']}")
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    u = everythingHelper.makeRandomNumber()
    if u < data["probIncrucisare"]: 
        cromDeIncrucisat.append(individ)
        file.write(f" < {data['probIncrucisare']} participa")

everythingHelper.printCromozomi(data, file)

random.shuffle(cromDeIncrucisat)
for i in range(0, sizeIncrucisare - 1):
    pctRupere = int(random.uniform(1, data["nrBiti"]))
    incrucisare.incruciseaza(cromDeIncrucisat[i], cromDeIncrucisat[i + 1], pctRupere)

everythingHelper.printCromozomi(data, file)