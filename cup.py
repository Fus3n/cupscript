from cupsrc.cup_interp import run, VERSION
import os
import sys

args = sys.argv
if not len(args) > 1:
    os.system('cls' if os.name == 'nt' else 'cls')
    print("-" * 35)
    print(f"Cup Shell {VERSION} - Python {sys.version.split('(')[0]}")
    print("-" * 35)
    print("Type 'help()' for a list of commands")
while True:
    text = ""
    if len(args) > 1:
        path = str(args[1].replace("\\", "/"))
        result, err = run(os.path.split(path)[1], f"Run('{path}')")
        if err: print(err)
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
        break
    else:
        text = input("cup >> ")
        result, err = run("<stdin>", text)

    if text.strip() == '': continue

    if err: print(err)
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
