import argparse
import sys
import time

from tekken_auto_accept.alerts import PushOver, Sound
from tekken_auto_accept.control import TekkenController
from tekken_auto_accept.models.screen_state import ScreenState
from tekken_auto_accept.models.tekken_state import TekkenState
from tekken_auto_accept.models.tekkenconfig import TekkenConfig
from tekken_auto_accept.util import probable_next_state

import logging


def create_parser():
    """Parses command line args."""
    epilog = """

        e.g., tekken_auto_accept -c marduk

    """
    parser = argparse.ArgumentParser(
        description="Auto accept ranked matches",
        epilog=epilog,
    )
    parser.add_argument("-c", "--character", required=True)
    parser.add_argument(
        "-s",
        "--side",
        default="p1",
    )
    parser.add_argument(
        "-r",
        "--rematch",
        help="Auto re-match after 5 seconds",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-a", "--alert", help="Send alert", choices=["sound", "pushover"], default=""
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
