package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"regexp"
	"strings"
	"time"
)

type Point struct {
	x int
	y int
}

func addPoints(a Point, b Point) Point {
	return Point{x: a.x + b.x, y: a.y + b.y}
}

const NorthSouth rune = '|'
const EastWest rune = '-'
const NorthEast rune = 'L'
const NorthWest rune = 'J'
const SouthEast rune = 'F'
const SouthWest rune = '7'
const Ground rune = '.'
const Start rune = 'S'

var Adjacencies = map[rune][]bool{
	NorthSouth: {true, false, true, false},
	EastWest:   {false, true, false, true},
	NorthEast:  {true, true, false, false},
	NorthWest:  {true, false, false, true},
	SouthEast:  {false, true, true, false},
	SouthWest:  {false, false, true, true},
	Start:      {true, true, true, true},
	Ground:     {false, false, false, false},
}

type Set[T string | int | rune | Point] map[T]struct{}

var Void = struct{}{}

type Man struct {
	delta       Point
	adjacencies Set[rune]
}

var Men = []Man{
	{delta: Point{x: 0, y: -1}, adjacencies: Set[rune]{SouthWest: Void, NorthSouth: Void, SouthEast: Void}},
	{delta: Point{x: 1, y: 0}, adjacencies: Set[rune]{NorthWest: Void, EastWest: Void, SouthWest: Void}},
	{delta: Point{x: 0, y: 1}, adjacencies: Set[rune]{NorthWest: Void, NorthSouth: Void, NorthEast: Void}},
	{delta: Point{x: -1, y: 0}, adjacencies: Set[rune]{SouthEast: Void, EastWest: Void, NorthEast: Void}},
}

func getStart(area *[]string) (Point, rune) {
	for i := 0; i < len(*area); i++ {
		startIndex := strings.IndexRune((*area)[i], Start)
		if startIndex >= 0 {
			point := Point{x: startIndex, y: i}
			// now determine what pipe the S would have been if it wasn't an S
			// this is important for getting regex stuff to work in part 2
			a := 0
			b := 0
			aFound := false
			for j := 0; j < len(Men); j++ {
				prospectivePoint := addPoints(point, Men[j].delta)
				if isPointWithinArea(area, prospectivePoint) {
					prospectivePipe := getPipeFromPoint(area, prospectivePoint)
					_, ok := Men[j].adjacencies[prospectivePipe]
					if ok {
						if !aFound {
							a = j
							aFound = true
						} else {
							b = j
							break

						}
					}
				}
			}
			if !aFound {
				panic("fark")
			}
			// find the pipe where `a` and `b` are both true
			for pipe, adjacencies := range Adjacencies {
				if pipe != Start && adjacencies[a] && adjacencies[b] {
					return point, pipe
				}
			}
			panic("fark2")
		}
	}
	panic("No start point in data!")
}

func isPointWithinArea(area *[]string, point Point) bool {
	return point.y >= -0 && point.y < len(*area) && point.x >= 0 && point.x < len((*area)[0])
}

func getPipeFromPoint(area *[]string, point Point) rune {
	return rune((*area)[point.y][point.x])
}

func printArea(area *[]string, prev map[Point]Point, end Point, tilesInsideLoop Set[Point]) {
	// reconstruct path so we can bold it in the printed drawing
	pointsInPath := make(Set[Point])
	incumbent := end
	for {
		previousPoint, ok := prev[incumbent]
		if !ok {
			break
		}
		pointsInPath[previousPoint] = Void
		incumbent = previousPoint
	}
	// print drawings with box-drawing chars because we're being a bit fancy tonight
	regularBoxCharacters := map[rune]rune{
		NorthSouth: '│',
		EastWest:   '─',
		NorthEast:  '└',
		NorthWest:  '┘',
		SouthWest:  '┐',
		SouthEast:  '┌',
		Start:      'S',
		Ground:     ' ',
	}
	boldBoxCharacters := map[rune]rune{
		NorthSouth: '┃',
		EastWest:   '━',
		NorthEast:  '┗',
		NorthWest:  '┛',
		SouthWest:  '┓',
		SouthEast:  '┏',
		Start:      'S',
		Ground:     ' ',
	}

	for i := 0; i < len(*area); i++ {
		for j := 0; j < len((*area)[i]); j++ {
			manToPrint := ' '
			_, ok1 := prev[Point{x: j, y: i}]
			_, ok2 := pointsInPath[Point{x: j, y: i}]
			_, ok3 := tilesInsideLoop[Point{x: j, y: i}]
			if i == end.y && j == end.x {
				manToPrint = 'E'
			} else if ok2 {
				manToPrint = boldBoxCharacters[rune((*area)[i][j])]
			} else if ok3 {
				manToPrint = 'I'
			} else if ok1 {
				manToPrint = regularBoxCharacters[rune((*area)[i][j])]
			}
			fmt.Print(string(manToPrint))
		}
		fmt.Println("")
	}
	fmt.Println("")
}

func walkPipes(area *[]string) (map[Point]int, map[Point]Point, Point) {
	start, _ := getStart(area)
	frontier := make(chan Point, 10000)
	frontier <- start
	var ok bool
	distances := map[Point]int{start: 0}
	prev := make(map[Point]Point) // track the longest path

	for len(frontier) > 0 {
		point := <-frontier
		pipe := getPipeFromPoint(area, point)
		for i := 0; i < len(Men); i++ {
			if Adjacencies[pipe][i] {
				prospectivePoint := addPoints(point, Men[i].delta)
				if isPointWithinArea(area, prospectivePoint) {
					prospectivePipe := getPipeFromPoint(area, prospectivePoint)
					_, ok = Men[i].adjacencies[prospectivePipe]
					if ok {
						_, ok = distances[prospectivePoint]
						prospectiveDistance := distances[point] + 1
						if (!ok) || distances[prospectivePoint] > prospectiveDistance {
							// record distance
							distances[prospectivePoint] = prospectiveDistance
							// add to frontier to explore its neighbours
							frontier <- prospectivePoint
							prev[prospectivePoint] = point
						}
					}
				}
			}

		}
	}
	// get max distance
	incumbent := start
	for point_, dist := range distances {
		if dist > distances[incumbent] {
			incumbent = point_
		}
	}
	return distances, prev, incumbent
}

func computeTilesInsideLoop(area *[]string, loopTiles map[Point]int) Set[Point] {
	// this is bad and awful and terrible and slow and not good but im just glad it works to be honest
	tilesInsideLoopFromLeft := make(Set[Point])
	start, startPipe := getStart(area)
	myRegex := regexp.MustCompile("L-*7")
	mySecondRegex := regexp.MustCompile("F-*J")
	for i := 0; i < len(*area); i++ {
		lineUpUntilHere := "" // build this up with characters from the outer loop
		for j := 0; j < len((*area)[0]); j++ {
			newChar := ' '
			point := Point{x: j, y: i}
			_, ok := loopTiles[point]
			if point == start {
				newChar = startPipe
			} else if ok {
				newChar = rune((*area)[i][j])
			}
			lineUpUntilHere += string(newChar)

			// count elbows to determine if we are or aren't within the outer loop
			matches := myRegex.FindAllStringSubmatch(lineUpUntilHere, -1)
			matches2 := mySecondRegex.FindAllStringSubmatch(lineUpUntilHere, -1)
			counter := strings.Count(lineUpUntilHere, "|") + len(matches) + len(matches2)
			_, pointIsLoopTile := loopTiles[point]
			if counter%2 == 1 && (!pointIsLoopTile) {
				tilesInsideLoopFromLeft[point] = Void
			}
		}
	}
	return tilesInsideLoopFromLeft
}

func puzzle(fileName string) (int, int) {
	area := lib.ReadFileAsSliceOfType(fileName, lib.ConvertToString)
	distances, prev, incumbent := walkPipes(&area)
	tilesInsideLoop := computeTilesInsideLoop(&area, distances)
	printArea(&area, prev, incumbent, tilesInsideLoop)
	return distances[incumbent], len(tilesInsideLoop)
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("example_2.txt"))
	fmt.Println(puzzle("example_3.txt"))
	fmt.Println(puzzle("example_4.txt"))
	fmt.Println(puzzle("example_5.txt"))
	fmt.Println(puzzle("example_6.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
