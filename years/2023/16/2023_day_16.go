package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"slices"
	"time"
)

type Set[T Beam | lib.Point] map[T]struct{}

var Void = struct{}{} // consumes 0 memory

func (s Set[T]) Add(item T) {
	s[item] = Void
}

func (s Set[T]) Remove(item T) {
	delete(s, item)
}

func (s Set[T]) Has(item T) bool {
	_, ok := s[item]
	return ok
}

var Deltas = []lib.Point{
	{0, -1}, // north
	{1, 0},  // east
	{0, 1},  // south
	{-1, 0}, // west
}

var Splitters = []rune{'|', '\\', '-', '/'}

type Beam struct {
	point     lib.Point
	direction int
}

func isPointWithinBounds(point lib.Point, width int, height int, widen int) bool {
	return point.X >= 0-widen &&
		point.X < width+widen &&
		point.Y >= 0-widen &&
		point.Y < height+widen
}

func getPointsAlongEdges(width int, height int) []Beam {
	points := make([]Beam, 0, width*2+height*2)
	for i := 0; i < width; i++ {
		points = append(points, Beam{point: lib.Point{X: i, Y: -1}, direction: 2})
		points = append(points, Beam{point: lib.Point{X: i, Y: height}, direction: 0})
	}
	for i := 0; i < height; i++ {
		points = append(points, Beam{point: lib.Point{X: -1, Y: i}, direction: 1})
		points = append(points, Beam{point: lib.Point{X: width, Y: i}, direction: 3})
	}
	return points
}

func getRuneAtPoint(area []string, point lib.Point) rune {
	return rune(area[point.Y][point.X])
}

func simulateBeams(area []string, startPositions []Beam) int {
	width := len(area[0])
	height := len(area)

	cachedSimulatedBeams := make(map[Beam][]Beam)

	simulateBeam := func(beam Beam) []Beam {
		var beams []Beam
		var ok bool

		// reuse cached results if possible
		beams, ok = cachedSimulatedBeams[beam]
		if ok {
			return beams
		}

		beams = []Beam{} // default return value if not in bounds
		// being 1 tile outside the area here is ok because this is where our start positions sit
		if !isPointWithinBounds(beam.point, width, height, 1) {
			return beams
		}
		// traverse in direction of beam until you hit something
		isVertical := (beam.direction % 2) == 0
		delta := Deltas[beam.direction] // move 1 tile to begin with in case we start on a splitter
		newPoint := beam.point.Add(delta)
		passThrough := []rune{'.', Splitters[2*(beam.direction%2)]}
		for isPointWithinBounds(newPoint, width, height, 0) && slices.Contains(passThrough, getRuneAtPoint(area, newPoint)) {
			prospectiveNewPoint := newPoint.Add(delta)
			if isPointWithinBounds(prospectiveNewPoint, width, height, 0) {
				newPoint = prospectiveNewPoint
			} else {
				break
			}
		}
		if isPointWithinBounds(newPoint, width, height, 0) {
			runeAtNewPoint := getRuneAtPoint(area, newPoint)
			clockwise := (beam.direction + 4 + 1) % 4
			counterClockwise := (beam.direction + 4 - 1) % 4
			if slices.Contains(passThrough, runeAtNewPoint) {
				// continue straight. this beam will exit the system when it's processed as it's on the edge of the area
				beams = []Beam{{point: newPoint, direction: beam.direction}}
			} else if (runeAtNewPoint == '/' && isVertical) || (runeAtNewPoint == '\\' && !isVertical) {
				// turn clockwise
				beams = []Beam{{point: newPoint, direction: clockwise}}
			} else if (runeAtNewPoint == '\\' && isVertical) || (runeAtNewPoint == '/' && !isVertical) {
				// turn counter-clockwise
				beams = []Beam{{point: newPoint, direction: counterClockwise}}
			} else {
				// must have hit a splitter. turn clockwise and counter-clockwise
				beams = []Beam{{point: newPoint, direction: clockwise}, {point: newPoint, direction: counterClockwise}}
			}
		}

		// cache
		cachedSimulatedBeams[beam] = beams

		return beams
	}

	maxLength := 0
	for i := 0; i < len(startPositions); i++ {
		startPosition := startPositions[i]
		queue := make(chan Beam, 10000) // idk how big
		queue <- startPosition
		explored := make(Set[Beam])
		energisedPoints := make(Set[lib.Point])

		for len(queue) > 0 {
			beam := <-queue
			resultantBeams := simulateBeam(beam)
			for j := 0; j < len(resultantBeams); j++ {
				resultantBeam := resultantBeams[j]
				if !explored.Has(resultantBeam) {
					queue <- resultantBeam
					explored.Add(resultantBeam)
				}

				// record which points have been seen
				if isPointWithinBounds(beam.point, width, height, 0) {
					energisedPoints.Add(beam.point)
				}
				man := beam
				for man.point != resultantBeams[j].point {
					man.point = man.point.Add(Deltas[man.direction])
					if isPointWithinBounds(man.point, width, height, 0) {
						energisedPoints.Add(man.point)
					}

				}
			}
		}
		if maxLength < len(energisedPoints) {
			maxLength = len(energisedPoints)
		}
	}
	return maxLength
}

func puzzle(fileName string) (int, int) {
	start := time.Now()

	data := lib.ReadFileAsSliceOfType(fileName, lib.ConvertToString)
	part1 := simulateBeams(data, []Beam{Beam{point: lib.Point{X: -1, Y: 0}, direction: 1}})
	part2 := simulateBeams(data, getPointsAlongEdges(len(data[0]), len(data)))

	duration := time.Since(start)
	fmt.Println(duration.Seconds())
	return part1, part2
}

func main() {
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
}
