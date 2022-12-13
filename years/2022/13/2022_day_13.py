import json
from functools import cmp_to_key
from typing import TypeAlias

PacketItem: TypeAlias = int | list["PacketItem"]
Packet: TypeAlias = list[PacketItem]
PacketPair: TypeAlias = tuple[Packet, Packet]


def read_input_file_as_pairs(file_name: str = "input.txt") -> list[PacketPair]:
    packet_pairs = []
    with open(file_name, "r") as f:
        for group in f.read().split("\n\n"):
            split_group = group.splitlines()
            assert len(split_group) == 2
            packet_pairs.append((json.loads(split_group[0]), json.loads(split_group[1])))
    return packet_pairs


def read_input_file_as_flat_list(file_name: str = "input.txt") -> list[Packet]:
    with open(file_name, "r") as f:
        return [json.loads(line_stripped) for line in f.read().splitlines() if (line_stripped := line.strip())]


def is_packet_pair_in_order(packet_pair: PacketPair, source_of_truth_packet: int = 0) -> bool:
    for i in range(len(packet_pair[source_of_truth_packet])):
        try:
            left, right = packet_pair[0][i], packet_pair[1][i]
            if isinstance(left, int) and isinstance(right, int):
                if left != right:
                    return left < right
            else:
                return is_packet_pair_in_order(
                    (left if isinstance(left, list) else [left], right if isinstance(right, list) else [right]),
                    source_of_truth_packet=source_of_truth_packet,
                )
        except IndexError:
            return False
    return True


if __name__ == "__main__":
    print(
        "The sum of the indices of the packet pairs in the correct order is "
        f"{sum([i + 1 for i, x in enumerate(read_input_file_as_pairs('input.txt')) if is_packet_pair_in_order(x)])}."
    )
    sorted_packets = sorted(
        read_input_file_as_flat_list("input.txt") + [[[2]], [[6]]],  # add the two divider packets,
        key=cmp_to_key(lambda x, y: -1 if is_packet_pair_in_order((x, y)) else 1),  # type: ignore  # mypy weirdness
    )
    print(
        "The decoder key of the distress signal is "
        f"{(sorted_packets.index([[2]])+1)*(sorted_packets.index([[6]])+1)}."
    )
