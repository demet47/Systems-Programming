all:	Main.class ExecutionObject.class ErrorObject.class
	jar cfm mylang2ir x.txt Main.class ExecutionObject.class ErrorObject.class

Main.class: Main.java
	javac -cp . Main.java

ExecutionObject.class: ExecutionObject.java
	javac -cp . ExecutionObject.java


ErrorObject.class: ErrorObject.java
	javac -cp . ErrorObject.java
