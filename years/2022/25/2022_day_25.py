SNAFU_POWER = 5
SNAFU_TO_DECIMAL = {"1": 1, "2": 2, "0": 0, "-": -1, "=": -2}


def snafu_to_decimal(snafu: str) -> int:
    return sum([SNAFU_TO_DECIMAL[x] * (SNAFU_POWER ** (len(snafu) - 1 - i)) for i, x in enumerate(snafu)])


def decimal_to_snafu(decimal: int) -> str:
    # determine how many snafu places this number requires
    number_of_characters = 0
    while True:
        number_of_characters += 1
        if sum([max(SNAFU_TO_DECIMAL.values()) * (SNAFU_POWER**i) for i in range(number_of_characters)]) >= decimal:
            break

    # initialise our result string with 0's, then for each snafu place, find the char that gets us closest to `decimal`
    snafu = "0" * number_of_characters
    for i in range(number_of_characters):
        snafu = min(
            [snafu[0:i] + x + snafu[i + 1 :] for x in SNAFU_TO_DECIMAL.keys()],
            key=lambda my_snafu: abs(decimal - snafu_to_decimal(my_snafu)),
        )
    assert snafu_to_decimal(snafu) == decimal
    return snafu


def read_input_file(file_name: str = "input.txt") -> list[str]:
    with open(file_name, "r") as f:
        return [x.strip() for x in f.readlines() if x.strip()]


if __name__ == "__main__":
    s = decimal_to_snafu(sum([snafu_to_decimal(s) for s in read_input_file("input.txt")]))
    print(f"The SNAFU number you need to supply to Bob's console is {s}.")
