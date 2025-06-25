from math import sqrt
from .constants import *


class City:
    """
    Klasa koja predstavlja grad sa koordinatama (x, y)
    """
    def __init__(self, i: int, x: float, y: float) -> None:
        self.i = i
        self.x = x
        self.y = y

    """
    Izračunava euklidsko rastojanje između ovog grada i drugog
    """
    def distance(self, other: 'City') -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self) -> str:
        return f"{self.i}"      # Prikazuje ID grada ispisu samog objekta

def load_cities(filename: str) -> list[City]:
    """
    Učitava gradove iz fajla. Svaka linija treba da sadrži: ID X Y
    """
    cities = []
    with open(filename, 'r') as f:
        for line in f:
            i, x, y = line.strip().split()
            cities.append(City(int(i), float(x), float(y)))
    return cities

def compute_distance_matrix(cities: list[City]) -> tuple[list[list[float]], dict[City, int]]:
    """
    Pravi matricu rastojanja između svih parova gradova.
    Takođe vraća i mapiranje objekata gradova na njihove indekse u listi.
    """
    size = len(cities)
    
    city_index = {}
    for idx, city in enumerate(cities):
        city_index[city] = idx

    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i != j:
                distance = cities[i].distance(cities[j])
            else:
                distance = 0.0
            row.append(distance)
        matrix.append(row)

    return matrix, city_index

def total_distance(path: list[City], dist_matrix: list[list[float]], city_index: dict[City, int]) -> float:
    """
    Računa ukupnu dužinu zadate putanje kroz gradove
    """
    total = 0.0

    for i in range(len(path) - 1):
        from_city = path[i]
        to_city = path[i + 1]

        from_index = city_index[from_city]
        to_index = city_index[to_city]

        distance = dist_matrix[from_index][to_index]
        total += distance

    return total
