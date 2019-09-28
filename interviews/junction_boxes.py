def parse_box(box_string):
    parts = box_string.split()
    identifier = parts[0]
    version = " ".join(parts[1:])
    return {"identifier": identifier, "version": version}


def unparse_box(box):
    return "{} {}".format(box["identifier"], box["version"])


def is_old_box(box):
    # Old junction box versions are all alphabetic characters, so checking just
    # the first should be sufficient.
    return box["version"][0].isalpha()


def ordered_junction_boxes(number_of_boxes, box_strings):
    boxes = [parse_box(b) for b in box_strings]
    old_boxes = sorted(
        (b for b in boxes if is_old_box(b)),
        key=lambda x: (x["version"], x["identifier"]),
    )
    new_boxes = [b for b in boxes if not is_old_box(b)]
    return [unparse_box(b) for b in old_boxes + new_boxes]


# boxes = ["mi2 jog mid pet", "wz3 34 54 398", "a1 alps cow bar", "x4 45 21 7"]

boxes = [
    "t2 13 121 98",
    "r1 box ape bit",
    "b4 xi me nu",
    "br8 eat nim did",
    "w1 has uni gry",
    "f3 52 54 31",
]

print(parse_box(boxes[0]))
print(is_old_box(parse_box(boxes[0])))
print(ordered_junction_boxes(4, boxes))
