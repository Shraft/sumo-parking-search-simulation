import xml.etree.ElementTree as ET
import json
import sys


def parse_parking_areas(xml_input_path, json_output_path="parking_areas.json"):
    """
    Parses SUMO parkingArea XML and writes a JSON dict:
    {area_id: roadsideCapacity}
    """

    tree = ET.parse(xml_input_path)
    root = tree.getroot()

    parking_areas = []

    for parking_area in root.findall("parkingArea"):
        area_id = parking_area.get("id")
        capacity = parking_area.get("roadsideCapacity")
        lane = parking_area.get("lane")

        if area_id is not None and capacity is not None and lane is not None:
            parking_areas.append({"area_id": area_id,
                                  "capacity": int(capacity),
                                  "lane": lane})

    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(parking_areas, f, indent=4)

    print(f"Saved {len(parking_areas)} parking areas to {json_output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_parking_xml.py input.xml [output.json]")
    else:
        xml_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "parking_areas.json"

        parse_parking_areas(xml_path, output_path)
