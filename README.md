# Algoritmi Avansati - Proiect

Proiect Python pentru etape clasice din algoritm genetic: codificare, selectie, incrucisare, mutatii si initializare populatie.

## Cerinte

- Python 3.14+ (sau o versiune apropiata)
- Docker (optional, pentru rulare containerizata)

## Rulare Locala

Din folderul proiectului:

```bash
python main.py
```

Datele de intrare sunt citite din fisierele `input*.in`, iar rezultatul principal este scris in `output.out`.

## Rulare Cu Docker

Construieste imaginea:

```bash
docker build -t algavansati-proiect .
```

Ruleaza containerul:

```bash
docker run --rm algavansati-proiect
```

Optional, pentru a folosi fisierele locale direct (bind mount):

```powershell
docker run --rm -v ${PWD}:/app algavansati-proiect
```

## Structura Principala

- `main.py`: punct de intrare al proiectului
- `codificare.py`: codificare/decodificare + discretizare
- `selectie.py`: calcul fitness si probabilitati de selectie
- `incrucisare.py`: crossover
- `mutatii.py`: mutatii pe cromozomi
- `initHelper.py`: generare si initializare indivizi
- `individ.py`: clasa individ
