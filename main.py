
# import syntaxfunctions
import lexfunctions
import project3
import sys

errorflag = [False, ""]

# reads in file inputted by user, formats to lowercase, stores in rawdata as string.
rawdata = lexfunctions.getFile()

# splits raw data by spaces into separate elements in a list
lexlist = lexfunctions.parsedata(rawdata)
print("TOKENS", "Lexemes", sep="           =             ")
for tokenSet in lexlist:
    print(tokenSet[0], tokenSet[1], sep="           =             ")
    print("\n")
    if tokenSet[0] == "invalid input":
        errorflag = [True, "Invalid input in lexical analyzer. Invalid token: " + tokenSet[1]]
if errorflag[0]:
    sys.exit(errorflag[1])

printqueue = []
#if syntaxfunctions.isvalidsyntax(lexlist, printqueue):
if project3.isvalidsyntax(lexlist, printqueue):
    printqueue.append("The input is syntactically correct.")
else:
    printqueue.append("Syntax Error")

outputfile = open("outputfile", "w")
outputfile.writelines(printqueue)
outputfile.close()
print("Syntax Analysis output sent to outputfile.txt")




