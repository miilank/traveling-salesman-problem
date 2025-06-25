import random
from .City import *
from typing import NoReturn


def initial_population(cities: list[City], population_size: int) -> list[list[City]]:
    """
    Generiše početnu populaciju slučajnih putanja
    Svaka putanja se završava ponavljanjem početnog grada (zatvorena ruta)
    """
    population = []
    for _ in range(population_size):
        # nasumična permutacija bez ponavljanja
        route = random.sample(cities, len(cities))
        # dodaje se početni grad kao završni u ruti
        route.append(route[0])
        population.append(route)
    return population

def compute_fitnesses(population: list[list[City]], dist_matrix: list[list[float]], city_index: dict[City, int]) -> tuple[list[float], list[float]]:
    """
    Računa ukupne distance za sve jedinke i pretvara ih u normalizovane fitnese
    """
    distances = [total_distance(p, dist_matrix, city_index) for p in population]
    # što je veći fitnes manja je distanca
    fitnesses = [1 / d for d in distances]
    # bez dijeljenja u odnosu na druge ne bismo znali koliko je jedna jedinka dobra u odnosu na ostale
    total_fit = sum(fitnesses)
    # normalizovani fitnes jeste šansa da jedinka preživi ili da se reprodukuje
    normalized = [f / total_fit for f in fitnesses]
    return distances, normalized

def tournament_selection(population: list[list[City]], normalized_fitnesses: list[float], k: int = TOURNAMENT_SELECTION_SIZE) -> list[City]:
    """
    Biranje jednog roditelja tako što se nasumično izabere k jedinki
    i od njih se uzme ona sa najvećim normalizovanim fitnesom.
    """
    # Uparujemo svaku jedinku iz populacije sa njenim normrailzovanim fitnesom
    individuals_with_fitness = list(zip(population, normalized_fitnesses))

    # Nasumično biramo k kandidata
    tournament_candidates = random.sample(individuals_with_fitness, k)

    # Pravimo promjenljivu za trenutno najboljeg kandidata (prvi izabrani)
    best_candidate = tournament_candidates[0]

    # Poređenjem nalazimo onog sa najvećim fitnesom (najbolje rješenje)
    for candidate in tournament_candidates[1:]:
        if candidate[1] > best_candidate[1]:
            best_candidate = candidate

    # Vraćamo samo jedinku (putanju), ne i njen normalizovani fitnes
    return best_candidate[0]

def ordered_crossover(parent1: list[City], parent2: list[City]) -> list[City]:
    """
    Crossover (ukrštanje) po metodi "ordered crossover" (OX)
    """
    # uklanjamo posljednji grad da ne bude duplikata
    parent1 = parent1[:-1]
    parent2 = parent2[:-1]
    
    # Broj gradova u roditelju (bez posljednjeg)
    n = len(parent1)

    # Izaberi dva nasumična indeksa između 0 i n-1
    index1 = random.randint(0, n - 1)
    index2 = random.randint(0, n - 1)

    # Osiguraj da su različiti (ponavljaj dok nisu)
    while index1 == index2:
        index2 = random.randint(0, n - 1)

    # Pronađi manji i veći indeks
    start = min(index1, index2)
    end = max(index1, index2)

    child = parent1[start:end]
    for city in parent2:
        if city not in child:
            child.append(city)
    
    # vraćam prvi grad na kraj
    child.append(child[0])
    return child

def mutate(path: list[City], mutation_rate: float) -> list[City]:
    """
    Mutacija putanje: reverzija ili permutacija segmenta
    """
    path = path[:-1]
    # mutacija se dešava samo ponekad, što je i poželjno, nasumičan broj od 0 do 1 se bira
    if random.random() < mutation_rate:
        # Ukupan broj elemenata u putanji
        n = len(path)

        # Izaberi dva različita nasumična indeksa
        index1 = random.randint(0, n - 1)
        index2 = random.randint(0, n - 1)

        # Ponavljaj dok ne budu različiti
        while index1 == index2:
            index2 = random.randint(0, n - 1)

        # Pronađi manji i veći indeks
        i = min(index1, index2)
        j = max(index1, index2)

        if random.random() < 0.5:
            path[i:j] = reversed(path[i:j])
        else:
            segment = path[i:j]
            random.shuffle(segment)
            path[i:j] = segment
    path.append(path[0])
    return path


def next_generation(parents: list[list[City]], parent_dists: list[float], children: list[list[City]], child_dists: list[float], elite_size: int) -> list[list[City]]:
    """
    Formira novu generaciju tako što zadržava najbolje roditelje (elitizam),
    a ostatak popunjava najboljim potomstvom.
    Ukupan broj jedinki ostaje konstantan.
    """

    parents_with_dists = list(zip(parent_dists, parents))
    parents_with_dists.sort(key=lambda x: x[0])
    elites = [individual for _, individual in parents_with_dists[:elite_size]]
    children_with_dists = list(zip(child_dists, children))
    children_with_dists.sort(key=lambda x: x[0])
    top_children = [individual for _, individual in children_with_dists[:INITIAL_POPULATION_SIZE - elite_size]]
    next_gen = elites + top_children

    return next_gen


def genetic_algorithm(cities: list[City]) -> tuple[list[City], float]:
    """
    Glavna petlja genetskog algoritma
    """
    dist_matrix, city_index = compute_distance_matrix(cities)
    population = initial_population(cities, INITIAL_POPULATION_SIZE)
    # Računamo distance za sve rute
    distances = []
    for p in population:
        d = total_distance(p, dist_matrix, city_index)
        distances.append(d)

    # pronalazimo indeks najmanje distance
    min_index = distances.index(min(distances))

    # uzimamo najbolju rutu po toj distanci
    best = population[min_index]

    best_distance = total_distance(best, dist_matrix, city_index)
    no_improvement = 0
    mutation_rate = MUTATION_RATE

    for gen in range(MAX_GENERATIONS):
        parent_dists, normalized_fitnesses = compute_fitnesses(population, dist_matrix, city_index)
        best_dist = min(parent_dists)

        print(f"Generacija {gen+1}: Najbolja = {best_dist:.2f}")

        children = []
        while len(children) < INITIAL_POPULATION_SIZE - ELITISM_SIZE:
            p1 = tournament_selection(population, normalized_fitnesses)
            p2 = tournament_selection(population, normalized_fitnesses)

            # Dijete 1
            child1 = ordered_crossover(p1, p2)
            child1 = mutate(child1, mutation_rate)
            children.append(child1)

            # Dijete 2
            if len(children) < INITIAL_POPULATION_SIZE - ELITISM_SIZE:
                child2 = ordered_crossover(p2, p1)
                child2 = mutate(child2, mutation_rate)
                children.append(child2)


        child_dists, _ = compute_fitnesses(children, dist_matrix, city_index)
        population = next_generation(population, parent_dists, children, child_dists, ELITISM_SIZE)

        # Računamo distance za sve rute
        distances = []
        for p in population:
            d = total_distance(p, dist_matrix, city_index)
            distances.append(d)

        # pronalazimo indeks najmanje distance
        min_index = distances.index(min(distances))

        # uzimamo najbolju rutu po toj distanci
        current_best = population[min_index]

        current_best_dist = total_distance(current_best, dist_matrix, city_index)

        if current_best_dist < best_distance:
            best = current_best
            best_distance = current_best_dist
            no_improvement = 0
        else:
            no_improvement += 1

        if no_improvement >= MAX_STAGNATION:
            print(f"Rano zaustavljanje u generaciji {gen+1}")
            break

    return best, best_distance

def run(filename: str) -> NoReturn:
    """
    Učitava gradove i pokreće algoritam
    """
    cities = load_cities(filename)
    best, best_distance = genetic_algorithm(cities)
    print("Najbolja putanja:", [city.i for city in best])
    print("Najkraća distanca:", best_distance)
