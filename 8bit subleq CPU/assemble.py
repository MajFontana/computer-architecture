import ext
import re

CODE = "assembly.txt"
OUTPUT = "assembled.bin"

def parse(value):
    if re.match("^0[a-zA-Z]", value):
        if value[1] == "b":
            parsed = int(value, 2)
        elif value[1] == "x":
            parsed = int(value, 16)
    else:
        parsed = int(value)
    return parsed

with open(CODE, "r") as f:
    lines = f.read().lower().replace("\t", " ").split("\n")

lookup = {}
counter = 0
section = None
sequence = []
for line in lines:
    line = line.split(";")[0]
    if line:
        if line[0] == ".":
            section = line[1:]
        elif section == "data":
            line = line.replace(" ", "")
            token, value = line.split("=")
            lookup[token] = parse(value)
        elif section == "code":
            if line[0] == ":":
                line = line.replace(" ", "")
                lookup[line[1:]] = counter
            else:
                tokens = [token for token in line.split(" ") if token]
                arguments = [parse(token) if token[0].isdigit() else token for token in tokens[1:]]
                sequence.append((counter, tokens[0], arguments))
                counter += ext.inst_size(tokens[0])

raw = b""
for macro in sequence:
    num = ext.render_inst(macro[1], macro[2], macro[0], lookup)
    for operation in num:
        binary = b"".join([value.to_bytes(1, "little") for value in ((operation[0] << 4) | operation[1], operation[2])])
        raw += binary

with open(OUTPUT, "wb") as f:
    f.write(raw)

print("Program size: %i operations (%i bytes)" % (len(raw) // 2, len(raw)))
print("Lookup table:")
for key, value in lookup.items():
    print("    %s: %i" % (key, value))
