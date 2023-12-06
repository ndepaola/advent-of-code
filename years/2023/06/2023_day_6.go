package main

import (
	"fmt"
	"math"
	"ndepaola/advent-of-code/lib"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func parseData(fileName string) (string, string) {
	reWhitespace := regexp.MustCompile("\\s\\s+")
	splitData := strings.Split(lib.ReadFile(fileName), "\r")
	raceTimeString := strings.Split(reWhitespace.ReplaceAllString(splitData[0], " "), "Time: ")[1]
	raceDistanceString := strings.Split(reWhitespace.ReplaceAllString(splitData[1], " "), "Distance: ")[1]
	return raceTimeString, raceDistanceString
}

func computeRoots(raceDuration int, benchmark int) (int, int) { // basic quadratic equation implementation
	a := -1
	b := -1 * raceDuration
	c := -1 * benchmark
	lowerBound := -1 * (float64(-1*b) - math.Sqrt(float64(b*b-(4*a*c)))) / float64(2*a)
	upperBound := -1 * (float64(-1*b) + math.Sqrt(float64(b*b-(4*a*c)))) / float64(2*a)
	roundedLowerBound := int(math.Floor(lowerBound))
	roundedUpperBound := int(math.Floor(upperBound - 0.00001)) // bad awfulness to catch non-inclusivity with integers
	return roundedLowerBound, roundedUpperBound
}

func computeRacePossibilities(raceTimeStrings []string, raceDistanceStrings []string) int {
	product := 1.0
	for i := 0; i < len(raceTimeStrings); i++ {
		var raceTime, raceDistance int
		var err error
		raceTime, err = strconv.Atoi(raceTimeStrings[i])
		if err != nil {
			panic(err)
		}
		raceDistance, err = strconv.Atoi(raceDistanceStrings[i])
		if err != nil {
			panic(err)
		}
		root1, root2 := computeRoots(raceTime, raceDistance)
		product *= math.Abs(float64(root2 - root1))
	}
	return int(product)
}

func puzzle(fileName string) (int, int) {
	raceTimeString, raceDistanceString := parseData(fileName)

	// part 1
	raceTimeStrings := strings.Split(raceTimeString, " ")
	raceDistanceStrings := strings.Split(raceDistanceString, " ")
	waysToBeatAllRaces := computeRacePossibilities(raceTimeStrings, raceDistanceStrings)

	// part 2
	raceTimeSingletonStrings := []string{strings.Replace(raceTimeString, " ", "", -1)}
	raceDistanceSingletonStrings := []string{strings.Replace(raceDistanceString, " ", "", -1)}
	waysToBeatSingleRace := computeRacePossibilities(raceTimeSingletonStrings, raceDistanceSingletonStrings)

	return waysToBeatAllRaces, waysToBeatSingleRace
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
