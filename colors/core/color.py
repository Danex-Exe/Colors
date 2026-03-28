from colors.core import constants
from colors.formatters.simple import apply_simple
from colors.formatters.gradient import apply_gradient
from colors.formatters.block import format_block


class Color:
    def __init__(self):
        self.black = constants.BLACK
        self.red = constants.RED
        self.green = constants.GREEN
        self.yellow = constants.YELLOW
        self.blue = constants.BLUE
        self.white = constants.WHITE

        self.bold = constants.BOLD
        self.italic = constants.ITALIC
        self.underline = constants.UNDERLINE
        self.strike = constants.STRIKE

        self.reset = constants.RESET

    def rgb_color(self, r: str | int, g: str | int, b: str | int):
        """
        Create RGB foreground color.

        Example:
            >>> c = Color()
            >>> print(c.rgb_color(255, 0, 0) + "Hello" + c.reset)
        """
        return f"\033[38;2;{r};{g};{b}m"


    def rgb_bgcolor(self, r: str | int, g: str | int, b: str | int):
        """
        Create RGB background color.

        Example:
            >>> c = Color()
            >>> print(c.rgb_bgcolor(0, 0, 255) + "Hello" + c.reset)
        """
        return f"\033[48;2;{r};{g};{b}m"


    def color_message(self, message, color=None, gradient=False, gradient_colors=None, gradient_bgcolors=None, style=None,):
        """
        Format message with colors, styles, or gradients.

        Example:
            >>> c = Color()

            # simple color
            >>> print(c.color_message("Hello", color=c.red))

            # style
            >>> print(c.color_message("Bold", style=c.bold))

            # gradient
            >>> print(c.color_message(
            ...     "Gradient",
            ...     gradient=True,
            ...     gradient_colors=[
            ...         c.rgb_color(255,0,0),
            ...         c.rgb_color(0,0,255)
            ...     ]
            ... ))
        """
        if gradient:
            return apply_gradient(message, style, gradient_colors or [], gradient_bgcolors or [], self)

        return apply_simple(message, color, style, self)


    def format_message_block(self, *args, **kwargs):
        """
        Render message inside a colored block.

        Example:
            >>> c = Color()
            >>> print(c.format_message_block(
            ...     "Hello",
            ...     height=5,
            ...     bg_colors=[
            ...         c.rgb_bgcolor(255,0,0),
            ...         c.rgb_bgcolor(0,0,255)
            ...     ]
            ... ))
        """
        return format_block(*args, **kwargs, color_obj=self)