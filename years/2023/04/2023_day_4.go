package main

import (
	"fmt"
	"math"
	"ndepaola/advent-of-code/lib"
	"regexp"
	"strconv"
	"strings"
)

type Set map[int]struct{}

type Card struct {
	id      int
	overlap int
}

type Cards map[int]Card // keyed by id

func calculateCardOverlap(ownedNumbers Set, winningNumbers Set) int {
	overlap := make(Set)
	for key, _ := range ownedNumbers {
		_, ok := winningNumbers[key]
		if ok {
			overlap[key] = struct{}{}
		}
	}
	return len(overlap)
}

func parseLine(line string) Card {
	reWhitespace := regexp.MustCompile("\\s\\s+")
	fixedLine := reWhitespace.ReplaceAllString(line, " ")
	re := regexp.MustCompile("^Card (\\d+):([\\d\\s]+)|([\\d\\s]+)$")
	matches := re.FindAllStringSubmatch(fixedLine, -1)

	var err error
	var cardId, value int
	cardId, err = strconv.Atoi(matches[0][1])
	if err != nil {
		panic(err)
	}
	winningNumberStrings := strings.Split(strings.TrimSpace(matches[0][2]), " ")
	winningNumbers := make(Set)
	for i := 0; i < len(winningNumberStrings); i++ {
		value, err = strconv.Atoi(winningNumberStrings[i])
		if err != nil {
			panic(err)
		}
		winningNumbers[value] = struct{}{}
	}
	ownedNumberStrings := strings.Split(strings.TrimSpace(matches[1][0]), " ")
	ownedNumbers := make(Set)
	for i := 0; i < len(ownedNumberStrings); i++ {
		value, err = strconv.Atoi(ownedNumberStrings[i])
		if err != nil {
			panic(err)
		}
		ownedNumbers[value] = struct{}{}
	}
	overlap := calculateCardOverlap(ownedNumbers, winningNumbers)
	return Card{id: cardId, overlap: overlap}
}

func calculateCardValue(card Card) int {
	return int(math.Pow(float64(2), float64(card.overlap-1)))
}

func calculateTotalCards(cards Cards) int {
	total := len(cards)

	cardIdQueue := make([]int, 100000)

	tailIndex := 0
	for _, card := range cards {
		// initialise with all known cards
		cardIdQueue[tailIndex] = card.id
		tailIndex += 1
	}
	for {
		// until the queue is empty: pop a card off the queue then add all cards it produces onto the queue
		tailIndex -= 1
		if tailIndex == -1 {
			break
		}
		card := cards[cardIdQueue[tailIndex]]
		cardIdQueue[tailIndex] = 0
		for newCardId := card.id + 1; newCardId <= card.id+card.overlap; newCardId++ {
			_, ok := cards[newCardId]
			if ok {
				cardIdQueue[tailIndex] = newCardId
				tailIndex += 1
				total += 1
			}
		}
	}
	return total
}

func puzzle(fileName string) (int, int) {
	cardsSlice := lib.ReadFileAsSliceOfType(fileName, parseLine)
	cards := make(Cards)

	pointsTotal := 0
	for i := 0; i < len(cardsSlice); i++ {
		card := cardsSlice[i]
		pointsTotal += calculateCardValue(card)
		cards[card.id] = card
	}
	totalCards := calculateTotalCards(cards)

	return pointsTotal, totalCards
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
