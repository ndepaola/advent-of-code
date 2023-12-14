package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"time"
)

const Square rune = '#'
const Circle rune = 'O'

func parseRocks(fileName string) (lib.Set[lib.Point], lib.Set[lib.Point], int, int) {
	circles := make(lib.Set[lib.Point])
	squares := make(lib.Set[lib.Point])
	data := lib.ReadFileAsSliceOfType(fileName, lib.ConvertToString)
	width := len(data[0])
	height := len(data)
	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {
			switch rune(data[i][j]) {
			case Square:
				squares.Add(lib.Point{X: j, Y: i})
			case Circle:
				circles.Add(lib.Point{X: j, Y: i})
			}
		}
	}
	return circles, squares, width, height
}

var Deltas = []lib.Point{
	{0, -1},
	{-1, 0},
	{0, 1},
	{1, 0},
}

func moveCircles(circles lib.Set[lib.Point], squares lib.Set[lib.Point], width int, height int, direction int) {
	if direction < 0 || direction > 3 {
		panic("invalid direction")
	}
TopLoop:
	for {
		for circle, _ := range circles {
			movedCircle := circle.Add(Deltas[direction])
			circlePositionWithinBounds := movedCircle.X >= 0 &&
				movedCircle.X < width &&
				movedCircle.Y >= 0 &&
				movedCircle.Y < height
			circlePositionOccupied := circles.Has(movedCircle) || squares.Has(movedCircle)
			if circlePositionWithinBounds && !circlePositionOccupied {
				circles.Add(movedCircle)
				circles.Remove(circle)
				continue TopLoop
			}
		}
		break
	}
}

func isPointWithinBounds(point lib.Point, width int, height int) bool {
	return point.X >= 0 &&
		point.X < width &&
		point.Y >= 0 &&
		point.Y < height
}

func calculateLoad(circles lib.Set[lib.Point], height int) int {
	total := 0
	for circle, _ := range circles {
		total += height - circle.Y
	}
	return total
}

func hashPoint(point lib.Point, height int) int {
	return point.X + height*point.Y
}

func hashPoints(points lib.Set[lib.Point], height int) int {
	total := 0
	for point, _ := range points {
		total += hashPoint(point, height)
	}
	return total
}

func part1(circles lib.Set[lib.Point], squares lib.Set[lib.Point], width int, height int) int {
	mutatedCircles := make(lib.Set[lib.Point])
	for circle, _ := range circles {
		mutatedCircles.Add(circle)
	}
	moveCircles(mutatedCircles, squares, width, height, 0)
	return calculateLoad(mutatedCircles, height)
}

func part2(circles lib.Set[lib.Point], squares lib.Set[lib.Point], width int, height int, iterations int) int {
	mutatedCircles := make(lib.Set[lib.Point])
	for circle, _ := range circles {
		mutatedCircles.Add(circle)
	}
	answers := make([]int, 1000) // some upper limit on how big we think cycles might be
	iteration := 0
	jumped := false
TopLoop:
	for iteration < iterations {
		// simulate circle movements
		for direction := 0; direction < len(Deltas); direction++ {
			moveCircles(mutatedCircles, squares, width, height, direction)
		}
		hash := hashPoints(mutatedCircles, height)

		// attempt to skip cycles
		if !jumped {
			for i := iteration - 1; i >= 0; i-- {
				// a cycle has been detected - jump to the end to avoid repeating this cycle many times
				if answers[i] == hash {
					cycleLength := iteration - i
					jumped = true
					iterationsToJump := ((iterations-iteration)/cycleLength)*cycleLength + 1
					iteration += iterationsToJump
					continue TopLoop
				}
			}
		}

		if !jumped {
			answers[iteration] = hash
		}
		iteration++
	}
	return calculateLoad(mutatedCircles, height)
}

func puzzle(fileName string) (int, int) {
	start := time.Now()

	circles, squares, width, height := parseRocks(fileName)
	part1Answer := part1(circles, squares, width, height)
	part2Answer := part2(circles, squares, width, height, 1000000000)

	duration := time.Since(start)
	fmt.Println(duration.Seconds())
	return part1Answer, part2Answer
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
