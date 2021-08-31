
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.lang.String;

/**
 * Main class of the program.
 * 
 * 
 * @author Ecenur Sezer 
 * @author Demet Yayla
 */
public class Main {

    /**
     * Main method of the program. Reading the lines is done in here. Takes an
     * argument input file to read. After the lines are read, they are sent to
     * specify their type. After their type is specified, they are sent to execution
     * methods according to their types. If there are empty lines or comment lines,
     * they are skipped. Finally, a PrintWriter object prints the llvm ir
     * instructions to given argument output file.
     * 
     * 
     * @param args
     * @throws FileNotFoundException
     */
    public static void main(String[] args) throws FileNotFoundException {

        File input = new File(args[0]);
        Scanner x = new Scanner(input);
        String inputName = input.getName();
        String outputName = inputName.substring(0, inputName.length()-3);
        File output = new File(outputName+ ".ll");
        PrintWriter writer = new PrintWriter(output);
        ErrorObject syn = new ErrorObject();
        ExecutionObject exe = new ExecutionObject();
        int while_if = 0;
        int lineNum = 0 - 1;
        boolean whif = false;

        // reading line-by-line
        while (x.hasNextLine() && !syn.error) {
            String ece = x.nextLine();
            lineNum++;
            ece = ece.replaceAll("\t", " ");
            if (ece.contains("#"))
                ece = ece.substring(0, ece.indexOf("#"));
            int type = exe.typeChecker(ece);
            int keep = 0;
            switch (type) {
            case 1: // assignment
                syn.assignmentCheck(ece);
                ece = ece.replaceAll(" ", "");
                if (!syn.error)
                    exe.expression(ece);
                else {
                    break;
                }
                break;
            case 2: // while/if entrance
                keep = lineNum;
                if (whif) {
                    syn.error = true;
                    break;
                }
                syn.conditionCheck(ece);
                ece = ece.replaceAll(" ", "");
                if (syn.error) {
                    break;
                }
                whif = true;
                while_if = exe.conditioner(ece);
                break;
            case 3: // while/if enclosure
                syn.closeCheck(ece);
                if (syn.error || !whif) {
                    syn.printError(keep, writer);
                    writer.close();
                    x.close();
                    return;
                }
                if (while_if == 1) {
                    exe.outputs.add("br label %whcond");
                    exe.outputs.add("\n");
                    exe.outputs.add("whend:" + "\n");
                } else if (while_if == 2) {
                    exe.outputs.add("br label %ifend");
                    exe.outputs.add("\n");
                    exe.outputs.add("ifend:" + "\n");
                }
                whif = false;
                break;
            case 4: // print
                syn.printCheck(ece);
                ece = ece.replaceAll(" ", "");
                if (syn.error) {
                    break;
                }
                exe.print(ece);

                break;

            case 0: // irrelevant lines
                ece = ece.replaceAll(" ", "");
                if (ece.length() == 0) {
                    continue;
                }
                syn.error = true;
                break;
            }
        }

        // checking syntax errors
        if (syn.error) {
            syn.printError(lineNum, writer);
            writer.close();
            x.close();
            return;
        }
        if (whif) {
            syn.printError(lineNum, writer);
            writer.close();
            x.close();
            return;
        }

        // writing
        writer.println("; ModuleID = \'mylang2ir\' \n" + "declare i32 @printf(i8*, ...)\n"
                + "@print.str = constant [4 x i8] c\"%d\\0A\\00\" \n\n" + "define i32 @main() {");
        exe.outputs.add("\nret i32 0");
        exe.outputs.add("\n }");

        for (String s : exe.declaredVariables) {
            writer.println("%" + s + " = alloca i32");
        }
        writer.println();
        for (String s : exe.declaredVariables) {
            writer.println("store i32 0, i32* %" + s);
        }
        writer.println();

        for (String s : exe.outputs) {
            writer.println(s);
        }
        writer.close();
        x.close();
    }
}