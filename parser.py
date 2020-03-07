import sys
import pathlib
import re

##############################
#### FUNCTION DEFINITIONS ####
##############################

def populateEq(line):
    equals = line[10:].split(" ")
    # TODO may be able to do this with just regex, no splitting required
    if len(equals) == 1:
        x = re.search("^[\w\\\=]+$", equals[0])
        if not x:
            print(f"ERROR: Equality symbol {equals[0]} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores, backslashes or = only. Example: \\my_eq=")
            sys.exit(1)
        else:
            return x.group()
    elif len(equals) == 0:
        print("ERROR: Equality symbol undefined")
        sys.exit(1)
    else:
        print(f"ERROR: {len(equals)} equality symbols found, please supply only 1")
        sys.exit(1)
    
def populateConn(line):
    entries = line[13:].split(" ")
    conns = []
    neg = ""
    if len(entries) == 5:
        for i in range(4):
            x = re.search("^[\w\\\]+$", entries[i])
            if not x:
                print(f"ERROR: Connective {entries[i]} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores or backslashes only. Example: \\my_conn")
                sys.exit(1)
            else:
                conns.append(x.group())
        n = re.search("^[\w\\\]+$",entries[4])
        if not n:
            print(f"ERROR: Connective {entries[4]} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores or backslashes only.")
            sys.exit(1)
        else:
            neg = entries[4]
    elif len(entries) == 0:
        print("ERROR: Connectives undefined")
        sys.exit(1)
    else: 
        print(f"ERROR: {len(entries)} connectives found. Please supply exactly 5, separated by spaces, in the following order: AND OR IMPLIES IFF NOT")
        sys.exit(1)
    return(conns,neg)

def populateQuant(line):
    entries = line[13:].split(" ")
    quants = []
    if len(entries) == 2:
        for q in entries:
            x = re.search("^[\w\\\]+$", q)
            if not x:
                print(f"ERROR: Quantifier {q} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores or backslashes only. Example: \\my_quant")
                sys.exit(1)
            else:
                quants.append(x.group())
    elif len(entries) == 0:
        print("ERROR: Quantifiers undefined")
        sys.exit(1)
    else: 
        print(f"ERROR: {len(entries)} quantifiers found. Please supply exactly 2, separated by spaces, in the following order: Exists ForAll")
        sys.exit(1)
    return(quants)

def populatePred(line):
    entries = line[12:].split(" ")
    if len(entries) == 0:
        print("No predicates defined.")
        return
    predicates = {}
    for j in entries:
        x = re.search("^\w+\[\d+\]$",j)
        if not x:
            print(f"ERROR: Predicate {j} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters or underscores only, followed immediately by an integer greater than 0 enclosed in square brackets. Example: my_pred[5]")
            sys.exit(1)
        else:
            y = re.search("\[\d+\]",j)
            num = y.group()[1:][:-1]
            if num.isdigit():
                arity = int(num)
                if arity > 0:
                    predicates[j[:y.span()[0]]] = arity
                else:
                    print(f"ERROR: Arity {num} of predicate {j} is an integer less than 1.")
                    sys.exit(1)
            else:
                print(f"ERROR: Arity {num} of predicate {j} is not an integer.")
                sys.exit(1)
    return(predicates)

def populateVar(line):
    entries = line[11:].split(" ")
    ## TODO make this a regex of "setName: followed by 0+ spaces" to check for empty string
    if len(entries) == 0:
        print("No variables defined.")
        return
    variables = []
    for j in entries:
        x = re.search("^\w+$",j)
        if not x:
            print(f"ERROR: Variable {j} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters or underscores only. Example: my_var")
            sys.exit(1)
        else:
            variables.append(x.group())
    return(variables)

def populateConst(line):
    entries = line[11:].split(" ")
    if len(entries) == 0:
        print("No constants defined.")
        return
    constants = []
    for j in entries:
        x = re.search("^\w+$",j)
        if not x:
            print(f"ERROR: Constant {j} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters or underscores only. Example: my_const")
            sys.exit(1)
        else:
            constants.append(x.group())
    return(constants)

##############################
####### FILE INGESTION #######
##############################

if len(sys.argv) != 2:
    print("ERROR: Invalid amount of arguments. Please run the program including your filename as a parameter, in the format of 'python parser.py filename.ext'")
    sys.exit(1)

filename = sys.argv[1]
path = pathlib.Path.cwd() / filename

with open(path,"r") as f:
    content = []
    for line in f:
        content.append(line)

if not content:
    print("ERROR: Empty file")
    sys.exit(1)

## TODO Check there are at least 7 lines, and that exactly 7 of them start "setName:" - otherwise, funky behaviour occurs. FInd the indices of the lines here, and supply them to the logic later.
# if content[i][0:10] == "variables:":

length = len(content)

if length < 7:
    print(f"ERROR: A file needs at least 7 lines to be valid, but {filename} has {length}.")
    sys.exit(1)

eqSeen = False
connSeen = False
quantSeen = False
varSeen = False
constSeen = False
predSeen = False
formSeen = False

eqInd = 0
connInd = 0
quantInd = 0
varInd = 0
constInd = 0
predInd = 0
formInd = 0

for line in content:
    if line[0:10] == "variables:":
        varSeen = True






for i in range(length):
    content[i] = content[i].replace("\n","")

# TODO Make the indices use the line indices found by line-checker

forbiddenNames = set()

connTuple = populateConn(content[4])
connectives = connTuple[0]
for x in connectives:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
print(f"Binary Connectives AND: {connectives[0]} OR: {connectives[1]} IMPLIES: {connectives[2]} IFF: {connectives[3]}")
connectives = set(connectives)

negation = connTuple[1]
print(f"Negation Symbol: {negation}")
if negation not in forbiddenNames:
    forbiddenNames.add(negation)
else: 
    print(f"ERROR: The identifier {negation} has been used more than once. Please ensure all identifiers are unique.")
    sys.exit(1)
negation = set(negation)

equality = populateEq(content[3])
if equality not in forbiddenNames:
    forbiddenNames.add(equality)
else: 
    print(f"ERROR: The identifier {equality} has been used more than once. Please ensure all identifiers are unique.")
    sys.exit(1)
print(f"Equality Symbol: {equality}")
equality = set(equality)

quantifiers = populateQuant(content[5])
for x in quantifiers:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
print(f"Quantifiers Exists: {quantifiers[0]} ForAll: {quantifiers[1]}")
quantifiers = set(quantifiers)

variables = populateVar(content[0])
for x in variables:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
varString = " ".join([x for x in variables])
print(f"Variables: {varString}")
variables = set(variables)

constants = populateConst(content[1])
for x in constants:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
constString = " ".join([x for x in constants])
print(f"Constants: {constString}")
constants = set(constants)

# TODO fix allowing two same-name different-arity predicates (this is a problem in the population function, because we have a dictionary that just updates the arity of the previously-seen name)

predicates = populatePred(content[2])
for x in predicates:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
predString = " ".join([f"{x} (arity {predicates[x]})" for x in predicates])
print(f"Predicates: {predString}")

formula = "".join(content)[9:]
formula = " ".join(formula.split())

#print(f"Formula: {formula}")