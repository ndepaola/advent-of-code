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
