package main

import (
    "bufio"
    "fmt"
    "os"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func count_trees(forest [][]rune, dx int, dy int) (int) {
    x := 0
    num_trees := 0
    for y := 0; y < len(forest); y += dy {
        row := forest[y]
        if row[x] == '#' {
            num_trees++
        }
        x = (x + dx) % len(row)
    }
    fmt.Printf("Slope = %d/%d Num Trees = %d\n", dx, dy, num_trees)
    return num_trees;
}

func main() {
    fd, err := os.Open("input.txt")
    check(err)
    defer fd.Close()

    forest := [][]rune{}
    scanner := bufio.NewScanner(fd)
    for scanner.Scan() {
        forest = append(forest, []rune(scanner.Text()))
    }

    result := count_trees(forest, 1, 1) *
              count_trees(forest, 3, 1) *
              count_trees(forest, 5, 1) *
              count_trees(forest, 7, 1) *
              count_trees(forest, 1, 2)
    fmt.Println(result)
}
