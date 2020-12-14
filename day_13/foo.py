import functools

from aoc_utils.data import *

def main():
    earliest_departure, times = list(read_lines())
    # earliest_departure, times = list(read_lines('day_13/example.txt'))

    earliest_departure = int(earliest_departure)
    buses = [(i, int(bus_id)) for i, bus_id in enumerate(times.split(',')) if bus_id != 'x']
    buses = list(sorted(buses, key=lambda x: x[1], reverse=True))

    next_departures = [(((earliest_departure+bus_id) // bus_id) * bus_id - earliest_departure, bus_id) for _, bus_id in buses]
    next_departure = min(next_departures, key=lambda x: x[0])

    print('part 1 =', next_departure[0] * next_departure[1])

    # Sascha's solution:
    #
    # ts = buses[0][1] - buses[0][0]
    # inc_ = 1
    # for i, bus_id in buses:
    #     while (ts + i) % bus_id != 0:
    #         ts += inc_
    #     inc_ *= bus_id

    # https://www.dave4math.com/mathematics/chinese-remainder-theorem/

    Ni = [i * bus_id for i, bus_id in buses]
    Ai = [-i for i, _ in buses]
    N = functools.reduce(lambda x, y: x * y, [bus_id for _, bus_id in buses])
    N_bar_i = [N//bus_id for _, bus_id in buses]
    Ui = [(n+1) % bus_id for (n, (_, bus_id)) in zip(N_bar_i, buses)]

    Ui = []
    for n, (_, bus_id) in zip(N_bar_i, buses):
      ts = n 
      c = 1
      while (ts-1) % bus_id != 0:
        ts += n
        c += 1
      Ui.append(c)
    X = sum(a * n * u for a, n, u in zip(Ai, N_bar_i, Ui))
    ts = X % N
    print('part 2 =', ts)

if __name__ == '__main__':
    main()
