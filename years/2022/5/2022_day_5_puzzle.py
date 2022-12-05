import dataclasses
import re


@dataclasses.dataclass
class CrateStack:
    crates: list[str]

    def add_crate(self, crate: str) -> None:
        self.crates.append(crate)


@dataclasses.dataclass
class Transform:
    num_crates: int
    source_stack: int
    target_stack: int

    @classmethod
    def from_line(cls, line: str) -> "Transform":
        num_crates, source_stack, target_stack = re.match(  # type: ignore  # technically sloppy but known input data
            "^move ([0-9].*) from ([0-9].*) to ([0-9].*)$", line.strip()
        ).groups()
        return cls(num_crates=int(num_crates), source_stack=int(source_stack) - 1, target_stack=int(target_stack) - 1)


@dataclasses.dataclass
class CrateStackSet:
    crate_stacks: list[CrateStack]
    transforms: list[Transform]

    @classmethod
    def pivot_crate_stacks_lines(cls, lines: list[str]) -> list[CrateStack]:
        num_stacks = len(re.sub(r"\s{2,}", " ", lines[-1]).strip().split(" "))
        crate_stacks = [CrateStack(crates=[]) for _ in range(num_stacks)]
        for line in lines[:-1][::-1]:  # iterate in reverse order and skip the bottom-most line of crate numbers
            # four characters per crate stack
            for stack_number in range(0, num_stacks):
                potential_crate = line[stack_number * 4 : stack_number * 4 + 4].strip()
                if potential_crate:
                    crate_stacks[stack_number].add_crate(potential_crate.replace("]", "").replace("[", ""))
        return crate_stacks

    @classmethod
    def from_input_file(cls, file_name: str = "input.txt") -> "CrateStackSet":
        crate_stacks_lines = []
        transform_lines = []
        read_stack_lines = True
        with open(file_name, "r") as f:
            for line in f.readlines():
                if not line.strip():
                    read_stack_lines = False  # we've reached the point in the file where it switches from stack to tf
                else:
                    if read_stack_lines:
                        crate_stacks_lines.append(line)
                    else:
                        transform_lines.append(line)
        crate_stacks = cls.pivot_crate_stacks_lines(crate_stacks_lines)  # exclude line with stack numbers
        return cls(crate_stacks=crate_stacks, transforms=[Transform.from_line(line) for line in transform_lines])

    def apply_transforms(self, reverse: bool) -> "CrateStackSet":
        transformed_stacks = [*self.crate_stacks]
        for transform in self.transforms:
            assert (
                len(transformed_stacks[transform.source_stack].crates) >= transform.num_crates
            ), "Cannot draw below 0 crates"
            crates_to_move = transformed_stacks[transform.source_stack].crates[
                len(transformed_stacks[transform.source_stack].crates) - transform.num_crates :
            ]
            if reverse:
                crates_to_move.reverse()
            transformed_stacks[transform.target_stack].crates = [
                *transformed_stacks[transform.target_stack].crates,
                *crates_to_move,
            ]
            transformed_stacks[transform.source_stack].crates = transformed_stacks[transform.source_stack].crates[
                0 : len(transformed_stacks[transform.source_stack].crates) - transform.num_crates
            ]

        return CrateStackSet(crate_stacks=transformed_stacks, transforms=self.transforms)

    def get_stack_message(self) -> str:
        return "".join([stack.crates[-1] for stack in self.crate_stacks])


if __name__ == "__main__":
    print(
        f"The crates on the top of each stack after the rearrangement procedure completes with the CrateMover 9000 are "
        f"{CrateStackSet.from_input_file().apply_transforms(reverse=True).get_stack_message()}."
    )
    print(
        f"The crates on the top of each stack after the rearrangement procedure completes with the CrateMover 9001 are "
        f"{CrateStackSet.from_input_file().apply_transforms(reverse=False).get_stack_message()}."
    )
