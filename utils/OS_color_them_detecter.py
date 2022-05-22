from colorama import Fore

try:
    import darkdetect
except ImportError as err:
    print(err)
    darkdetect = None


def detect_dark_mode():
    """Detecting dark mode in OS"""
    if darkdetect.isDark():
        return Fore.LIGHTWHITE_EX
    return Fore.BLACK
