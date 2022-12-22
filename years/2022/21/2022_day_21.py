"""
TODO: I hacked this one together by reducing the data down to minimal equations and plugging it into an equation solver.
Revise this and solve it properly.
"""

import operator
import re
from typing import Callable, TypeAlias

Monkeys: TypeAlias = dict[str, int]  # monkey name -> the number the monkey yells out
MonkeyDependencies: TypeAlias = dict[str, tuple[str, str]]
DependentMonkeys: TypeAlias = dict[str, Callable[[int, int], int]]

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    # "/": operator.truediv,
    "/": operator.floordiv,
}


def read_input_file(file_name: str = "input.txt") -> tuple[Monkeys, MonkeyDependencies, DependentMonkeys]:
    monkeys: Monkeys = {}
    monkey_dependencies: MonkeyDependencies = {}
    dependent_monkeys: DependentMonkeys = {}
    with open(file_name, "r") as f:
        for line in f.readlines():
            if stripped_line := line.strip():
                lhs, rhs = stripped_line.split(": ")
                if rhs.isdigit():
                    monkeys[lhs] = int(rhs)
                else:
                    op_string = [x for x in ["+", "-", "*", "/"] if x in rhs].pop()
                    monkey_1, monkey_2 = rhs.split(f" {op_string} ")
                    dependent_monkeys[lhs] = OPS[op_string]
                    monkey_dependencies[lhs] = (monkey_1, monkey_2)
        return monkeys, monkey_dependencies, dependent_monkeys


def resolve_monkeys(
    monkeys: Monkeys, monkey_dependencies: MonkeyDependencies, dependent_monkeys: DependentMonkeys
) -> int:
    mutated_monkeys = {**monkeys}
    resolved_monkeys = set(monkeys.keys())
    while monkey_dependencies:
        for monkey, monkeys_depended_on in monkey_dependencies.items():
            if set(monkeys_depended_on).issubset(resolved_monkeys):
                result = dependent_monkeys[monkey](
                    mutated_monkeys[monkeys_depended_on[0]], mutated_monkeys[monkeys_depended_on[1]]
                )
                mutated_monkeys[monkey] = result
                resolved_monkeys.add(monkey)
                monkey_dependencies.pop(monkey)
                break
    return int(mutated_monkeys["root"])


def determine_what_number_to_yell(
    monkeys: Monkeys, monkey_dependencies: MonkeyDependencies, dependent_monkeys: DependentMonkeys
) -> int:
    mutated_monkeys = {**monkeys}
    mutated_monkeys.pop("humn")
    print("")
    return 0


def quick_test(file_name: str = "input.txt"):
    with open(file_name, "r") as f:
        lhs_and_rhs: dict[str, str] = {}
        for line in f.readlines():
            if stripped_line := line.strip():
                lhs, rhs = stripped_line.split(": ")
                lhs_and_rhs[lhs] = int(rhs) if rhs.isdigit() else rhs  # .replace("/", "//")
        print(lhs_and_rhs)
        # equation_with_humn = [(key, value) for key, value in lhs_and_rhs.items() if "humn" in value].pop()
        # TODO
        # lhs_and_rhs.pop(equation_with_humn[0])
        equation_with_humn = "ptdq + dvpt"

        # while len(lhs_and_rhs.keys()) > 1:
        #     for key, value in lhs_and_rhs.items():
        #         if key != "root":  # deal with this later
        #             if key in equation_with_humn:
        #                 equation_with_humn = equation_with_humn.replace(key, value)
        #     print("")
        while len(lhs_and_rhs.keys()) > 1:
            for key, value in lhs_and_rhs.items():
                if key not in ["root", "humn"]:
                    equations_that_this_key_is_in = [k for k, v in lhs_and_rhs.items() if key in str(v)]
                    for thing in equations_that_this_key_is_in:
                        if thing not in ["root", "humn"]:
                            lhs_and_rhs[thing] = lhs_and_rhs[thing].replace(key, f"({value})")
                            # try:
                            #     lhs_and_rhs[thing] = eval(lhs_and_rhs[thing])
                            # except NameError:
                            # result = re.search(r"\((\w{4}) ([+\-*\/]) (\w{4})\)", lhs_and_rhs[thing])
                            # print("")
                            # if result is not None and isinstance(lhs_and_rhs[thing], str) and isinstance(number_1 := lhs_and_rhs[result.groups()[0]], int) and isinstance(number_2 := lhs_and_rhs[result.groups()[2]], int):
                            #     if result.groups()[0] != "humn" and result.groups()[2] != "humn":
                            #         lhs_and_rhs[thing] = lhs_and_rhs[thing].replace(result.string[result.span()[0]:result.span()[1]], str(OPS[result.groups()[1]](number_1, number_2)))
                            #         print("")
                            result = re.search(r"\((\w{4}) ([+\-*\/]) (\w{4})\)", lhs_and_rhs[thing])
                            if (
                                result is not None
                                and isinstance(lhs_and_rhs[thing], str)
                                and isinstance(number_1 := lhs_and_rhs[result.groups()[0]], int)
                                and isinstance(number_2 := lhs_and_rhs[result.groups()[2]], int)
                            ):
                                if result.groups()[0] != "humn" and result.groups()[2] != "humn":
                                    lhs_and_rhs[thing] = lhs_and_rhs[thing].replace(
                                        result.string[result.span()[0] : result.span()[1]],
                                        str(OPS[result.groups()[1]](number_1, number_2)),
                                    )
                                    print("")

                            # attempt to simplify
                while True:
                    # result = re.search(r"\(\(?(\d+)\)? ([+\-*\/]) \(?(\d+)\)?\)", str(lhs_and_rhs[key]))
                    result = re.search(r"\([0-9\+\-\*\/\s\.]+\)", str(lhs_and_rhs[key]))
                    print("")
                    if result is None:
                        break
                    # lhs_and_rhs[key] = lhs_and_rhs[key].replace(result.string[result.span()[0]:result.span()[1]], str(OPS[result.groups()[1]](int(result.groups()[0]), int(result.groups()[2]))))
                    lhs_and_rhs[key] = lhs_and_rhs[key].replace(
                        result.string[result.span()[0] : result.span()[1]],
                        str(eval(result.string[result.span()[0] : result.span()[1]])),
                    )
                    # if result is not None and isinstance(lhs_and_rhs[thing], str) and isinstance(
                    #         number_1 := lhs_and_rhs[result.groups()[0]], int) and isinstance(
                    #         number_2 := lhs_and_rhs[result.groups()[2]], int):
                    #     if result.groups()[0] != "humn" and result.groups()[2] != "humn":
                    #         lhs_and_rhs[thing] = lhs_and_rhs[thing].replace(
                    #             result.string[result.span()[0]:result.span()[1]],
                    #             str(OPS[result.groups()[1]](number_1, number_2)))
                    #         print("")

                    # result.groups()[0], result.groups()[1], result.groups()[2], OPS[result.groups()[1]](
                    #     lhs_and_rhs[result.groups()[0]], lhs_and_rhs[result.groups()[2]])
                    # ...  # TODO: continue this train of thought
                    # result.groups()[0], result.groups()[1], result.groups()[2],
                    # lhs_and_rhs[thing].replace(result.string[result.pos:result.endpos], "")
                print("")
                # [(result := re.search(r"[a-zA-Z]", str(lhs_and_rhs[x]))) is None or "humn" in result.string for x in
                #  lhs_and_rhs.keys() if x not in lhs_and_rhs["root"].split(" + ")]

                # dumb = re.sub(
                #     r"\((\d+)\)", "\g<1>", f"{lhs_and_rhs['brrs']} = {lhs_and_rhs['fcjl']}".replace("humn", "x")
                # )


if __name__ == "__main__":
    m, m_d, d_m = read_input_file("input.txt")
    # print(f"The monkey named `root` will yell the number {resolve_monkeys(m, m_d, d_m)}.")
    # determine_what_number_to_yell(m, m_d, d_m)
    # quick_test("example.txt")
    quick_test("input.txt")
