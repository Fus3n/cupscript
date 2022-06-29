from cupsrc.cup_interp import run, VERSION
import os
import sys


def handle_commands(args):
    if args[0] == '-h' or args[0] == "--help":
        print(f"Usage: {sys.argv[0]} [file]")
        print("If no file is specified, the interpreter will run in interactive mode.")
    else:
        path = str(args[0].replace("\\", "/"))
        fname = os.path.split(path)[0]
        if os.path.exists(path):
            with open(path, "r") as f:
                code = f.read()
        else:
            print(f"File '{fname}' does not exist")
            exit(1)                
        result, err = run(fname, code)
        if err:
            print(err)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        handle_commands(args)
        exit(0)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * 35)
    print(f"Cup Shell {VERSION} - Python {sys.version.split('(')[0]}")
    print("-" * 35)
    print("Type 'help()' for a list of commands")
    while True:
        text = input("cup >> ")
        result, err = run("<stdin>", text)

        if text.strip() == '': continue
        
        if err: print(err)
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
