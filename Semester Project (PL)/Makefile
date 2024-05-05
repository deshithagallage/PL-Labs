# Makefile for RPAL Interpreter

# Compiler
CC = python

# Interpreter script
INTERPRETER = myrpal.py

# Test script
TEST_SCRIPT = test.py

# Directory for test cases
TEST_DIR = test_cases

# Flags for executing the interpreter
INTERPRETER_FLAGS = 

# Target: Run the interpreter with a specific file
run:
	$(CC) $(INTERPRETER) $(INTERPRETER_FLAGS)

# Target: Run the interpreter with AST printing
ast:
	$(CC) $(INTERPRETER) -ast $(INTERPRETER_FLAGS)

# Target: Run all test cases
test:
	$(CC) $(TEST_SCRIPT)

# Target: Clean generated files
clean:
	rm -rf output_files

# Phony targets
.PHONY: run ast test clean
