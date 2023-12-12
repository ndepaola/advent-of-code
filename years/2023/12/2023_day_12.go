package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"strconv"
	"strings"
	"time"
)

type Spring struct {
	line             string
	outages          []int
	outagesRemaining []int
}

func parseSprings(line string, unfoldBy int) Spring {
	split := strings.Split(line, " ")
	man := strings.Repeat(split[0]+"?", unfoldBy)
	man = man[:len(man)-1]
	sizeStrings := strings.Split(split[1], ",")
	outages := make([]int, len(sizeStrings)*unfoldBy)
	totalOutages := 0
	for i := 0; i < len(sizeStrings)*unfoldBy; i++ {
		value, err := strconv.Atoi(sizeStrings[i%len(sizeStrings)])
		if err != nil {
			panic(err)
		}
		outages[i] = value
		totalOutages += value
	}
	outagesRemaining := make([]int, len(outages))
	totalRemaining := totalOutages
	for i := 0; i < len(outages); i++ {
		totalRemaining -= outages[i]
		outagesRemaining[i] = totalRemaining
	}

	return Spring{line: man, outages: outages, outagesRemaining: outagesRemaining}
}

type Key struct {
	outageIndex   int
	startIndex    int
	lastHashIndex int
}

func unfoldAndCountArrangement(spring Spring) int {
	cachedArrangementCounts := make(map[Key]int)

	var computeArrangements func(line string, outageIndex int, startIndex int, lastHashIndex int) int
	computeArrangements = func(line string, outageIndex int, startIndex int, lastHashIndex int) int {
		// `startIndex`, `outageIndex`, and `lastHashIndex` are mutated below.
		// here, we create copies of their initial values and use these values when caching the result at the end.
		startIndexOld := startIndex
		outageIndexOld := outageIndex
		lastHashIndexOld := lastHashIndex

		outages := spring.outages
		count := 0
	TopLoop:
		for outageIndex < len(outages) {
			value, ok := cachedArrangementCounts[Key{outageIndex: outageIndex, startIndex: startIndex, lastHashIndex: lastHashIndex}]
			if ok {
				return value
			}
			// return 0 if you cannot possibly fit the number of outages required from here on out
			// (break to ensure we hit the caching code at the bottom of the function)
			candidateCount := strings.Count(line[startIndex:], "#") + strings.Count(line[startIndex:], "?")
			if candidateCount < spring.outagesRemaining[outageIndex] {
				break
			}

			// step through one character at a time
			for i := startIndex; i < len(line); i++ {
				outageSize := outages[outageIndex]
				// attempt to fit the outage at `outageIndex` here
				if len(line)-i >= outageSize && // if the outage fits here
					!((i > 0 && line[i-1] == '#') || // if a # precedes our space of interest
						(i+outageSize < len(line) && line[i+outageSize] == '#') || // if a # succeeds our space of interest
						strings.IndexRune(line[i:i+outageSize], '.') >= 0 || // if any .'s are in our space of interest
						(strings.Count(line[lastHashIndex+1:i], "#") > 0) || // if we skipped over any #'s while trying to emplace
						(lastHashIndex >= 0 && i == lastHashIndex+1)) { // if we overlap with an outage we fit earlier
					// great, this outage fits! recursively check what happens if we don't put the outage in this spot
					if line[i] == '?' {
						count += computeArrangements(line, outageIndex, i+1, lastHashIndex)
					}

					// put the outage in this spot and continue checking the next outage/s
					outageIndex++
					startIndex = i + outageSize
					lastHashIndex = i + outageSize - 1
					if outageIndex >= len(outages) {
						break TopLoop
					} else {
						continue TopLoop
					}
				}
			}
			break
		}
		// check that all outages have been fitted and the correct number of hashes are in the resultant line
		if outageIndex >= len(outages) && (lastHashIndex == len(line)-1 || strings.Count(line[lastHashIndex+1:], "#") == 0) {
			count++
		}
		// cache `count` so it can be reused later
		cachedArrangementCounts[Key{outageIndex: outageIndexOld, startIndex: startIndexOld, lastHashIndex: lastHashIndexOld}] = count
		return count
	}
	return computeArrangements(spring.line, 0, 0, -1)
}

func unfoldAndCountArrangements(fileName string, unfoldBy int) int {
	parse := func(line string) Spring { return parseSprings(line, unfoldBy) }
	springs := lib.ReadFileAsSliceOfType(fileName, parse)
	total := 0
	for i := 0; i < len(springs); i++ {
		total += unfoldAndCountArrangement(springs[i])
	}
	return total
}

func puzzle(fileName string) (int, int) {
	start := time.Now()
	part1 := unfoldAndCountArrangements(fileName, 1)
	part2 := unfoldAndCountArrangements(fileName, 5)
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
	return part1, part2
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
