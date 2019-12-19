import time
import ciscopy.config as config

class Command:
    """Not used yet. Needed in future."""

    def __new__(cls, str_or_command):
        if type(str_or_command) is str:
            return Command(str_or_command)  # how not to loop???
        elif type(str_or_command) is Command:
            return str_or_command
        else:
            raise NotImplementedError("Command has to be string.")

    def execute(self, router):
        router.send_command(self)


def PAUSE():
    """Waits for user input"""

    if config.DRY_RUN:
        print("SHOULD WAIT FOR USER OUTPUT HERE...")
        return

    input("Press ENTER to continue...\n")
    print("Continuing...")

def WAIT(s=5):
    """Waits `s` seconds and continues executing"""
    if config.DRY_RUN:
        print(f"SHOULD WAIT {s} seconds HERE...")
        return

    time.sleep(s)
