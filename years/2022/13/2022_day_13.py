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


def is_packet_pair_in_order(left_packet: Packet, right_packet: Packet) -> bool | None:
    for i in range(len(left_packet)):
        try:
            left, right = left_packet[i], right_packet[i]
            if isinstance(left, int) and isinstance(right, int):
                if left != right:
                    return left < right
            else:
                left_item = left if isinstance(left, list) else [left]
                right_item = right if isinstance(right, list) else [right]
                comparison_result = is_packet_pair_in_order(left_packet=left_item, right_packet=right_item)
                if comparison_result is not None:
                    return comparison_result
        except IndexError:
            return False
    if len(left_packet) == len(right_packet):
        return None  # packets are the same length and no comparison was made
    return True


if __name__ == "__main__":
    print(
        "The sum of the indices of the packet pairs in the correct order is "
        f"{sum([i + 1 for i, x in enumerate(read_input_file_as_pairs('input.txt')) if is_packet_pair_in_order(*x)])}."
    )
    sorted_packets = sorted(
        read_input_file_as_flat_list("input.txt") + [[[2]], [[6]]],  # add the two divider packets,
        key=cmp_to_key(  # type: ignore
            lambda x, y: {True: -1, False: 1, None: 0}[is_packet_pair_in_order(left_packet=x, right_packet=y)]
        ),
    )
    print(
        "The decoder key of the distress signal is "
        f"{(sorted_packets.index([[2]])+1)*(sorted_packets.index([[6]])+1)}."
    )
