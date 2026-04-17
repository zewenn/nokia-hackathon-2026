from pathlib import Path
from typing import Dict, Optional, List
import json


def clean_key(key: str) -> str:
    return key.replace(".", "").strip().lower().replace("-", "_").replace(" ", "_")


def parse_ipconfig(file_name: str, file_contents: str) -> Dict[str, str | List[str]]:
    obj = {"file_name": file_name, "adapters": []}
    current_adapter: Optional[Dict[str, str | List[str]]] = None
    last_key: Optional[str] = None

    for line in file_contents.splitlines():
        clean_line = line.strip()
        if clean_line.strip() == "":
            continue

        if not (line.startswith(" ") or line.startswith("\t")) and clean_line.endswith(
            ":"
        ):
            if current_adapter is not None:
                obj["adapters"].append(current_adapter)

            current_adapter = {"adapter_name": clean_line[:-1]}
            continue

        if line.startswith(" ") or line.startswith("\t"):
            if current_adapter is None:
                current_adapter = {"adapter_name": ""}

            if last_key is not None and not clean_line.__contains__(":"):
                if type(current_adapter[last_key]) == str:
                    current_adapter[last_key] = [current_adapter[last_key], clean_line]  # type: ignore

                current_adapter[last_key].append(clean_line)  # type: ignore

                continue

            if not line.__contains__(":"):
                continue

            data: List[str] = clean_line.split(":", 1)
            key = clean_key(data[0])
            value = data[1].strip()

            current_adapter[key] = value
            last_key = key

    return obj


def main():
    objs: List[Dict[str, str | List[str]]] = []

    for path in sorted(Path(".").glob("*.txt")):
        data = Path(path.name).read_text(encoding="utf-16")
        objs.append(parse_ipconfig(path.name, data))

    print(json.dumps(objs, indent=2, ensure_ascii=False))
    with open("output.json", "w", encoding="utf-16") as wf:
        json.dump(objs, wf, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
