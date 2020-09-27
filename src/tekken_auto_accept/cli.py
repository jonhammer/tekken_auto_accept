import argparse

from models.tekken_state import TekkenState

SIDE_MAP = {"left": ["b"], "right": ["left", "b"]}

CHARACTER_MAP = {"test": ["left, left", "left", "b"]}


def create_parser():
    """Parses command line args."""
    epilog = """

        e.g., tekken_auto_accept -c marduk

    """
    parser = argparse.ArgumentParser(
        description="Auto accept ranked matches", epilog=epilog,
    )
    parser.add_argument(
        "-c", "--character", required=True
    )
    parser.add_argument(
        "-s", "--side", default='p1',
    )
    parser.add_argument(
        "-r",
        "--rematch",
        help="Auto re-match after 5 seconds",
        default=False,
        action="store_true",
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    tekken_state = TekkenState(args.character, args.side)

    tekken_state.run()


if __name__ == "__main__":
    main()