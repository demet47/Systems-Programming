import java.util.ArrayList;
import java.util.HashSet;
import java.util.StringTokenizer;

/**
 * Execution object of the program. All executions of the lines are made with
 * this object's methods.
 */
public class ExecutionObject {
    /**
     * A hash set of string which stores the non-temporary and declared variables in
     * the program.
     */
    public HashSet<String> declaredVariables = new HashSet<String>();
    /**
     * An integer variable used to name temporary variables arbitarily.(e.g %t0,
     * %t1). Starts from 0.
     */
    public int number = 0;
    /**
     * An arraylist of string which stores the lines to print in .ll file. To keep
     * the desired order of lines in outputs, the lines were not printed directly to
     * the .ll file.
     * 
     */
    public ArrayList<String> outputs = new ArrayList<String>();
    /**
     * An integer variable used to name the variables which stores the results of
     * choose functions.(e.g cho1, cho2). Starts from 1.
     */
    public int chooseNum = 1;
    /**
     * An integer variable to keep track of how deep are nested choose functions.
     */
    public int depth = 0;

    /**
     * Checks if the given string is an assignment statement, a closing curly
     * bracket, an opening curly bracket or a print line.
     * 
     * @param ece line to check
     * @return 1 if assignment statement, 2 if opening curly bracket, 3 if closing
     *         curly bracket, 4 if print statement and 0 if an error line.
     */
    public int typeChecker(String ece) {
        if (ece.contains("=")) {
            return 1;
        } else if (ece.contains("{")) {
            return 2;
        } else if (ece.contains("}")) {
            return 3;
        } else if (ece.contains("print")) {
            return 4;
        } else {
            return 0;
        }
    }

    /**
     * A recursive function which prints the llvm code for a choose function. If
     * there are nested choose functions, it replaces the result of deepest choose
     * with the choose function itself. Keeps going until all choose functions are
     * evaluated.
     * 
     * @param ece choose statement
     * @return evaluated value
     */

    public String choose(String ece) {

        // true ise br yap çık
        boolean dummy = false;
        declaredVariables.add("cho" + chooseNum);
        outputs.add("br label %choose" + chooseNum);
        outputs.add("choose" + chooseNum + ":");
        String[] variables = new String[4];
        int ab = ece.indexOf("(");
        int bc = findChoose(ece);
        String exp = ece.substring(ab + 1, bc); // choose un ici
        StringTokenizer a = new StringTokenizer(exp, ",", false);
        int i = 0;
        while (a.hasMoreTokens()) {
            String tempE = a.nextToken();
            if (tempE.contains("choose")) {
                dummy = true;
                depth++;
                // chooseNum++;
                int ef = exp.indexOf("(");
                int cd = findChoose(exp);
                String s = exp.substring(ef, cd + 1);
                s = "choose" + s;
                chooseNum++;
                exp = choose(exp);
                // exp = exp.substring(0, exp.indexOf("choose"))+ "cho" + (chooseNum) +
                // exp.substring(bc+1);
                // exp = exp.substring(0, (ab-6))+ "cho" +(chooseNum-1) + exp.substring(bc+1);
                chooseNum -= 2;
                a = new StringTokenizer(exp, ",", false);
                i = 0;
                // variables[i] = "cho" + (chooseNum-1);
                // System.out.println(ece);
            } else {
                tempE = tempE.replaceAll(" ", "");
                if (variables[i] != (null)) {
                    i++;
                    continue;
                }
                variables[i] = removeParan(tempE);
                if (variables[i].contains("~")) {
                    variables[i] = variables[i].substring(1);

                } else if (!variables[i].contains("%")) {
                    // outputs.add("%t" + number++ +" = load i32* %" + variables[i]);
                    variables[i] = "%t" + (number - 1);
                }
                i++;
            }
        }
        // outputs.add("\ndefine i32 @choose"+"(i32 "+variables[0]+", i32 "+variables[1]
        // +", i32 "+variables[3] + ", i32 "+variables[4] + ") {");
        // outputs.add("\nentry:");
        outputs.add("%t" + number++ + " = icmp sgt i32 " + variables[0] + ", 0");
        outputs.add("br i1 %t" + (number - 1) + ", label %greaterEnd" + chooseNum + ", label %equalCheck" + chooseNum);
        outputs.add("greaterEnd" + chooseNum + ":");
        outputs.add("store i32 " + variables[2] + ", i32* %cho" + chooseNum);
        outputs.add("br label %end" + chooseNum);
        outputs.add("equalCheck" + chooseNum + ":");
        outputs.add("%t" + number++ + " = icmp eq i32 " + variables[0] + ", 0");
        outputs.add("br i1 %t" + (number - 1) + ", label %equalEnd" + chooseNum + ", label %negativeEnd" + chooseNum);
        outputs.add("equalEnd" + chooseNum + ":");
        outputs.add("store i32 " + variables[1] + ", i32* %cho" + chooseNum);
        outputs.add("br label %end" + chooseNum);
        outputs.add("negativeEnd" + chooseNum + ":");
        outputs.add("store i32 " + variables[3] + ", i32* %cho" + chooseNum);
        outputs.add("br label %end" + chooseNum);
        outputs.add("end" + chooseNum + ":");

        if (dummy) {
            // chooseNum += 2;
            dummy = false;
            int temp = ece.length();
            if (bc == temp - 1) {
                ece = ece.substring(0, (ab - 6)) + "cho" + (chooseNum) + ece.substring(bc);
                ece = ece.substring(0, ece.length() - 1);
            } else {
                ece = ece.substring(0, (ab - 6)) + "cho" + (chooseNum) + ece.substring(bc + 1);
            }

        } else {
            // chooseNum++;
            int temp = ece.length();
            if (bc == temp - 1) {
                ece = ece.substring(0, (ab - 6)) + "cho" + (chooseNum) + ece.substring(bc);
                ece = ece.substring(0, ece.length() - 1);
            } else {
                ece = ece.substring(0, (ab - 6)) + "cho" + (chooseNum) + ece.substring(bc + 1);
                // choose = false;
            }
        }
        chooseNum++;
        return ece;

    }

    /**
     * Finds the first and last index of parantheses in a choose function line.
     * 
     * @param ece choose statement
     * @return index of closing parantheses
     */
    public int findChoose(String ece) {
        int i = 0;
        boolean first = true;
        int index = 0;
        for (int k = ece.indexOf("choose"); k < ece.length(); k++) {
            if (ece.charAt(k) == ')') {
                first = false;
                i--;
            } else if (ece.charAt(k) == '(') {
                first = false;
                i++;
            }
            if (i == 0 && !first) {
                index = k;
                break;
            }
        }
        // index += ece.indexOf("choose");
        return index;

    }

    /**
     * evaluates the assignment statements. Parses them with respect to = sign and
     * evaluates the expression part.
     * 
     * @param ece assignment statement
     */
    public void expression(String ece) {

        String temporary = "";

        if (ece.contains("=")) {
            StringTokenizer dec = new StringTokenizer(ece, "=", false);
            String varName = dec.nextToken();
            String value = dec.nextToken();
            if (value.contains("choose")) {
                value = choose(value);
                chooseNum += depth;
                depth = 0;
            }
            temporary = removeParan(value);
            // temporary = aticine(value);
            if (temporary.contains("%")) {
                outputs.add("store i32 " + temporary + ", i32* %" + varName);
            } else if (temporary.charAt(0) != '~') {
                outputs.add("store i32 %t" + (number - 1) + ", i32* %" + varName);
            } else {
                outputs.add("store i32 " + value + ", i32* %" + varName);
            }
            declaredVariables.add(varName);
            // if(!t[0]){
            // outputs.add("end:");
            // }
        }
    }

    /**
     * evaluates the print statements
     * 
     * @param ece print statement
     */
    public void print(String ece) {
        StringTokenizer cond = new StringTokenizer(ece, "()", false);
        cond.nextToken();
        String printStatement = cond.nextToken();
        printStatement = aticine(printStatement);

        outputs.add("call i32 (i8*, ...)* @printf(i8* getelementptr ([4 x i8]* @print.str, i32 0, i32 0), i32 " + "%t"
                + (number - 1) + " )");
    }

    /**
     * evaluates the condition statements.
     * 
     * @param ece condition statement
     * @return 1 if the condition statement is a while statements, 2 if it is an if
     *         statement.
     */
    public int conditioner(String ece) {
        StringTokenizer cond = new StringTokenizer(ece, "()", false);
        String s = cond.nextToken();
        if (s.equals("while")) {
            outputs.add("br label %whcond");
            outputs.add("\n");
            outputs.add("whcond:");
            int a = ece.indexOf("(") + 1;
            int b = ece.lastIndexOf(")");
            String temporary = removeParan(ece.substring(a, b));
            if (temporary.contains("%"))
                outputs.add("%t" + number++ + " = icmp ne i32 " + temporary + ", 0");
            else if (temporary.charAt(0) != '~') {
                // outputs.add("%t" + number++ + " = load i32* %" + temporary);
                outputs.add("%t" + number++ + " = icmp ne i32 %t" + (number - 2) + ", 0");
            } else {
                outputs.add("%t" + number++ + " = icmp ne i32 " + temporary.substring(1) + ", 0");
            }
            outputs.add("br i1 %t" + (number - 1) + ", label %whbody, label %whend");
            outputs.add("\n");
            outputs.add("whbody:");
            return 1;

        } else if (s.equals("if")) {
            outputs.add("br label %ifcond");
            outputs.add("\n");
            outputs.add("ifcond:");
            int a = ece.indexOf("(") + 1;
            int b = ece.lastIndexOf(")");
            String temporary = removeParan(ece.substring(a, b));
            if (temporary.contains("%"))
                outputs.add("%t" + number++ + " = icmp ne i32 " + temporary + ", 0");
            else if (temporary.charAt(0) != '~') {
                outputs.add("%t" + number++ + " = icmp ne i32 %t" + (number - 2) + ", 0");
            } else
                outputs.add("%t" + number++ + " = icmp ne i32 " + temporary.substring(1) + ", 0");

            outputs.add("br i1 %t" + (number - 1) + ", label %ifbody, label %ifend");
            outputs.add("\n");
            outputs.add("ifbody:");
            return 2;

        }
        return 0;

    }

    /**
     * Checks if a variable has any unaccepted characters.(e.g !,*,-)
     * 
     * @param s variable
     * @return 2 if there is syntax error, 0 if variable is integer, 1 if it is an
     *         accepted variable name.
     */
    public int checkTypeValidity(String s) {
        StringTokenizer tok = new StringTokenizer(s, " ", false);
        if (tok.countTokens() != 1)
            return 2;
        s = s.replaceAll(" ", "");
        boolean integer = true;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if ((int) ch <= 57 && (int) ch >= 48)
                continue; // if integer
            else if (((int) ch <= 122 && (int) ch >= 97) || ((int) ch <= 132 && (int) ch >= 101))
                integer = false;
            else
                return 2;
        }
        if (integer)
            return 0;
        else
            return 1;
    }

    /**
     * removes parantheses in an expression while evaluating the expressions inside
     * the parantheses.
     * 
     * @param ece expression with parantheses
     * @return the original expression but the temporary variable which holds the
     *         result of the expression inside the parantheses is replaced.
     */
    public String removeParan(String ece) {
        if (!ece.contains("(")) {
            return aticine(ece);
        }

        while (ece.contains("(")) {
            // System.out.println(ece);
            int a = ece.lastIndexOf("(");
            int b = ece.indexOf(")", ece.lastIndexOf("("));
            String tmp = ece.substring(a + 1, b);
            tmp = removeParan(tmp);
            tmp = tmp.charAt(0) == '~' ? tmp.substring(1) : tmp;
            ece = ece.substring(0, a) + tmp + (b == ece.length() - 1 ? "" : ece.substring(b + 1, ece.length()));
            // System.out.println(ece);
        }
        return aticine(ece);
    }

    /**
     * A method to parse and execute the algebraic expression without parantheses
     * with respect to operator precedence.
     * 
     * @param islem An arraylist of string which contains th operands and the
     *              operators.
     */
    public void calculation(ArrayList<String> islem) {
        while (islem.size() != 1) {
            int i = 0;

            // boolean integerA = true;
            try {
                int a = Integer.parseInt(islem.get(i));
            } catch (NumberFormatException e) {
                // integerA = false;
                if (islem.get(i).charAt(0) != '%') { // here means the variable is neither an integer nor a %t variable
                    outputs.add("%t" + number + " = load i32* %" + islem.get(i));
                    declaredVariables.add(islem.get(i));
                    islem.set(i, "%t" + number++);
                }
            }

            // boolean integerB = true;
            try {
                int a = Integer.parseInt(islem.get(i + 2));
            } catch (NumberFormatException e) {
                if (islem.get(i + 2).charAt(0) != '%') {
                    outputs.add("%t" + number + " = load i32* %" + islem.get(i + 2));
                    declaredVariables.add(islem.get(i + 2));
                    islem.set(i + 2, "%t" + number++);
                }
                // integerB = false;
            }

            String exp = islem.get(i + 1);

            switch (exp) {

            case "*":
                // %t6 = add i32 %t4, %t5
                outputs.add("%t" + number++ + "= mul i32 " + islem.get(i) + ", " + islem.get(i + 2));
                islem.set(0, "%t" + (number - 1));
                islem.remove(i + 1);
                islem.remove(i + 1);

                break;
            case "/":

               
                outputs.add("%t" + number++ + " = sdiv i32 " + islem.get(i) + ", " + islem.get(i + 2));
                islem.set(0, "%t" + (number - 1));
                islem.remove(i + 1);
                islem.remove(i + 1);

                break;
            case "+":
                outputs.add("%t" + number++ + " = add i32 " + islem.get(i) + ", " + islem.get(i + 2));
                islem.set(0, "%t" + (number - 1));
                islem.remove(i + 1);
                islem.remove(i + 1);

                break;
            case "-":
                outputs.add("%t" + number++ + " = sub i32 " + islem.get(i) + ", " + islem.get(i + 2));
                islem.set(0, "%t" + (number - 1));
                islem.remove(i + 1);
                islem.remove(i + 1);

                break;
            }

        }
    }

    /**
     * Takes an expression without parantheses, parses it with respect to operator
     * precedence, then evaluates the algebraic expressions using helper methods.
     * 
     * @param ali algebraic expression to evaluate
     * @return the temporary variable which is the result of the algebraic
     *         expression.
     */
    public String aticine(String ali) {
        ArrayList<String> son = new ArrayList<String>();

        if (ali.contains("+") || ali.contains("-")) {

            StringTokenizer aticine = new StringTokenizer(ali, "+-", true);
            while (aticine.hasMoreTokens()) {
                ArrayList<String> islem = new ArrayList<String>();
                String ayse = aticine.nextToken();
                if (ayse.contains("*") || ayse.contains("/")) {

                    StringTokenizer aticine2 = new StringTokenizer(ayse, "*/", true);
                    while (aticine2.hasMoreTokens()) {
                        String exp = aticine2.nextToken();
                        islem.add(exp);

                    }
                    calculation(islem);
                    son.add(islem.get(0));
                } else {
                    son.add(ayse);
                }
            }
        } else if (ali.contains("*") || ali.contains("/")) {

            StringTokenizer aticine = new StringTokenizer(ali, "*/", true);
            ArrayList<String> islem = new ArrayList<String>();
            while (aticine.hasMoreTokens()) {
                String exp = aticine.nextToken();

                islem.add(exp);

            }
            calculation(islem);
            son.add(islem.get(0));

        } else {
            try {
                int a = Integer.parseInt(ali);
                return "~" + ali;
            } catch (NumberFormatException e) {
                if (ali.charAt(0) != '%') {
                    outputs.add("%t" + number++ + " = load i32* %" + ali);
                    declaredVariables.add(ali);
                    return ali;
                } else {
                    return ali;
                }
            }
        }

        calculation(son);
        return son.get(0);
    }
}