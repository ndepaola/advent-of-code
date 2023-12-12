package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"time"
)

type Point struct {
	x int
	y int
}

const Galaxy = '#'

func getUniverseExpansionRowsAndCols(universe *[]string) ([]int, []int) {
	rows := make([]int, 0, 10000)
	cols := make([]int, 0, 10000)
	// by-row
	for i := 0; i < len(*universe); i++ {
		noGalaxies := true
		for j := 0; j < len((*universe)[i]); j++ {
			if (*universe)[i][j] == Galaxy {
				noGalaxies = false
				break
			}
		}
		if noGalaxies {
			rows = append(rows, i)
		}
	}
	// by-column
	for j := 0; j < len((*universe)[0]); j++ {
		noGalaxies := true
		for i := 0; i < len(*universe); i++ {
			if (*universe)[i][j] == Galaxy {
				noGalaxies = false
				break
			}
		}
		if noGalaxies {
			cols = append(cols, j)
		}
	}
	return rows, cols
}

func getGalaxies(universe *[]string) []Point {
	galaxies := make([]Point, 0, 10000)
	for i := 0; i < len(*universe); i++ {
		for j := 0; j < len((*universe)[i]); j++ {
			if (*universe)[i][j] == Galaxy {
				point := Point{x: j, y: i}
				galaxies = append(galaxies, point)
			}
		}
	}
	return galaxies
}

func manhattanDistance(a Point, b Point) int {
	xDist := a.x - b.x
	if xDist < 0 {
		xDist *= -1
	}
	yDist := a.y - b.y
	if yDist < 0 {
		yDist *= -1
	}
	return xDist + yDist
}

func computeSumOfLengths(galaxies []Point, rows []int, cols []int, expansionFactor int) int {
	total := 0
	for i := 0; i < len(galaxies); i++ {
		for j := i + 1; j < len(galaxies); j++ {
			dist := manhattanDistance(galaxies[i], galaxies[j])

			// expand the universe. im sure there's a more efficient way of doing this but w/e
			minX := min(galaxies[i].x, galaxies[j].x)
			maxX := max(galaxies[i].x, galaxies[j].x)
			minY := min(galaxies[i].y, galaxies[j].y)
			maxY := max(galaxies[i].y, galaxies[j].y)
			for k := 0; k < len(rows); k++ {
				if rows[k] > minY && rows[k] < maxY {
					dist += expansionFactor - 1
				}
			}
			for k := 0; k < len(cols); k++ {
				if cols[k] > minX && cols[k] < maxX {
					dist += expansionFactor - 1
				}
			}

			total += dist
		}
	}
	return total
}

func puzzle(fileName string) (int, int) {
	universe := lib.ReadFileAsSliceOfType(fileName, lib.ConvertToString)
	rows, cols := getUniverseExpansionRowsAndCols(&universe)
	galaxies := getGalaxies(&universe)
	total1 := computeSumOfLengths(galaxies, rows, cols, 2)
	total2 := computeSumOfLengths(galaxies, rows, cols, 1000000)
	return total1, total2
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
