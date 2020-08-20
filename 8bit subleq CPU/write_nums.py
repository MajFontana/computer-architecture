with open("raw.txt", "r") as f:
    lines = f.readlines()
raw = b""
for line in lines:
    vals = line.replace("\n", "").split(" ")
    if vals:
        ops = sum([int(vals[i]) * (16, 1)[i] for i in range(2)]).to_bytes(1, "little")
        dest = int(vals[2]).to_bytes(1, "little")
        print(ops.hex(), dest.hex())
        raw += ops + dest
with open("subleq.raw", "wb") as f:
    f.write(raw)
