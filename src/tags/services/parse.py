"""
JSON objects annotation parsers
"""

import json

from .geometry import Rectangle


def parse(file: str, family_name="KIT(DS)1") -> tuple[list[Rectangle], list[Rectangle]]:
    """
    Parses input objects annotation file.

    Args:
        file: File name.
        family_name: Objects of interest family name.

    Returns:
        tuple: List of objects with `family_name` family name
        and list of other objects as `Rectangle` instances.
    """

    target_objects = []
    other_objects = []

    data = json.load(file)

    for obj in data:
        label = str(obj["id"])
        coordinates = obj["coordinates"]

        min_coordinates = coordinates["min"]
        max_coordinates = coordinates["max"]

        min_x = float(min_coordinates["x"])
        min_y = float(min_coordinates["y"])
        max_x = float(max_coordinates["x"])
        max_y = float(max_coordinates["y"])

        object_rectangle = Rectangle(x0=min_x, x1=max_x, y0=min_y, y1=max_y, label=label)

        if coordinates["family_name"] == family_name:
            target_objects.append(object_rectangle)
        else:
            other_objects.append(object_rectangle)

    return target_objects, other_objects
