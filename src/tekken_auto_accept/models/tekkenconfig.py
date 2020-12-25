class TekkenConfig(object):
    def __init__(self):
        self.character = None
        self.side = None
        self.alert = None
        self.rematch = None
        self.auto_select = None

    def process_args(self, args):
        self.character = args.character
        self.side = args.side
        self.auto_select = args.auto_select
        if args.alert == "none":
            self.alert = None
        else:
            self.alert = args.alert
        self.rematch = args.rematch
