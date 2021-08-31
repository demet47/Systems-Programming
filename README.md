# Systems-Programming
Simulation of a compiler.

First file "Assemble-Exec" has two codes: cpu230assemble.py and cpuexec.py. Former translates an assembly language self-defined to hexedecimal machine code. As for the latter one,
it executes the instructions translated to hexadecimal instructions by the former code. It works like a code-written CPU.

The other file "LLVM IR language" has Main.java to execute and regulate the translation from a self-defined high level programming language to LLVM IR language. We give 
all the tools to parse the high-level language in ExecutionObject.java. We did intermixing our knowledge from the course Principles of Programming Languages in parallel 
to this course. Other file ErrorObject.java checks for all possible syntax errors and gives syntax error warning without creating an assembled code.
