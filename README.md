## 🧬 Genetski algoritam - Problem putujućeg trgovca (TSP)

> Projektni zadatak iz predmeta **Nelinearno programiranje i evolutivni algoritmi**  
> Univerzitet u Novom Sadu – Fakultet tehničkih nauka

**Autori:**

- Stevanović Aleksandar, SV04/2023
- Kačarević Milan, SV73/2023

---

### 📌 Opis problema

Problem putujućeg trgovca (TSP – _Travelling Salesman Problem_) predstavlja poznat optimizacioni problem: kako pronaći najkraću moguću zatvorenu rutu koja povezuje sve zadate gradove, tako da se svaki posjeti tačno jednom, a polazna i krajnja tačka budu isti grad.

Pošto broj mogućih ruta rapidno raste sa brojem gradova (n!), koristi se **genetski algoritam** – evolutivna heuristika koja u razumnom vremenu pronalazi približno optimalna rešenja.

---

### ⚙️ Tehnologije

- **Python 3.12.6**

---

### 🧠 Kratak uvod u genetski algoritam

Genetski algoritam koristi principe prirodne selekcije:

- **Jedinka:** jedna ruta (putanja) kroz sve gradove
- **Populacija:** skup različitih jedinki
- **Selekcija:** biranje najboljih jedinki za reprodukciju
- **Ukrštanje:** kombinovanje roditelja radi generisanja potomaka
- **Mutacija:** nasumične promjene rute radi diverziteta
- **Fitnes:** kriterijum kvaliteta – kraća ruta = bolji fitnes

---

### 🧠 Struktura projekta i metode

Ovaj projekat se sastoji od sljedećih klasa i metoda:

- `City` – predstavlja jedan grad sa koordinatama `(x, y)` i ID-em

  - `distance(other)` – računa euklidsko rastojanje između dva grada

- `load_cities(filename)` – učitava gradove iz `.txt` fajla (format: ID X Y)
- `compute_distance_matrix(cities)` – kreira matricu rastojanja između svih gradova + mapira gradove na indekse
- `total_distance(path, dist_matrix, city_index)` – računa ukupnu dužinu zadate rute
- `initial_population(cities, population_size)` – generiše početnu populaciju zatvorenih ruta permutacijom gradova
- `compute_fitnesses(population, dist_matrix, city_index)` – izračunava ukupne distance i normalizovane fitnes vrijednosti
- `tournament_selection(population, normalized_fitnesses, k)` – bira roditelje metodom turnirske selekcije
- `ordered_crossover(parent1, parent2)` – ukrštanje: kombinuje segmente roditelja uz očuvanje redoslijeda
- `mutate(path, mutation_rate)` – mutira rutu reverzijom ili permutacijom segmenta sa zadatom vjerovatnoćom
- `next_generation(parents, parent_dists, children, child_dists, elitism_size)` – stvara novu generaciju zadržavanjem roditelja i najboljih potomaka
- `genetic_algorithm(cities)` – glavna metoda genetskog algoritma:

  - generiše populaciju
  - iterativno vrši selekciju, ukrštanje, mutaciju, elitizam
  - prati napredak i zaustavlja se ako nema poboljšanja

- `run(filename)` – učitava gradove, pokreće algoritam i prikazuje najkraću rutu grafički (`matplotlib`)

---

### 🧪 Parametri algoritma

| Parametar                   | Vrijednost | Opis                                  |
| --------------------------- | ---------- | ------------------------------------- |
| `POPULATION_SIZE`           | 700        | Broj jedinki u populaciji             |
| `TOTAL_GENERATIONS`         | 600        | Maksimalan broj generacija            |
| `MUTATION_RATE`             | 0.04       | Vjerovatnoća mutacije                 |
| `ELITISM_SIZE`              | 4          | Broj najboljih jedinki koje se čuvaju |
| `MAX_STAGNATION`            | 200        | Maks. generacija bez poboljšanja      |
| `TOURNAMENT_SELECTION_SIZE` | 5          | Broj učesnika u turnirskoj selekciji  |

---

### 📈 Rezultati i zaključak

Najbolja pronađena distanca: `7544.37`
![Najbolje rješenje](img/best_solution.png) <br>
Vizuelni prikaz najkraće rute pronađene tokom izvršavanja algoritma.

Ostale zabilježene distance:

- 7782.98
- 8242.37
- 8285.81
- 7821.74
- 7661.01
- 8201.59
- 8034.17
- 8471.40

Ovo potvrđuje da algoritam pronalazi dobra približna rješenja sa vrlo malom varijacijom.

---

### 🖼️ Vizualizacija

Na kraju izvršavanja algoritma, najbolja ruta se prikazuje grafički, kako je prikazano na slici. Gradovi su označeni brojevima, a linije povezuju gradove redosledom obilaska.

---

### 📂 Kako pokrenuti

1. Instaliraj Python 3.x
2. Instaliraj potrebne biblioteke:
   ```bash
   pip install matplotlib
   ```
