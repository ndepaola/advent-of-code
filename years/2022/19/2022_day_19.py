import dataclasses
import enum
import math
import re
import time
from functools import cached_property
from typing import TypeAlias

RobotRecipe: TypeAlias = dict[str, int]  # ingredient => quantity required
Blueprint: TypeAlias = dict[str, RobotRecipe]  # robot => recipe to make the robot


class Materials(str, enum.Enum):
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"


def read_input_file(file_name: str = "input.txt") -> tuple[Blueprint, ...]:
    with open(file_name, "r") as f:
        blueprints: list[Blueprint] = []
        for line in f.readlines():
            if stripped_line := line.strip():
                blueprint: Blueprint = {}
                # sorry for this disgusting fucking regex 🗿
                matches = re.findall(
                    r"Each ([a-zA-Z]+) robot costs (?:(\d+) ([a-zA-Z]+) and )*(?:(\d+) ([a-zA-Z]+)(?: and )?)+\.\s?",
                    stripped_line,
                )
                for match in matches:
                    blueprint[match[0]] = {
                        match[i + 1]: int(match[i]) for i in range(1, len(matches), 2) if match[i] and match[i + 1]
                    }
                blueprints.append(blueprint)
        return tuple(blueprints)


@dataclasses.dataclass
class State:
    time: int  # number of minutes on the clock - starts from zero
    time_steps: int  # total number of minutes
    blueprint: Blueprint
    inventory: dict[str, int]  # ingredient => quantity of ingredient
    robots: dict[str, int]  # robot => quantity of robot

    def get_possible_states(self) -> list["State"]:
        states = []
        for robot_you_can_make in self.robots.keys():
            # determine the earliest point in time that this robot can be made

            # this checks whether you have at least one of each robot for the materials required to make this robot
            if min([self.robots[x] for x in self.blueprint[robot_you_can_make]]) > 0:
                # check if this robot is necessary. if you have 5 ore robots and the recipe that requires the most ore
                # needs 5 of it, you don't need to produce any more ore robots. building another ore robot will not
                # unlock future build decisions. this doesn't apply to geode because geode contributes to the objective.
                if (
                    robot_you_can_make != Materials.GEODE
                    and max([x.get(robot_you_can_make, 0) for x in self.blueprint.values()])
                    <= self.robots[robot_you_can_make]
                ):
                    continue

                # determine how long it will take to accumulate enough resources to build this robot
                time_until_you_can_make_this_robot = max(
                    # calculate maximum time your robots need to produce the difference between your inventory
                    # and the recipe between all materials the recipe requires
                    [
                        math.ceil(max(quantity_required - self.inventory[material], 0) / self.robots[material])
                        for material, quantity_required in self.blueprint[robot_you_can_make].items()
                    ]
                )
                if (self.time + time_until_you_can_make_this_robot + 1) < self.time_steps:
                    state = State(
                        time=self.time + time_until_you_can_make_this_robot + 1,
                        time_steps=self.time_steps,
                        blueprint=self.blueprint,
                        inventory={
                            material: (
                                quantity
                                - self.blueprint[robot_you_can_make].get(material, 0)
                                + (time_until_you_can_make_this_robot + 1) * self.robots.get(material, 0)
                            )
                            for material, quantity in self.inventory.items()
                        },
                        robots={
                            robot: quantity + (1 if robot == robot_you_can_make else 0)
                            for robot, quantity in self.robots.items()
                        },
                    )
                    states.append(state)
        return states

    @cached_property
    def objective(self) -> int:
        return (self.robots[Materials.GEODE] * (self.time_steps - self.time)) + self.inventory[Materials.GEODE]

    @cached_property
    def estimate(self) -> int:
        # a super highball estimate for the potential of this state
        # assuming you build a geode robot for each time step from here on out, how much geode would you end up with?
        return self.objective + sum(range(self.time_steps - self.time))


def simulate_blueprint(blueprint: Blueprint, time_steps: int = 24) -> State:
    starting_state = State(
        time=0,
        time_steps=time_steps,
        blueprint=blueprint,
        inventory={Materials.ORE: 0, Materials.CLAY: 0, Materials.OBSIDIAN: 0, Materials.GEODE: 0},
        robots={Materials.ORE: 1, Materials.CLAY: 0, Materials.OBSIDIAN: 0, Materials.GEODE: 0},
    )
    frontier: list[State] = starting_state.get_possible_states()
    best_state: State = starting_state
    while frontier:
        state = frontier.pop(0)
        for possible_state in state.get_possible_states():
            if possible_state.objective > best_state.objective:
                best_state = possible_state
            if possible_state.time < time_steps and possible_state.estimate > best_state.objective:
                # only explore the node if it has the potential to exceed the current best solution
                # and if there's any time left on the clock for it
                frontier.append(possible_state)
    return best_state


def calculate_quality_level(blueprints: tuple[Blueprint, ...]) -> None:
    quality_level = 0
    print(f"Commencing evaluation of {len(blueprints)} blueprint{'s' if len(blueprints) != 1 else ''}.\n")
    for i, blueprint in enumerate(blueprints):
        print(f"Evaluating blueprint {i+1} for 24 minutes... ", end="", flush=True)
        t0 = time.time()
        solution = simulate_blueprint(blueprint, 24)
        print(f"and done! Score is {solution.objective}, computing that took {round(time.time() - t0, 2)} seconds.")
        quality_level += (i + 1) * solution.objective
    print(f"\nAll blueprints evaluated. Total quality level: {quality_level}.")


def calculate_multiplied_geodes(blueprints: tuple[Blueprint, ...], num_blueprints: int = 3) -> None:
    result = 1
    print(f"\nCommencing evaluation of the first {num_blueprints} blueprint{'s' if num_blueprints != 1 else ''}.\n")
    for i in range(num_blueprints):
        print(f"Evaluating blueprint {i + 1} for 32 minutes... ", end="", flush=True)
        t0 = time.time()
        solution = simulate_blueprint(blueprints[i], 32)
        print(f"and done! Score is {solution.objective}, computing that took {round(time.time() - t0, 2)} seconds.")
        result *= solution.objective
    print(f"\nAll blueprints evaluated. Multiplied number of geodes across blueprints: {result}.")


if __name__ == "__main__":
    b = read_input_file("input.txt")
    t1 = time.time()
    calculate_quality_level(b)
    calculate_multiplied_geodes(b)
    print(f"\nTotal runtime: {round(time.time() - t1, 2)} seconds.")
