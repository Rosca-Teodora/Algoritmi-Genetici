# Algoritmi Avansati - Proiect

Implementare in Python a unui algoritm genetic pentru maximizarea unei functii polinomiale de gradul 2 pe un interval dat.

## Rulare (Tutorial Rapid)

### Rulare locala

1. Deschide terminalul in folderul proiectului.
2. Ruleaza:

```bash
python main.py
```

3. Verifica fisierul de iesire generat:

```text
evolutie.out
```

### Rulare cu Docker (optional)

Construieste imaginea:

```bash
docker build -t algavansati-proiect .
```

Ruleaza containerul:

```bash
docker run --rm algavansati-proiect
```

Optional, cu bind mount (pentru a vedea fisierele direct in workspace):

```powershell
docker run --rm -v ${PWD}:/app algavansati-proiect
```

## Ce face proiectul

Algoritmul cauta un maxim pentru functia:

```text
f(x) = a*x^2 + b*x + c
```

pe domeniul inchis [stanga, dreapta], folosind:

- codificare binara a indivizilor
- selectie proportionala cu fitness-ul (roulette wheel)
- determinarea intervalului de selectie cu cautare binara
- incrucisare cu un singur punct de rupere
- mutatie pe fiecare gena cu probabilitate p
- selectie elitista (cel mai bun individ trece nemodificat in generatia urmatoare)

## Date de intrare

Fisierul principal de intrare este:

```text
Inputs/inputMain.in
```

Ordinea valorilor citite de program:

1. numar cromozomi (dimensiunea populatiei)
2. domeniu: doua valori intregi (capete interval)
3. coeficienti polinom: a b c
4. precizie
5. probabilitate incrucisare (in procente, ex: 25)
6. probabilitate mutatie (in procente, ex: 1)
7. numar etape (generatii)

Exemplu de format:

```text
20
-1 2
-1 1 2
6
25
1
50
```

## Date de iesire

Programul scrie rezultatele in:

```text
evolutie.out
```

Continutul include:

- Populatia initiala (bits, x, fitness)
- Probabilitati de selectie si intervale cumulative
- Detalii selectie pentru prima generatie (valorile u si cromozomul selectat)
- Detalii incrucisare pentru prima generatie
- Detalii mutatii pentru prima generatie
- Populatia dupa mutatie (cu elita adaugata la final)
- Evolutia maximului pe toate generatiile

Nota: implementarea calculeaza si media fitness-ului intern, dar in varianta curenta din `main.py` se afiseaza explicit doar maximul in fisierul final.

## Fluxul algoritmului

1. Se initializeaza populatia random in domeniu.
2. Se calculeaza fitness-ul fiecarui individ.
3. Se construiesc probabilitatile cumulative de selectie.
4. Se selecteaza `n-1` indivizi prin roulette wheel + cautare binara.
5. Se extrage elita (best fitness) din populatia curenta.
6. Se aplica incrucisare pe indivizii selectati.
7. Se aplica mutatii pe biti.
8. Se recalculeaza `x` si fitness dupa modificari.
9. Elita este adaugata la final, nemodificata.
10. Se repeta pentru numarul de etape cerut.

## Structura fisierelor

- `main.py`
	- punct de intrare
	- orchestrare selectie, incrucisare, mutatie, elitism
	- generare raport in `evolutie.out`

- `individ.py`
	- clasa `Individ(bits, value, fitness)`
	- metoda `update(data)` pentru recalculare valoare decodificata si fitness

- `codificare.py`
	- calcul numar biti
	- pas de discretizare
	- codificare `x -> bits`
	- decodificare `bits -> x`

- `selectie.py`
	- functia de fitness
	- lista fitness-uri
	- fitness total
	- probabilitati + cumulare pentru selectie

- `incrucisare.py`
	- crossover cu un punct de rupere

- `mutatii.py`
	- mutatie bit cu bit (`0 <-> 1`)

- `everythingHelper.py`
	- initializare populatie
	- numere random pentru selectie
	- cautare binara in intervalele cumulative
	- functii pentru elita
	- `aplicaOperatiiGenetice(...)` pentru reutilizarea crossover + mutatie

- `Inputs/`
	- fisiere pentru scenarii/teste locale pe module individuale:
		- `inputMain.in`
		- `inputCodificare.in`
		- `inputSelectie.in`
		- `inputIncrucisare.in`
		- `inputMutatii.in`

## Cerinte

- Python 3.14+ (sau versiune apropiata)
- Docker (optional)

## Observatii importante

- Algoritmul este nedeterminist (foloseste random), deci rulări diferite produc rezultate diferite.
- Daca vrei rezultate reproductibile, poti fixa seed-ul la inceputul `main.py`.
- Elitismul este implementat corect: elita este adaugata dupa crossover si mutatie, astfel nu este alterata.

## Idei de extensie

- Afisarea in fisier a perechii `maxim, medie` pentru fiecare generatie.
- Adaugarea unui seed configurabil din fisierul de input.
- Interfata grafica pentru plot-ul evolutiei fitness-ului.
