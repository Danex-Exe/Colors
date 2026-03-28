def is_rgb_color(code: str) -> bool:
    """
    Check if the given ANSI code is an RGB color.

    Example:
        >>> is_rgb_color("\033[38;2;255;0;0m")
        True

        >>> is_rgb_color("\033[31m")
        False
    """
    return code.startswith("\033[38;2;") or code.startswith("\033[48;2;")

def is_basic_color(code: str) -> bool:
    """
    Check if the given ANSI code is a basic color.

    Example:
        >>> is_basic_color("\033[31m")
        True

        >>> is_basic_color("\033[38;2;255;0;0m")
        False
    """
    return code.startswith("\033[")

def parse_rgb(code: str):
    """
    Extract RGB values from ANSI escape code.

    Example:
        >>> parse_rgb("\033[38;2;255;100;50m")
        (255, 100, 50)
    """
    parts = code[2:-1].split(";")
    return tuple(map(int, parts[2:5]))

def interpolate_color(seq: tuple[int] | list[tuple[int]], progress: float) -> tuple[int]:
    """
    Interpolate between multiple RGB colors.

    Args:
        seq: list of (r, g, b)
        progress: float from 0.0 to 1.0

    Example:
        >>> interpolate_color([(255, 0, 0), (0, 0, 255)], 0.5)
        (128, 0, 128)
    """
    if len(seq) == 1:
        return seq[0]

    pos = progress * (len(seq) - 1)
    i = int(pos)
    t = pos - i

    if i >= len(seq) - 1:
        return seq[-1]

    return tuple(
        round(seq[i][j] + (seq[i + 1][j] - seq[i][j]) * t)
        for j in range(3)
    )

def parse_bg_color(code: str) -> tuple[int]:
    """
    Extract RGB values from background ANSI code.

    Example:
        >>> parse_bg_color("\033[48;2;10;20;30m")
        (10, 20, 30)
    """
    parts = code[2:-1].split(";")
    return tuple(map(int, parts[2:5]))

def generate_gradient(colors: list[tuple], steps: int) -> list[str]:
    """
    Generate background gradient ANSI codes.

    Example:
        >>> generate_gradient([(255,0,0), (0,0,255)], 3)
        [
            '\\033[48;2;255;0;0m',
            '\\033[48;2;128;0;128m',
            '\\033[48;2;0;0;255m'
        ]
    """
    if not colors:
        return []

    if len(colors) == 1:
        return [f"\033[48;2;{colors[0][0]};{colors[0][1]};{colors[0][2]}m"] * steps

    result = []
    segment = (steps - 1) / (len(colors) - 1)

    for i in range(steps):
        pos = i / segment
        idx = int(pos)
        t = pos - idx

        if idx >= len(colors) - 1:
            r, g, b = colors[-1]
        else:
            r = int(colors[idx][0] + (colors[idx + 1][0] - colors[idx][0]) * t)
            g = int(colors[idx][1] + (colors[idx + 1][1] - colors[idx][1]) * t)
            b = int(colors[idx][2] + (colors[idx + 1][2] - colors[idx][2]) * t)

        result.append(f"\033[48;2;{r};{g};{b}m")

    return result