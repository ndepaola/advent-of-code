package lib

import (
	"os"
	"path"
	"runtime"
	"strconv"
	"strings"
)

func ReadFile(fileName string) string {
	// identify the location of the puzzle call site
	// bit disgusting but w/e
	var callSiteFileName string
	var ok bool
	i := 0
	for {
		_, callSiteFileName, _, ok = runtime.Caller(i)
		if !ok {
			panic("Could not find file name of caller")
		}
		if strings.Contains(callSiteFileName, "advent-of-code/years") {
			break
		} else {
			i++
		}
	}

	absolutePath := path.Join(path.Dir(callSiteFileName), fileName)
	data, err := os.ReadFile(absolutePath)
	if err != nil {
		panic(err)
	}
	return strings.TrimRight(string(data), "\n")
}

type convert[T any] func(data string) T

func ReadFileAsSliceOfType[T any](fileName string, fn convert[T]) []T {
	split := strings.Split(ReadFile(fileName), "\r\n")
	converted := make([]T, len(split))
	for i := 0; i < len(split); i++ {
		converted[i] = fn(strings.TrimSpace(split[i]))
	}
	return converted
}

func ConvertToString(data string) string {
	return strings.TrimSpace(data)
}

func ConvertToFloat64(data string) float64 {
	parsed, err := strconv.ParseFloat(data, 64)
	if err != nil {
		panic(err)
	}
	return parsed
}

func ConvertToInt(data string) int {
	parsed, err := strconv.Atoi(data)
	if err != nil {
		panic(err)
	}
	return parsed
}

func ConvertToIntSlice(data string) []int {
	split := strings.Split(data, " ")
	man := make([]int, len(split))
	for i := 0; i < len(man); i++ {
		parsed, err := strconv.Atoi(split[i])
		if err != nil {
			panic(err)
		}
		man[i] = parsed
	}
	return man
}

type Point struct {
	X int
	Y int
}

func (p Point) Add(other Point) Point {
	return Point{X: p.X + other.X, Y: p.Y + other.Y}
}

type Set[T string | int | rune | Point] map[T]struct{}

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
