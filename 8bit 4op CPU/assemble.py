import sys
import re
import os
import math

CMDS = {"nand": 0, "shr": 1, "str": 2, "jz": 3}
RESERVED = ["halt"]

def parse(string):
    if string[0].isdigit():
        try:
            val = string
            if string[-1].isalpha():
                val, enc = val[:-1], val[-1]
                if enc == "h":
                    parsed = int(val, 16)
                elif enc == "b":
                    parsed = int(val, 2)
            else:
                parsed = int(val)
            return [parsed, "val"]
        except ValueError:
            pass
    elif string[0].isalpha() or string[0] == "_":
        return [string, "name"]
    return [None, "fail"]

def compiled(ents, ln):
    res = ["fail"]
    if len(ents) == 1:
        cmd = CMDS.get(ents[0].lower())
        if cmd != None:
            return ["exec", cmd, 0, "val"]
    if len(ents) == 2:
        if ents[1] == ":":
            name, typ = parse(ents[0])
            if typ == "name" and not name.lower() in RESERVED:
                return ["setvar", name , ln]
        else:
            val, typ = parse(ents[1])
            cmd = CMDS.get(ents[0].lower())
            if typ != "fail" and cmd != None:
                if typ == "name" and val.lower() in RESERVED:
                    typ = "val"
                    if val.lower() == RESERVED[0]:
                        val = ln
                return ["exec", cmd, val, typ]
    elif len(ents) == 3:
        if ents[1] == "=":
            name, typ1 = parse(ents[0])
            val, typ2 = parse(ents[2])
            if typ1 == "name" and typ2 == "val" and not name.lower() in RESERVED:
                return ["setvar", name, val]
    return res

def encode_cmd(cmd):
    return bin(cmd)[2:].rjust(SIZE[0], "0")

def encode_val(val):
    return bin(val)[2:].rjust(SIZE[1], "0")

def main():
    if os.path.isfile(FPATH):
        with open(FPATH, "r") as f:
            data = f.readlines()
    else:
        print("File does not exist")
        quit()
    
    var = {}
    raw = ""
    fail = True
    ln = 0
    for line in data:
        cmd = line.split(";", 1)[:1]
        if cmd:
            ents = [i for i in re.split(r"([ =\n:])", cmd[0]) if i and (i not in " \n")]
            if ents:
                cmd = compiled(ents, ln)
                if cmd[0] == "setvar":
                    var[cmd[1]] = cmd[2]
                elif cmd[0] == "exec":
                    if cmd[3] == "name":
                        if cmd[2] in var:
                            val = var[cmd[2]]
                        else:
                            break
                    elif cmd[3] == "val":
                        val = cmd[2]
                    raw += encode_cmd(cmd[1]) + encode_val(val)
                    ln += 1
                elif cmd[0] == "fail":
                    break
    else:
        fail = False
    if fail:
        print("Syntax error on line %i:\n%s" % (ln, line))
    else:
        with open(FPATH2, "w") as f:
            f.write(raw)

if __name__ == "__main__":
    FPATH = "sum.txt"
    SIZE = (2, 6)
    FPATH2 = "sum.bin"
else:
    if len(sys.argv) < 5:
            print("Not enough arguments")
            quit()
    FPATH = sys.argv[1]
    FPATH2 = sys.argv[2]
    try:
        SIZE = (int(sys.argv[3]), int(sys.argv[4]))
    except ValueError:
        print("Invalid bitsize arguments")
    
main()
