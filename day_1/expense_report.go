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
	for a := 0; a < len(vals) - 2; a++ {
		for b := a + 1; b < len(vals) - 1; b++ {
			for c := b + 1; c < len(vals); c++ {
				aa := vals[a]
				bb := vals[b]
				cc := vals[c]
				if aa + bb + cc == 2020 {
					fmt.Println(aa, bb, cc, aa + bb + cc, aa * bb * cc)
				}
			}
		}
	}
}
