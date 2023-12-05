package main

import (
	"fmt"
	"ndepaola/advent-of-code/lib"
	"strconv"
	"strings"
	"time"
)

type Set map[int]struct{}

type Range struct {
	start  int
	length int
}

func (r *Range) withinRange(number int) bool {
	return number >= r.start && number < r.start+r.length
}

type PipelineRange struct {
	sourceRange Range
	targetRange Range
}

type Pipeline []PipelineRange

func parsePipelines(data string) []Pipeline {
	pipelineStrings := strings.Split(data, "\r\n\r\n")
	pipelines := make([]Pipeline, len(pipelineStrings))
	for i := 0; i < len(pipelines); i++ {
		pipelineRangesStrings := strings.Split(strings.Trim(pipelineStrings[i], "\r\n"), "\r\n")
		pipelineRanges := make(Pipeline, len(pipelineRangesStrings)-1)
		for j := 0; j < len(pipelineRangesStrings)-1; j++ { // skip the first line
			numberStrings := strings.Split(pipelineRangesStrings[j+1], " ")
			var err error
			var targetRange, sourceRange, rangeLength int
			targetRange, err = strconv.Atoi(numberStrings[0])
			if err != nil {
				panic(err)
			}
			sourceRange, err = strconv.Atoi(numberStrings[1])
			if err != nil {
				panic(err)
			}
			rangeLength, err = strconv.Atoi(numberStrings[2])
			if err != nil {
				panic(err)
			}
			pipelineRanges[j] = PipelineRange{sourceRange: Range{start: sourceRange, length: rangeLength}, targetRange: Range{start: targetRange, length: rangeLength}}
		}
		pipelines[i] = pipelineRanges
	}
	return pipelines
}

func parseSeedsNaively(data string) []Range { // part 1 - each number is a seed
	seedStrings := strings.Split(data[7:], " ") // chop off `seeds: `
	seeds := make([]Range, len(seedStrings))
	for i := 0; i < len(seeds); i++ {
		value, err := strconv.Atoi(seedStrings[i])
		if err != nil {
			panic(err)
		}
		seeds[i] = Range{start: value, length: 1}
	}
	return seeds
}

func parseSeedsProperly(data string) []Range { // part 2 - each pair of numbers represents a range
	seedStrings := strings.Split(data[7:], " ") // chop off `seeds: `
	seeds := make([]Range, len(seedStrings)/2)
	for i := 0; i < len(seeds); i++ {
		var err error
		var start, length int
		start, err = strconv.Atoi(seedStrings[2*i])
		if err != nil {
			panic(err)
		}
		length, err = strconv.Atoi(seedStrings[2*i+1])
		if err != nil {
			panic(err)
		}
		seeds[i] = Range{start: start, length: length}
	}
	return seeds
}

func applyPipelines(number int, pipelines []Pipeline) int {
	// note: this assumes the pipelines are ordered in the input data (i.e. the material type labels don't matter)
	convertedNumber := number
	for i := 0; i < len(pipelines); i++ {
		pipeline := pipelines[i]
		for j := 0; j < len(pipeline); j++ {
			if pipeline[j].sourceRange.withinRange(convertedNumber) {
				convertedNumber = convertedNumber - pipeline[j].sourceRange.start + pipeline[j].targetRange.start
				break
			}
		}

	}
	return convertedNumber
}

func unapplyPipelines(number int, pipelines []Pipeline) int {
	convertedNumber := number
	for i := len(pipelines) - 1; i >= 0; i-- {
		pipeline := pipelines[i]
		for j := 0; j < len(pipeline); j++ { // don't worry about iterating in reverse - assume ranges do not overlap
			if pipeline[j].targetRange.withinRange(convertedNumber) {
				convertedNumber = convertedNumber - pipeline[j].targetRange.start + pipeline[j].sourceRange.start
				break
			}
		}
	}
	return convertedNumber
}

func getMinimalSeeds(seeds []Range, pipelines []Pipeline) Set {
	// here, we compute the set of possible input seeds based on the bounds of each pipeline
	// the assumption here is that any seed between these inputs cannot be more optimal than one
	// of these inputs
	minimalSeeds := make(Set)
	for i := 0; i < len(pipelines); i++ {
		pipeline := pipelines[i]
		for j := 0; j < len(pipeline); j++ {
			// back-calculate the starting seed for the upper and lower bounds of the pipeline
			sourceStart := unapplyPipelines(pipeline[j].sourceRange.start, pipelines[:i])
			minimalSeeds[sourceStart] = struct{}{}
			targetStart := unapplyPipelines(pipeline[j].targetRange.start, pipelines[:i])
			minimalSeeds[targetStart] = struct{}{}
		}
	}
	for i := 0; i < len(seeds); i++ {
		// the upper and lower bounds of each seed are valid seeds too of course!
		minimalSeeds[seeds[i].start] = struct{}{}
		minimalSeeds[seeds[i].start+seeds[i].length] = struct{}{}
	}
	return minimalSeeds
}

func findLowestLocationNumber(seeds []Range, pipelines []Pipeline) int {
	minimalSeeds := getMinimalSeeds(seeds, pipelines)
	lowestNumber := applyPipelines(seeds[0].start, pipelines) // just initialising with some valid non-zero number
	for seedCandidate, _ := range minimalSeeds {
		// only check seed candidates which fit within the ranges of the specified seeds
		for i := 0; i < len(seeds); i++ {
			if seeds[i].withinRange(seedCandidate) {
				number := applyPipelines(seedCandidate, pipelines)
				if number < lowestNumber {
					lowestNumber = number
				}
				break
			}
		}
	}
	return lowestNumber
}

func puzzle(fileName string) (int, int) {
	data := lib.ReadFile(fileName)

	seedString, pipelineString, found := strings.Cut(data, "\r\n")
	if !found {
		panic("fuck")
	}
	pipelines := parsePipelines(pipelineString)

	// part 1
	naiveSeeds := parseSeedsNaively(seedString)
	lowestLocationNumberNaively := findLowestLocationNumber(naiveSeeds, pipelines)

	// part 2
	properSeeds := parseSeedsProperly(seedString)
	lowestLocationNumberProperly := findLowestLocationNumber(properSeeds, pipelines)

	return lowestLocationNumberNaively, lowestLocationNumberProperly
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
