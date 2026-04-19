# inainte de incrucisare
# c1 = x0 x1 x2 ... xi-1 xi xi+1 ... xl-1
# c2 = y0 y1 y2 ... yi-1 yi yi+1 ... yl-1

# dupa: 
# c1 = x0 x1 x2 ... xi-1 yi yi+1 ... yl-1
# c2 = y0 y1 y2 ... yi-1 xi xi+1 ... xl-1

# returneaza o lista cu 2 cromozomi (lista de char, NU string)
def incruciseaza(cromozom1, cromozom2, pctRupere):
    c1Incrucisat = []
    c2Incrucisat = []
    for i in range (0, pctRupere):
        c1Incrucisat.append(cromozom1[i])
        c2Incrucisat.append(cromozom2[i])

    for i in range (pctRupere, l):
        c1Incrucisat.append(cromozom2[i])
        c2Incrucisat.append(cromozom1[i])

    return [c1Incrucisat, c2Incrucisat]

if __name__ == "__main__":
    file = open("Inputs/inputIncrucisare.in", "r")

    l = int(file.readline().strip()) # nr de biti
    c1 = file.readline().strip() # cromozomul 1
    c2 = file.readline().strip() # cromozomul 2
    pctRupere = int(file.readline().strip()) # punctul i de la care se va face incrucisarea

    file.close()

    rez = incruciseaza(c1, c2, pctRupere)

    c1Incrucisat = rez[0]
    c2Incrucisat = rez[1]

    print(f"Dupa incrucisare:\nc1= {c1Incrucisat},\nc2= {c2Incrucisat}")