import abc
from typing import Type


class Option:
    @classmethod
    @abc.abstractmethod
    def get_player_code(cls) -> str:
        # first column in strategy guide
        ...

    @classmethod
    @abc.abstractmethod
    def get_opponent_code(cls) -> str:
        # from incorrectly decoding the second column in strategy guide
        ...

    @classmethod
    @abc.abstractmethod
    def get_value(cls) -> int:
        # value the player gets for selecting this
        ...


class Rock(Option):
    @classmethod
    def get_player_code(cls) -> str:
        return "X"

    @classmethod
    def get_opponent_code(cls) -> str:
        return "A"

    @classmethod
    @abc.abstractmethod
    def get_value(cls) -> int:
        return 1


class Paper(Option):
    @classmethod
    def get_player_code(cls) -> str:
        return "Y"

    @classmethod
    def get_opponent_code(cls) -> str:
        return "B"

    @classmethod
    @abc.abstractmethod
    def get_value(cls) -> int:
        return 2


class Scissors(Option):
    @classmethod
    def get_player_code(cls) -> str:
        return "Z"

    @classmethod
    def get_opponent_code(cls) -> str:
        return "C"

    @classmethod
    @abc.abstractmethod
    def get_value(cls) -> int:
        return 3


OPTIONS = [Rock, Paper, Scissors]


class GameOutcome:
    @classmethod
    @abc.abstractmethod
    def get_code(cls) -> str:
        ...

    @classmethod
    @abc.abstractmethod
    def get_index_offset(cls) -> int:
        ...


class Win(GameOutcome):
    @classmethod
    def get_code(cls) -> str:
        return "Z"

    @classmethod
    def get_index_offset(cls) -> int:
        return 1


class Draw(GameOutcome):
    @classmethod
    def get_code(cls) -> str:
        return "Y"

    @classmethod
    def get_index_offset(cls) -> int:
        return 0


class Lose(GameOutcome):
    @classmethod
    def get_code(cls) -> str:
        return "X"

    @classmethod
    def get_index_offset(cls) -> int:
        return -1


OUTCOMES = [Win, Draw, Lose]


def wrap_index(index: int, length: int) -> int:
    return ((index % length) + length) % length


def does_player_win(player_option: Type[Option], opponent_option: Type[Option]) -> bool:
    return OPTIONS[wrap_index(OPTIONS.index(opponent_option) + Win.get_index_offset(), len(OPTIONS))] == player_option


def incorrectly_read_strategy_guide(file_name: str = "input.txt") -> list[tuple[Type[Option], Type[Option]]]:
    options_by_opponent_code = {x.get_opponent_code(): x for x in [Rock, Paper, Scissors]}
    options_by_player_code = {x.get_player_code(): x for x in [Rock, Paper, Scissors]}
    with open(file_name, "r") as f:
        return [
            (options_by_opponent_code[(split_line := x.strip().split(" "))[0]], options_by_player_code[split_line[1]])
            for x in f.readlines()
        ]


def count_score_for_incorrectly_following_strategy_guide(
    strategy_guide: list[tuple[Type[Option], Type[Option]]], win_bonus: int = 6, draw_bonus: int = 3
) -> int:
    score = 0
    for opponent_option, player_option in strategy_guide:
        if player_option == opponent_option:
            score += draw_bonus
        elif does_player_win(player_option=player_option, opponent_option=opponent_option):
            score += win_bonus
        score += player_option.get_value()
    return score


def correctly_read_strategy_guide(file_name: str = "input.txt") -> list[tuple[Type[Option], Type[GameOutcome]]]:
    options_by_opponent_code = {x.get_opponent_code(): x for x in [Rock, Paper, Scissors]}
    game_outcomes_by_code = {x.get_code(): x for x in OUTCOMES}
    with open(file_name, "r") as f:
        return [
            (options_by_opponent_code[(split_line := x.strip().split(" "))[0]], game_outcomes_by_code[split_line[1]])
            for x in f.readlines()
        ]


def count_score_for_correctly_following_strategy_guide(
    strategy_guide: list[tuple[Type[Option], Type[GameOutcome]]], win_bonus: int = 6, draw_bonus: int = 3
) -> int:
    score = 0
    for opponent_action, game_outcome in strategy_guide:
        player_action = OPTIONS[
            wrap_index(OPTIONS.index(opponent_action) + game_outcome.get_index_offset(), len(OPTIONS))
        ]
        if game_outcome == Win:
            score += win_bonus
        elif game_outcome == Draw:
            score += draw_bonus
        score += player_action.get_value()
    return score


if __name__ == "__main__":
    incorrect_guide = incorrectly_read_strategy_guide()
    print(
        f"The total score for playing according to the incorrectly interpreted strategy guide is "
        f"{count_score_for_incorrectly_following_strategy_guide(incorrect_guide)}."
    )
    correct_guide = correctly_read_strategy_guide()
    print(
        f"The total score for playing according to the correctly interpreted strategy guide is "
        f"{count_score_for_correctly_following_strategy_guide(correct_guide)}."
    )
