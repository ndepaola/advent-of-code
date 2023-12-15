package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"strconv"
	"strings"
	"time"
)

func hash(line string) int {
	total := 0
	for i := 0; i < len(line); i++ {
		total += int(line[i])
		total = (total * 17) % 256
	}
	return total
}

func part1(data []string) int {
	total := 0
	for i := 0; i < len(data); i++ {
		subtotal := hash(strings.TrimSpace(data[i]))
		total += subtotal
	}
	return total
}

func part2(data []string) int {
	hashmap := make(map[int][]string)
	for i := 0; i < 256; i++ {
		hashmap[i] = make([]string, 0, 1000) // idk how big these will get. 1000 is probably a reasonable upper bound
	}
	focalLengthMap := make(map[string]int)

	for i := 0; i < len(data); i++ {
		line := strings.TrimSpace(data[i])
		equalsIndex := strings.IndexRune(line, '=')
		dashIndex := strings.IndexRune(line, '-')
		label := line[:max(equalsIndex, dashIndex)]
		hashed := hash(label)
		if equalsIndex >= 0 {
			// equals
			focalLength, err := strconv.Atoi(line[equalsIndex+1:])
			if err != nil {
				panic(err)
			}
			idx := -1
			for j := 0; j < len(hashmap[hashed]); j++ {
				if hashmap[hashed][j] == label {
					idx = j
					break
				}
			}
			if idx < 0 {
				// failed to find - append
				hashmap[hashed] = append(hashmap[hashed], label)
			}
			focalLengthMap[label] = focalLength
		} else {
			// subtract
			for j := 0; j < len(hashmap[hashed]); j++ {
				if hashmap[hashed][j] == label {
					// shitty implementation w/ possibility of fragmentation
					// . can't be bothered to implement a linked list right now, maybe later
					hashmap[hashed][j] = ""
				}
			}
		}
	}

	// calculate focusing power
	total := 0
TopLoop:
	for key, value := range focalLengthMap {
		// compute hash
		hashed := hash(key)
		// find index in box
		man := 0 // track offsets from my shitty fragmented array implementation
		for i := 0; i < len(hashmap[hashed]); i++ {
			if hashmap[hashed][i] == key {
				subtotal := (hashed + 1) * (i - man + 1) * value
				total += subtotal
				continue TopLoop
			} else if hashmap[hashed][i] == "" {
				man++
			}
		}
	}
	return total
}

func puzzle(fileName string) (int, int) {
	start := time.Now()

	data := strings.Split(strings.TrimSpace(lib.ReadFile(fileName)), ",")
	part1Answer := part1(data)
	part2Answer := part2(data)

	duration := time.Since(start)
	fmt.Println(duration.Seconds())
	return part1Answer, part2Answer
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
