class Node:
    def __init__(self, id_number: int, cost: int):
        self.id = id_number
        self.cost = cost
        self.children: list[int] = []


def main():
    nodes_count: int = int(input())
    nodes = {}

    for i in range(nodes_count):
        cost = int(input())
        nodes[i] = Node(i, cost)

    edges_count: int = int(input())
    for i in range(edges_count):
        inp = input().split()
        first = int(inp[0])
        second = int(inp[1])

        parent: Node = nodes[first]
        parent.children.append(second)

    start_index = int(input())
    end_index = int(input())
    max_nodes = 3
    current_paths: list[int] = [([start_index], start_index)]
    passed_nodes = set()
    passed_nodes.add(start_index)

    while True:
        expanded_nodes = []
        for (path, node) in current_paths:
          for child in nodes[node].children:
            if child == end_index:
                  print(path + [child])
                  break

            expanded_nodes.append((path + [child], child))

        if not expanded_nodes:
            break

    sorted_expanded_nodes = sorted(expanded_nodes, key=lambda entry: nodes[entry[1]].cost)
    current_paths = sorted_expanded_nodes[:max_nodes]


if __name__ == '__main__':
  main()


  