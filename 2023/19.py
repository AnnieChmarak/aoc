from typing import Optional

class NoSolution(Exception):
    pass

Detail = dict[str: int]
WorkflowRule = tuple[str, str, int]
Workflows = dict[str: list[tuple[Optional[WorkflowRule], str]]]

def parse(input: str, verbose: bool = False) -> tuple[Workflows, list[Detail]]:
    workflows_desc, details_desc = input.split('\n\n')
    
    workflows: Workflows = {}
    for workflow in workflows_desc.split():
        name, rules = workflow.split('{')
        rules = rules.split(',')
        else_target = rules[-1].strip('}')
        rules = rules[:-1]

        workflows[name] = []
        for rule in rules:
            condition, target = rule.split(':')
            for comp in '<>':
                if comp in condition:
                    part, value = condition.split(comp)
                    workflows[name].append(((part, comp, int(value)), target))
        workflows[name].append((None, else_target))
    
    details = []
    for detail in details_desc.split():
        details.append({})
        detail = detail.strip('{}')
        for part_desc in detail.split(','):
            part, value = part_desc.split('=')
            details[-1][part] = int(value)
    
    return workflows, details

def _invert_rule(rule: WorkflowRule) -> WorkflowRule:
    inverted_comp = {
        '<': '>=',
        '>': '<=',
        '<=': '>',
        '>=': '<',
    }[rule[1]]
    return (rule[0], inverted_comp, rule[2])

def _target_rules(target: str, workflows: Workflows, known_targets: dict[str: list[set[WorkflowRule]]] = {}) -> list[set[WorkflowRule]]:
    if target == 'A':
        known_targets.clear()
    elif target in known_targets:
        return known_targets[target]

    target_rules = []
    for wf_name in workflows:
        wf_target_rules = set()
        for r, t in workflows[wf_name]:
            if t == target:
                wf_target_rules_alt = wf_target_rules.copy()
                if r: 
                    wf_target_rules.add(r)
                    wf_target_rules_alt.add(_invert_rule(r))
                if wf_name != 'in':
                    nested_target_rules = _target_rules(wf_name, workflows, known_targets)
                    assert wf_name != 'A'
                    assert wf_name != 'R'
                    assert len(nested_target_rules) == 1
                    wf_target_rules.update(nested_target_rules[0])

                target_rules.append(wf_target_rules)
                wf_target_rules = wf_target_rules_alt
            else:
                if r:
                    wf_target_rules.add(_invert_rule(r))
    
    known_targets[target] = target_rules
    return target_rules

def _passes(detail: Detail, rule: WorkflowRule) -> bool:
    part, comp, req_value = rule
    detail_value = detail[part]
    return {
        '<': detail_value < req_value,
        '>': detail_value > req_value,
        '<=': detail_value <= req_value,
        '>=': detail_value >= req_value,
    }[comp]

def _simplify_rules(rules: set[WorkflowRule]) -> dict[str: tuple[Optional[int], Optional[int]]]:
    simplified_rules = {}
    for current_part in 'xmas':
        min_value = None
        max_value = None
        for part, comp, req_value in rules:
            if part == current_part:
                if comp == '<':
                    max_value = min(max_value, req_value - 1) if max_value else req_value - 1
                elif comp == '<=':
                    max_value = min(max_value, req_value) if max_value else req_value
                elif comp == '>':
                    min_value = max(min_value, req_value + 1) if min_value else req_value + 1
                elif comp == '>=':
                    min_value = max(min_value, req_value) if min_value else req_value
        simplified_rules[current_part] = (min_value, max_value)
    return simplified_rules

def _rating(detail: Detail) -> int:
    return sum(detail.values())

def solve_A(input: str, verbose: bool = False) -> int:
    workflows, details = parse(input, verbose)

    accepted_rating = 0
    A_rules = _target_rules('A', workflows)
    for detail in details:
        for rule_set in A_rules:
            if all(_passes(detail, r) for r in rule_set):
                accepted_rating += _rating(detail)
                break

    return accepted_rating

def solve_B(input: str, verbose: bool = False) -> int:
    workflows, _ = parse(input, verbose)

    possible_range = (1, 4000)
    accepted_comnibations = 0
    A_rules = _target_rules('A', workflows)
    for rule_set in A_rules:
        simplified_rules = _simplify_rules(rule_set)
        rule_accepted_comnibations = 1
        for part in 'xmas':
            min_value, max_value = simplified_rules[part]
            if not min_value:
                min_value = possible_range[0]
            if not max_value:
                max_value = possible_range[1]
            rule_accepted_comnibations *= max_value - min_value + 1
        accepted_comnibations += rule_accepted_comnibations

    return accepted_comnibations