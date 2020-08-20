import random

ASSEMBLED = "assembled.bin"
RAM_INIT = {0: 13, 1: 29, 12: 0, 13: 255, 14: 1, 15: 0}

with open(ASSEMBLED, "rb") as f:
    raw = f.read()

ram = [RAM_INIT[i] if i in RAM_INIT else random.randint(0, 255) for i in range(16)]
rom = raw.ljust(256, b"\x00")
num = list(rom)
sequence = [(num[i] >> 4 , num[i] & 0x0F, num[i + 1]) for i in range(0, len(num), 2)]

pc = 0
counter = 0
halt = False
while not halt:
    counter += 1
    operation = sequence[pc // 2]
    ram[operation[1]] = (ram[operation[1]] - ram[operation[0]]) & 0xFF
    if ram[operation[1]] == 0 or ram[operation[1]] > 127:
        pc = operation[2]
    else:
        pc += 2
    if pc == 255:
        halt = True

print("Program took %i operations to halt (%i clock cycles)" % (counter, counter * 3))
print("Final RAM image:")
for i in range(16):
    print("    %i: %i" % (i, ram[i]))
