from ciscopy.config import DRY_RUN


def save_output_to_file(output_lines, filename):
    """Save list of lines to file.
    If DRY_RUN set in config, only print debug.

    :param output_lines: list of strings
    :param filename: filename (or path) to save
    """

    if DRY_RUN:
        print(f"WOULD SAVE COMMAND OUTPUT TO FILE {filename} HERE")
        return

    with open(filename, 'w') as f:
        if type(output_lines) is list:
            for line in output_lines:
                print(line, file=f)
        elif type(output_lines) is str:
            print(output_lines, file=f)
        elif output_lines is None:
            print(output_lines, file=f)
        else:
            raise NotImplementedError


def set_ip_address(interface, ip, mask):
    router = interface.router
    with interface.config():
        router.send_command(f"ip address {ip} {mask}")
        router.send_command("no shutdown")


def create_and_set_interface(router, name, ip, mask):
    interface = router.create_interface(name)
    set_ip_address(interface, ip, mask)
    return interface


def send_and_save(router, commands_or_command, filename, wait=10):
    router.flush_buffer()

    if type(commands_or_command) == str:
        command = commands_or_command
    elif type(commands_or_command) == list:
        commands, command = commands_or_command[:-1], commands_or_command[-1]
        for com in commands:
            router.send_command(com)
    else:
        raise NotImplementedError

    out = router.send_command(command, wait_for_output=wait)
    save_output_to_file(out, filename)