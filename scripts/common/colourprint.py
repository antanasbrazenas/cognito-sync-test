import sys


class Colours:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Printer:
    @staticmethod
    def err(msg):
        sys.exit('{}{}{}'.format(Colours.FAIL, msg, Colours.END_C))

    @staticmethod
    def success():
        print("\n{}============ SUCCESS ============{}\n".format(Colours.OK_GREEN, Colours.END_C))
        sys.exit()

    @staticmethod
    def green(text):
        print('{}{}{}'.format(Colours.OK_GREEN, text, Colours.END_C))

    @staticmethod
    def red(text):
        print('{}{}{}'.format(Colours.FAIL, text, Colours.END_C))
