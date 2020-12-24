import argparse
import time

from tekken_auto_accept.alerts import PushOver, Sound
from tekken_auto_accept.control import TekkenController
from tekken_auto_accept.models.screen_state import ScreenState
from tekken_auto_accept.models.tekken_state import TekkenState
from tekken_auto_accept.models.tekkenconfig import TekkenConfig
from tekken_auto_accept.util import probable_next_state

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
    parser.add_argument(
        "-a",
        "--alert",
        help="Send alert",
        choices=['sound', 'pushover'],
        default=''
    )
    parser.add_argument('--alert_on_challenger', default=False, action='store_true')
    parser.add_argument('--pushover_user_token', required=False)
    parser.add_argument('--pushover_app_token', required=False)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    config = TekkenConfig()
    config.process_args(args)

    tekken_state = TekkenState()
    tekken_state.process_config(config)
    controller = TekkenController()
    screen_scanner = ScreenState()

    next_state = []
    character_selected = False
    sleep_duration = .2
    last_alert_time = time.time()
    in_match = False
    if args.alert_on_challenger:
        alert_screen = 'new_challenger'
    else:
        alert_screen = 'loading'

    while True:
        current_screen = None
        if next_state:
            for i in range(10):
                current_screen = screen_scanner.scan_screen(next_state)
                if current_screen:
                    break
            next_state = []
        else:
            current_screen = screen_scanner.scan_screen(tekken_state.state_images)

        if not current_screen:
            time.sleep(.5)
            continue

        tekken_state.set_state(current_screen)
        commands = tekken_state.current_state.run()
        if commands:
            time.sleep(.5)
        controller.run_commands(commands)

        if alert_screen in tekken_state.current_state_name and tekken_state.alert:
            now = time.time()
            if now - last_alert_time < 60 or in_match:
                pass
            elif tekken_state.alert == 'pushover':
                print("Sending pushover alert")
                alert = PushOver()
                alert.user_token = args.pushover_user_token
                alert.app_token = args.pushover_app_token
                alert.trigger()
            elif tekken_state.alert == 'sound':
                print("Making sound")
                alert = Sound()
                alert.trigger()
            print("setting in match to True")
            in_match = True
            time.sleep(10)
        elif not [i for i in ['post_match', 'loading'] if i in tekken_state.current_state_name]:
            print("setting in match to False")
            in_match = False

        likely_next_state = probable_next_state(tekken_state.current_state_name)
        likely_next_state = [i for i in tekken_state.state_images if likely_next_state in i]
        if likely_next_state == next_state:
            next_state = []
        else:
            next_state = likely_next_state

        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()