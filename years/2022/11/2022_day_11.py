import copy
import dataclasses
from functools import reduce
from operator import mul
from typing import Callable


@dataclasses.dataclass
class Monkey:
    items: list[int]  # ordered list of items, represented by their worry value
    operation: Callable[[int], int]  # old value => new value
    throw: Callable[[int], int]  # value => monkey to throw the item to
    inspection_count: int = 0


def read_input_file(file_name: str = "input.txt") -> tuple[list[Monkey], int]:
    with open(file_name, "r") as f:
        monkeys = []
        product_mod_base = 1  # used to keep worrying under control while being mathematically equivalent
        for monkey_text in f.read().split("\n\n"):
            _, starting_items_text, operation_text, mod_base_text, test_true_target_monkey, test_false_target_monkey = [
                x.strip() for x in monkey_text.splitlines()
            ]
            mod_base = int(mod_base_text[len("Test: divisible by ") :])
            product_mod_base *= mod_base
            monkeys.append(
                Monkey(  # WARNING: using `eval` like this is super unsafe! don't do this in non-toy code.
                    items=[int(x.strip()) for x in starting_items_text[len("Starting items: ") :].split(",")],
                    operation=(
                        lambda value, callable_text=operation_text[  # type: ignore  # mypy unhappy with closures
                            len("Operation: new = ") :
                        ].replace("old", "{0}"): eval(callable_text.format(value))
                    ),
                    throw=(
                        lambda value, true_value=int(  # type: ignore  # mypy unhappy with closures
                            test_true_target_monkey[len("If true: throw to monkey ") :]
                        ), false_value=int(
                            test_false_target_monkey[len("If true: throw to monkey ") :]
                        ), base=mod_base: (
                            true_value if value % base == 0 else false_value
                        )
                    ),
                )
            )
        return monkeys, product_mod_base


def calculate_monkey_business(monkeys: list[Monkey], worrywort: bool, mod_base: int, num_rounds: int = 20) -> int:
    mutated_monkeys = copy.deepcopy(monkeys)  # avoid mutating input list. [*monkeys] doesn't cut it here.
    for round_ in range(num_rounds):
        for monkey in mutated_monkeys:
            while monkey.items:
                value = monkey.operation(monkey.items.pop(0))  # grab an item for the monkey to inspect and inspect it
                if worrywort:
                    value = value % mod_base  # keep anxiety under control with mathematics
                else:
                    value = value // 3  # keep anxiety under control by taking a chill pill
                monkey.inspection_count += 1  # track number of inspections for calculating monkey business
                mutated_monkeys[monkey.throw(value)].items.append(value)  # pass the item to the next monkey
    return reduce(mul, sorted([x.inspection_count for x in mutated_monkeys], reverse=True)[0:2], 1)


if __name__ == "__main__":
    m, product_base = read_input_file("input.txt")
    print(
        f"The total level of monkey business in this situation when you're not a worrywort and the monkeys pass "
        f"your stuff around for 20 rounds is "
        f"{calculate_monkey_business(m, worrywort=False, num_rounds=20, mod_base=product_base)}."
    )
    print(
        f"The total level of monkey business in this situation when your anxiety is unbounded and the monkeys pass "
        f"your stuff around for 10,000 rounds is "
        f"{calculate_monkey_business(m, worrywort=True, num_rounds=10_000, mod_base=product_base)}."
    )
