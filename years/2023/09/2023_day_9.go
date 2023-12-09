package main

import (
	"fmt"
	"math/big"
	"ndepaola/advent-of-code/lib"
	"time"
)

func evaluateLagrangePolynomial(yValues []int, targetX int) int { // x indexing begins from 0
	// need to use bigint here because the numerators & denominators get too big otherwise
	value := big.NewInt(0)
	for i := 0; i < len(yValues); i++ {
		numerator := big.NewInt(1)
		denominator := big.NewInt(1)
		for j := 0; j < len(yValues); j++ {
			if i != j {
				numeratorItem := big.NewInt(int64(targetX - j))
				denominatorItem := big.NewInt(int64(i - j))
				numerator = numerator.Mul(numerator, numeratorItem)
				denominator = denominator.Mul(denominator, denominatorItem)
			}
		}
		bigYValue := big.NewInt(int64(yValues[i]))
		value = value.Add(value, bigYValue.Mul(bigYValue, numerator.Div(numerator, denominator)))
	}
	return int(value.Int64())
}

func puzzle(fileName string) (int, int) {
	data := lib.ReadFileAsSliceOfType(fileName, lib.ConvertToIntSlice)
	total1 := 0
	total2 := 0
	for i := 0; i < len(data); i++ {
		total1 += evaluateLagrangePolynomial(data[i], len(data[i]))
		total2 += evaluateLagrangePolynomial(data[i], -1)
	}
	return total1, total2
}

func main() {
	start := time.Now()
	fmt.Println(puzzle("example.txt"))
	fmt.Println(puzzle("input.txt"))
	duration := time.Since(start)
	fmt.Println(duration.Seconds())
}
