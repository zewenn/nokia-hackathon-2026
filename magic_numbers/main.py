from pathlib import Path
from typing import Tuple, List
import time


def next_magic_number_array(base_number: Tuple[int, ...]):
    if all([x == 9 for x in base_number]):
        return [1] + [0 for _ in range(len(base_number) - 1)] + [1]

    length = len(base_number)
    middle_index = length // 2
    left_smaller_than_right = False
    left_index = middle_index - 1
    right_index = middle_index + 1 if (length % 2 == 1) else middle_index

    result: List[int] = list(base_number[:])

    flag = False

    while left_index >= 0:
        left_index -= 1
        right_index += 1

        if right_index >= length:
            break

        if result[left_index] == result[right_index] and not flag:
            continue

        if not flag:
            left_smaller_than_right = result[left_index] < result[right_index]

        flag = True
        result[right_index] = result[left_index]

    if left_index < 0:
        left_smaller_than_right = True

    if left_smaller_than_right:
        carry = 1
        left_index = middle_index - 1

        if length % 2 == 1:
            result[middle_index] += carry
            carry = result[middle_index] // 10
            result[middle_index] %= 10
            right_index = middle_index + 1
        else:
            right_index = middle_index

        while left_index >= 0:
            result[left_index] += carry
            carry = result[left_index] // 10
            result[left_index] %= 10
            result[right_index] = result[left_index]
            right_index += 1
            left_index -= 1

    return result[:]


def next_magic_number(base: Tuple[int, ...]) -> int:
    return int("".join(str(x) for x in next_magic_number_array(base)[:]))


def main():
    data = Path("input.txt").read_text(encoding="utf-8")

    print(data, end="")

    for line in data.split("\n"):
        if line.strip() == "":
            continue

        if line.__contains__("^"):
            parts: List[str] = line.split("^")
            if parts[0].isdigit() and parts[1].isdigit() and len(parts) == 2:
                base = int(parts[0])
                exponent = int(parts[1])
                result = str(base**exponent)
                print(next_magic_number(tuple([int(c) for c in result])))
                continue

        if not line.isdigit():
            print(f"cannot solve for {line}")
            continue

        print(next_magic_number(tuple([int(c) for c in line])))


if __name__ == "__main__":
    main()
