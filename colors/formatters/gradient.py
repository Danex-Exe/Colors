from colors.utils.color_utils import is_rgb_color, parse_rgb, interpolate_color


def apply_gradient(message: str, style: str, fg_colors: list[str], bg_colors: list[str], color_obj):
    """
    Apply a smooth RGB gradient to each character of a message.

    Example:
        >>> gradient_text = apply_gradient("Hello", "\\033[1m",
        ...                                ["\\033[38;2;255;0;0m", "\\033[38;2;0;0;255m"],
        ...                                color_obj=color_obj)
        >>> print(gradient_text)
    """
    if not fg_colors and not bg_colors:
        raise ValueError("You must provide gradient_colors or gradient_bgcolors")

    fg_seq = [parse_rgb(c) for c in fg_colors]
    bg_seq = [parse_rgb(c) for c in bg_colors]

    result = []

    if style:
        result.append(style)

    for i, char in enumerate(message):
        progress = i / (len(message) - 1) if len(message) > 1 else 0

        parts = []

        if fg_seq:
            r, g, b = interpolate_color(fg_seq, progress)
            parts.append(color_obj.rgb_color(r, g, b))

        if bg_seq:
            r, g, b = interpolate_color(bg_seq, progress)
            parts.append(color_obj.rgb_bgcolor(r, g, b))

        result.append("".join(parts) + char)

    result.append(color_obj.reset)
    return "".join(result)