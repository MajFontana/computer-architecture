INSTRUCTIONS = "ext_insts.txt"

with open(INSTRUCTIONS, "r") as f:
    lines = f.read().lower().replace("\t", " ").split("\n")

instset = {}
stage = 0
for line in lines:
    tokens = [token for token in line.split(" ") if token]
    if tokens:
        if stage == 0:
            counter = 0
            instset[tokens[0]] = {"sequence": [], "arguments": tokens[1:]}
            inst = tokens[0]
            stage = 1
        else:
            if len(tokens) == 2:
                dest = counter + 2
            else:
                dest = tokens[2]
                if dest.isdigit():
                    dest = int(dest)
            operation = tokens[:2] + [dest]
            instset[inst]["sequence"].append(operation)
            counter += 2
    else:
        stage = 0

def render_inst(inst, tokens, pos, lookup):
    desc = instset[inst]
    mapping = {desc["arguments"][i]: lookup[tokens[i]] for i in range(len(desc["arguments"]))}
    num = []
    for operation in desc["sequence"]:
        num.append([])
        for i in range(3):
            if type(operation[i]) is str:
                if operation[i] in mapping:
                    value = mapping[operation[i]]
                else:
                    value = lookup[operation[i]]
            else:
                value = operation[i]
                if i == 2:
                    value += pos
            num[-1].append(value)
    return num

def inst_size(inst):
    size = len(instset[inst]["sequence"]) * 2
    return size
