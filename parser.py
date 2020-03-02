import sys
import pathlib

if len(sys.argv) < 2:
    print("ERROR: Please run the program including your filename as a parameter, in the format of 'python parser.py filename.ext'")
    sys.exit()

pathname = sys.argv[1]

path = pathlib.Path.cwd() / pathname

with open(path,"r") as f:
    content = []
    for line in f:
        content.append(line)

print(content)


#content = content.replace("\n","")
#print(content)
#content = content.replace("\t","")
#print(content)
#content = content.replace(" ","")
#print(content)
#content = content.replace(";;",";")
#print(content)