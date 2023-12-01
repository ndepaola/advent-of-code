package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"strconv"
	"strings"
)

func puzzle(fileName string, wordsCountAsNumbers bool) int {
	data := strings.Split(lib.ReadFile(fileName), "\n")
	sum := 0
	numberWords := []string{
		"one",
		"two",
		"three",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
	}
	for i := 0; i < len(data); i++ {
		line := data[i]

		if wordsCountAsNumbers {
			for j := 0; j < len(numberWords); j++ {
				word := numberWords[j]
				// insert the digit after the 1st character of the word in case multiple words overlap
				line = strings.Replace(line, word, word[0:1]+fmt.Sprint(j+1)+word[1:len(word)], -1)
			}
		}

		firstNumber := 0
		lastNumber := 0
		foundFirstNumber := false
		for j := 0; j < len(line); j++ {
			value, err := strconv.Atoi(string(line[j]))
			if err == nil {
				if !foundFirstNumber {
					foundFirstNumber = true
					firstNumber = value
				}
				lastNumber = value
			}
		}
		sum += 10*firstNumber + lastNumber
	}
	return sum
}

func main() {
	fmt.Println(puzzle("example_2.txt", true))
}
