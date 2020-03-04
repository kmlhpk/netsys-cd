import sys
import pathlib
import re

if len(sys.argv) != 2:
    print("ERROR: Invalid amount of arguments. Please run the program including your filename as a parameter, in the format of 'python parser.py filename.ext'")
    sys.exit(1)

pathname = sys.argv[1]
path = pathlib.Path.cwd() / pathname

with open(path,"r") as f:
    content = []
    for line in f:
        content.append(line)

if not content:
    print("ERROR: Empty file")

for i in range(len(content)):
    content[i] = content[i].replace("\n","")

equality = set()
negation = set()
connectives = set()
quantifiers = set()
variables = set()
constants = set()
predicates = {}

toPop = []

for i in range(len(content)):
    if content[i][0:9] == "equality:":
        equality = set(content[i][10:].split(" "))
        toPop.append(i)

    elif content[i][0:12] == "connectives:":
        connectives = set(content[i][13:].split(" "))
        toPop.append(i)

    elif content[i][0:12] == "quantifiers:":
        quantifiers = set(content[i][13:].split(" "))
        toPop.append(i)

    elif content[i][0:10] == "variables:":
        variableList = content[i][11:].split(" ")
        # Should count Not in its own set, like equality
        for j in range(len(variableList)-1):
            x = re.search("\w+",variableList[j])
            if not x:
                print(f"ERROR: Variable {j} is formatted in an invalid way. Ensure it is a mix of alphanumeric characters and underscores only.")
            else:
        toPop.append(i)

    elif content[i][0:10] == "constants:":
        constants = set(content[i][11:].split(" "))
        toPop.append(i)

    elif content[i][0:11] == "predicates:":
        predicateList = content[i][12:].split(" ")
        for j in predicateList:
            x = re.search("^\w+\[\d+\]$",j)
            if not x:
                print(f"ERROR: Predicate {j} is formatted in an invalid way. Program could not determine arity.")
            else:
                y = re.search("\[\d+\]",j)
                num = y.group()[1:][:-1]
                if num.isdigit():
                    arity = int(num)
                    if arity > 0:
                        predicates[j[:y.span()[0]]] = arity
                    else:
                        print(f"ERROR: Arity {num} of predicate {j} is an integer less than 1.")
                else:
                    print(f"ERROR: Arity {num} of predicate {j} is not an integer.")
        toPop.append(i)

toPop.sort(reverse=True)
for i in toPop:
    content.pop(i)

print()
print(predicates)
print()

formula = "".join(content)[9:]
formula = " ".join(formula.split())

print(formula)