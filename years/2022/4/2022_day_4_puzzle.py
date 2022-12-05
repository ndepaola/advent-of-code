import dataclasses


@dataclasses.dataclass
class SectionAssignment:
    min_id: int
    max_id: int

    @classmethod
    def from_line(cls, line: str) -> "SectionAssignment":
        line_split = line.split("-")
        assert len(line_split) == 2, f"Attempted to create a SectionAssignment with {len(line_split)} bits"
        return cls(min_id=int(line_split[0]), max_id=int(line_split[1]))


@dataclasses.dataclass
class ElfPair:
    first_elf: SectionAssignment
    second_elf: SectionAssignment

    @classmethod
    def from_line(cls, line: str) -> "ElfPair":
        line_split = line.split(",")
        assert len(line_split) == 2, f"Attempted to create an ElfPair with {len(line_split)} bits"
        return cls(
            first_elf=SectionAssignment.from_line(line_split[0]), second_elf=SectionAssignment.from_line(line_split[1])
        )

    def is_pairing_strictly_redundant(self) -> bool:
        return (
            self.first_elf.min_id >= self.second_elf.min_id and self.first_elf.max_id <= self.second_elf.max_id
        ) or (self.second_elf.min_id >= self.first_elf.min_id and self.second_elf.max_id <= self.first_elf.max_id)

    def is_pairing_redundant_at_all(self) -> bool:
        return (
            self.first_elf.max_id >= self.second_elf.min_id and self.first_elf.min_id <= self.second_elf.max_id
        ) or (self.second_elf.max_id >= self.first_elf.min_id and self.second_elf.min_id <= self.first_elf.max_id)


@dataclasses.dataclass
class ElfPairs:
    elf_pairs: list[ElfPair]

    @classmethod
    def from_input_file(cls, file_name: str = "input.txt") -> "ElfPairs":
        with open(file_name, "r") as f:
            return cls(elf_pairs=[ElfPair.from_line(line) for line in f.readlines()])

    def count_redundant_work_allocations_across_elf_pairs(self) -> int:
        return len(list(filter(lambda x: x.is_pairing_strictly_redundant(), self.elf_pairs)))

    def count_all_redundant_work_allocations(self) -> int:
        return len(list(filter(lambda x: x.is_pairing_redundant_at_all(), self.elf_pairs)))


if __name__ == "__main__":
    elf_pairs = ElfPairs.from_input_file()
    print(
        f"There are {elf_pairs.count_redundant_work_allocations_across_elf_pairs()} "
        f"redundant work allocations across Elf pairs."
    )
    print(f"There are {elf_pairs.count_all_redundant_work_allocations()} " f"redundant work allocations in total.")
