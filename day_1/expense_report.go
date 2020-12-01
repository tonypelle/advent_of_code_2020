package main

import (
	"bufio"
	"fmt"
    "os"
    "strconv"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func main() {
    fd, err := os.Open("input.txt")
    check(err)

	var vals []int

	scanner := bufio.NewScanner(fd)
	for scanner.Scan() {
		v, err := strconv.Atoi(scanner.Text())
	    check(err)
		vals = append(vals, v)
	}
	for a := 0; a < len(vals) - 1; a++ {
		for b := a + 1; b < len(vals); b++ {
			aa := vals[a]
			bb := vals[b]
			if aa + bb == 2020 {
				fmt.Println(aa, bb, aa + bb, aa * bb)
			}
		}
	}
}
