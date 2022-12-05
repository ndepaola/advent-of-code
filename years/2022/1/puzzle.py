def aggregate_calories_by_elf(lines: list[str]) -> list[int]:
    # Return a list of the total calories each Elf is carrying in descending order.
    calories_by_elf = []
    count = 0
    for line in lines:
        if stripped_line := line.strip():
            count += int(stripped_line)
        else:
            if count > 0:
                calories_by_elf.append(count)
            count = 0
    return sorted(calories_by_elf, reverse=True)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        calories = aggregate_calories_by_elf(f.readlines())
        print(f"The elf carrying the most calories is carrying {calories[-1]} calories.")
        print(f"The three elves carrying the most calories are altogether carrying {sum(calories[0:3])} calories.")
