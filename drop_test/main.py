from pathlib import Path


def min_num_of_drops(N, K):
    backing_array = [0] * (N + 1)

    while backing_array[N] < K:
        for i in range(N, 0, -1):
            backing_array[i] += 1 + backing_array[i - 1]

    return backing_array[1]


def main():
    data = Path("input.txt").read_text(encoding="utf-8")

    for line in data.splitlines():
        line_data = line.split(", ")
        n = int(line_data[0])
        k = int(line_data[1])
        print(min_num_of_drops(n, k))


if __name__ == "__main__":
    main()
