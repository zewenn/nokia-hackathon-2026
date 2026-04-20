import json
from pathlib import Path
from typing import List, Dict, Any


MULTI_VALUE_KEYS = ["dns_servers", "default_gateway"]

json_keys = [
    "description",
    "physical_address",
    "dhcp_enabled",
    "ipv4_address",
    "subnet_mask",
    "default_gateway",
    "dns_servers",
]

label_to_key = {
    "Description": "description",
    "Physical Address": "physical_address",
    "DHCP Enabled": "dhcp_enabled",
    "IPv4 Address": "ipv4_address",
    "Autoconfiguration IPv4 Address": "ipv4_address",
    "Subnet Mask": "subnet_mask",
    "Default Gateway": "default_gateway",
    "DNS Servers": "dns_servers",
}


def create_empty_adapter(name: str) -> Dict[str, Any]:
    adapter = {"adapter_name": name}
    for key in json_keys:
        if key in MULTI_VALUE_KEYS:
            adapter[key] = []  # type: ignore
        else:
            adapter[key] = ""
    return adapter


def parse_ipconfig_file(file_path: Path) -> Dict[str, Any]:

    try:
        content = file_path.read_text(encoding="utf-16")
    except UnicodeDecodeError:
        content = file_path.read_text(encoding="utf-8", errors="replace")

    file_data = {"file_name": file_path.name, "adapters": []}
    current_adapter = None
    last_json_key = None

    for line in content.splitlines():
        trimmed_line = line.strip()
        if not trimmed_line:
            continue

        if not line.startswith((" ", "\t")) and trimmed_line.endswith(":"):
            if current_adapter:
                file_data["adapters"].append(current_adapter)
            current_adapter = create_empty_adapter(trimmed_line[:-1])
            last_json_key = None
            continue

        if current_adapter is not None:

            found_key = None
            if ":" in line:

                potential_label = line.split(":", 1)[0].replace(".", "").strip()
                found_key = label_to_key.get(potential_label)

            if found_key:
                value = line.split(":", 1)[1].strip()

                clean_value = value.split("(")[0].strip()

                if found_key in MULTI_VALUE_KEYS:
                    if clean_value:
                        current_adapter[found_key].append(clean_value)
                else:
                    current_adapter[found_key] = clean_value

                last_json_key = found_key

            elif last_json_key in MULTI_VALUE_KEYS and (line.startswith("     ")):
                val = trimmed_line
                if val:

                    current_adapter[last_json_key].append(val)

    if current_adapter:
        file_data["adapters"].append(current_adapter)

    return file_data


def main():
    all_results = []

    base_path = Path(".")
    for path in sorted(base_path.glob("*.txt")):
        if path.name == "requirements.txt":
            continue
        result = parse_ipconfig_file(path)
        all_results.append(result)

    print(json.dumps(all_results, indent=2, ensure_ascii=False))
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
