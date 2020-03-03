import sys
import pathlib
import re

if len(sys.argv) < 2:
    print("ERROR: Please run the program including your filename as a parameter, in the format of 'python parser.py filename.ext'")
    sys.exit()

pathname = sys.argv[1]
path = pathlib.Path.cwd() / pathname

with open(path,"r") as f:
    content = []
    for line in f:
        content.append(line)

for i in range(len(content)):
    content[i] = content[i].replace("\n","")

equality = set()
connectives = set()
quantifiers = set()
variables = set()
constants = set()
predicateList = []
predicates = {}

toPop = []

for i in range(len(content)):
    if content[i][0:10] == "variables:":
        variables = set(content[i][11:].split(" "))
        toPop.append(i)
    elif content[i][0:10] == "constants:":
        constants = set(content[i][11:].split(" "))
        toPop.append(i)
    elif content[i][0:11] == "predicates:":
        predicateList = content[i][12:].split(" ")
        for i in predicateList:

        toPop.append(i)
    elif content[i][0:9] == "equality:":
        equality = set(content[i][10:].split(" "))
        toPop.append(i)
    elif content[i][0:12] == "connectives:":
        connectives = set(content[i][13:].split(" "))
        toPop.append(i)
    elif content[i][0:12] == "quantifiers:":
        quantifiers = set(content[i][13:].split(" "))
        toPop.append(i)

toPop.sort(reverse=True)
for i in toPop:
    content.pop(i)

formula = "".join(content)[9:]

print(equality,connectives,quantifiers,predicates,variables,constants)
print(formula)

while "  " in formula:
    formula = formula.replace("  "," ")

print(formula)