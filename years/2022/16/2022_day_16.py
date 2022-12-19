import dataclasses
import re
import time
from collections import defaultdict
from itertools import combinations, permutations
from typing import TypeAlias

Movements: TypeAlias = dict[str, set[str]]  # node => which nodes can you move to from here?
SolvedMovements: TypeAlias = dict[str, dict[str, int]]  # source => {destination node => moves to get to this node}
FlowRates: TypeAlias = dict[str, int]  # node => flow rate
Agent: TypeAlias = tuple[str, int]  # which valve the agent is standing at and how much time they have left


def get_total_steam_released(opened_valves: dict[str, int], flows: FlowRates) -> int:
    # how much steam will be released from now until the end of the simulation if nothing else changes?
    return sum([flows[valve] * time_step for valve, time_step in opened_valves.items()])


def dijkstra(moves: Movements) -> SolvedMovements:
    # compute a map of how long it takes to get from each node to each other node
    # i didn't realise this until tonight, but running dijkstra from each possible starting point is called
    # the floyd-warshall algorithm. wikipedia reckons this only works if all edge weights are non-negative.
    solved_moves: SolvedMovements = defaultdict(dict)
    all_nodes = set(moves.keys())
    for source_node in all_nodes:
        frontier = {source_node}
        node_distances = {x: None if x != source_node else 0 for x in all_nodes}
        explored = set()
        while frontier:
            node = frontier.pop()
            neighbours = moves[node]
            node_distance = node_distances[node]
            assert node_distance is not None
            for neighbour in neighbours:
                neighbour_distance = node_distances[neighbour]
                if neighbour_distance is None:
                    node_distances[neighbour] = node_distance + 1
                else:
                    node_distances[neighbour] = min(neighbour_distance, node_distance + 1)
                if neighbour not in explored:
                    frontier.add(neighbour)
            explored.add(node)
        assert None not in node_distances.values()
        solved_moves[source_node] = node_distances  # type: ignore  # mmm i'm so full from gorging on mypy errors, yum
    return solved_moves


@dataclasses.dataclass(frozen=True)
class State:
    agents: list[Agent]
    opened_valves: dict[str, int]  # node => which time step it was opened in
    total_steam_released: int = 0  # avoid recalculating every time this is referenced

    def get_possible_states(self, moves: SolvedMovements, flows: FlowRates) -> list["State"]:
        valves_with_flows_greater_than_zero = {valve for valve, flow_rate in flows.items() if flow_rate > 0}
        possible_destination_valves = valves_with_flows_greater_than_zero - set(self.opened_valves.keys())
        possible_states = []

        if not (agents_with_some_time_left := [x for x in self.agents if x[1] > 0]):
            return []

        # if all agents at same time and place, we can use combinations rather than permutations to reduce nodes
        perm_getter = (
            combinations
            if len({x[1] for x in self.agents}) == 1 and len({x[0] for x in self.agents}) == 1
            else permutations
        )
        for valves_per_agent in perm_getter(possible_destination_valves, len(agents_with_some_time_left)):
            agents_and_valve_open_times = []
            for target_valve, agent in zip(valves_per_agent, agents_with_some_time_left):
                # -1 here because it takes one time step to open a valve once you arrive there
                agents_and_valve_open_times.append((target_valve, agent[1] - moves[agent[0]][target_valve] - 1))
            if min([x[1] for x in agents_and_valve_open_times]) >= 0:  # ensure this move would not cause illegal state
                possible_state_valves = self.opened_valves | {v: t for v, t in agents_and_valve_open_times}
                possible_states.append(
                    State(
                        agents=agents_and_valve_open_times,
                        opened_valves=possible_state_valves,
                        total_steam_released=get_total_steam_released(possible_state_valves, flows),
                    ),
                )
        return possible_states

    def estimate_best_answer(self, moves: SolvedMovements, flows: FlowRates) -> int:
        # how much steam could theoretically be released in total from here?
        # this naive estimate assumes the agent with the most time travels to each valve and opens it without losing
        # time - e.g. if the elephant has 20 minutes and there are 4 unopened valves, this will count the total pressure
        # you would achieve by the elephant moving to each valve from t=20 and opening it
        agent_with_most_time = max(self.agents, key=lambda x: x[1])
        return sum(
            [
                flow_rate  # multiply by the time it was opened if it's opened, or estimate the earliest time to open it
                * self.opened_valves.get(valve, agent_with_most_time[1] - moves[agent_with_most_time[0]][valve] + 1)
                for valve, flow_rate in flows.items()
            ]
        )


def read_input_file(file_name: str = "input.txt") -> tuple[Movements, FlowRates]:
    moves: Movements = {}
    flows: FlowRates = {}
    with open(file_name, "r") as f:
        for line in f.readlines():
            if stripped_line := line.strip():
                valve, flow_rate_string, destination_valves = re.match(
                    r"^Valve (\w{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+?)(?:,|$)$", stripped_line
                ).groups()  # type: ignore  # technically sloppy but known input data so w/e
                moves[valve] = {x.strip() for x in destination_valves.split(", ")}
                flows[valve] = int(flow_rate_string)
    return moves, flows


def maximise_pressure_reduction(
    moves: SolvedMovements, flows: FlowRates, max_time_steps: int = 30, num_agents: int = 1
) -> int:
    num_valves_with_flows_greater_than_zero = len([valve for valve, flow_rate in flows.items() if flow_rate > 0])
    starting_state = State(agents=[("AA", max_time_steps) for _ in range(num_agents)], opened_valves={})
    frontier: list[State] = []
    for possible_state in starting_state.get_possible_states(moves=moves, flows=flows):
        frontier.append(possible_state)
    state_with_max_steam: State = starting_state
    while frontier:
        state = frontier.pop()  # popping from the back and appending to the back -> depth first search
        if state.total_steam_released > state_with_max_steam.total_steam_released:
            state_with_max_steam = state
        for possible_state in state.get_possible_states(moves, flows):
            if possible_state.total_steam_released > state_with_max_steam.total_steam_released:
                state_with_max_steam = possible_state
            if (  # if you can still open more valves here and this state has the potential for more steam than curr max
                len(possible_state.opened_valves.keys()) < num_valves_with_flows_greater_than_zero
                and possible_state.estimate_best_answer(moves, flows) > state_with_max_steam.total_steam_released
            ):
                frontier.append(possible_state)
    return state_with_max_steam.total_steam_released


if __name__ == "__main__":
    movements, flow_rates = read_input_file("input.txt")
    solved_movements = dijkstra(movements)
    t0 = time.time()
    print(
        f"The maximum amount of steam which can be released by just yourself in 30 minutes is "
        f"{maximise_pressure_reduction(solved_movements, flow_rates, max_time_steps=30, num_agents=1)} pressure. "
        f"Computing this took roughly {int(time.time() - t0)} second/s."
    )
    t1 = time.time()
    print(
        f"The maximum amount of steam which can be released by you and your elephant friend in 26 minutes is "
        f"{maximise_pressure_reduction(solved_movements, flow_rates, max_time_steps=26, num_agents=2)} pressure. "
        f"Computing this took roughly {int(time.time() - t1)} second/s."
    )
