from colors import Color
from colors.utils.color_utils import is_rgb_color, is_basic_color


def apply_simple(message: str, color: str, style: str, color_obj: Color):
    """
    Apply a single color and/or style to the entire message

    Example:
        >>> from colorama import Fore
        >>> result = apply_simple("Hello", "\\033[31m", "\\033[1m", color_obj)
        >>> print(result)  # outputs red bold "Hello" followed by reset
    """
    parts = []

    if style:
        parts.append(style)

    if color:
        if not is_rgb_color(color) and not is_basic_color(color):
            raise ValueError("Use class methods to define colors")
        parts.append(color)

    return f'{"".join(parts)}{message}{color_obj.reset}' if parts else message