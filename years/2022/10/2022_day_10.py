from collections import defaultdict
from typing import TypeAlias

Instructions: TypeAlias = dict[int, int]  # cycle: value to add to the register


def read_input_file(file_name: str = "input.txt") -> Instructions:
    with open(file_name, "r") as f:
        instructions: dict[int, int] = defaultdict(int)
        instructions[-1] = 1
        cycle: int = 0
        for line in f.readlines():
            split_line = line.strip().split(" ")
            match split_line[0]:
                case "noop":
                    cycle += 1
                case "addx":
                    instructions[cycle + 3] += int(split_line[1])
                    cycle += 2
        return instructions


def calculate_x_register_value(instructions: Instructions, cycle: int) -> int:
    return sum([instructions[x] for x in range(-1, cycle + 1)])


def calculate_total_signal_strength(instructions: Instructions, cycle_step: int = 40, starting_cycle: int = 20) -> int:
    total_strength = 0
    for cycle in range(starting_cycle, max(instructions.keys()), cycle_step):
        total_strength += calculate_x_register_value(instructions, cycle) * cycle
    return total_strength


def render_crt_output(instructions: Instructions, width: int = 40, height: int = 6, sprite_width: int = 3) -> str:
    output = ""
    sprite_position = calculate_x_register_value(instructions, -1)
    for cycle in range(1, width * height + 1):
        if cycle in instructions.keys():
            sprite_position = calculate_x_register_value(instructions, cycle)
        character = "#" if ((cycle - 1) % width) + 1 in range(sprite_position, sprite_position + sprite_width) else "."
        output += character + "\n" if cycle % width == 0 else character
    return output


if __name__ == "__main__":
    inst = read_input_file("input.txt")
    print(f"The total signal strength starting at 20 and with steps of 40 is {calculate_total_signal_strength(inst)}.")
    print(f"The CRT draws the following pixels:\n\n{render_crt_output(inst)}")
