from gooey import GooeyParser, Gooey

from tekken_auto_accept.settings import CHARACTERS


def create_parser():
    parser = GooeyParser()

    auto_accept_options = parser.add_argument_group("Auto Accept")
    auto_accept_options.add_argument(
        "-r",
        "--rematch",
        help="Auto re-match",
        default=False,
        action="store_true",
        widget="BlockCheckbox",
    )
    auto_accept_options.add_argument(
        "-l",
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
    )
    alert_options = parser.add_argument_group("Alert Options", description="See https://pushover.net/ to setup push notifications")
    alert_options.add_argument(
        "-a",
        "--alert",
        help="Type of alert to send when match is found",
        choices=["sound", "pushover", "none"],
        default="sound",
    )
    alert_options.add_argument("--pushover_user_token", required=False, help="")
    alert_options.add_argument("--pushover_app_token", required=False)

    auto_select_options = parser.add_argument_group("Auto Character Select")
    auto_select_options.add_argument(
        "--auto_select",
        help="Automatically navigate menus and select your character and start looking for matches",
        default=False,
        action="store_true",
        widget="BlockCheckbox",
    )
    auto_select_options.add_argument(
        "--character",
        choices=sorted(CHARACTERS[0] + CHARACTERS[1] + CHARACTERS[2]),
        default="marduk",
        widget="FilterableDropdown"
    )
    auto_select_options.add_argument(
        "-s",
        "--side",
        default="p1",
        choices=["p1", "p2"],
    )
    return parser
