import sys
import pathlib
import re

####################################
####### FUNCTION DEFINITIONS #######
####################################

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

justFormula = ["" for x in range(length)]

for i in range(length):
    if content[i][0:9] == "equality:":
        if eqSeen:
            print(f"ERROR: Equality defined on more than one line in input file.")
            sys.exit(1)
        eqSeen = True
        eqInd = i
    elif content[i][0:12] == "connectives:":
        if connSeen:
            print(f"ERROR: Connectives defined on more than one line in input file.")
            sys.exit(1)
        connSeen = True
        connInd = i
    elif content[i][0:12] == "quantifiers:":
        if quantSeen:
            print(f"ERROR: Quantifiers defined on more than one line in input file.")
            sys.exit(1)
        quantSeen = True
        quantInd = i
    elif content[i][0:10] == "variables:":
        if varSeen:
            print(f"ERROR: Variables defined on more than one line in input file.")
            sys.exit(1)
        varSeen = True
        varInd = i
    elif content[i][0:10] == "constants:":
        if constSeen:
            print(f"ERROR: Constants defined on more than one line in input file.")
            sys.exit(1)
        constSeen = True
        constInd = i
    elif content[i][0:11] == "predicates:":
        if predSeen:
            print(f"ERROR: Predicates defined on more than one line in input file.")
            sys.exit(1)
        predSeen = True
        predInd = i
    elif content[i][0:8] == "formula:":
        if formSeen:
            print(f"ERROR: Formula beginning defined on more than one line in input file.")
            sys.exit(1)
        formSeen = True
        formInd = i
        justFormula[i] = content[i]
    else:
        justFormula[i] = content[i]

if not eqSeen:
    print(f"ERROR: Equality undefined.")
    sys.exit(1)
elif not connSeen:
    print(f"ERROR: Connectives undefined.")
    sys.exit(1)
elif not quantSeen:
    print(f"ERROR: Quantifiers undefined.")
    sys.exit(1)
elif  not varSeen:
    print(f"ERROR: Variables undefined.")
    sys.exit(1)
elif not constSeen:
    print(f"ERROR: Constants undefined.")
    sys.exit(1)
elif not predSeen:
    print(f"ERROR: Predicates undefined.")
    sys.exit(1)
elif not formSeen:
    print(f"ERROR: Formula undefined.")
    sys.exit(1)

# TODO Formula lines need to be contiguous
'''
lastLine = 0
for i in range(length):
    if justFormula[i] != "":
        if i > lastLine:
            lastLine = i

if lastLine = formInd:
    if length([x for x in justFormula if x != ""]) != 1:
        print(f"ERROR: Formula beginning defined on more than one line in input file.")
        sys.exit(1)

    else:
        searchIndex = i
        if searchIndex == 0:
        print(f"ERROR: The first line of your file must be a definition of a set or the beginning of a formula.")
        sys.exit(1)
        while searchIndex != formInd:
            searchIndex -= 1
            if searchIndex != formInd:
                if searchIndex == eqInd or searchIndex == connInd or searchIndex == quantInd or searchIndex == connInd or
'''

print("FILE CONTENTS:\n")

for i in range(length):
    content[i] = content[i].replace("\n","")

forbiddenNames = set()

connTuple = populateConn(content[connInd])
connectives = connTuple[0]
for x in connectives:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
print(f"Binary Connectives (And, Or, Implies, Iff):\n{connectives[0]} {connectives[1]} {connectives[2]} {connectives[3]}\n")
connectives = set(connectives)

negation = connTuple[1]
if negation not in forbiddenNames:
    forbiddenNames.add(negation)
else: 
    print(f"ERROR: The identifier {negation} has been used more than once. Please ensure all identifiers are unique.")
    sys.exit(1)
print(f"Negation Symbol:\n{negation}\n")
#a = set()
#a.add(negation)
#negation = a

equality = populateEq(content[eqInd])
if equality not in forbiddenNames:
    forbiddenNames.add(equality)
else: 
    print(f"ERROR: The identifier {equality} has been used more than once. Please ensure all identifiers are unique.")
    sys.exit(1)
print(f"Equality Symbol:\n{equality}\n")
#a = set()
#a.add(equality)
#equality = a

quantifiers = populateQuant(content[quantInd])
for x in quantifiers:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
print(f"Quantifiers (Exists, ForAll):\n{quantifiers[0]} {quantifiers[1]}\n")
quantifiers = set(quantifiers)

variables = populateVar(content[varInd])
for x in variables:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
varString = " ".join([x for x in variables])
print(f"Variables:\n{varString}\n")
variables = set(variables)

constants = populateConst(content[constInd])
for x in constants:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
constString = " ".join([x for x in constants])
print(f"Constants:\n{constString}\n")
constants = set(constants)

# TODO fix allowing two same-name different-arity predicates (this is a problem in the population function, because we have a dictionary that just updates the arity of the previously-seen name)

predicates = populatePred(content[predInd])
for x in predicates:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        print(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
        sys.exit(1)
predString = " ".join([f"{x} (arity {predicates[x]})" for x in predicates])
print(f"Predicates:\n{predString}\n")

formula = "".join([content[6],content[7]])[9:]
formula = formula.replace("("," ( ")
formula = formula.replace(")"," ) ")
formula = formula.replace(","," , ")
formula = " ".join(formula.split())
print(f"Formula:\n{formula}\n")

tokens = formula.split(" ")
#print(f"Token stream: {tokens}")

##################################
####### PRINTING GRAMMAR #######
##################################

## TODO Make sure it handles empty var/const/pred

grammar = []
grammar.append("Non-Terminal Symbols:\n")
grammar.append("F E T Q L C V P\n\n")
grammar.append("Terminal Symbols:\n")

predString2 = " ".join([x for x in predicates])
quantString = " ".join([x for x in quantifiers])
connString = " ".join([x for x in connectives])

grammar.append(f"( ) , {equality} {negation} {varString} {constString} {predString2} {quantString} {connString}\n\n")

grammar.append("Production Rules:\n")
grammar.append(f"F -> (E) | Q V F | {negation} F | P\n")
grammar.append(f"E -> T {equality} T | F L F\n")
grammar.append("T -> C | V\n")

quantProds = f""
for x in quantifiers:
    quantProds += f"{x} | "
quantProds = quantProds[:-3]

connProds = f""
for x in connectives:
    connProds += f"{x} | "
connProds = connProds[:-3]

constProds = f""
for x in constants:
    constProds += f"{x} | "
constProds = constProds[:-3]

varProds = f""
for x in variables:
    varProds += f"{x} | "
varProds = varProds[:-3]

predProds = f""
for key in predicates:
    predProds += f"{key}("
    v = ["V" for x in range(predicates[key])]
    predProds += ",".join(v)
    predProds += ") | "
predProds = predProds[:-3]

grammar.append(f"Q -> {quantProds}\n")
grammar.append(f"L -> {connProds}\n")
grammar.append(f"C -> {constProds}\n")
grammar.append(f"V -> {varProds}\n")
grammar.append(f"P -> {predProds}\n")

try:
    grammarPath = pathlib.Path.cwd() / "grammar.txt"
    with open(grammarPath,"w") as f:
        f.writelines(grammar)
except:
    print("ERROR: Could not print grammar to ./grammar.txt - printing to console instead")
    for x in grammar:
        print(x)

####################################
####### PARSING TOKEN STREAM #######
####################################

