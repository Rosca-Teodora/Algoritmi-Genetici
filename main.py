import random
import codificare
import selectie
import incrucisare
import mutatii
import initHelper
import individ as id

file = open("inputMain.in", "r")

# dictionar in care se pastreaza tot pt a putea trimite datele catre functii helper
data = {}

# citire data
data["nrCromozomi"] = int(file.readline().strip()) # dimensiunea populatiei
data["domeniu"] = [int(x) for x in file.readline().strip().split()] # capetele intervalului inchis
data["coef"] = [float(x) for x in file.readline().strip().split()] # parametrii functiei/ coef polinomului de grad 2
data["prec"] = int(file.readline().strip()) # precizia cu care se discretizeaza intervalul
data["probRecombinare"] = int(file.readline().strip()) # probabilitatea de crossover/ incrucisare
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

initHelper.initializareCromozomi(data)
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    file.write(f"{i + 1}: {individ.bits}")
    file.write(f" x = {individ.value}")
    file.write(f" f = {individ.fitness}")
    file.write("\n")

file.write("Probabilitati de Selectie:\n")
