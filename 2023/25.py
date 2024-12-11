import networkx as nx

class NoSolution(Exception):
    pass

def parse(input: str, verbose: bool) -> dict:
    components = {}
    for line in input.split('\n'):
        source, targets = line.split(': ')
        components[source] = targets.split(' ')
    return components

def solve_A(input: str, verbose: bool = False) -> int:
    components = parse(input, verbose)
    
    connections = {}
    for source, targets in components.items():
        if source not in connections:
            connections[source] = set()
        for t in targets:
            if t not in connections:
                connections[t] = set()
            connections[source].add(t)
            connections[t].add(source)

    nx_graph = nx.DiGraph()
    for component in connections:
        for next_component in connections[component]:
            nx_graph.add_edge(component, next_component, capacity=1.0)
            nx_graph.add_edge(next_component, component, capacity=1.0)

    for x in [list(connections.keys())[0]]:
        for y in connections:
            if x == y:
                continue
            joins, (set_a, set_b) = nx.minimum_cut(nx_graph, x, y)
            if joins == 3:
                return len(set_a) * len(set_b)

    raise NoSolution

def solve_B(input: str, verbose: bool = False) -> int:
    raise NoSolution