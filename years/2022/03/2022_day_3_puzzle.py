import dataclasses
from typing import Self


def get_value_for_character(character: str) -> int:
    assert len(character) == 1, f"Attempted to get the value of a character but the string was {len(character)} long"
    if character.isupper():
        return ord(character) - 64 + 26
    return ord(character) - 96


@dataclasses.dataclass
class Compartment:
    contents: str


@dataclasses.dataclass
class Rucksack:
    first_compartment: Compartment
    second_compartment: Compartment

    @classmethod
    def from_line(cls, line: str) -> "Rucksack":
        stripped_line = line.strip()
        assert len(stripped_line) % 2 == 0, "Line must be even length"
        half_length = int(len(stripped_line) / 2)
        return cls(
            first_compartment=Compartment(contents=stripped_line[0:half_length]),
            second_compartment=Compartment(contents=stripped_line[half_length:]),
        )

    def get_unique_items(self) -> set[str]:
        return set(self.first_compartment.contents) | set(self.second_compartment.contents)

    def get_overlapping_items(self) -> set[str]:
        return set(self.first_compartment.contents) & set(self.second_compartment.contents)

    def get_overlapping_item(self) -> str:
        overlapping_items = self.get_overlapping_items()
        assert len(overlapping_items) == 1
        return overlapping_items.pop()


@dataclasses.dataclass
class RucksackContainer:
    rucksacks: list[Rucksack]

    @classmethod
    def from_input_file(cls, file_name: str = "input.txt") -> "RucksackContainer":
        with open(file_name, "r") as f:
            return cls(rucksacks=[Rucksack.from_line(line) for line in f.readlines()])

    def get_sum_of_priorities_of_overlapping_items_for_all_rucksacks(self) -> int:
        # assume that each rucksack only has one overlapping item
        return sum(get_value_for_character(rucksack.get_overlapping_item()) for rucksack in self.rucksacks)

    def get_sum_of_priorities_of_badges_per_group(self, group_size: int) -> int:
        assert group_size > 1, "Don't use this function with a group size of 1"
        assert len(self.rucksacks) % group_size == 0, f"Cannot cleanly divide rucksacks into {group_size} groups"
        total_priority = 0
        for i in range(0, int(len(self.rucksacks) / group_size)):
            rucksack_unique_items = [rucksack.get_unique_items() for rucksack in self.rucksacks[3 * i : 3 * i + 3]]
            common_item_set = rucksack_unique_items[0]
            for items in rucksack_unique_items[1:]:
                common_item_set = common_item_set.intersection(items)
            assert (
                len(common_item_set) == 1
            ), f"Expected there to be exactly 1 common item per group, got {len(common_item_set)}"
            total_priority += get_value_for_character(common_item_set.pop())
        return total_priority


if __name__ == "__main__":
    rucksack_container = RucksackContainer.from_input_file()
    group_size = 3
    print(
        f"The sum of priorities of overlapping items for all rucksacks is "
        f"{rucksack_container.get_sum_of_priorities_of_overlapping_items_for_all_rucksacks()}."
    )
    print(
        f"The sum of priorities of each group's badge (group size {group_size}) is "
        f"{rucksack_container.get_sum_of_priorities_of_badges_per_group(group_size)}."
    )
