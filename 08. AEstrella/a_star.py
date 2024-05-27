import copy
import os
import sys
import csv
from typing import Optional

dir_path = os.path.dirname(os.path.realpath(__file__))

class City:
    def __init__(self, name: str, value: int, parent: Optional['City'] = None) -> None:
        self.name = name
        self.value = value
        self.parent = parent

class Path:
    def __init__(self, city1: str, city2: str, value: int) -> None:
        self.city1 = city1
        self.city2 = city2
        self.value = value

def read_cities(path=f'{dir_path}/cities.csv') -> list[City]:
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        return [City(name=line['name'], value=int(line['value'])) for line in reader]

def read_paths(path=f'{dir_path}/paths.csv') -> list[Path]:
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        return [Path(city1=line['city1'], city2=line['city2'], value=int(line['value'])) for line in reader]

def a_star(f: list[City], cities: list[City], paths: list[Path]) -> Optional[City]:
    if not f:
        return None
    current = f.pop(0)
    if goal_test(node=current):
        return current
    successors = expand(node=current, cities=cities, paths=paths)
    f.extend(successors)
    f = evaluate(nodes=f, paths=paths)
    return a_star(f, cities=cities, paths=paths)

def expand(node: City, cities: list[City], paths: list[Path]) -> list[City]:
    successors = []
    for path in paths:
        if node.name == path.city1:
            city = find_city(city_name=path.city2, cities=cities)
        elif node.name == path.city2:
            city = find_city(city_name=path.city1, cities=cities)
        else:
            continue
        node_copy = copy.deepcopy(node)
        city.parent = node_copy
        successors.append(city)
    return successors

def find_city(city_name: str, cities: list[City]) -> City:
    for city in cities:
        if city.name == city_name:
            return copy.deepcopy(city)

def get_gx(node: City, paths: list[Path]) -> int:
    count = 0
    while node.parent:
        for path in paths:
            if node.name == path.city1 and node.parent.name == path.city2\
                    or node.name == path.city2 and node.parent.name == path.city1:
                count += path.value
                node = node.parent
                break
    return count

def evaluate(nodes: list[City], paths: list[Path]) -> list[City]:
    class Tuple:
        def __init__(self, node: City, fx: int) -> None:
            self.node = node
            self.fx = fx

    evaluated_nodes: list[Tuple] = []
    for node in nodes:
        hx = node.value
        gx = get_gx(node=node, paths=paths)
        fx = gx + hx
        evaluated_nodes.append(Tuple(node=node, fx=fx))
    evaluated_nodes.sort(key=lambda node: node.fx)
    return [node.node for node in evaluated_nodes]

def goal_test(node: City) -> bool:
    return node.value == 0

def print_path(node: City) -> None:
    path = f'{node.name}'
    while node.parent:
        node = node.parent
        path = f'{node.name} -> {path}'
    print(path)

def main() -> None:
    cities = read_cities()
    paths = read_paths()
    arad = find_city('Arad', cities)
    f = [arad]
    result = a_star(f, cities, paths)
    if result:
        print_path(result)
    else:
        print('No solution found')

if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()