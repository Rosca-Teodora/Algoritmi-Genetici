def calculeazaFitness(a, b, c, value):
    return a * value ** 2 + b * value + c

# return lista de fitness-uri
def getListaFitnessIndividual(a, b, c):
    f = [] # fitnesul individual -> f[xi] = f(xi)
    for i in range(0, n):
        # pe f[i] adaug fitnesul
        f.append(a * cromozomi[i] ** 2 + b * cromozomi[i] + c)
    return f

def findFitnessTotal(f):
    fTotal = sum(f)
    return fTotal

# calcul intervale de selectie:
# [p0, p1), [p1, p2), ...
# returneaza lista: pe prima pozitie e lista de prob pe a doua lista de cumularea probabilitatilor
def detProbAndCumulate(fitnessIndividual, fitnessTotal):
    p = [] # probabilitatile fiecarui cromozom
    q = [] # probabilitatile cumulate: pi = p1 + p2 + p3 + ... pi
    currentSum = 0

    for i in range(0, n + 1):
        if (i == n):
            p.append(1)
        else:
            p.append(round(currentSum / fitnessTotal, 5))
            currentSum = currentSum + fitnessIndividual[i]
        q.append(sum(p))

    return [p, q]

if __name__ == "__main__":
    file = open("Inputs/inputSelectie.in", "r")

    input = file.readline()
    input = input.strip().split()

    coef = [int(x) for x in input]
    # f(x) = a * x^2 + b * x + c
    a = coef[0] 
    b = coef[1]
    c = coef[2]
    print(f"{a} * x^2 + ({b} * x) + ({c})")

    n = int(file.readline().strip())
    # cromozomi = lista de x
    cromozomi = file.read().strip().split()
    cromozomi = [float(x) for x in cromozomi]

    f = getListaFitnessIndividual(a, b, c)
    rez = detProbAndCumulate(f, findFitnessTotal(f))
    p = rez[0]
    q = rez[1]

    for i in p:
        print(f"{i:.5f}")

    print(q)

    file.close()