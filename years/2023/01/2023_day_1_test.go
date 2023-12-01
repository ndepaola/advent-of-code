package main

import "testing"

func TestPart1Example(t *testing.T) {
	answer := puzzle("example.txt", false)
	if answer != 142 {
		panic("Answer is incorrect")
	}
}

func TestPart1Input(t *testing.T) {
	answer := puzzle("input.txt", false)
	if answer != 54940 {
		panic("Answer is incorrect")
	}
}

func TestPart2Example(t *testing.T) {
	answer := puzzle("example_2.txt", true)
	if answer != 281 {
		panic("Answer is incorrect")
	}
}

func TestPart2Input(t *testing.T) {
	answer := puzzle("input.txt", true)
	if answer != 54208 {
		panic("Answer is incorrect")
	}
}
