
def isvalidsyntax(lexlist, printqueue):

    candidate = lexformatter(lexlist, printqueue)
    if not candidate:
        return False

    # each statement (separated by ";") is evaluated separately.
    for statement in candidate:
        statement.append("$")
        statestack = [0]

        printqueue.append("Stack \t\t Input \t\t Table Entry \t\t Action \n")

        if not bup(statement, printqueue, statestack):
            return False

    return True


def lexformatter(lexlist, printqueue):
    formattedlist = []
    statementcount = 0
    templist = []
    for element in lexlist:
        if element[0] == "identifier":
            templist.append("id")
        elif element[0] == "real":
            printqueue.append("Reals are not accepted as valid syntax for this exercise, and will not be parsed.\n")
            return False
        elif element[1] == ";":
            statementcount = statementcount + 1
            formattedlist.append(templist)
            templist = []
        else:
            templist.append(element[1])
    return formattedlist


def bup(candidate, printqueue ,statestack):
    while True:

        # save snapshot of current stack and input to be printed out later
        printstack = ""
        for element in statestack:
            printstack = printstack + str(element)
        printqueue.append(printstack + "\t\t")

        printcandidate = ""
        for element in candidate:
            printcandidate = printcandidate + str(element)
        printqueue.append(printcandidate + "\t\t")
        # end of print section

        # currentstate = TOS
        currentstate = statestack[-1]

        tableresult = runBUPtable(currentstate, candidate[0], printqueue)
        if not tableresult:
            return False

        # save snapshot of table result to be printed out later
        printqueue.append(str(tableresult) + "\t\t")

        if tableresult == "ACCT":
            printqueue.append("\n""\n")
            return True

        elif tableresult[0] == "S":
            shiftcandidate = candidate.pop(0)
            statestack.append(shiftcandidate)
            statestack.append(tableresult[1])

            printqueue.append("Push(" + str(shiftcandidate) + ");push(" + tableresult[1] + ")\n")

        elif tableresult[0] == "R":
            if tableresult[1] == "6":
                # pop 2 * size of rule
                statestack.pop()
                statestack.pop()
                # peek TOS
                currentstate = statestack[-1]
                statestack.append("F")
                tableresult = runBUPtable(currentstate, "F", printqueue)
                if not tableresult:
                    return False
                statestack.append(tableresult)
                printqueue.append("F->id; Table[" + str(currentstate) + ",F]=" + str(tableresult) + "\n")

            elif tableresult[1] == "5":
                # pop 2 * size of rule
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                # peek TOS
                currentstate = statestack[-1]
                statestack.append("F")
                tableresult = runBUPtable(currentstate, "F", printqueue)
                if not tableresult:
                    return False
                statestack.append(tableresult)
                printqueue.append("F->(E); Table[" + str(currentstate) + ",F]=" + str(tableresult) + "\n")

            elif tableresult[1] == "4":
                # pop 2 * size of rule
                statestack.pop()
                statestack.pop()
                # peek TOS
                currentstate = statestack[-1]
                statestack.append("T")
                tableresult = runBUPtable(currentstate, "T", printqueue)
                if not tableresult:
                    return False
                statestack.append(tableresult)
                printqueue.append("T->F; Table[" + str(currentstate) + ",T]=" + str(tableresult) + "\n")

            elif tableresult[1] == "3":
                # pop 2 * size of rule
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                # peek TOS
                currentstate = statestack[-1]
                statestack.append("T")
                tableresult = runBUPtable(currentstate, "T", printqueue)
                if not tableresult:
                    return False
                statestack.append(tableresult)
                printqueue.append("T->T * F; | T / F; Table[" + str(currentstate) + ",T]=" + str(tableresult) + "\n")

            elif tableresult[1] == "2":
                # pop 2 * size of rule
                statestack.pop()
                statestack.pop()
                # peek TOS
                currentstate = statestack[-1]
                statestack.append("E")
                tableresult = runBUPtable(currentstate, "E", printqueue)
                if not tableresult:
                    return False
                statestack.append(tableresult)
                printqueue.append("E->T; Table[" + str(currentstate) + ",E]=" + str(tableresult) + "\n")

            elif tableresult[1] == "1":
                # pop 2 * size of rule
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                statestack.pop()
                # peek TOS
                currentstate = statestack[-1]
                statestack.append("E")
                tableresult = runBUPtable(currentstate, "E", printqueue)
                if not tableresult:
                    return False
                statestack.append(tableresult)
                printqueue.append("E->E + T; | E - T; Table[" + str(currentstate) + ",E]=" + str(tableresult) + "\n")


def runBUPtable(currentstate, candidate, printqueue):
    try:
        tableresult = bupTable[int(currentstate)][candidate]
    except KeyError:
        printqueue.append("\nNo matching table entry for input " + str(candidate) +
                          " and state " + str(currentstate) + ", therefore not syntactically correct.\n")
        return False
    return tableresult


bupTable = [

    {  # state 0

        "id": "S5",
        "(": "S4",
        "E": "1",
        "T": "2",
        "F": "3"
    },
    {  # state 1
        "+": "S6",
        "-": "S6",
        "$": "ACCT"
    },
    {  # state 2
        "+": "R2",
        "-": "R2",
        "*": "S7",
        "/": "S7",
        ")": "R2",
        "$": "R2"
    },
    {  # state 3
        "+": "R4",
        "-": "R4",
        "*": "R4",
        "/": "R4",
        ")": "R4",
        "$": "R4"
    },
    {  # state 4
        "id": "S5",
        "(": "S4",
        "E": "8",
        "T": "2",
        "F": "3"
    },
    {  # state 5
        "+": "R6",
        "-": "R6",
        "*": "R6",
        "/": "R6",
        ")": "R6",
        "$": "R6"
    },
    {  # state 6
        "id": "S5",
        "(": "S4",
        "T": "9",
        "F": "3"
    },
    {  # state 7
        "id": "S5",
        "(": "S4",
        "F": "10"
    },
    {  # state 8
        "+": "S6",
        "-": "S6",
        ")": "S11"
    },
    {  # state 9
        "+": "R1",
        "-": "R1",
        "*": "R7",
        "/": "R7",
        ")": "R1",
        "$": "R1"
    },
    {
        # state 10
        "+": "R3",
        "-": "R3",
        "*": "R3",
        "/": "R3",
        ")": "R3",
        "$": "R3",

    },
    {  # state 11
        "+": "R5",
        "-": "R5",
        "/": "R5",
        "*": "R5",
        ")": "R5",
        "$": "R5"
    }

]
