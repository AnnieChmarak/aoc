class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = {}
        self.towel = ''


class SingleLinkedList:
    def __init__(self):
        self.root = Node()

    def insert(self, towel):
        current_node = self.root
        for char in towel:
            if char not in current_node.children:
                current_node.children[char] = Node(char)
            current_node = current_node.children[char]
        current_node.towel = towel


def parse(input: str, verbose: bool) -> tuple[SingleLinkedList, list[str]]:
    towels_desc, patterns_desc = input.split('\n\n')
    towels = SingleLinkedList()
    for t in towels_desc.split(', '):
        towels.insert(t)
    patterns = patterns_desc.split('\n')
    return towels, patterns


def solve_A(input: str, verbose: bool = False) -> int:
    towels, patterns = parse(input, verbose)

    possible_patterns = 0
    for pattern in patterns:
        if verbose:
            print(pattern)

        is_possible_pattern = False
        nodes = [towels.root]
        for char in pattern:
            is_possible_pattern = False
            next_nodes = []
            for prev_node in nodes:
                if char in prev_node.children:
                    node = prev_node.children[char]
                    next_nodes.append(node)
                    if len(node.towel) > 0:
                        is_possible_pattern = True
                        if verbose:
                            print('found a towel: ' + node.towel)
                        if towels.root not in next_nodes:
                            next_nodes.append(towels.root)
            nodes = next_nodes

        if verbose:
            print(f'{pattern} is possible: {is_possible_pattern}')
            print()
        if is_possible_pattern:
            possible_patterns += 1
    return possible_patterns


def solve_B(input: str, verbose: bool = False) -> int:
    towels, patterns = parse(input, verbose)

    all_possible_patterns = 0
    for pattern in patterns:
        if verbose:
            print(pattern)

        branches = [([towels.root], 1)]
        possible_patterns = 0
        for char in pattern:
            possible_patterns = 0
            next_branches = []
            for nodes, branch_count in branches:
                next_nodes = []
                for prev_node in nodes:
                    if char in prev_node.children:
                        node = prev_node.children[char]
                        next_nodes.append(node)
                        if node.towel != '':
                            possible_patterns += branch_count
                            if verbose:
                                print('found a towel: ' + node.towel)

                            has_root = False
                            for i, (b, r) in enumerate(next_branches):
                                if b == [towels.root]:
                                    next_branches[i] = (b, r + branch_count)
                                    has_root = True
                                    break
                            if not has_root:
                                next_branches.append(([towels.root], branch_count))

                next_branches.append((next_nodes, branch_count))
            branches = next_branches

        all_possible_patterns += possible_patterns
        if verbose:
            print(f'{pattern} is possible {possible_patterns} times')
            print()
    return all_possible_patterns