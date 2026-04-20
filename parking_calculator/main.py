from pathlib import Path
import math
from datetime import datetime


def get_fee_by_minutes(minutes: int, round_to_hours: bool) -> int:
    days = minutes // (24 * 60)
    remaining_minutes = minutes % (24 * 60)

    overflow_amount = 0

    if remaining_minutes <= 30:
        overflow_amount = 0
    elif remaining_minutes <= 3 * 60 + 30:
        overflow_amount = (
            (remaining_minutes - 30) * (300 / 60)
            if not round_to_hours
            else math.ceil((remaining_minutes - 30) / 60) * 300
        )
    else:
        overflow_amount = (
            900 + (remaining_minutes - 210) * (500 / 60)
            if not round_to_hours
            else 900 + math.ceil((remaining_minutes - 210) / 60) * 500
        )

    return days * 10_000 + int(overflow_amount)


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    output = ""

    output += "RENDSZAM\tDIJ\n"
    for line in data.splitlines()[2:]:
        line_data = line.split("\t\t")

        if len(line_data) != 3:
            print(f"invalid data: {line}")
            continue

        plate_number = line_data[0].strip()
        arrival = datetime.strptime(line_data[1], "%Y-%m-%d %H:%M:%S")
        leave = datetime.strptime(line_data[2], "%Y-%m-%d %H:%M:%S")

        if leave < arrival:
            print(f"Invalid data: {plate_number} left before arriving")
            continue

        diff = leave - arrival
        minutes = math.ceil(diff.total_seconds() / 60)

        output += f"{plate_number}\t\t{get_fee_by_minutes(minutes, True)}"
        print(output)

        with open("output.txt", "w", encoding="utf-8") as wf:
            wf.write(output)


if __name__ == "__main__":
    main()
