import shutil

from colors import Color
from colors.utils.text_utils import wrap_text, vertical_center
from colors.utils.color_utils import parse_bg_color, generate_gradient


def format_block(message: str, width: int=None, height: int=5, bg_colors: list[str]=None, text_color: str=None, color_obj: Color=None,):
    """
    Format a centered text block with optional gradient background and colored text.

    Example:
        >>> block = format_block("Hello", width=10, height=3,
        ...                      bg_colors=["\\033[48;2;255;0;0m", "\\033[48;2;0;0;255m"],
        ...                      text_color="\\033[37m", color_obj=color_obj)
        >>> print(block)
    """
    console_width = shutil.get_terminal_size().columns

    block_width = min(width or console_width, console_width)
    left_padding = (console_width - block_width) // 2

    bg_rgb = [parse_bg_color(c) for c in bg_colors] if bg_colors else []
    gradient = generate_gradient(bg_rgb, height)

    text_lines = wrap_text(message, block_width)
    text_block = vertical_center(text_lines, height)

    result = []

    for i in range(height):
        bg = gradient[i] if gradient else ""
        line = f"{' ' * left_padding}{bg}{' ' * block_width}{color_obj.reset}"

        if i < len(text_block) and text_block[i]:
            text = text_block[i]
            pos = left_padding + (block_width - len(text)) // 2
            colored = f"{text_color or ''}{text}"
            line = f"{line[:pos]}{colored}{line[pos + len(text):]}"

        result.append(line)

    return "\n".join(result)