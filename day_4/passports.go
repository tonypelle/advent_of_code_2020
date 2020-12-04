package main

import (
    "bufio"
    "fmt"
    "os"
    "regexp"
    "strconv"
    "strings"
)

var required_fields []string = []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
var valid_eye_colours []string = []string{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func atoi(s string) (int) {
    n, _ := strconv.Atoi(s)
    return n 
}

func check_year(value string, min_value int, max_value int) (bool) {
    year_re := regexp.MustCompile(`^\d{4}$`)
    if year_re.MatchString(value) {
        year := atoi(value)
        if year >= min_value && year <= max_value {
            return true;
        }
    }
    return false;
}

func check_height(value string) (bool) {
    height_re := regexp.MustCompile(`^(\d+)(in|cm)$`)
    parts := height_re.FindStringSubmatch(value)
    if parts == nil {
        return false;
    }
    height := atoi(parts[1])
    return (parts[2] == "cm" && height >= 150 && height <= 193) ||
           (parts[2] == "in" && height >= 59 && height <= 76)
}

func check_pid(value string) (bool) {
    pid_re := regexp.MustCompile(`^[0-9]{9}$`)
    return pid_re.MatchString(value)
}

func check_hair_colour(value string) (bool) {
    colour_re := regexp.MustCompile(`^#[a-f0-9]{6}$`)
    return colour_re.MatchString(value)
}

func check_eye_colour(value string) (bool) {
    for _, valid_eye_color := range valid_eye_colours {
        if valid_eye_color == value {
            return true
        }
    }
    return false
}

func check_validity(passport map[string]string) (bool) {
    for _, required_field := range required_fields {
        _, ok := passport[required_field]
        if !ok {
            return false
        }
    }
    if !check_year(passport["byr"], 1920, 2002) {
        return false
    }
    if !check_year(passport["iyr"], 2010, 2020) {
        return false
    }
    if !check_year(passport["eyr"], 2020, 2030) {
        return false
    }
    if !check_height(passport["hgt"]) {
        return false
    }
    if !check_pid(passport["pid"]) {
        return false
    }
    if !check_hair_colour(passport["hcl"]) {
        return false
    }
    if !check_eye_colour(passport["ecl"]) {
        return false
    }
    return true;
}

func read_passports(input_file string) <-chan map[string]string {
    ch := make(chan map[string]string)

    go func () {
        fd, err := os.Open(input_file)
        check(err)
        defer fd.Close()

        passport := make(map[string]string)
        scanner := bufio.NewScanner(fd)
        space_re := regexp.MustCompile(`\s+`)

        for scanner.Scan() {
            line := scanner.Text()
            if line == "" {
                ch <- passport
                passport = make(map[string]string)
            } else {
                parts := space_re.Split(line, -1)
                for _, part := range parts {
                    kv := strings.Split(part, ":")
                    passport[kv[0]] = kv[1]
                }
            }
        }
        ch <- passport
        close(ch)
    } ()
    return ch
}

func main() {
    valid := 0
    invalid := 0
    for passport := range read_passports("input.txt") {
        if check_validity(passport) {
            valid++
        } else {
            invalid++
        }
    }
    fmt.Printf("Invalid = %d\n", invalid)
    fmt.Printf("Valid = %d\n", valid)
}
