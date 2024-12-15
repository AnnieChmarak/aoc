Rules = dict()
Pages = list(list())


class NoSolution(Exception):
    pass


def parse(input: str, verbose: bool) -> tuple[Rules, Pages]:
    input_part = 1
    rules: Rules = {}
    pages: Pages = []

    lines = input.split('\n')
    for line in lines:
        if len(line) == 0:
            input_part = 2
            continue

        if input_part == 1:
            before, after = line.split('|')
            if after not in rules:
                rules[after] = set()
            rules[after].add(before)
        else:
            pages.append(line.split(','))

    return rules, pages


def check_order(page: list[str], rules: Rules, verbose: bool = False) -> bool:
    preceding_pages = set()
    for i in range(len(page)):
        correct_order = True
        rules_for_page = set()
        if page[i] in rules:
            rules_for_page = rules[page[i]] & set(page)
            correct_order = len(rules_for_page & preceding_pages) == len(rules_for_page)
        if verbose:
            print(f'{page} - {page[i]}: {rules_for_page} -> {correct_order}')
        if not correct_order:
            return False
        preceding_pages.add(page[i])
    return len(preceding_pages) == len(page)


def reorder(page: list[str], rules: Rules, verbose: bool = False) -> list[str]:
    reordered_page = list[str]()
    for i in range(len(page)):
        if page[i] in reordered_page:
            continue
        rules_for_page = set()
        if page[i] in rules:
            rules_for_page = rules[page[i]] & set(page)
            missing_rules = list(rules_for_page - set(reordered_page))
            missing_rules = reorder(missing_rules, rules)
            reordered_page += missing_rules
        reordered_page.append(page[i])
        if verbose:
            print(f'{page} - {page[i]}: {rules_for_page} -> {reordered_page}')
    return reordered_page


def solve_A(input: str, verbose: bool = False) -> int:
    middle_page_numbers = 0
    rules, pages = parse(input, verbose)
    for page in pages:
        assert len(page) == len(set(page))
        correct = check_order(page, rules, verbose)

        if correct:
            assert len(page) % 2 == 1
            middle_page_numbers += int(page[len(page) // 2])
        if verbose:
            print(f'+{int(page[len(page) // 2])}' if correct else '+0')
    return middle_page_numbers


def solve_B(input: str, verbose: bool = False) -> int:
    middle_page_numbers = 0
    rules, pages = parse(input, verbose)
    incorrect_pages = [page for page in pages if not check_order(page, rules)]
    if verbose:
        print(incorrect_pages)
    for page in incorrect_pages:
        corrected_page = reorder(page, rules,verbose)
        assert check_order(corrected_page, rules)
        assert len(corrected_page) % 2 == 1
        middle_page_numbers += int(corrected_page[len(corrected_page) // 2])
        if verbose:
            print(f'+{int(page[len(page) // 2])}')
    return middle_page_numbers
