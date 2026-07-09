"""Parse a Sysmon Event ID 1 (process creation) XML event into clean JSON."""

import argparse
import json
import xml.etree.ElementTree as ET

NAMESPACE = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

# Image/CommandLine/ParentImage/User/IntegrityLevel cover the core
# who/what/how/privilege questions an analyst asks first when triaging
# a process-creation event.
FIELDS = ["Image", "CommandLine", "ParentImage", "User", "IntegrityLevel"]

# A shell (cmd.exe/powershell.exe) spawning a recon binary is a classic
# early-discovery pattern in an intrusion, since attackers commonly script
# these commands rather than running them interactively.
SUSPICIOUS_SHELLS = {"cmd.exe", "powershell.exe"}

# Maps known discovery/recon binaries to the MITRE ATT&CK technique an
# analyst would tag them with. Kept as a plain dict (not a scoring model)
# so the mapping stays inspectable and easy to extend.
DISCOVERY_BINARIES = {
    "whoami.exe": "T1033",     # System Owner/User Discovery
    "net.exe": "T1087",        # Account Discovery
    "net1.exe": "T1087",       # net.exe re-execs as net1.exe under the hood
    "systeminfo.exe": "T1082", # System Information Discovery
}


def _basename(path: str) -> str:
    return path.rsplit("\\", 1)[-1].lower()


def detect_suspicious_pair(image: str | None, parent_image: str | None) -> str | None:
    """Flag a ParentImage/Image pair matching shell-spawns-recon-binary."""
    if not image or not parent_image:
        return None

    parent_name = _basename(parent_image)
    image_name = _basename(image)

    if parent_name in SUSPICIOUS_SHELLS and image_name in DISCOVERY_BINARIES:
        technique_id = DISCOVERY_BINARIES[image_name]
        return f"{parent_name} spawned {image_name} ({technique_id})"

    return None


def parse_event(xml_text: str) -> dict:
    root = ET.fromstring(xml_text)

    event_id = root.findtext("ns:System/ns:EventID", namespaces=NAMESPACE)
    if event_id != "1":
        raise ValueError(f"Expected Sysmon Event ID 1 (process creation), got {event_id!r}")

    data = {
        elem.get("Name"): elem.text
        for elem in root.findall("ns:EventData/ns:Data", NAMESPACE)
    }

    result = {field: data.get(field) for field in FIELDS}
    result["detection_flag"] = detect_suspicious_pair(result["Image"], result["ParentImage"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "xml_path",
        nargs="?",
        default="sample_event.xml",
        help="Path to a Sysmon Event ID 1 XML file (default: sample_event.xml)",
    )
    args = parser.parse_args()

    with open(args.xml_path, "r", encoding="utf-8") as f:
        xml_text = f.read()

    print(json.dumps(parse_event(xml_text), indent=2))


if __name__ == "__main__":
    main()
