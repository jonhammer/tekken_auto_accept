from gooey import GooeyParser

from tekken_auto_accept.settings import CHARACTERS

parser = GooeyParser(description="Tekken Auto-Accept")
parser.add_argument(
    "auto_select",
    help="Automatically navigate menus and select your character and start looking for matches",
    default=False,
    action="store_true",
)
parser.add_argument(
    "character",
    choices=sorted(CHARACTERS[0] + CHARACTERS[1] + CHARACTERS[2]),
    default="marduk",
    help="Only needed for auto_select",
)
parser.add_argument(
    "-s",
    "--side",
    default="p1",
    choices=["p1", "p2"],
    help="Only needed for auto_select",
)
parser.add_argument(
    "-r",
    "--rematch",
    help="Auto re-match",
    default=False,
    action="store_true",
)
parser.add_argument(
    "-a",
    "--alert",
    help="Type of alert to send when match is found",
    choices=["sound", "pushover", "none"],
    default="sound",
)
parser.add_argument("--pushover_user_token", required=False)
parser.add_argument("--pushover_app_token", required=False)
parser.add_argument(
    "-l",
    "--log-level",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="INFO",
)
