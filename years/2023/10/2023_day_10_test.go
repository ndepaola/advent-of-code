package main

import "testing"

func TestPart1Example(t *testing.T) {
	answer, _ := puzzle("example_3.txt")
	if answer != 8 {
		panic("Answer is incorrect")
	}
}

func TestPart1Input(t *testing.T) {
	answer, _ := puzzle("input.txt")
	if answer != 6897 {
		panic("Answer is incorrect")
	}
}

func TestPart2Example(t *testing.T) {
	_, answer := puzzle("example_6.txt")
	if answer != 10 {
		panic("Answer is incorrect")
	}
}

func TestPart2Input(t *testing.T) {
	_, answer := puzzle("input.txt")
	if answer != 367 {
		panic("Answer is incorrect")
	}
}
