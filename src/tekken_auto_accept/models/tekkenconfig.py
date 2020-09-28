class TekkenConfig(object):
    def __init__(self):
        self.character = None
        self.side = None
        self.alert = None
        self.rematch = None

    def process_args(self, args):
        self.character = args.character
        self.side = args.side
        self.alert = args.alert
        self.rematch = args.rematch
