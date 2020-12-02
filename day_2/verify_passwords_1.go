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
    n, err := strconv.Atoi(s)
    check(err)
    return n
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
        start := atoi(parts[1])
        end := atoi(parts[2])
        char, _ := utf8.DecodeRuneInString(parts[3])
        password := parts[4]
        count := 0
        for _, c := range password {
            if c == char {
                count++
            }
        }
        if count < start || count > end {
            fmt.Println("Bad password:", scanner.Text())
            num_bad_passwords++
        } else {
            num_valid_passwords++
        }
    }
    fmt.Println("Total Bad passwords:", num_bad_passwords)
    fmt.Println("Total Valid passwords:", num_valid_passwords)
}
