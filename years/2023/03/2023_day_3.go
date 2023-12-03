package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"regexp"
	"strconv"
	"strings"
)

const ASTERISK byte = '*'
const PERIOD byte = '.'

type Schematic []string

type Number struct {
	value  int
	xStart int
	xEnd   int
	y      int
}

func isCharacterSymbol(character byte) bool {
	return (character > 57 || character < 48) && character != PERIOD
}

func isNumberPart(schematic Schematic, number Number) bool {
	for i := max(number.xStart-1, 0); i < min(number.xEnd+1, len(schematic[0])); i++ {
		for j := max(number.y-1, 0); j < min(number.y+2, len(schematic)); j++ {
			if (j != number.y || i >= number.xStart || i <= number.xEnd) && isCharacterSymbol(schematic[j][i]) {
				return true
			}
		}
	}
	return false
}

func extractPartNumbers(schematic Schematic) []Number {
	partNumbers := make([]Number, 10000) // some large upper bound
	numberIndex := 0
	re := regexp.MustCompile("(\\d{1,100})") // some large upper bound on number length
	for i := 0; i < len(schematic); i++ {
		line := schematic[i]
		matches := re.FindAllStringIndex(line, -1)
		for j := 0; j < len(matches); j++ {
			match := matches[j]
			value, err := strconv.Atoi(line[match[0]:match[1]])
			if err != nil {
				panic(err)
			}
			number := Number{
				value:  value,
				xStart: match[0],
				xEnd:   match[1],
				y:      i,
			}
			if isNumberPart(schematic, number) {
				partNumbers[numberIndex] = number
				numberIndex += 1
			}
		}
	}
	return partNumbers[0:numberIndex]
}

func calculateSchematicSum(partNumbers []Number) int {
	total := 0
	for i := 0; i < len(partNumbers); i++ {
		total += partNumbers[i].value
	}
	return total
}

func calculateGearRatioSum(partNumbers []Number, schematic Schematic) int {
	total := 0
	for i := 0; i < len(schematic); i++ {
		line := schematic[i]
		marker := 0
	Loop:
		for {
			if marker >= len(line) {
				break
			}
			asteriskIndex := strings.Index(line[marker:], string(ASTERISK))
			if asteriskIndex < 0 {
				break
			}
			asteriskIndex += marker
			marker = asteriskIndex + 1

			adjacentPartNumbers := 0
			product := 1
			for j := 0; j < len(partNumbers); j++ {
				partNumber := partNumbers[j]
				if adjacentPartNumbers > 2 {
					continue Loop
				}
				if asteriskIndex >= partNumber.xStart-1 && asteriskIndex < partNumber.xEnd+1 && i >= partNumber.y-1 && i <= partNumber.y+1 {
					adjacentPartNumbers += 1
					product *= partNumber.value
				}
			}
			if adjacentPartNumbers == 2 {
				total += product
				continue Loop
			}
		}
	}
	return total
}

func puzzle(fileName string) (int, int) {
	schematic := strings.Split(lib.ReadFile(fileName), "\r\n")
	partNumbers := extractPartNumbers(schematic)
	schematicSum := calculateSchematicSum(partNumbers)
	gearRatioSum := calculateGearRatioSum(partNumbers, schematic)
	return schematicSum, gearRatioSum
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
