keywordList = ["int", "float", "bool", "true", "false", "if", "else", "then", "endif", "endelse",
               "while", "whileend", "do", "enddo", "for", "endfor", "stdinput", "stdoutput", "and", "or", "not"]
operatorList = ["*", "+", "-", "=", "/", ">", "<", "%"]
seperatorList = ["(", ")", "[", "]", "{", "}", ",", ".", ":", ";"]

def getFile():
    #allows user to input filepath of a text file and reads file.
    userInput = input("Please enter file path for the input file: ")

    inputfile = open(userInput, "r")
    fileData = ""
    # stores data from file into a string, and formats to lowercase.

    for fileChar in inputfile:
        fileData = fileData + fileChar.lower()
    #returns file info as lowercase string.
    return fileData


def parsedata(rawdata):
    # splits raw data by spaces into separate elements in a list
    currentstring = ""
    enddata = []
    state = 0

    for i in rawdata:

        if state == 0:
            #default state/alpha state
            if i == "!":
                state = 1
            elif i == " ":
                state = 4
            elif i == "\n" or i == "\t":
                pass
            elif i.isalpha():
                currentstring = currentstring + i
                state = 0
            elif i.isnumeric():
                currentstring = currentstring + i
                state = 2
            elif i in seperatorList:
                #seperatorList = ["[", "]", "{", "}", ",", ".", ":", ";"]
                #operatorList = ["*", "+", "-", "=", "/", ">", "<", "%"]
                state = 3
            else:
                #catch-all for other characters. Errors will get caught in lexer() and call it invalid syntax there
                currentstring = currentstring + i

        elif state == 1:
            #comment state
            if i == "!":
                state = 0
            else:
                pass

        elif state == 2:
            #numeric state
            if i.isnumeric() or i == ".":
                currentstring = currentstring + i
            elif i in seperatorList:
                # seperatorList = ["[", "]", "{", "}", ",", ".", ":", ";"]
                state = 3
            elif i == " ":
                state = 4
            else:
                #catch-all for other characters. Errors will get caught in lexer() and call it invalid syntax there
                currentstring = currentstring + i
                state = 0
        if state == 3:
            #seperator state
            if currentstring != "":
                enddata.append(lexer(currentstring))
                currentstring = ""
            enddata.append(lexer(i))
            state = 0

        if state == 4:
            #space state (" ")
            if not currentstring == "":
                enddata.append(lexer(currentstring))
            currentstring = ""
            state = 0
    return enddata




def lexer (tokencandidate):
#lexer is lowercase sensitive, as it assumes input is lowercase after being processed by getFile()
#will return type of token, as well as original input
#returns invalid input if input does not fall into a token category.



    for keyword in keywordList:
        #keywordList = ["int", "float", "bool", "true", "false", "if", "else", "then", "endif", "endelse",
        #"while", "whileend", "do", "enddo", "for", "endfor", "stdinput", "stdoutput", "and", "or", "not"]
        if tokencandidate == keyword:
            return ("keyword", tokencandidate)

    if tokencandidate[0].isalpha():
        for element in tokencandidate:
            if not element.isnumeric() and not element.isalpha() and element != "$" and element != "_":
                return ("invalid input", tokencandidate)
        return ("identifier", tokencandidate)

    if tokencandidate[0].isnumeric():
        periodcount = 0
        for element in tokencandidate:
            if not element.isnumeric():
                if element == ".":
                    periodcount = periodcount + 1
                    if periodcount > 1:
                        break
        return ("real", tokencandidate)




    for token in operatorList:
        #operatorList = ["*", "+", "-", "=", "/", ">", "<", "%"]
        if tokencandidate == token:
            return ("operator", tokencandidate)


    for token in seperatorList:
        #seperatorList = ["[", "]", "{", "}", ",", ".", ":", ";"]
         if tokencandidate == token:
             return ("separator", tokencandidate)

    #if its not anything else, it'll return invalid input, helps catch logic errors
    return ("invalid input", tokencandidate)
