import json
from pathlib import Path
from typing import List, Dict, Any

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
        if key == "dns_servers":
            adapter[key] = []  # type: ignore
        else:
            adapter[key] = ""
    return adapter


def parse_ipconfig_file(file_path: Path) -> Dict[str, Any]:
    content = file_path.read_text(encoding="utf-16")
    file_data = {"file_name": file_path.name, "adapters": []}

    current_adapter = None
    last_json_key = None

    for line in content.splitlines():
        if not line.strip():
            continue

        if (
            not line.startswith(" ")
            and not line.startswith("\t")
            and line.strip().endswith(":")
        ):
            if current_adapter:
                if not current_adapter["dns_servers"]:
                    current_adapter["dns_servers"] = ""
                file_data["adapters"].append(current_adapter)

            current_adapter = create_empty_adapter(line.strip()[:-1])
            last_json_key = None
            continue

        if current_adapter is not None:
            if ":" in line:
                parts = line.split(":", 1)
                label = parts[0].replace(".", "").strip()
                value = parts[1].strip()

                found_key = label_to_key.get(label)

                if found_key:
                    if found_key in ["dns_servers", "default_gateway"]:
                        if value:
                            if found_key == "dns_servers":
                                current_adapter[found_key].append(value)
                            else:
                                current_adapter[found_key] = value
                    else:
                        current_adapter[found_key] = value.split("(")[0]
                    last_json_key = found_key
                else:
                    last_json_key = None
            else:
                if last_json_key in ["dns_servers", "default_gateway"]:
                    val = line.strip()
                    if val:
                        if last_json_key == "dns_servers":
                            current_adapter[last_json_key].append(val)
                        else:
                            current_adapter[last_json_key] += f" {val}"

    if current_adapter:
        if not current_adapter["dns_servers"]:
            current_adapter["dns_servers"] = ""
        file_data["adapters"].append(current_adapter)

    return file_data


def main():
    all_results = []

    for path in sorted(Path(".").glob("*.txt")):
        if path.name == "requirements.txt":
            continue

        result = parse_ipconfig_file(path)
        all_results.append(result)

    print(json.dumps(all_results, indent=2, ensure_ascii=False))

    with open("output.json", "w", encoding="utf-16") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
