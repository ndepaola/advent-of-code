package main

import "testing"

func TestPart1Example(t *testing.T) {
	answer, _ := puzzle("example.txt")
	if answer != 405 {
		panic("Answer is incorrect")
	}
}

func TestPart1Input(t *testing.T) {
	answer, _ := puzzle("input.txt")
	if answer != 31739 {
		panic("Answer is incorrect")
	}
}

func TestPart2Example(t *testing.T) {
	_, answer := puzzle("example.txt")
	if answer != 400 {
		panic("Answer is incorrect")
	}
}

func TestPart2Input(t *testing.T) {
	_, answer := puzzle("input.txt")
	if answer != 31539 {
		panic("Answer is incorrect")
	}
}
