import math

# calcul l cu formula data (numarul de biti)
def findNrBiti(capatStanga, capatDreapta, precizie):    
    l = math.log((capatDreapta - capatStanga) * pow(10, precizie), 2) # log2((b - a) * 10 ^ p)
    l = math.ceil(l)
    return l

def findPasDiscretizare(capatStanga, capatDreapta, nrBiti):
    d = (capatDreapta - capatStanga) / pow(2, nrBiti) # (b - a) / 2 ^ l
    return d

def codifica(x, capatStanga, pasDiscretizare, nrBiti):
    intDiscretizare = 0

    while (x >= capatStanga + (intDiscretizare + 1) * pasDiscretizare): 
        intDiscretizare = intDiscretizare + 1
    
    xBinar = []
    while intDiscretizare: 
        xBinar.append((str)(intDiscretizare % 2))
        intDiscretizare = intDiscretizare // 2
    xBinar = xBinar[::-1] # reverse xBinar

    #tb adus la lungimea l calculata mai sus
    while (len(xBinar) < nrBiti):
        xBinar.insert(0, "0")
    return xBinar

def decodifica(cromozom, capatStanga, pasDiscretizare):
    if isinstance(cromozom, list):
        cromozom = ''.join(cromozom)

    intDiscretizare = 0
    pow2 = 0
    reverseB = cromozom[::-1]

    for bit in reverseB:
        if bit == '1':
            intDiscretizare = intDiscretizare + 2 ** pow2
        pow2 = pow2 + 1
    return capatStanga + intDiscretizare * pasDiscretizare


if __name__ == "__main__": # verificare necesara pt a nu executa codul cand dau import    
    f = open("Inputs/inputCodificare.in", "r")

    # citire input file 
    domeniu = f.readline()
    domeniu = domeniu.strip().split()
    a = (int)(domeniu[0]) # capatul din stanga
    b = (int)(domeniu[1]) # capatul din dreapta
    p = (int)(f.readline()) # precizia 
    m = (int)(f.readline()) # numarul de teste
    
    l = findNrBiti(a, b, p)
    d = findPasDiscretizare(a, b, l)

    for i in range(1, 2*m):
        line = f.readline().strip()
        #print(f"test: {line}")
        if line == "TO":
            x = (float)(f.readline())
            xBinar = codifica(x, a, d, l)
            print(xBinar)
        if (line == "FROM"):
            b = f.readline().strip()
            print(decodifica(b, a, d))

    f.close()
