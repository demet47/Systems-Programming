import java.io.PrintWriter;
import java.util.StringTokenizer;

/**
 * object to check errors in a line
 *
 */
public class ErrorObject {
    /**
     * A boolean field named "error" which becomes true if there are any syntax
     * errors. False as default.
     */
    public boolean error = false;

    /**
     * Checks the "choose" lines
     * 
     * @param ece "choose" line to check if there are errors.
     * @return empty string if there are errors. If there are nested "choose" calls
     *         and no error, returns the original line but the inner choose function
     *         replaced with 1.
     */
    public String checkChoose(String ece) {
        while (ece.contains("choose")) {
            int a = ece.indexOf("choose");
            int b = findChoose(ece);
            if (b == 0) {
                error = true;
                return "";
            }
            if (ece.substring(a + 6, ece.indexOf("(", a + 6)).replaceAll(" ", "").length() != 0) {
                error = true;
                return "";
            }

            int choClose = b + 1;
            if (choClose == 1) { // if no closing phar exists exists and we still open a bracket
                error = true;
                return "";
            }

            String cho = ece.substring(a + 7, b); // inside choose phar
            ece = ece.substring(0, ece.indexOf("choose") + 7) + insideCheck(cho) + ece.substring(b);

            if (error == true)
                return "";

            a = ece.indexOf("choose");

            b = findChoose(ece);

            ece = ece.substring(0, a) + "1" + ece.substring(b + 1);

        }
        return ece;

    }

    /**
     * Checks the expressions of choose functions
     * 
     * @param ece line to check.
     * @return empty string if there are errors. Otherwise, returns the original
     *         line.
     */
    public String insideCheck(String ece) {
        StringTokenizer tok = new StringTokenizer(ece, ",", false);
        int i = 0;
        while (tok.hasMoreTokens() && i != 4) {
            String k = tok.nextToken();
            if (k.contains("choose")) {
                String temp = k.substring(k.indexOf("choose"), findChoose(k) + 1);
                checkChoose(temp);
                if (error == true)
                    return "";
                ece = ece.substring(0, ece.indexOf("choose")) + "1" + ece.substring(findChoose(ece) + 1);
                tok = new StringTokenizer(ece, ",", false);
                for (int j = 0; j <= i; j++) {
                    tok.nextToken();
                }
            } else {
                expressionCheck(k);
                if (error)
                    return "";
            }

            i++;
        }

        if (tok.hasMoreTokens()) {
            error = true;
            return "";
        }

        if (i < 4) {
            error = true;
            return "";
        }
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
                if (i < 0) {
                    error = true;
                    return 0;
                }
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
     * Prints the llvm script for error message
     * 
     * @param lineNum line number of syntax error
     * @param writer  PrintWriter object to write to the file
     */

    public void printError(int lineNum, PrintWriter writer) {
        writer.println("; ModuleID = 'mylang2ir'");
        writer.println("declare i32 @printf(i8*, ...)");
        writer.println("@print.str = private constant [22 x i8] c\"" + "Line " + lineNum + ": syntax error\\0A\\00\"");
        writer.println("define i32 @main() {");
        writer.println("call i32 (i8*, ...)* @printf(i8* getelementptr ([22 x i8]* @print.str, i32 0, i32 0))");
        writer.println("ret i32 0");
        writer.println("}");

    }

    /**
     * checks if the variable whose value is updated has any unaccepted characters
     * or if is there more than one assignment variable.
     * 
     * @param s assignment statement to be checked.
     */
    public void assignmentCheck(String s) {
        StringTokenizer t = new StringTokenizer(s, "=", false);
        if (t.countTokens() != 2) {
            error = true;
            return;
        }

        String varName = t.nextToken();
        if (checkTypeValidity(varName) != 1) {
            error = true;
            return;
        }
        expressionCheck(t.nextToken());
    }

    /**
     * checks if the expression statements have any syntax errors.
     * 
     * @param s expression statement to be checked.
     */
    public void expressionCheck(String s) {
        StringTokenizer tok = new StringTokenizer(s, "+/*-()", true);
        String test = s;
        test = test.replaceAll(" ", "");
        if (test.length() == 0) {
            error = true;
            return;
        }

        s = checkChoose(s);
        if (error)
            return;

        removePar(s);

    }

    /**
     * checks if the condition statements(if/while) have any syntax errors.
     * 
     * @param s condition statement line to check.
     */
    public void conditionCheck(String s) {
        s = s.replaceAll("\\(", " ( ");
        s = s.replaceAll("\\)", " ) ");
        s = s.replaceAll("\\{", " { ");
        StringTokenizer tok1 = new StringTokenizer(s, " ", false);
        String cond = tok1.nextToken();
        if (!(cond.equals("while") || cond.equals("if"))) {
            error = true;
            return;
        } else if (!(tok1.nextToken().equals("("))) {
            error = true;
            return;
        } else if (s.indexOf(")") == -1) {
            error = true;
            return;
        } else {
            String exp = s.substring((s.indexOf("(") + 1), s.lastIndexOf(")"));
            expressionCheck(exp);
            if (error)
                return;
            s = s.replaceAll(" ", "");
            if (s.substring(s.lastIndexOf(")") + 1).length() != 1) {
                error = true;
                return;
            }
        }

    }

    /**
     * Checks if there are any unnecessary characters in the closing curly bracket
     * line,
     * 
     * @param ece closing curly bracket line to check.
     */
    public void closeCheck(String ece) {
        ece = ece.replaceAll(" ", "");
        if (ece.length() != 1) {
            error = true;
            return;
        }
    }

    /**
     * Checks if the print statements have any syntax errors.
     * 
     * @param s Print statement to check.
     */
    public void printCheck(String s) {
        s = s.replaceAll("\\(", " ( ");
        s = s.replaceAll("\\)", " ) ");
        StringTokenizer tok1 = new StringTokenizer(s, " ", false);
        String cond = tok1.nextToken();
        if (!(cond.equals("print"))) {
            error = true;
            return;
        } else if (tok1.hasMoreTokens() && !(tok1.nextToken().equals("("))) {
            error = true;
            return;
        } else if (s.indexOf(")") == -1) {
            error = true;
            return;
        } else {
            String exp = s.substring((s.indexOf("(") + 1), s.lastIndexOf(")"));
            expressionCheck(exp);
            if (error)
                return;
            s = s.replaceAll(" ", "");
            if (s.substring(s.lastIndexOf(")") + 1).length() != 0) {
                error = true;
                return;
            }
        }
    }

    /**
     * removes parantheses in an expression
     * 
     * @param ece expression with parantheses
     * @return "2" if there are any errors, else the original expression.
     */
    private String removePar(String ece) {

        if (!ece.contains("(")) {
            return parser(ece);
        }

        while (ece.contains("(")) {
            int a = ece.lastIndexOf("(");
            int b = ece.indexOf(")", ece.lastIndexOf("("));
            if (b == -1) {
                error = true;
                return "2";
            }

            ece = ece.substring(0, a) + removePar(ece.substring(a + 1, b))
                    + (b == ece.length() - 1 ? "" : ece.substring(b + 1, ece.length()));
        }
        parser(ece);

        return ece;
    }

    /**
     * Takes an expression without parantheses, parses it with respect to operator
     * precedence, then checks if there are any syntax errors (e.g missing
     * operators, unaccepted characters, number format errors) in it.
     * 
     * @param ali expression to check
     * @return "1" if there are no syntax errors, "0" otherwise.
     */
    public String parser(String ali) {
        // first tokning to + -
        if (ali.contains("+") || ali.contains("-")) {
            ali = ali.replaceAll("\\+", " + ");
            ali = ali.replaceAll("\\-", " - ");
            StringTokenizer aticine = new StringTokenizer(ali, "+-", false);
            while (aticine.hasMoreTokens()) {
                String ayse = aticine.nextToken();
                if (ayse.contains("*") || ayse.contains("/")) {
                    ayse = ayse.replaceAll("\\*", " * ");
                    ayse = ayse.replaceAll("\\/", " / ");

                    StringTokenizer aticine2 = new StringTokenizer(ayse, "*/", false);

                    while (aticine2.hasMoreTokens()) {
                        String a = aticine2.nextToken();
                        StringTokenizer b = new StringTokenizer(a, " ", false);

                        if (b.countTokens() != 1) {
                            error = true;
                            return "";
                        } else {
                            a = a.replaceAll(" ", "");
                            if (checkTypeValidity(a) == 2) {
                                error = true;
                                return "";
                            }
                        }
                    }
                } else {
                    StringTokenizer b = new StringTokenizer(ayse, " ", false);
                    if (b.countTokens() != 1) {
                        error = true;
                        return "";
                    } else {
                        String a = b.nextToken();
                        a = a.replaceAll(" ", "");
                        if (checkTypeValidity(a) == 2) {
                            error = true;
                            return "";
                        }
                    }
                }
            }
        } else if (ali.contains("*") || ali.contains("/")) {
            ali = ali.replaceAll("\\*", " * ");
            ali = ali.replaceAll("\\/", " / ");
            StringTokenizer aticine2 = new StringTokenizer(ali, "*/", false);
            while (aticine2.hasMoreTokens()) {
                String a = aticine2.nextToken();
                StringTokenizer b = new StringTokenizer(a, " ", false);
                if (b.countTokens() != 1) {
                    error = true;
                    return "";
                } else {
                    String c = b.nextToken();
                    c = c.replaceAll(" ", "");
                    if (checkTypeValidity(a) == 2) {
                        error = true;
                        return "";
                    }
                }
            }
        } else {
            StringTokenizer b = new StringTokenizer(ali, " ", false);
            if (b.countTokens() != 1) {
                error = true;
                return "";
            } else {
                String a = b.nextToken();
                a = a.replaceAll(" ", "");
                if (checkTypeValidity(a) == 2) {
                    error = true;
                    return "";
                }
            }
        }
        return "1";
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
        if(s.equals("while") || s.equals("if"))
            return 2;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if ((int) ch <= 57 && (int) ch >= 48) {
                continue; // if integer
            } else if (((int) ch <= 122 && (int) ch >= 97) || ((int) ch <= 90 && (int) ch >= 65) || ch == 95)
                integer = false;
            else 
                return 2;
        }
        if (integer)
            return 0;
        else
            return 1;
    }
}