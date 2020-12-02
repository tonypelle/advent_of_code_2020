package main

import (
    "bufio"
    "fmt"
    "os"
    "regexp"
    "strconv"
    "unicode/utf8"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func atoi(s string) (int) {
    n, _ := strconv.Atoi(s)
    return n - 1
}

func main() {
    fd, err := os.Open("input.txt")
    check(err)
    defer fd.Close()

    re := regexp.MustCompile(`([0-9]+)-([0-9]+)\s+([a-z])\s*:\s+(.+)`)

    num_bad_passwords := 0
    num_valid_passwords := 0
    scanner := bufio.NewScanner(fd)
    for scanner.Scan() {
        parts := re.FindStringSubmatch(scanner.Text())
        pos0 := atoi(parts[1])
        pos1 := atoi(parts[2])
        char, _ := utf8.DecodeRuneInString(parts[3])
        password := []rune(parts[4])
        is_valid := (password[pos0] == char) != (password[pos1] == char)
        if ! is_valid {
            fmt.Println("Bad password:", scanner.Text())
            num_bad_passwords++
        } else {
            num_valid_passwords++
        }
    }
    fmt.Println("Total Bad passwords:", num_bad_passwords)
    fmt.Println("Total Valid passwords:", num_valid_passwords)
}
