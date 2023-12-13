package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"strings"
	"time"
)

type Pattern []string

func transposePattern(pattern Pattern) Pattern {
	// initialise
	transposedPattern := make(Pattern, len(pattern[0]))
	for i := 0; i < len(transposedPattern); i++ {
		transposedPattern[i] = strings.Repeat(".", len(pattern))
	}
	// fill in contents
	for i := 0; i < len(pattern); i++ {
		for j := 0; j < len(pattern[0]); j++ {
			transposedPattern[j] = transposedPattern[j][0:i] + string(pattern[i][j]) + transposedPattern[j][min(i+1, len(transposedPattern[j])):]
		}
	}
	return transposedPattern
}

func countHorizontalReflections(pattern Pattern, doNotMatch int) int {
	for i := 1; i < len(pattern); i++ {
		if i == doNotMatch {
			continue
		}
		rowA := i - 1
		rowB := i
		matched := true
		for matched {
			matched = matched && pattern[rowA] == pattern[rowB]
			if matched && (rowA == 0 || rowB == len(pattern)-1) {
				return i
			}
			rowA -= 1
			rowB += 1
		}
	}
	return 0 // no match found
}

func countReflections(pattern Pattern, transposedPattern Pattern) int {
	v := 100 * countHorizontalReflections(pattern, 0)
	if v > 0 {
		return v
	}
	return countHorizontalReflections(transposedPattern, 0)
}

func countUnsmudgedReflections(pattern Pattern) int {
	transposedPattern := transposePattern(pattern)
	return countReflections(pattern, transposedPattern)
}

func countSmudgedReflections(pattern Pattern) int {
	transposedPattern := transposePattern(pattern)
	unsmudgedHorizontalLine := countHorizontalReflections(pattern, 0)
	unsmudgedVerticalLine := countHorizontalReflections(transposedPattern, 0)

	mutatedPattern := make(Pattern, len(pattern))
	copy(mutatedPattern, pattern)
	men := map[uint8]uint8{'#': '.', '.': '#'}
	for i := 0; i < len(pattern); i++ {
		for j := 0; j < len(pattern[0]); j++ {
			mutatedPattern[i] = pattern[i][0:j] + string(men[uint8(pattern[i][j])]) + pattern[i][j+1:]
			transposedMutatedPattern := transposePattern(mutatedPattern)

			smudgedHorizontalLine := countHorizontalReflections(mutatedPattern, unsmudgedHorizontalLine)
			if smudgedHorizontalLine > 0 {
				return 100 * smudgedHorizontalLine
			}
			smudgedVerticalLine := countHorizontalReflections(transposedMutatedPattern, unsmudgedVerticalLine)
			if smudgedVerticalLine > 0 {
				return smudgedVerticalLine
			}
			mutatedPattern[i] = pattern[i]
		}
	}
	panic("fuck") // no smudged variant was found - this indicates a bug somewhere
}

func parsePatterns(fileName string) []Pattern {
	data := strings.Split(lib.ReadFile(fileName), "\r\n\r\n")
	patterns := make([]Pattern, len(data))
	for i := 0; i < len(patterns); i++ {
		patterns[i] = strings.Split(strings.TrimSpace(data[i]), "\r\n")
	}
	return patterns
}

func puzzle(fileName string) (int, int) {
	start := time.Now()
	patterns := parsePatterns(fileName)
	total1 := 0
	total2 := 0
	var subtotal int
	for i := 0; i < len(patterns); i++ {
		subtotal = countUnsmudgedReflections(patterns[i])
		total1 += subtotal
		subtotal = countSmudgedReflections(patterns[i])
		total2 += subtotal
	}
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
	return total1, total2
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
