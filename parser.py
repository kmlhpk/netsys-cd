import sys
import pathlib
import re
import graphviz as gv

################################
####### LOGGING FUNCTION #######
################################

def log(message):
    try:
        logPath = pathlib.Path.cwd() / "log.log"
        with open(logPath,"w") as f:
            f.write(message)
        print("Message successfully printed to ./log.log - exiting program.")
    except:
        print("ERROR: Could not print grammar to ./log.log - printing to console instead.")
        print(message)
        print("Exiting program.")
    sys.exit()

###################################################
####### FILE INGESTION FUNCTION DEFINITIONS #######
###################################################

def populateEq(line):
    equals = line[10:].split(" ")
    # TODO may be able to do this with just regex, no splitting required
    if len(equals) == 1:
        x = re.search("^[\w\\\=]+$", equals[0])
        if not x:
            log(f"ERROR: Equality symbol {equals[0]} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores, backslashes or = only. Example: \\my_eq=")
        else:
            return x.group()
    elif len(equals) == 0:
        log("ERROR: Equality symbol undefined")
    else:
        log(f"ERROR: {len(equals)} equality symbols found, please supply only 1")
    
def populateConn(line):
    entries = line[13:].split(" ")
    conns = []
    neg = ""
    if len(entries) == 5:
        for i in range(4):
            x = re.search("^[\w\\\]+$", entries[i])
            if not x:
                log(f"ERROR: Connective {entries[i]} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores or backslashes only. Example: \\my_conn")
            else:
                conns.append(x.group())
        n = re.search("^[\w\\\]+$",entries[4])
        if not n:
            log(f"ERROR: Connective {entries[4]} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores or backslashes only.")
        else:
            neg = entries[4]
    elif len(entries) == 0:
        log("ERROR: Connectives undefined")
    else: 
        log(f"ERROR: {len(entries)} connectives found. Please supply exactly 5, separated by spaces, in the following order: And Or Implies Iff Not")
    return(conns,neg)

def populateQuant(line):
    entries = line[13:].split(" ")
    quants = []
    if len(entries) == 2:
        for q in entries:
            x = re.search("^[\w\\\]+$", q)
            if not x:
                log(f"ERROR: Quantifier {q} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters, underscores or backslashes only. Example: \\my_quant")
            else:
                quants.append(x.group())
    elif len(entries) == 0:
        log("ERROR: Quantifiers undefined")
    else: 
        log(f"ERROR: {len(entries)} quantifiers found. Please supply exactly 2, separated by spaces, in the following order: Exists ForAll")
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
            log(f"ERROR: Predicate {j} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters or underscores only, followed immediately by an integer greater than 0 enclosed in square brackets. Example: my_pred[5]")
        else:
            y = re.search("\[\d+\]",j)
            num = y.group()[1:][:-1]
            if num.isdigit():
                arity = int(num)
                if arity > 0:
                    predicates[j[:y.span()[0]]] = arity
                else:
                    log(f"ERROR: Arity {num} of predicate {j} is an integer less than 1.")
            else:
                log(f"ERROR: Arity {num} of predicate {j} is not an integer.")
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
            log(f"ERROR: Variable {j} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters or underscores only. Example: my_var")
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
            log(f"ERROR: Constant {j} is formatted in an invalid way. Ensure it is comprised of alphanumeric characters or underscores only. Example: my_const")
        else:
            constants.append(x.group())
    return(constants)

########################################
####### FILE INGESTION MAIN FLOW #######
########################################

if len(sys.argv) != 2:
    log("ERROR: Invalid amount of arguments. Please run the program including your filename as a parameter, in the format of 'python parser.py filename.ext'")

filename = sys.argv[1]
path = pathlib.Path.cwd() / filename

with open(path,"r") as f:
    content = []
    for line in f:
        content.append(line)

if not content:
    log("ERROR: Empty file")

length = len(content)

if length < 7:
    log(f"ERROR: A file needs at least 7 lines to be valid, but {filename} has {length}.")

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
            log(f"ERROR: Equality defined on more than one line in input file.")
        eqSeen = True
        eqInd = i
    elif content[i][0:12] == "connectives:":
        if connSeen:
            log(f"ERROR: Connectives defined on more than one line in input file.")
        connSeen = True
        connInd = i
    elif content[i][0:12] == "quantifiers:":
        if quantSeen:
            log(f"ERROR: Quantifiers defined on more than one line in input file.")
        quantSeen = True
        quantInd = i
    elif content[i][0:10] == "variables:":
        if varSeen:
            log(f"ERROR: Variables defined on more than one line in input file.")
        varSeen = True
        varInd = i
    elif content[i][0:10] == "constants:":
        if constSeen:
            log(f"ERROR: Constants defined on more than one line in input file.")
        constSeen = True
        constInd = i
    elif content[i][0:11] == "predicates:":
        if predSeen:
            log(f"ERROR: Predicates defined on more than one line in input file.")
        predSeen = True
        predInd = i
    elif content[i][0:8] == "formula:":
        if formSeen:
            log(f"ERROR: Formula beginning defined on more than one line in input file.")
        formSeen = True
        formInd = i
        justFormula[i] = content[i]
    else:
        justFormula[i] = content[i]

if not eqSeen:
    log(f"ERROR: Equality undefined.")
elif not connSeen:
    log(f"ERROR: Connectives undefined.")
elif not quantSeen:
    log(f"ERROR: Quantifiers undefined.")
elif  not varSeen:
    log(f"ERROR: Variables undefined.")
elif not constSeen:
    log(f"ERROR: Constants undefined.")
elif not predSeen:
    log(f"ERROR: Predicates undefined.")
elif not formSeen:
    log(f"ERROR: Formula undefined.")

# TODO test the above undefined and multi define catching

# TODO Formula lines need to be contiguous

'''
lastLine = 0
for i in range(length):
    if justFormula[i] != "":
        if i > lastLine:
            lastLine = i

if lastLine = formInd:
    if length([x for x in justFormula if x != ""]) != 1:
        log(f"ERROR: Formula beginning defined on more than one line in input file.")

    else:
        searchIndex = i
        if searchIndex == 0:
        log(f"ERROR: The first line of your file must be a definition of a set or the beginning of a formula.")
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
        log(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
print(f"Binary Connectives (And, Or, Implies, Iff):\n{connectives[0]} {connectives[1]} {connectives[2]} {connectives[3]}\n")
connectives = set(connectives)

negation = connTuple[1]
if negation not in forbiddenNames:
    forbiddenNames.add(negation)
else: 
    log(f"ERROR: The identifier {negation} has been used more than once. Please ensure all identifiers are unique.")
print(f"Negation Symbol:\n{negation}\n")

equality = populateEq(content[eqInd])
if equality not in forbiddenNames:
    forbiddenNames.add(equality)
else: 
    log(f"ERROR: The identifier {equality} has been used more than once. Please ensure all identifiers are unique.")
print(f"Equality Symbol:\n{equality}\n")

quantifiers = populateQuant(content[quantInd])
for x in quantifiers:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        log(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
print(f"Quantifiers (Exists, ForAll):\n{quantifiers[0]} {quantifiers[1]}\n")
quantifiers = set(quantifiers)

variables = populateVar(content[varInd])
for x in variables:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        log(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
varString = " ".join([x for x in variables])
print(f"Variables:\n{varString}\n")
variables = set(variables)

constants = populateConst(content[constInd])
for x in constants:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        log(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
constString = " ".join([x for x in constants])
print(f"Constants:\n{constString}\n")
constants = set(constants)

# TODO fix allowing two same-name different-arity predicates (this is a problem in the population function, because we have a dictionary that just updates the arity of the previously-seen name)

predicates = populatePred(content[predInd])
for x in predicates:
    if x not in forbiddenNames:
        forbiddenNames.add(x)
    else: 
        log(f"ERROR: The identifier {x} has been used more than once. Please ensure all identifiers are unique.")
predString = " ".join([f"{x} (arity {predicates[x]})" for x in predicates])
print(f"Predicates:\n{predString}\n")

formula = "".join([content[6],content[7]])[9:]
formula = formula.replace("("," ( ")
formula = formula.replace(")"," ) ")
formula = formula.replace(","," , ")
formula = " ".join(formula.split())
print(f"Formula:\n{formula}\n")

tokens = formula.split(" ")
print(f"Token stream: {tokens}")

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
    print("Grammar successfully printed to ./grammar.txt")
except:
    print("ERROR: Could not print grammar to ./grammar.txt - printing to console instead")
    for x in grammar:
        print(x)

####################################
####### PARSING TOKEN STREAM #######
####################################

## TODO: Make unique IDs either by making non-terminals have a forbidden char, making a new variable that ticks up and making separate addEdge() method, or alex's dictionary way

class Parser():
    def __init__(self,tokens):
        self.laIndex = 0
        self.lookahead = tokens[self.laIndex]
        self.dot = gv.Digraph(comment="Parse Tree")
        self.label = 0

    def labelNo(self):
        self.label += 1
        return self.label

    def formNT(self,parent):
        self.dot.node(parent, "F")
        if self.lookahead in quantifiers:
            self.dot.edge(parent,f"Q{self.laIndex}")
            self.quantNT(f"Q{self.laIndex}")
            self.dot.edge(parent,f"V{self.laIndex}")
            self.varNT(f"V{self.laIndex}")
            self.dot.edge(parent,f"F{self.laIndex}")
            self.formNT(f"F{self.laIndex}")
        elif self.lookahead == "(":
            self.dot.edge(parent,f"({self.laIndex}")
            self.match("(",f"({self.laIndex}")
            self.dot.edge(parent,f"E{self.laIndex}")
            self.exprNT(f"E{self.laIndex}")
            self.dot.edge(parent,f"){self.laIndex}")
            self.match(")",f"){self.laIndex}")
        elif self.lookahead == negation:
            self.dot.edge(parent,f"{negation}{self.laIndex}")
            self.match(negation,f"{negation}{self.laIndex}")
            self.dot.edge(parent,f"F{self.laIndex}")
            self.formNT(f"F{self.laIndex}")
        elif self.lookahead in predicates:
            self.dot.edge(parent,f"P{self.laIndex}")
            self.predNT(f"P{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a quantifier, open bracket, negation or predicate, consistent with F's production rules, but encountered {self.lookahead}.")
            
    def exprNT(self,parent):
        self.dot.node(parent, "E")
        if self.lookahead in constants or self.lookahead in variables:
            self.dot.edge(parent,f"T{self.laIndex}")
            self.termNT(f"T{self.laIndex}")
            self.dot.edge(parent,f"{equality}{self.laIndex}")
            self.match(equality,f"{equality}{self.laIndex}")
            self.dot.edge(parent,f"T{self.laIndex}")
            self.termNT(f"T{self.laIndex}")
        elif self.lookahead in quantifiers or self.lookahead == "(" or self.lookahead == negation or self.lookahead in predicates:
            self.dot.edge(parent,f"F{self.laIndex}")
            self.formNT(f"F{self.laIndex}")
            self.dot.edge(parent,f"L{self.laIndex}")
            self.logNT(f"L{self.laIndex}")
            self.dot.edge(parent,f"F{self.laIndex}")
            self.formNT(f"F{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a quantifier, open bracket, negation, predicate, constant or variable, consistent with E's production rules, but encountered {self.lookahead}.")

    def termNT(self,parent):
        self.dot.node(parent, "T")
        if self.lookahead in constants:
            self.dot.edge(parent,f"C{self.laIndex}")
            self.constNT(f"C{self.laIndex}")
        elif self.lookahead in variables:
            self.dot.edge(parent,f"V{self.laIndex}")
            self.varNT(f"V{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a constant or variable, consistent with T's production rules, but encountered {self.lookahead}.")

    def quantNT(self,parent):
        self.dot.node(parent, "Q")
        if self.lookahead in quantifiers:
            self.dot.edge(parent,f"{self.lookahead}{self.laIndex}")
            self.match(self.lookahead,f"{self.lookahead}{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a quantifier ({quantString}), consistent with Q's production rules, but encountered {self.lookahead}.")

    def logNT(self,parent):
        self.dot.node(parent, "L")
        if self.lookahead in connectives:
            self.dot.edge(parent,f"{self.lookahead}{self.laIndex}")
            self.match(self.lookahead,f"{self.lookahead}{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a binary connective ({connString}), consistent with L's production rules, but encountered {self.lookahead}.")

    def constNT(self,parent):
        self.dot.node(parent, "C")
        if self.lookahead in constants:
            self.dot.edge(parent,f"{self.lookahead}{self.laIndex}")
            self.match(self.lookahead,f"{self.lookahead}{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a constant, but encountered {self.lookahead}.")

    def varNT(self,parent):
        self.dot.node(parent, "V")
        if self.lookahead in variables:
            self.dot.edge(parent,f"{self.lookahead}{self.laIndex}")
            self.match(self.lookahead,f"{self.lookahead}{self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a variable, but encountered {self.lookahead}.")

    def predNT(self,parent):
        self.dot.node(parent, "P")
        if self.lookahead in predicates:
            varCount = predicates[self.lookahead] 
            self.dot.edge(parent,f"{self.lookahead}{self.laIndex}")
            self.match(self.lookahead,f"{self.lookahead}{self.laIndex}")
            self.dot.edge(parent,f"({self.laIndex}")
            self.match("(",f"({self.laIndex}")
            if varCount == 1:
                self.dot.edge(parent,f"V{self.laIndex}")
                self.varNT(f"V{self.laIndex}")
                self.dot.edge(parent,f"){self.laIndex}")
                self.match(")",f"){self.laIndex}")
            elif varCount >= 2:
                for i in range(varCount-1):
                    self.dot.edge(parent,f"V{self.laIndex}")
                    self.varNT(f"V{self.laIndex}")
                    self.dot.edge(parent,f",{self.laIndex}")
                    self.match(",",f",{self.laIndex}")
                self.dot.edge(parent,f"V{self.laIndex}")
                self.varNT(f"V{self.laIndex}")
                self.dot.edge(parent,f"){self.laIndex}")
                self.match(")",f"){self.laIndex}")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be a predicate, but encountered {self.lookahead}.")

    def match(self,t,parent):
        if self.lookahead == t:
            self.dot.node(parent, t)
            if self.laIndex != len(tokens)-1:
                self.laIndex += 1
                self.lookahead = tokens[self.laIndex]
            else:
                print("Parser has reached end of token stream")
        else:
            log(f"ERROR: Symbol Number {self.laIndex} Parser expected next symbol to be {t}, but encountered {self.lookahead}.")
        
    def parse(self):
        self.formNT("origin")

p = Parser(tokens)
p.parse()
#print(p.dot.source)
p.dot.render("parsetree.gv.pdf", view=True)
log(f"Successfully parsed input {filename}")