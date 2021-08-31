from collections import *
import sys
import os
import textwrap
from typing import BinaryIO
#lets open a global boolean that holds if there is any runtime error or syntax error


#The class we formed to store the hardware elements of the CPU. Formed as a static class
class MyCPU:
    registers = [0,0,0,0,0,0,65535]
    S = 65534 #will decrement with each call
    ZF = 0 #zero flag
    SF = 0 #sign flag
    CF = 0 #carry flag
    memory = ['00000000'] * 64 * 1024 #default values zero
    f = "file to be initiated"
    error = False

#converts the given int to its 16 bit twos complement equivalent. Returns an 17 bit string if it overflows 16 bits 
#(in case of SUB and ADD). return type: string, parameter type: integer
def int_to_twos_complement(number):
    if number>0:
        binary_number = "{0:016b}".format(int(number))
        return binary_number
    elif number < 0:
        if len(bin(number)) > 18:
            binary_number = "{0:016b}".format(int(-number))
            binary_number = binary_number.replace("1",'x')
            binary_number = binary_number.replace("0","1")
            binary_number = binary_number.replace('x',"0")
            flipped_binary_number = "{0:016b}".format(int(binary_number,2) + 1)
            return flipped_binary_number
        else:
            binary_number = "{0:016b}".format(int(-number))
            binary_number = binary_number.replace("1",'x')
            binary_number = binary_number.replace("0","1")
            binary_number = binary_number.replace('x',"0")
            flipped_binary_number = "{0:016b}".format(int(binary_number,2) + 1)
            return flipped_binary_number
    else:
        binary_number = "{0:016b}".format(number)
        return binary_number



#turns a twos complement represenation to the corresponding integer. return type:int, parameter type:string
def twos_complement_to_int(string):
    if string[:1] == '1':
        string = string.replace("1",'x')
        string = string.replace("0","1")
        string = string.replace('x',"0")
        flipped_binary_number = int(string,2) + 1
        return (-1*flipped_binary_number)
    else:
        return int(string,2)
  


#INSTRUCTIONS BELOW




#ECE'S PART



#loads the operand to register A. All addressing modes are allowed
def LOAD(addressing, opcode):
    if addressing == 0:
        MyCPU.registers[1] = opcode
    elif addressing == 1:
        op2 = twos_complement_to_int(opcode)
        MyCPU.registers[1] = MyCPU.registers[op2]
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)
        MyCPU.registers[1] = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
    elif addressing == 3:
        X = twos_complement_to_int(opcode)
        MyCPU.registers[1] = MyCPU.memory[X] + MyCPU.memory[X+1]




#stores the content of register A to the operand. immediate data storing isn't allowed
def STORE(addressing, opcode):
    if(addressing == 0):
        print("illegal addressing mode: instruction STORE")
        MyCPU.error = True
        return
    if addressing == 1:
        op2 = twos_complement_to_int(opcode)
        MyCPU.registers[op2] = MyCPU.registers[1]
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)
        s = MyCPU.registers[1]
        first_half  = s[:len(s)//2]
        second_half = s[len(s)//2:]
        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction STORE")
            MyCPU.error = True
            return
        MyCPU.memory[MemoryInt] = first_half
        MyCPU.memory[MemoryInt+1] = second_half
    elif addressing == 3:
        X = twos_complement_to_int(opcode)
        s = MyCPU.registers[1]
        first_half  = s[:len(s)//2]
        second_half = s[len(s)//2:]
        if (X > 65534) or (X < 0):
            print("memory out of range: instruction STORE")
            MyCPU.error = True
            return
        MyCPU.memory[X] = first_half
        MyCPU.memory[X+1] = second_half
        MyCPU.registers[1] = MyCPU.memory[X] + MyCPU.memory[X+1]



#Adds the provided operand to the content of register A. Sets CF, SF, ZF accordingly
def ADD(addressing, opcode):
    if addressing == 0:
        Var1 = twos_complement_to_int(opcode)
        Var2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement((Var1 + Var2))
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Var1 + Var2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        MyCPU.registers[1] = Result

    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Var2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Var1 + Var2)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Var1 + Var2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        MyCPU.registers[1] = Result
        

    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)
        Var1 = twos_complement_to_int(MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1])
        Var2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Var1 + Var2)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction ADD")
            MyCPU.error = True
            return

        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Var1 + Var2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        MyCPU.registers[1] = Result 
    elif addressing == 3:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.memory[X] +  MyCPU.memory[X+1])
        Var2 = twos_complement_to_int(MyCPU.registers[1])
        
        if (X > 65534) or (X < 0):
            print("memory out of range: instruction ADD")
            MyCPU.error = True
            return

        Result = int_to_twos_complement(Var1 + Var2)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Var1 + Var2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        MyCPU.registers[1] = Result






#Subtracts provided operand from the contents of register A. Does the subtraction as A + (-data_of_operand). Updates CF, SF, ZF
#Used for comparisons with zero addressing mode
def SUB(addressing, opcode):
    if addressing == 0:
        opcode = twist(opcode)
        ADD(0, opcode)
    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = MyCPU.registers[X]
        Var1 = twist(Var1)
        ADD(0, Var1)
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction SUB")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Var1 = twist(Var1)
        ADD(0, Var1)
    elif addressing == 3:
        X = twos_complement_to_int(opcode)
        
        if (X > 65534) or (X < 0):
            print("memory out of range: instruction STORE")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[X] +  MyCPU.memory[X+1]
        Var1 = twist(Var1)
        ADD(0, Var1)
       


#Incremets the provided data inplace. A change is observed only in flags in case of an immediate data for a change cannot occur in
# case of an immediate data. Updates SF, CF, ZF.       
def INC(addressing, opcode):
    if addressing == 0:
        Num1 = twos_complement_to_int(opcode)
        bin1 = int_to_twos_complement(Num1 + 1)
        if len(str(bin1)) == 17:
            bin1 = bin1[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if bin1[0] == 1:  
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Num1 + 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Result = int_to_twos_complement(Var1 + 1)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Var1 + 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        MyCPU.registers[X] = Result
            
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction INC")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Num1 = twos_complement_to_int(Var1)
        Result = int_to_twos_complement(Num1 + 1)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Num1 + 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        first_half  = Result[:len(Result)//2]
        second_half = Result[len(Result)//2:]
        MyCPU.memory[MemoryInt] = first_half
        MyCPU.memory[MemoryInt+1] = second_half
        
    elif addressing == 3:
        X = twos_complement_to_int(opcode)

        if (X > 65534) or (X < 0):
            print("memory out of range: instruction INC")
            MyCPU.error = True
            return

        Num1 = twos_complement_to_int(MyCPU.memory[X] +  MyCPU.memory[X+1])
        Result = int_to_twos_complement(Num1 + 1)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Num1 + 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        first_half  = Result[:len(Result)//2]
        second_half = Result[len(Result)//2:]
        MyCPU.memory[X] = first_half
        MyCPU.memory[X+1] = second_half

                
                
                
# Decremets the provided data inplace. A change is observed only in flags in case of an immediate data for a change cannot occur in
# case of an immediate data. Updates SF, CF, ZF. 
def DEC(addressing, opcode):
    if addressing == 0:
        Num1 = twos_complement_to_int(opcode)
        bin1 = int_to_twos_complement(Num1 - 1)
        if len(str(bin1)) == 17:
            bin1 = bin1[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if bin1[0] == 1:
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Num1 - 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Result = int_to_twos_complement(Var1 - 1)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Var1 - 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        MyCPU.registers[X] = Result
            
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction DEC")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Num1 = twos_complement_to_int(Var1)
        Result = int_to_twos_complement(Num1 - 1)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Num1 - 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        first_half  = Result[:len(Result)//2]
        second_half = Result[len(Result)//2:]
        MyCPU.memory[MemoryInt] = first_half
        MyCPU.memory[MemoryInt+1] = second_half
        
    elif addressing == 3:
        X = twos_complement_to_int(opcode)

        if (X > 65534) or (X < 0):
            print("memory out of range: instruction DEC")
            MyCPU.error = True
            return

        Num1 = twos_complement_to_int(MyCPU.memory[X] +  MyCPU.memory[X+1])
        Result = int_to_twos_complement(Num1 - 1)
        if len(str(Result)) == 17:
            Result = Result[1:]
            MyCPU.CF = 1
        else:
            MyCPU.CF = 0
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
        if Num1 - 1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
        
        first_half  = Result[:len(Result)//2]
        second_half = Result[len(Result)//2:]
        MyCPU.memory[X] = first_half
        MyCPU.memory[X+1] = second_half
       
             
       
# XORs the contents of register A with the provided data. Updates SF and ZF.       
def XOR(addressing, opcode):
    if addressing == 0:
        Num1 = twos_complement_to_int(opcode)
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 ^ Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
            
        if Num1 ^ Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0
            
        MyCPU.registers[1] = Result
    
    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Var1 ^ Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0
            
        if Var1 ^ Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction XOR")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Num1 = twos_complement_to_int(Var1)
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 ^ Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 ^ Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
        
    elif addressing == 3:
        X = twos_complement_to_int(opcode)
        
        if (X > 65534) or (X < 0):
            print("memory out of range: instruction XOR")
            MyCPU.error = True
            return
        
        Var1 = MyCPU.memory[X] +  MyCPU.memory[X+1]
        Num2 = twos_complement_to_int(Var1)
        Num1 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 ^ Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 ^ Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
        

        
# ANDs the contents of register A with the provided data. Updates SF and ZF.        
def AND(addressing, opcode):
    if addressing == 0:
        Num1 = twos_complement_to_int(opcode)
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 & Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 & Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
    
    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Var1 & Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Var1 & Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction AND")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Num1 = twos_complement_to_int(Var1)
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 & Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 & Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
        
    elif addressing == 3:
        X = twos_complement_to_int(opcode)
        
        if (X > 65534) or (X < 0):
            print("memory out of range: instruction AND")
            MyCPU.error = True
            return
        
        Var1 = MyCPU.memory[X] +  MyCPU.memory[X+1]
        Num2 = twos_complement_to_int(Var1)
        Num1 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 & Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 & Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          

# ORs the contents of register A with the provided data. Updates SF and ZF.         
def OR(addressing, opcode):
    if addressing == 0:
        Num1 = twos_complement_to_int(opcode)
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 | Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 | Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
    
    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Var1 | Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Var1 | Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction OR")
            MyCPU.error = True
            return
        
        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Num1 = twos_complement_to_int(Var1)
        Num2 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 | Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 | Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
        
    elif addressing == 3:
        X = twos_complement_to_int(opcode)

        if (X > 65534) or (X < 0):
            print("memory out of range: instruction OR")
            MyCPU.error = True
            return
        
        Var1 = MyCPU.memory[X] +  MyCPU.memory[X+1]
        Num2 = twos_complement_to_int(Var1)
        Num1 = twos_complement_to_int(MyCPU.registers[1])
        Result = int_to_twos_complement(Num1 | Num2)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if Num1 | Num2 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
  
  
# Negates the provided data. Updates SF and ZF.  
def NOT(addressing, opcode):
    if addressing == 0:
        Num1 = twos_complement_to_int(opcode)
        bin1 = int_to_twos_complement(~Num1)
        
        if bin[1] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if ~Num1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = bin1
        
    
    elif addressing == 1:
        X = twos_complement_to_int(opcode)
        Var1 = twos_complement_to_int(MyCPU.registers[X])
        Result = int_to_twos_complement(~Var1)
        
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if ~Var1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
            
    elif addressing == 2:
        X = twos_complement_to_int(opcode)
        MemoryAd = MyCPU.registers[X]
        MemoryInt = twos_complement_to_int(MemoryAd)

        if (MemoryInt > 65534) or (MemoryInt < 0):
            print("memory out of range: instruction NOT")
            MyCPU.error = True
            return

        Var1 = MyCPU.memory[MemoryInt] + MyCPU.memory[MemoryInt+1]
        Num1 = twos_complement_to_int(Var1)
        Result = int_to_twos_complement(~Num1)
    
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if ~Num1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          
        
    elif addressing == 3:
        X = twos_complement_to_int(opcode)

        if (X > 65534) or (X < 0):
            print("memory out of range: instruction NOT")
            MyCPU.error = True
            return

        Num1 = twos_complement_to_int(MyCPU.memory[X] +  MyCPU.memory[X+1])
        Result = int_to_twos_complement(~Num1)
        if Result[0] == '1':
            MyCPU.SF = 1
        else:
            MyCPU.SF = 0

        if ~Num1 == 0:
            MyCPU.ZF = 1
        else:
            MyCPU.ZF = 0

        MyCPU.registers[1] = Result
          


# performs negation of a given binary string           
def twist(opcode):
    Var = twos_complement_to_int(opcode)
    opcode = int_to_twos_complement(-1*Var)
    return opcode





#DEMET'S PART




# Prints the ASCII ewuivalent character of the data from given operand to the console. 
# Prints just a single character, not multicharacter strings.
def PRINT(addressing_mode, operand):
    num = ""
    if addressing_mode == 0: #immediate addressing
        num = twos_complement_to_int(operand)

    elif addressing_mode == 1 or addressing_mode == 2: #operand in register
        reg = twos_complement_to_int(operand)
        if reg > 6 or reg < 0:
            print("invalid register")
            MyCPU.error = True
            return
        num = twos_complement_to_int(MyCPU.registers[reg])

        if addressing_mode == 2: #memory adress in register
            if (num > 65534) or (num < 0):
                print("memory out of range: instruction PRINT")
                MyCPU.error = True
                return
            num = twos_complement_to_int(MyCPU.memory[num] + MyCPU.memory[num+1])

    elif addressing_mode == 3: #operand is memory address
        index = twos_complement_to_int(operand)

        if (index > 65534) or (index < 0):
            print("memory out of range: instruction PRINT")
            MyCPU.error = True
            return

        temp = MyCPU.memory[index] + MyCPU.memory[index+1]
        num = twos_complement_to_int(temp)


    MyCPU.f.write(chr(num) + "\n")


# Reads from the console a single character and stores in a register or memory given as operand
def READ(addressing_mode, operand):
    string = input()
    if len(string) != 1:
        print('input error: a character expected')
        MyCPU.error = True
        return
    elif addressing_mode == 0:
        print('read error: reading cannot be stored as immediate data')
        MyCPU.error = True
        return

    s = ord(string)
    binary = int_to_twos_complement(s)

    if addressing_mode == 1:#to register
        reg = twos_complement_to_int(operand)
        if reg < 0 or reg > 6:
            print("invalid register")
            MyCPU.error = True
            return
        else:
            MyCPU.registers[reg] = binary
    elif addressing_mode == 2: #memory address given in register
        reg = twos_complement_to_int(operand)
        if reg > 6 or reg < 0:
            print("invalid register")
            MyCPU.error = True
            return
        num = twos_complement_to_int(MyCPU.registers[reg])
        num = twos_complement_to_int(MyCPU.memory[num] + MyCPU.memory[num+1])
        
        if (num > 65534) or (num < 0):
            print("memory out of range: instruction PRINT")
            MyCPU.error = True
            return

        MyCPU.memory[num] = binary[:8]
        MyCPU.memory[num+1] = binary[8:]
    else:#memory address
        memory = twos_complement_to_int(operand)
        
        if (memory > 65534) or (memory < 0):
            print("memory out of range: instruction PRINT")
            MyCPU.error = True
            return

        MyCPU.memory[memory] = binary[:8]
        MyCPU.memory[memory+1] = binary[8:]



#Jumps to the given address if below. Only immediate adddressing mode is allowed
def JB(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JB instruction')
       MyCPU.error = True
       return
    
    if (MyCPU.SF == 1) & (MyCPU.ZF == 0) :
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory #goes to the specified instruction

# Jumps to the given address if below or equal. Only immediate adddressing mode is allowed.
def JBE(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JBE instruction')
        MyCPU.error = True
        return
    
    if MyCPU.SF == 1 or MyCPU.ZF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if above or equal. Only immediate adddressing mode is allowed. 
def JAE(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JAE instruction')
        MyCPU.error = True
        return
    
    if (MyCPU.SF == 0) or (MyCPU.ZF == 1):
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if above. Only immediate adddressing mode is allowed.
def JA(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JA instruction')
        MyCPU.error = True
        return
    
    if MyCPU.SF == 0 and MyCPU.ZF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if carry flag is off. Only immediate adddressing mode is allowed.
def JNC(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JNC instruction')
        MyCPU.error = True
        return
    
    if MyCPU.CF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if carry flag is on. Only immediate adddressing mode is allowed.
def JC(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JC instruction')
       MyCPU.error = True
       return
    
    if MyCPU.CF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if not zero. Only immediate adddressing mode is allowed.
def JNZ(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JNZ instruction')
       MyCPU.error = True
       return
    
    if MyCPU.ZF != 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if not equal. Only immediate adddressing mode is allowed.
def JNE(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JNE instruction')
       MyCPU.error = True
       return
    
    if MyCPU.ZF != 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if zero. Only immediate adddressing mode is allowed.
def JZ(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JC instruction')
       MyCPU.error = True
       return
    
    if MyCPU.ZF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address if equal. Only immediate adddressing mode is allowed.    
def JE(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JC instruction')
       MyCPU.error = True
       return
    
    if MyCPU.ZF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory

# Jumps to the given address unconditionally. Only immediate adddressing mode is allowed.
def JMP(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JMP instruction')
       MyCPU.error = True
       return
    
    memory = twos_complement_to_int(operand)
    MyCPU.registers[0] = memory

# Compares the data given through operand with the contents of register A through A+(-operand). Updates SF, ZF, CF.
def CMP(addressing_mode, operand):
    subtract = ""
    if addressing_mode == 0:
        subtract = operand
    elif addressing_mode == 1: #operand in register
        reg = twos_complement_to_int(operand)
        if (reg > 6) or (reg < 0):
            print("invalid register: instruction CMP")
            MyCPU.error = True
            return
        subtract = MyCPU.registers[reg]
    elif addressing_mode == 2: #memory address given in register
        reg = twos_complement_to_int(operand)
        if (reg > 6) or (reg < 0):
            print("invalid register: instruction CMP")
            MyCPU.error = True
            return
        regad = MyCPU.registers[reg]
        index = twos_complement_to_int(regad)

        if (index > 65534) or (index < 0):
            print("memory out of range: instruction CMP")
            MyCPU.error = True
            return

        subtract = MyCPU.memory[index]+MyCPU.memory[index+1]
    elif addressing_mode == 3: #is memory address
        index = twos_complement_to_int(operand)

        if (index > 65534) or (index < 0):
            print("memory out of range: instruction CMP")
            MyCPU.error = True
            return

        subtract = MyCPU.memory[index] + MyCPU.memory[index+1]
    temp = MyCPU.registers[1]
    #MyCPU.registers[1] = '0000000000000000'
    SUB(0, subtract)
    MyCPU.registers[1] = temp

# Pops from the stack memory to a register given
def POP(addressing_mode, operand):
    if addressing_mode != 1:
        print('wrong addressing mode: POP instruction')
        MyCPU.error = True
        return
    if(MyCPU.S == 65534):
        print('invalid operation, stack empty: POP instruction')
    data = MyCPU.memory[MyCPU.S+2]+MyCPU.memory[MyCPU.S+3]
    MyCPU.S += 2
    reg = twos_complement_to_int(operand)
    MyCPU.registers[reg] = data

# Pushes to the stac memory from the reister given
def PUSH(addressing_mode, operand):
    if addressing_mode != 1:
        print('wrong addressing mode: PUSH instruction')
        MyCPU.error = True
        return
    reg = twos_complement_to_int(operand)
    if reg < 0 or reg > 6:
        print('invalid register: PUSH instruction')
        MyCPU.error =True
        return
    high = MyCPU.registers[reg][0:8]
    low = MyCPU.registers[reg][8:]
    MyCPU.memory[MyCPU.S] = high
    MyCPU.memory[MyCPU.S+1] = low
    MyCPU.S -= 2

# No operation. Used to avoid glitches in hardware signals.
def NOP(addressing_mode, operand):
    pass  

# Shifts the operan to right by one bit. updates SF, ZF. Only registers are allowed
def SHR(addressing_mode, operand):
    if addressing_mode != 1:
        print('invalid addressing mode: SHR instruction')
        MyCPU.error =True
        return
    reg = twos_complement_to_int(operand)
    if reg < 0 or reg > 6:
        print('invalid register: SHR instruction')
        MyCPU.error =True
        return
    data = MyCPU.registers[reg]
    value = int(data, 2) >> 1
    data = int_to_twos_complement(value)
    if data[15] == "1":
        MyCPU.SF = 1
    else:
        MyCPU.SF = 0

    if value == 0:
        MyCPU.ZF = 1
    else:
        MyCPU.ZF = 0

    MyCPU.registers[reg] = data

# Shifts the operan to left by one bit. updates SF, ZF, Cf. Only registers are allowed.
def SHL(addressing_mode, operand):
    if addressing_mode != 1:
        print('invalid addressing mode: SHR instruction')
        MyCPU.error =True
        return
    reg = twos_complement_to_int(operand)
    if reg < 0 or reg > 6:
        print('invalid register: SHR instruction')
        MyCPU.error =True
        return
    data = MyCPU.registers[reg]
    value = int(data, 2) << 1
    data = int_to_twos_complement(value)
    if len(data) == 17:
        MyCPU.CF = 1
    
    if data[15] == "1":
        MyCPU.SF = 1
    else:
        MyCPU.SF = 0

    if value == 0:
        MyCPU.ZF = 1
    else:
        MyCPU.ZF = 0

    MyCPU.registers[reg] = data




# given an instruction of 24 bits in form of binray string, returns corresponding opcode, addressing mode and operand.
# return types ==> opcode: integer (from twos complement to corresponding int code of the instruction),
# addressing_mode: integer (from 0 to 4), operand: binary string
def interprete(line):
    operand =(line[-16:])# I deleted sth here
    addressing_mode = twos_complement_to_int('0' + line[-18:-16])
    opcode = twos_complement_to_int('0'+line[:-18])
    return opcode, addressing_mode,operand

# halts the program
def HALT():
    return False





#program execution is below
demet = sys.argv[1]
file = open(demet, "tr")

MyCPU.f = open(demet[0:-4] + ".txt", 'tw')

i = 0
lineCount = 0
for line in file:
    if(len(line) == 0):
        continue
    if line[-1] == "\n":
        line = line[:-1]
    line = "{0:024b}".format(int(line, 16))
    lineList = textwrap.wrap(line, 8)
    MyCPU.memory[i] = lineList[0]
    MyCPU.memory[i+1] = lineList[1]
    MyCPU.memory[i+2] = lineList[2]
    i += 3
    lineCount+=1

while(MyCPU.registers[0] != lineCount*3):
    print(MyCPU.registers[0])
    opcode,addressing_mode, operand = interprete(MyCPU.memory[MyCPU.registers[0]] + MyCPU.memory[MyCPU.registers[0]+1] + MyCPU.memory[MyCPU.registers[0]+2] )
    temp = int(operand,2)
    MyCPU.registers[0] += 3

    if (opcode<1) or (opcode >28) or (addressing_mode < 0) or  (addressing_mode > 3):
        print('undefined instruction MyCPU.error\n')
        print(MyCPU.registers[0])
        flag = False
    elif opcode == 1:
        break
    elif opcode == 2:
        LOAD(addressing_mode,operand)
    elif opcode == 3:
        STORE(addressing_mode,operand)
    elif opcode == 4:
        ADD(addressing_mode,operand)
    elif opcode == 5:
        SUB(addressing_mode,operand)
    elif opcode == 6:
        INC(addressing_mode,operand)
    elif opcode == 7:
        DEC(addressing_mode,operand)
    elif opcode == 8:    
        XOR(addressing_mode,operand)
    elif opcode == 9:    
        AND(addressing_mode,operand)
    elif opcode == 10:
        OR(addressing_mode,operand)
    elif opcode == 11: 
        NOT(addressing_mode,operand)
    elif opcode == 12:
        SHL(addressing_mode,operand)
    elif opcode == 13:
        SHR(addressing_mode,operand)
    elif opcode == 14:
        NOP(addressing_mode,operand)
    elif opcode == 15:    
        PUSH(addressing_mode,operand)
    elif opcode == 16:
        POP(addressing_mode,operand)
    elif opcode == 17:
        CMP(addressing_mode,operand)
    elif opcode == 18:
        JMP(addressing_mode,operand)
    elif opcode == 19: #here there exists a zero flag check 
        JZ(addressing_mode,operand)
        JE(addressing_mode,operand)
    elif opcode == 20: #here there exists a zero flag check
        JNZ(addressing_mode,operand)
        #JNE(addressing_mode,operand)
    elif opcode == 21:
        JC(addressing_mode,operand)  
    elif opcode == 22:
        JNC(addressing_mode,operand)
    elif opcode == 23:    
        JA(addressing_mode,operand)
    elif opcode == 24:
        JAE(addressing_mode,operand)
    elif opcode == 25:
        JB(addressing_mode,operand) 
    elif opcode == 26:
        JBE(addressing_mode,operand)
    elif opcode == 27:    
        READ(addressing_mode,operand)
    elif opcode == 28:
        PRINT(addressing_mode,operand)


    if MyCPU.error == True:
        MyCPU.f.close()
        file.close()
        t = sys.argv[1]
        os.remove((t[0:-4] + ".bin"))
        os.remove(t[0:-4] + ".txt")
        break

