from colors.utils.color_utils import is_rgb_color, is_basic_color


def apply_simple(message, color, style, color_obj):
    parts = []

    if style:
        parts.append(style)

    if color:
        if not is_rgb_color(color) and not is_basic_color(color):
            raise ValueError("Use class methods to define colors")
        parts.append(color)

    return f'{"".join(parts)}{message}{color_obj.reset}' if parts else message