import networkx as nx

cities = ['a', 'b', 'c', 'd']
distances = {
    ('a', 'b'): 10, ('a', 'c'): 15, ('a', 'd'): 20,
    ('b', 'c'): 35, ('b', 'd'): 25,
    ('c', 'd'): 30
}

G = nx.Graph()
for (start, end), distance in distances.items():
    G.add_edge(start, end, weight=distance)

def get_distance(_start, _end):
    try:
        return G[_start][_end]['weight']
    except KeyError:
        return 0

# for start in cities:
#     for end in cities[cities.index(start) + 1:]:
#         if start != end:
#             print(f'{start} -> {end} = {get_distance(start, end)}')

for path in [
    [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')],
    [('a', 'c'), ('c', 'd'), ('d', 'b'), ('b', 'a')],
]:
    path_len = 0
    for start, end in path:
        dist = get_distance(start, end)
        path_len += dist
        print(f'{start} -> {end} = {dist}')
    print(f'Path length: {path_len}')
