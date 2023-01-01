import operator
import re
from typing import Callable, TypeAlias

Operator: TypeAlias = Callable[[int, int], int]

OPS: dict[str, Operator] = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}
REVERSED_OPS = {value: key for key, value in OPS.items()}
HUMN = "humn"
ROOT = "root"


def read_input_file(file_name: str = "input.txt") -> dict[str, str]:
    with open(file_name, "r") as f:
        parsed_input = {}
        for line in f.readlines():
            if stripped_line := line.strip():
                lhs, rhs = stripped_line.split(": ")
                parsed_input[lhs] = rhs
        return parsed_input


def parse_monkey_line(line: str) -> str | tuple[Operator, str, str]:
    if line.isdigit():
        return line
    else:
        match = re.match(r"^([a-zA-Z]{4}) ([\+\-\*\/]) ([a-zA-Z]{4})$", line)
        assert match is not None and len(match.groups()) == 3
        return OPS[str(match.groups()[1])], str(match.groups()[0]), str(match.groups()[2])


def resolve_monkeys(monkeys: dict[str, str], monkey_to_resolve: str = ROOT) -> tuple[int, list[str]]:
    assert monkey_to_resolve in monkeys
    equation, frontier, explored = monkey_to_resolve, [monkey_to_resolve], []
    while frontier:
        node = frontier.pop()
        if node in monkeys:
            equation = equation.replace(node, f"({monkeys[node]})")
            parsed = parse_monkey_line(monkeys[node])
            if isinstance(parsed, tuple):
                _, monkey_1, monkey_2 = parsed
                frontier += [monkey_1, monkey_2]
                explored += [monkey_1, monkey_2]
    return int(eval(equation)), explored


def get_mappings(monkeys: dict[str, str]) -> tuple[dict[str, tuple[str, str]], dict[str, str]]:
    parent_to_children_mapping: dict[str, tuple[str, str]] = {}
    child_to_parent_mapping: dict[str, str] = {}
    for key, val in monkeys.items():
        parsed = parse_monkey_line(val)
        if isinstance(parsed, tuple):
            parent_to_children_mapping[key] = (parsed[1], parsed[2])
            child_to_parent_mapping[parsed[1]] = key
            child_to_parent_mapping[parsed[2]] = key
    return parent_to_children_mapping, child_to_parent_mapping


def compress_monkey_tree(monkeys: dict[str, str]) -> dict[str, str]:
    # compress the tree by identifying any nodes where all nodes below it can be resolved,
    # then remove them from the tree and set the node's value to the value of that resolution.
    # this is critical to the implementation of part 2 which involves walking up the tree.
    mutated_monkeys = {**monkeys}
    frontier = [ROOT]
    while frontier:
        node = frontier.pop()
        if node in mutated_monkeys and not monkeys[node].isdigit():
            try:
                value, explored_nodes = resolve_monkeys(mutated_monkeys, monkey_to_resolve=node)
                # this node and all nodes below it can be collapsed into a single digit
                mutated_monkeys[node] = str(value)
                for explored_node in explored_nodes:
                    mutated_monkeys.pop(explored_node)
            except NameError:
                # this node cannot be collapsed. attempt to collapse its children individually.
                parsed = parse_monkey_line(mutated_monkeys[node])
                assert isinstance(parsed, tuple)
                frontier += [parsed[1], parsed[2]]
    return mutated_monkeys


def rearrange_for_first_operand(op: Operator, lhs: str, second_operand: str) -> tuple[Operator, str, str]:
    return {
        operator.add: (operator.sub, lhs, second_operand),
        operator.sub: (operator.add, lhs, second_operand),
        operator.mul: (operator.floordiv, lhs, second_operand),
        operator.floordiv: (operator.mul, lhs, second_operand),
    }[op]


def rearrange_for_second_operand(op: Operator, lhs: str, first_operand: str) -> tuple[Operator, str, str]:
    return {
        operator.add: (operator.sub, lhs, first_operand),
        operator.sub: (operator.sub, first_operand, lhs),
        operator.mul: (operator.floordiv, lhs, first_operand),
        operator.floordiv: (operator.floordiv, first_operand, lhs),
    }[op]


def determine_what_number_to_yell(monkeys: dict[str, str]) -> int:
    mutated_monkeys = compress_monkey_tree({k: v for k, v in monkeys.items() if k != HUMN})
    parent_to_children_mapping, child_to_parent_mapping = get_mappings(mutated_monkeys)

    def invert_line(monkey: str) -> tuple[str, set[str]]:
        parsed = parse_monkey_line(mutated_monkeys[child_to_parent_mapping[monkey]])
        assert isinstance(parsed, tuple)
        op, monkey_1, monkey_2 = parsed
        inverted_op, inverted_monkey_1, inverted_monkey_2 = (
            rearrange_for_first_operand(op, lhs=child_to_parent_mapping[monkey], second_operand=monkey_2)
            if monkey_1 == monkey
            else rearrange_for_second_operand(op, lhs=child_to_parent_mapping[monkey], first_operand=monkey_1)
        )
        variables = {inverted_monkey_1, inverted_monkey_2}
        return f"({inverted_monkey_1} {REVERSED_OPS[inverted_op]} {inverted_monkey_2})", variables

    # identify the nodes in the tree which are equal according to the `root` monkey's rules in part 2
    root_children = parent_to_children_mapping[ROOT]
    assert mutated_monkeys[root_children[0]].isdigit() or mutated_monkeys[root_children[1]].isdigit()
    left, right = (
        (root_children[1], root_children[0])
        if mutated_monkeys[root_children[0]].isdigit()
        else (root_children[0], root_children[1])
    )

    # starting from `humn`, walk up the tree and progressively compose an equation with LHS of `humn`
    composed_equation, frontier = invert_line(HUMN)
    while frontier:
        variable_to_walk = frontier.pop()
        if variable_to_walk == left:
            composed_equation = composed_equation.replace(variable_to_walk, mutated_monkeys[right])
        elif mutated_monkeys[variable_to_walk].isdigit():
            composed_equation = composed_equation.replace(variable_to_walk, mutated_monkeys[variable_to_walk])
        else:
            equation_section, new_variables = invert_line(variable_to_walk)
            composed_equation = composed_equation.replace(variable_to_walk, equation_section)
            frontier |= new_variables

    # substitute in known monkey numbers. the completion of this step should result in a valid equation.
    for key, value in mutated_monkeys.items():
        if value.isdigit():
            composed_equation = composed_equation.replace(key, value)

    return round(eval(composed_equation))


if __name__ == "__main__":
    m = read_input_file("input.txt")
    number_that_root_yells, _ = resolve_monkeys(m, monkey_to_resolve=ROOT)
    print(f"The monkey named `{ROOT}` will yell the number {number_that_root_yells}.")
    print(
        f"You must yell the number {determine_what_number_to_yell(m)} to satisfy the `{ROOT}` monkey's equality check."
    )
