def wrap_text(text: str, width: int) -> list[str]:
    """
    Wrap text into lines with max width.

    Example:
        >>> wrap_text("Hello world from Python", 10)
        ['Hello', 'world from', 'Python']
    """
    words = text.split()
    lines = []
    current = []

    for word in words:
        if len(" ".join(current + [word])) <= width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))

    return lines


def vertical_center(lines: list[str], height: int) -> list[str]:
    """
    Center text vertically inside a block.

    Example:
        >>> vertical_center(["Hello"], 3)
        ['', 'Hello', '']
    """
    if len(lines) > height:
        return lines[:height]

    top = (height - len(lines)) // 2
    bottom = height - len(lines) - top

    return [""] * top + lines + [""] * bottom