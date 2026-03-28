import argparse
from colors import Color


def main():
    parser = argparse.ArgumentParser(
        prog="colors",
        description="CLI for colored terminal output"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ========= PRINT =========
    print_parser = subparsers.add_parser("print", help="Print colored text")
    print_parser.add_argument("message", help="Text to print")

    print_parser.add_argument(
        "--color",
        choices=["black", "red", "green", "yellow", "blue", "white"],
        help="Basic text color"
    )

    print_parser.add_argument(
        "--style",
        choices=["bold", "italic", "underline", "strike"],
        help="Text style"
    )

    print_parser.add_argument(
        "--rgb",
        nargs=3,
        type=int,
        metavar=("R", "G", "B"),
        help="RGB foreground color"
    )

    print_parser.add_argument(
        "--bg-rgb",
        nargs=3,
        type=int,
        metavar=("R", "G", "B"),
        help="RGB background color"
    )

    print_parser.add_argument(
        "--gradient",
        action="store_true",
        help="Enable gradient (red → blue by default)"
    )

    # ========= BLOCK =========
    block_parser = subparsers.add_parser("block", help="Print message block")
    block_parser.add_argument("message")

    block_parser.add_argument("--height", type=int, default=5)
    block_parser.add_argument("--width", type=int)

    args = parser.parse_args()
    c = Color()

    # ========= COMMAND HANDLER =========
    if args.command == "print":
        color = None
        style = None

        # basic color
        if args.color:
            color = getattr(c, args.color)

        # style
        if args.style:
            style = getattr(c, args.style)

        # rgb override
        if args.rgb:
            color = c.rgb_color(*args.rgb)

        # background rgb
        bg = None
        if args.bg_rgb:
            bg = c.rgb_bgcolor(*args.bg_rgb)

        # gradient
        if args.gradient:
            result = c.color_message(
                args.message,
                gradient=True,
                gradient_colors=[
                    c.rgb_color(255, 0, 0),
                    c.rgb_color(0, 0, 255),
                ],
                style=style
            )
        else:
            final_color = ""
            if color:
                final_color += color
            if bg:
                final_color += bg

            result = c.color_message(
                args.message,
                color=final_color if final_color else None,
                style=style
            )

        print(result)

    elif args.command == "block":
        result = c.format_message_block(
            args.message,
            width=args.width,
            height=args.height,
            bg_colors=[
                c.rgb_bgcolor(255, 0, 0),
                c.rgb_bgcolor(0, 0, 255),
            ],
        )
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()