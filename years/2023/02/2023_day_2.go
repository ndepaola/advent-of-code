package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"regexp"
	"strconv"
	"strings"
)

type GameCubes map[string]int

type Game struct {
	id    int
	games []GameCubes
}

func lineToGame(line string) Game {
	re1 := regexp.MustCompile("Game (\\d{1,3}): (.+)")
	firstMatches := re1.FindAllStringSubmatch(line, -1)
	gameId, _ := strconv.Atoi(firstMatches[0][1])

	split := strings.Split(firstMatches[0][2], ";")
	games := make([]GameCubes, len(split))
	re2 := regexp.MustCompile("(?:(\\d{1,3}) (red|blue|green))+")
	for i := 0; i < len(games); i++ {
		secondMatches := re2.FindAllStringSubmatch(split[i], -1)
		cubes := make(GameCubes)
		for j := 0; j < len(secondMatches); j++ {
			marbleCount, _ := strconv.Atoi(secondMatches[j][1])
			cubes[secondMatches[j][2]] = marbleCount
		}
		games[i] = cubes
	}

	return Game{
		gameId,
		games,
	}
}

func isGamePossible(game Game, bag GameCubes) bool {
	for i := 0; i < len(game.games); i++ {
		for colour, marbleCount := range game.games[i] {
			if marbleCount > bag[colour] {
				return false
			}
		}
	}

	return true
}

func calculateGamePower(game Game) int {
	minCubes := GameCubes{"red": 0, "green": 0, "blue": 0}
	for i := 0; i < len(game.games); i++ {
		for colour, marbleCount := range game.games[i] {
			if marbleCount > minCubes[colour] {
				minCubes[colour] = marbleCount
			}
		}
	}
	product := 1
	for _, marbleCount := range minCubes {
		product *= marbleCount
	}
	return product
}

func puzzle(fileName string) (int, int) {
	bag := GameCubes{"red": 12, "green": 13, "blue": 14}
	data := strings.Split(lib.ReadFile(fileName), "\n")
	idTotal := 0
	powerTotal := 0
	for i := 0; i < len(data); i++ {
		game := lineToGame(data[i])
		if isGamePossible(game, bag) {
			idTotal += game.id
		}
		powerTotal += calculateGamePower(game)
	}
	return idTotal, powerTotal
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
