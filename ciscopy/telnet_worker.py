from telnetlib import Telnet
import ciscopy.config as config

DEFAULT_TIMEOUT = 5

class DryTelnet:
    def __init__(self, ip, port):
        self.log(f"DryTelnet: I am {ip} {port}")
        self.ip = ip
        self.port = port

    def write(self, bytes):
        command_text = bytes.decode('ASCII')
        if command_text == '\r\n':
            self.log(f"{self}: Got ENTER")
        else:
            self.log(f"{self}: Got command {repr(bytes.decode('ASCII'))}")

    def read_until(self, bytes, timeout):
        self.log(f"{self}: Output was read with timeout {timeout}")
        return b''

    def close(self):
        self.log(f'{self}: connection closed.')

    def log(self, text, *args, **kwargs):
        if config.SHOW_DRY_TELNET_LOGS:
            print(text, *args, **kwargs)

    def __str__(self):
        return f"DryTelnet({self.ip},{self.port})"

class TelnetWorker:
    def __init__(self, ip, port, dry=config.DRY_RUN):
        if dry:
            self.con = DryTelnet(ip, port)
        else:
            print('Connecting to', ip, port)
            self.con = Telnet(ip, port)
        self._whole_output = []
        self.starting_output = self.read_output(as_lines=True)
        self._whole_output = []
        self.send('terminal length 0')  # gets rid of ' --More-- ' for long outputs

    def send(self, text, with_enter=True):
        self.con.write(text.encode("ASCII"))
        if with_enter:
            self.send_enter()

    def send_enter(self):
        self.con.write(b"\r\n")

    def read_output(self, as_lines=False, timeout=DEFAULT_TIMEOUT):
        data = []
        bline = True

        while bline:
            bline = self.con.read_until(b'\r\n', timeout)
            line = bline.decode("ascii")
            line = line.rstrip()
            data.append(line)

        self._whole_output.extend(data)
        if as_lines:
            return data
        else:
            output = '\n'.join(data)
            return output

    @property
    def whole_output(self):
        return self._whole_output

    def close(self):
        self.con.close()

