import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, 'data/day6.txt')


def select_parent_node(graph):
    for node in graph:
        if not any(node in graph[n] for n in graph.keys()):
            return node


def dfs(graph, parent_code, deep=0):
    orbits_count = deep
    for n in graph[parent_code]:
        orbits_count += dfs(graph, n, deep + 1)
    return orbits_count


def read_input_graph():
    graph = {}
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            orbited, orbit = line.strip().split(')')
            if orbited not in graph:
                graph[orbited] = set()
            if orbit not in graph:
                graph[orbit] = set()
            graph[orbited].add(orbit)
    return graph


def path(graph, from_node, to_node, current_path):
    current_path.append(from_node)
    if not graph[from_node]:
        return None
    elif to_node in graph[from_node]:
        return current_path
    else:
        for n in graph[from_node]:
            p = path(graph, n, to_node, current_path.copy())
            if p:
                return p


def calculate_min_distance(graph):
    parent_node = select_parent_node(graph)
    path_to_you = path(graph, parent_node, 'YOU', [])
    path_to_santa = path(graph, parent_node, 'SAN', [])

    for i, (node1, node2) in enumerate(zip(path_to_you, path_to_santa)):
        if node1 != node2:
            return len(path_to_you[i:] + path_to_santa[i:])


def run_program():
    graph = read_input_graph()
    parent_node = select_parent_node(graph)

    print(dfs(graph, parent_node))  # task1
    print(calculate_min_distance(graph))
    return 1


if __name__ == '__main__':
    run_program()

