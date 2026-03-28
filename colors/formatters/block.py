import shutil

from colors.utils.text_utils import wrap_text, vertical_center
from colors.utils.color_utils import parse_bg_color, generate_gradient


def format_block(message, width=None, height=5, bg_colors=None, text_color=None, color_obj=None,):
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