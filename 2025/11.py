class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> dict[str, list[str]]:
    devices = {}
    for line in input.split('\n'):
        in_device = line.split(': ')[0]
        out_devices = line.split(': ')[1].split(' ')
        devices[in_device] = out_devices

    if verbose:
        print('PARSED:')
        print(devices)
    return devices


def count_paths(devices: dict[str, list[str]], start_device: str, end_device: str) -> int:
    known_path_counts = {start_device: 1}
    current_nodes = [start_device]
    while current_nodes:
        next_nodes = []
        for in_node in current_nodes:
            out_nodes = devices[in_node] if in_node in devices else []
            for out_node in out_nodes:
                if out_node not in known_path_counts:
                    known_path_counts[out_node] = 0
                known_path_counts[out_node] += known_path_counts[in_node]
                if out_node not in next_nodes:
                    next_nodes.append(out_node)
        current_nodes = next_nodes

    return known_path_counts[end_device]


def count_special_paths(devices: dict[str, list[str]], start_device: str, middle_devices: list[str], end_device: str) -> int:
    start_node = (start_device, tuple([False]*len(middle_devices)))
    known_path_counts = {start_node: 1}
    current_nodes = [start_node]
    while current_nodes:
        next_nodes = []
        for in_node in current_nodes:
            in_device, passed_middle_devices = in_node
            if in_device in middle_devices:
                passed_middle_devices = list(passed_middle_devices)
                passed_middle_devices[middle_devices.index(in_device)] = True
                passed_middle_devices = tuple(passed_middle_devices)
            out_devices = devices[in_device] if in_device in devices else []
            for out_device in out_devices:
                out_node = (out_device, passed_middle_devices)
                if out_node not in known_path_counts:
                    known_path_counts[out_node] = 0
                known_path_counts[out_node] += known_path_counts[in_node]
                if out_node not in next_nodes:
                    next_nodes.append(out_node)
        current_nodes = next_nodes

    return known_path_counts[(end_device, tuple([True]*len(middle_devices)))]


def solve_A(input: str, verbose: bool = False) -> int:
    devices = parse(input, verbose)
    paths_count = count_paths(devices, 'you', 'out')
    return paths_count


def solve_B(input: str, verbose: bool = False) -> int:
    devices = parse(input, verbose)
    paths_count = count_special_paths(devices, 'svr', ['fft', 'dac'], 'out')
    return paths_count