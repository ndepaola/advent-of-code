package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"slices"
	"strconv"
	"strings"
	"time"
)

// constants
const cardsWithoutJoker = "AKQJT98765432" // earlier in these strings indicates a higher score
const cardsWithJoker = "AKQT98765432J"    // note that jack is removed from the deck! i wasted a bunch of time on this :(
const Joker = 'J'

// types
type Hand struct {
	cards      string
	cardCounts CardCounts
	kind       int
	bid        int
}
type isHandKind func(cardCounts *CardCounts, countJokers bool) bool // one small step for hand, one giant leap for handkind
type CardCounts map[rune]int

func (c CardCounts) getJoker(countJokers bool) int {
	if !countJokers {
		return 0
	}
	return c[Joker]
}

// hand kind checks
func isFiveOfAKind(cardCounts *CardCounts, countJokers bool) bool {
	for card, count := range *cardCounts {
		if ((countJokers && card != Joker) || !countJokers) && count == (5-cardCounts.getJoker(countJokers)) {
			return true
		}
	}
	return false
}
func isFourOfAKind(cardCounts *CardCounts, countJokers bool) bool {
	for card, count := range *cardCounts {
		if ((countJokers && card != Joker) || !countJokers) && count == 4-cardCounts.getJoker(countJokers) {
			return true
		}
	}
	return false
}
func isFullHouse(cardCounts *CardCounts, countJokers bool) bool {
	twoFound := false
	threeFound := false
	jokersConsumed := 0
	for card, count := range *cardCounts {
		if !twoFound && ((countJokers && card != Joker) || !countJokers) && count == 2-(cardCounts.getJoker(countJokers)-jokersConsumed) {
			twoFound = true
			jokersConsumed += cardCounts.getJoker(countJokers)
		} else if !threeFound && ((countJokers && card != Joker) || !countJokers) && count == 3-(cardCounts.getJoker(countJokers)-jokersConsumed) {
			threeFound = true
			jokersConsumed += cardCounts.getJoker(countJokers)
		}
		if twoFound && threeFound {
			return true
		}
	}
	return false
}
func isThreeOfAKind(cardCounts *CardCounts, countJokers bool) bool {
	for card, count := range *cardCounts {
		if ((countJokers && card != Joker) || !countJokers) && count == 3-cardCounts.getJoker(countJokers) {
			return true
		}
	}
	return false
}
func isTwoPair(cardCounts *CardCounts, countJokers bool) bool {
	anotherPairFound := false
	jokersConsumed := 0
	for card, count := range *cardCounts {
		if ((countJokers && card != Joker) || !countJokers) && count == 2-(cardCounts.getJoker(countJokers)-jokersConsumed) {
			if anotherPairFound {
				return true
			}
			anotherPairFound = true
			jokersConsumed += cardCounts.getJoker(countJokers)
		}
	}
	return false
}
func isOnePair(cardCounts *CardCounts, countJokers bool) bool {
	for _, count := range *cardCounts {
		if count == 2-cardCounts.getJoker(countJokers) {
			return true
		}
	}
	return false
}

// these must be checked in this order. earlier in the array indicates a better hand.
var handKindCheckers = [...]isHandKind{isFiveOfAKind, isFourOfAKind, isFullHouse, isThreeOfAKind, isTwoPair, isOnePair}

func determineHandKind(cardCounts *CardCounts, countJokers bool) int {
	for i := 0; i < len(handKindCheckers); i++ {
		if handKindCheckers[i](cardCounts, countJokers) {
			return i
		}
	}
	return len(handKindCheckers) // default to high card
}

func countCards(hand string) CardCounts {
	// with / without joker doesn't matter here
	cardCounts := make(CardCounts)
	for i := 0; i < len(cardsWithoutJoker); i++ {
		cardCounts[rune(cardsWithoutJoker[i])] = strings.Count(hand, string(cardsWithoutJoker[i]))
	}
	return cardCounts
}

func parseHand(line string, includeJokers bool) Hand {
	splitLine := strings.Split(line, " ")
	hand := splitLine[0]
	bid, err := strconv.Atoi(splitLine[1])
	if err != nil {
		panic(err)
	}
	cardCounts := countCards(hand)
	kind := determineHandKind(&cardCounts, includeJokers)
	return Hand{cards: hand, cardCounts: cardCounts, kind: kind, bid: bid}
}

func parseHandWithoutJokers(line string) Hand {
	return parseHand(line, false)
}
func parseHandWithJokers(line string) Hand {
	return parseHand(line, true)
}

func compareHands(a Hand, b Hand, cards string) int {
	// cmp(a, b) should return a negative number when a < b, a positive number when a > b and zero when a == b.
	if a.kind > b.kind {
		return -1 // `a` is worse than `b`
	}
	if b.kind > a.kind {
		return 1 // `b` is worse than `a`
	}
	// tiebreak by checking card values
	for i := 0; i < len(a.cards); i++ {
		scoreA := strings.IndexRune(cards, rune(a.cards[i]))
		scoreB := strings.IndexRune(cards, rune(b.cards[i]))
		if scoreA > scoreB {
			return -1 // `a` is worse than `b`
		}
		if scoreB > scoreA {
			return 1 // `b` is worse than `a`
		}
	}
	return 0
}

func compareHandsWithoutJokers(a Hand, b Hand) int {
	return compareHands(a, b, cardsWithoutJoker)
}

func compareHandsWithJokers(a Hand, b Hand) int {
	return compareHands(a, b, cardsWithJoker)
}

func puzzle(fileName string) (int, int) {
	// part 1
	handsWithoutJokers := lib.ReadFileAsSliceOfType(fileName, parseHandWithoutJokers)
	slices.SortFunc(handsWithoutJokers, compareHandsWithoutJokers)
	totalWithoutJokers := 0
	for i := 0; i < len(handsWithoutJokers); i++ {
		totalWithoutJokers += (i + 1) * handsWithoutJokers[i].bid
	}

	// part 2
	handsWithJokers := lib.ReadFileAsSliceOfType(fileName, parseHandWithJokers)
	slices.SortFunc(handsWithJokers, compareHandsWithJokers)
	totalWithJokers := 0
	for i := 0; i < len(handsWithJokers); i++ {
		totalWithJokers += (i + 1) * handsWithJokers[i].bid
	}

	return totalWithoutJokers, totalWithJokers
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
