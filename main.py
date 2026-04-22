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
file = open("evolutie.out", "w") # deschide file write

# INITIALIZAREA PUPULATIEI
# genereaza cromozomii initiali prin nr aleatoare in intervalul si cu precizia ceruta

file.write("Populatia initiala\n")

everythingHelper.initializareCromozomi(data)
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    file.write(f"  {i + 1:2}: {''.join(individ.bits)} x={individ.value:8.6f} f={individ.fitness}\n")

# SELECTIE
# start prin a updata data a.i. sa apara fitnesul si intervalele de selectie
a = data["coef"][0]
b = data["coef"][1]
c = data["coef"][2]
data["listaFitness"] = selectie.getListaFitnessIndividualServiciu(a, b, c, data["listaIndivizi"], data["nrCromozomi"])
data["fitnessTotal"] = selectie.findFitnessTotal(data["listaFitness"])
data["intervaleSiCumulare"] = selectie.detProbAndCumulate(data["listaFitness"], data["fitnessTotal"], data["nrCromozomi"])

file.write("\nProbabilitati selectie \n")
for i in range(0, data["nrCromozomi"]):
    individ = data["listaIndivizi"][i]
    p = float(selectie.calculeazaFitness(a, b, c, individ.value) / data["fitnessTotal"])
    file.write(f"cromozom {i + 1:3} probabilitate {p}\n")

file.write(f"Intervale probabilitati selectie \n")
for val in data["intervaleSiCumulare"][0]:
    file.write(f"{val} ")
file.write("\n")

cromSelectati = []

# selectez doar 19 indivizi din cei pastrati pentru a putea pastra elita
for i in range(0, data["nrCromozomi"] - 1): 
    u = everythingHelper.makeRandomNumber()
    cromSelectat = everythingHelper.binarySearch(data, u) # cromSelectat = INDICELE cromozomului selectat 
    file.write(f"u={u}  selectam cromozomul {cromSelectat} \n")
    cromSelectati.append(data["listaIndivizi"][cromSelectat - 1]) # cromSelectat - 1 deoarece sunt indexati de la zero in lista de indivizi, nu de la 1

# calcul elita ce va trece direct in generatia urmatoare
posElita = everythingHelper.findPosEliteCromozome(data)
elita = data["listaIndivizi"][posElita - 1]

file.write(f"\nDupa selectie:\n")
for i in range(0, len(cromSelectati)):
    individ = cromSelectati[i]
    file.write(f"  {i + 1:2}: {''.join(individ.bits)} x={individ.value:8.6f} f={individ.fitness}\n")

# INCRUCISAREA si MUTATII pt prima generatie
cromDeIncrucisat = []

file.write(f"\nProbabilitatea de incrucisare {data['probIncrucisare']}\n")
for i in range(0, len(cromSelectati)):
    individ = cromSelectati[i]
    u = everythingHelper.makeRandomNumber()
    file.write(f"{i + 1}: {''.join(individ.bits)} u={u}")
    if u < data["probIncrucisare"]: 
        cromDeIncrucisat.append([individ, i])
        file.write(f"<{data['probIncrucisare']} participa")
    file.write(f" \n")

# detalii incrucisare pt prima generatie
i = 0
while i <  len(cromDeIncrucisat) - 1:
    pctRupere = int(random.uniform(1, data["nrBiti"] - 1))
    crom1 = cromDeIncrucisat[i][0]
    crom2 = cromDeIncrucisat[i + 1][0]
    pozitie1 = cromDeIncrucisat[i][1]
    pozitie2 = cromDeIncrucisat[i + 1][1]
    
    file.write(f'Recombinare dintre cromozomul {pozitie1 + 1} cu cromozomul {pozitie2 + 1}:\n')
    file.write(f'{''.join(crom1.bits)} {''.join(crom2.bits)} punct  {pctRupere}\n')
    
    rez = incrucisare.incruciseaza(crom1, crom2, pctRupere)
    crom1.bits = rez[0]
    crom2.bits = rez[1]
    
    # update value si fitness dupa incrucisare
    crom1.update(data)
    crom2.update(data)
    
    file.write(f'Rezultat    {''.join(crom1.bits)} {''.join(crom2.bits)}\n')
    cromSelectati[pozitie1] = crom1
    cromSelectati[pozitie2] = crom2
    i = i + 2

file.write('Dupa recombinare:\n')
for i in range(0, len(cromSelectati)):
    individ = cromSelectati[i]
    file.write(f"  {i + 1:2}: {''.join(individ.bits)} x={individ.value:8.6f} f={individ.fitness}\n")

# MUTATII detalii pt prima generatie
dictCromCuMutatii = {}
file.write(f'\nProbabilitate de mutatie pentru fiecare gena {data['probMutatie']}\n')
file.write('Au fost modificati cromozomii:\n')
for i in range(0, len(cromSelectati)):
    for j in range(0, data['nrBiti']): 
        u = everythingHelper.makeRandomNumber()
        if u <= data["probMutatie"]:
            if i not in dictCromCuMutatii: 
                file.write(f'{i + 1}\n')
                dictCromCuMutatii[i] = cromSelectati[i]
            cromSelectati[i].bits[j] = mutatii.mutate(cromSelectati[i].bits[j])

# update fitness dupa mutatii
for cheie in dictCromCuMutatii:
    cromSelectati[cheie].update(data)

file.write('Dupa mutatie:\n')

# add elita la sfarsit ca sa nu fie parte din restul operatiilor (trece direct la generatia viitoare)
cromSelectati.append(elita)
for i in range(0, len(cromSelectati)):
    individ = cromSelectati[i]
    file.write(f"  {i + 1:2}: {''.join(individ.bits)} x={individ.value:8.6f} f={individ.fitness}\n")

# partea finala de fitness maxim si mediu

file.write('\nEvolutia maximului \n')
# pt prima generatie calc fitness maxim si mediu
max_fitness = max([individ.fitness for individ in cromSelectati])
avg_fitness = sum([individ.fitness for individ in cromSelectati]) / len(cromSelectati)
file.write(f"{max_fitness}\n")

# RESTUL GENERATIILOR
for etapa in range(1, data["nrEtape"]):
    # update date selectie
    data["listaIndivizi"] = cromSelectati
    
    a = data["coef"][0]
    b = data["coef"][1]
    c = data["coef"][2]
    data["listaFitness"] = selectie.getListaFitnessIndividualServiciu(a, b, c, data["listaIndivizi"], data["nrCromozomi"])
    data["fitnessTotal"] = selectie.findFitnessTotal(data["listaFitness"])
    data["intervaleSiCumulare"] = selectie.detProbAndCumulate(data["listaFitness"], data["fitnessTotal"], data["nrCromozomi"])

    posElita = everythingHelper.findPosEliteCromozome(data)
    
    cromSelectati = []
    
    # selectie
    for i in range(0, data["nrCromozomi"] - 1):
        u = everythingHelper.makeRandomNumber()
        cromSelectat = everythingHelper.binarySearch(data, u)
        cromSelectati.append(data["listaIndivizi"][cromSelectat - 1])
    
    # Salveaza elita pentru a o adauga doar la sfarsit
    elita = data["listaIndivizi"][posElita - 1]
    
    # Aplica operatiile genetice (incrucisare si mutatie)
    cromSelectati = everythingHelper.aplicaOperatiiGenetice(cromSelectati, data)
    
    # Adaugare elita la sfarsit (dupa toate operatiile genetice)
    cromSelectati.append(elita)
    
    # Afisare fitness maxim si mediu
    max_fitness = max([individ.fitness for individ in cromSelectati])
    avg_fitness = sum([individ.fitness for individ in cromSelectati]) / len(cromSelectati)
    file.write(f"{max_fitness}\n")

file.close()