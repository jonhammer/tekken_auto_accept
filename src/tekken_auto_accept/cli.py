import argparse
import logging
import sys
import time

from gooey import Gooey

from tekken_auto_accept.alerts import PushOver, Sound
from tekken_auto_accept.control import TekkenController
from tekken_auto_accept.models.screen_state import ScreenState
from tekken_auto_accept.models.tekken_state import TekkenState
from tekken_auto_accept.models.tekkenconfig import TekkenConfig
from tekken_auto_accept.settings import CHARACTERS
from tekken_auto_accept.util import probable_next_state


@Gooey(
    program_name="Tekken Auto-Accept",
    show_stop_warning=False,
)
def create_parser():
    """Parses command line args."""
    epilog = """

        e.g., tekken_auto_accept -c marduk

    """
    parser = argparse.ArgumentParser(
        description="Automatically accept ranked matches",
        epilog=epilog,
    )
    parser.add_argument(
        "--auto_select",
        help="Automatically navigate menus and select your character and start looking for matches",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--character",
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
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.alert == "pushover":
        if not args.pushover_user_token or not args.pushover_app_token:
            raise ValueError(
                "Must provide pushover tokens for pushover alerts. See https://pushover.net/"
            )

    if args.auto_select:
        if not all([args.character, args.side]):
            raise ValueError("Must select character + side for auto-selection")

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s: %(levelname)s - %(threadName)s - %(module)s:%(lineno)s - %(message)s",
        stream=sys.stdout,
        level=args.log_level,
    )

    config = TekkenConfig()
    config.process_args(args)

    tekken_state = TekkenState()
    tekken_state.process_config(config)
    controller = TekkenController()
    screen_scanner = ScreenState()

    next_state = []
    sleep_duration = (
        0.5  # Duration to wait between scanning + before inputting commands
    )
    last_alert_time = time.time()
    logger.info("Scanning for game state.")
    logger.info("Scanning for game state.")
    while True:

        current_screen = None

        # If we think we know the next state, scan for that state 10x before proceeding.
        if next_state:
            for i in range(10):
                current_screen = screen_scanner.scan_screen(next_state)
                if current_screen:
                    break
            next_state = []
        else:
            current_screen = screen_scanner.scan_screen(tekken_state.state_images)

        if not current_screen:
            time.sleep(sleep_duration)
            continue

        tekken_state.set_state(current_screen)
        commands = tekken_state.current_state.run()
        if commands:
            if [
                i
                for i in ["no_rematch", "post_match"]
                if i in tekken_state.current_state_name
            ]:
                if not args.rematch:
                    continue
            time.sleep(sleep_duration)
        controller.run_commands(commands)

        if "new_challenger" in tekken_state.current_state_name and tekken_state.alert:
            now = time.time()

            time_since_last_alert = now - last_alert_time
            if time_since_last_alert < 30:
                logger.info(
                    f"Last alert was {time_since_last_alert} seconds ago. Ignoring."
                )
                continue

            last_alert_time = time.time()
            if tekken_state.alert == "pushover":
                logger.info("Sending pushover alert")
                alert = PushOver()
                alert.user_token = args.pushover_user_token
                alert.app_token = args.pushover_app_token
                alert.trigger()

            elif tekken_state.alert == "sound":
                logger.info("Making sound alert")
                alert = Sound()
                alert.trigger()

        likely_next_state = probable_next_state(tekken_state.current_state_name)
        likely_next_state = [
            i for i in tekken_state.state_images if likely_next_state in i
        ]
        if likely_next_state == next_state:
            next_state = []
        else:
            next_state = likely_next_state

        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
