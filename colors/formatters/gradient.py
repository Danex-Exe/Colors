from colors.utils.color_utils import is_rgb_color, parse_rgb, interpolate_color


def apply_gradient(message, style, fg_colors, bg_colors, color_obj):
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