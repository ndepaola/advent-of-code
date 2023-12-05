package main

import "testing"

func TestPart1Example(t *testing.T) {
	answer, _ := puzzle("example.txt")
	if answer != 35 {
		panic("Answer is incorrect")
	}
}

func TestPart1Input(t *testing.T) {
	answer, _ := puzzle("input.txt")
	if answer != 278755257 {
		panic("Answer is incorrect")
	}
}

func TestPart2Example(t *testing.T) {
	_, answer := puzzle("example.txt")
	if answer != 46 {
		panic("Answer is incorrect")
	}
}

func TestPart2Input(t *testing.T) {
	_, answer := puzzle("input.txt")
	if answer != 26829166 {
		panic("Answer is incorrect")
	}
}
