from ciscopy.config import DRY_RUN


def save_output_to_file(output_lines, filename):
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
