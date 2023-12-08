package main

import (
	"fmt"
	"math"
	"ndepaola/advent-of-code/lib"
	"regexp"
	"strings"
	"time"
)

type Node struct {
	left  string
	right string
}
type Nodes map[string]Node

func gcd(a int, b int) int { // euclid's algorithm
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func lcm(a int, b int) int {
	return int(math.Abs(float64(a*b))) / gcd(a, b)
}

func parseInput(fileName string) (Nodes, string) {
	data := strings.Split(lib.ReadFile(fileName), "\r\n\r\n")
	instructions := data[0]
	re := regexp.MustCompile("(\\w+) = \\((\\w+), (\\w+)\\)")
	nodeLines := strings.Split(data[1], "\r\n")
	nodes := make(Nodes)
	for i := 0; i < len(nodeLines); i++ {
		parsed := re.FindAllStringSubmatch(strings.TrimSpace(nodeLines[i]), -1)
		nodes[parsed[0][1]] = Node{left: parsed[0][2], right: parsed[0][3]}
	}
	return nodes, instructions
}

func walk(nodes Nodes, instructions string, startCondition func(string) bool, endCondition func(string) bool) int {
	// collect inputs
	positions := make([]string, 0, 10000) // some upper capacity limit
	for key, _ := range nodes {
		if startCondition(key) {
			positions = append(positions, key)
		}
	}

	// collect cycle times
	cycleTimes := make([]int, len(positions))

	// calculate cycle time for each starting position
	for i := 0; i < len(positions); i++ {
		position := positions[i]
		step := 0
		cycleTime := 0
		for {
			instruction := rune(instructions[step])
			node := nodes[position]
			position = node.left
			if instruction == 'R' {
				position = node.right
			}
			cycleTime++

			if endCondition(position) {
				break
			}

			// wrap around
			step += 1
			if step >= len(instructions) {
				step = 0
			}
		}
		cycleTimes[i] = cycleTime
	}

	// calculate lcm
	answer := cycleTimes[0]
	for i := 1; i < len(cycleTimes); i++ {
		answer = lcm(answer, cycleTimes[i])
	}
	return answer
}

func puzzle(fileName string) (int, int) {
	nodes, instructions := parseInput(fileName)

	part1 := walk(
		nodes,
		instructions,
		func(node string) bool { return node == "AAA" },
		func(node string) bool { return node == "ZZZ" },
	)
	part2 := walk(
		nodes,
		instructions,
		func(node string) bool { return strings.HasSuffix(node, "A") },
		func(node string) bool { return strings.HasSuffix(node, "Z") },
	)

	return part1, part2
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
