import os
import sys
import re
from collections import *
from typing import BinaryIO


flag = True
instructions = [ "HALT", "LOAD" , "STORE", "ADD", "SUB", "INC", "DEC", "XOR", "AND", "OR", 
    "NOT", "SHL", "SHR", "NOP", "PUSH", "POP", "CMP", "JMP", "JZ", "JNZ", "JC",
    "JNC", "JA", "JAE", "JB", "JBE", "READ", "PRINT", "JE","JNE"]
registers = ["A", "B", "C", "D", "E", "S", "PC"]
hex_equivalent = {"0": "0000", "1":"0001", "2": "0010", "3": "0011", "4":"0100", "5":"0101", "6":"0110", "7":"0111",
                "8": "1000", "9": "1001", "A":"1010", "B":"1011", "C":"1100", "D":"1101", "E": "1110", "F":"1111"}
hexadecimal = ""
reg_to_hex = {"PC":"0000000000000000", "A": "0000000000000001", "B":"0000000000000010", "C": "0000000000000011", 
            "D":"0000000000000100", "E":"0000000000000101","S":"0000000000000110"}
labels = {} #stores an integer mapped to labels


f = open(sys.argv[1], 'tr')
count = 0
for line in f:
    if line[-1:] == "\n":
        line = line[:-1]
    found = re.search(r"\S+.\S+", line)
    if found:
        line = found.group(0)
    else:
        continue
    if line[-1:] == ":":
        if labels.get(line[:-1]) is not None:
                print("no multiple occurence of a label is allowed")
                flag = False
        if line[0] in ["0","1","2","3","4","5","6","7","8","9"]:
            print("wrong format of labels: digit is not allowed initially")
            flag = False
        labels[line[:-1]] = count
        count -= 3
    count += 3
f.close()

#formats a given hex string to 16 bit string by prepending appropriate amount of zeros. 
def my_format(string, code):
    if code == 0:
        zero = 6-len(string)
        prepend = "0"*zero
        string = prepend+string
        return string
    else:
        zero = 4-len(string)
        prepend = "0"*zero
        string = prepend+string
        return string


ece = sys.argv[1]
file = open(ece, 'tr')
output = open((ece[0:-4] + ".bin"), "wt")
counter = 0
#file = open("input1.asm", 'tr')
#output = open("input1.bin", "wt")

for line in file:
    
    line = line.strip()
    counter += 1
    if len(line) == 0:
        continue
    tokens = re.findall('\S+', line)
    A = tokens[0]
    if A=="NOP":
        output.write("380000\n")
        continue
    if A not in instructions:
        if A[-1:] != ':': #my program doesn't allow space between label name and ':'
            print("invalid instruction")
            flag = False
    elif counter*3 >2545656:
        print("the memory available is exceded, program too large")    
        flag = False
    else:
        if A == "JNE":
            code = instructions.index("JNZ") + 1    
        elif (A == "JE"):
            code = instructions.index("JZ") + 1
        else:
            code = instructions.index(A) + 1
        hexadecimal = "{0:06b}".format(code)
        
        if code == 1 or code == 14:
            hexadecimal += "000000000000000000"
        else:
            if (len(tokens) != 2):
                print("not a valid instruction: too many variables")
                print(A)
                print(tokens[1])
                flag = False
            B = tokens[1]
            if B in registers: #operand is given in the register
                hexadecimal += "01"
                hexadecimal += reg_to_hex[B]
            elif B[-1] == "]" and B[0] == "[":
                B = B[1:-1]
                if B in registers: #operand is a memory address given in register
                    hexadecimal += "10"
                    hexadecimal += reg_to_hex[B]
                else: #operand is a memory address
                    hexadecimal += "11"
                    hexadecimal += "{0:016b}".format(int(B,16))
                
                #this part is fuzzy, write/add after proffessor gives answer
            else: #it is immediate data
                if B[0] == "'" and B[-1] == "'":
                    hexadecimal += "00" 
                    if len(B) != 3:
                        print("invalid operand, only caracter allowed")
                        flag = False
                    else:
                        ascii_value = ord(B[1:-1])
                        if ascii_value > 255:
                            print("ascii character out of range")
                            flag = False
                        hexadecimal += "{0:016b}".format(ascii_value)
                    
                elif labels.get(B) is not None: #if the operand is a label
                    
                    hexadecimal += "00"
                    hexadecimal += "{0:016b}".format(labels.get(B))
                else: #modify this according to proffessors answer
                    if not(len(B) < 6) | (len(B)>0):
                        print("hex format exception: illegal length for hex")
                        flag = False
                    elif B[0] != "0":
                        if B[0] in ["A","B","C","D","E","F"]:
                            print("hex format exception: illegal start of hex: should start with zero")
                            flag = False
                    hexadecimal += "00"
                    B = my_format(B, 1)
                    for i in B:
                        if i not in ["A", "B", "C", "D", "E", "F", "0", "1","2","3","4","5","6","7","8","9"]:
                            print("not a valid immediate data: not a hex value")
                            flag = False
                        hexadecimal += hex_equivalent.get(i)
                        
        output.write(my_format(hex(int(hexadecimal,2))[2:], 0).upper()+"\n")

    if flag == False:
        output.close()
        os.remove((ece[0:-4] + ".bin"))
        break


file.close()