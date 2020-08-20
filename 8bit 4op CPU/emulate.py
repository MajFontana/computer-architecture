import os
import time

BIN = "sum.bin"
DATASIZE = 6
CMDSIZE = 2 + DATASIZE

with open(BIN, "r") as f:
    data = f.read()

RAM = ["0" * (DATASIZE) for i in range(2 ** DATASIZE)]
RAM[0] = "001001"
RAM[1] = "001010"
PC = 0
REG = "0" * DATASIZE
run = True
while run:
    os.system("cls")
    print("RAM:")
    print("\n".join(RAM[:8]))
    print()
    print("REG:")
    print(REG)
    print()
    print("PC:")
    print(PC)
    print()
    print("---- EXECUTE: ----")
    cmd = data[PC * CMDSIZE:(PC + 1) * CMDSIZE]
    PC += 1
    opcode = cmd[:2]
    operand = int(cmd[2:], 2)
    if opcode == "00":
        print("NAND from %i" % operand)
        print("   ", REG, "NAND", RAM[operand])
        REG = RAM[operand][:-1] + str(int(not (int(RAM[operand][-1]) and int(REG[-1]))))
        print(REG)
    elif opcode == "01":
        print("SHR")
        print("   ", "SHR", REG)
        REG = REG[-1] + REG[:-1]
        print(REG)
    elif opcode == "10":
        print("STR to %i" % operand)
        RAM[operand] = REG
    elif opcode == "11":
        print("JZ to %i" % operand)
        print("   ", REG)
        if REG[-1] == "0":
            print("    Condition satisfied")
            if PC - 1 == operand:
                run = False
                print("    HALT")
            else:
                PC = operand
                print("   ", "-->", PC)
    input()
