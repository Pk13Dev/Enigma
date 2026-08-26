from multiprocessing import Process
from itertools import product
from itertools import islice

# Hardcodded rotor, reflector and entry disc wirings alligned with the Enigma I (Specifically service Enigma used by the German Army and Air Force)
rotor = [
    ["E","K","M","F","L","G","D","Q","V","Z","N","T","O","W","Y","H","X","U","S","P","A","I","B","R","C","J"],
    ["A","J","D","K","S","I","R","U","X","B","L","H","W","T","M","C","Q","G","Z","N","P","Y","F","V","O","E"],
    ["B","D","F","H","J","L","C","P","R","T","X","V","Z","N","Y","E","I","W","G","A","K","M","U","S","Q","O"],
    ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"],
    ["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]
]

reflector = [
    ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"],
    ["Y","R","U","H","Q","S","L","D","P","X","N","G","O","K","M","I","E","B","F","Z","C","W","V","J","A","T"],
    ["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]
]

entry = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]

rotorTurnover = ["Q","E","V","J","Z"]

def scrambler(letter, rotorsUsed, reflectorUsed, rotorPosision):
    # rotorPosition - rotor combination used
    currentLetter = entry.index(letter)
    for currentRotor in list(reversed(rotorsUsed)): 
        currentRotorIndex = rotorsUsed.index(currentRotor) # Index of the current rotor
        currentLetter = (currentLetter + rotorPosision[currentRotorIndex]) % 26
        currentLetter = entry.index(rotor[currentRotor][currentLetter]) 
        currentLetter = (currentLetter - rotorPosision[currentRotorIndex]) % 26
    
    currentLetter = entry.index(reflector[reflectorUsed][currentLetter])
    
    for currentRotor in rotorsUsed: 
            currentRotorIndex = rotorsUsed.index(currentRotor) # Index of the current rotor
            currentLetter = (currentLetter + rotorPosision[currentRotorIndex]) % 26
            currentLetter = rotor[currentRotor].index(entry[currentLetter])
            currentLetter = (currentLetter - rotorPosision[currentRotorIndex]) % 26
    return entry[currentLetter] # Return as letter

# Input: plain, cipher and starting pos
# Output: tuple of tuples including inputs

# Starting pos - The position of the letter regarding to the context of the plain<->cipher index
# aka, where is this letter in the context of the whole plaintext/ciphertext message?
def menuBuilder(plaintext, ciphertext):
    menuList = []
    letterStack = []
    normieArray = []
    letterArray = []
    if len(plaintext) == len(ciphertext):
        for letter in entry:
            count = plaintext.count(letter) + ciphertext.count(letter)
            if count > 1:
                letterArray.append((letter, count))
            if count != None:
                normieArray.append((letter, count))
        letterArray = sorted(letterArray, key=lambda x: x[1],reverse=True)
        print("Sorted letter array:", letterArray)
        letterStack.append(letterArray[0][0])
        totalCount = 0
        for letter, count in letterArray:
            if totalCount <= 12:
                for index in range(len(plaintext)):
                    if totalCount <= 12:
                        if plaintext[index] == letter or ciphertext[index] == letter:
                            menuList.append((plaintext[index], ciphertext[index], index))
                            totalCount += 1
                    else:
                        break
            else:
                break
                
        # for letter in letterStack:
        #     for index in range(len(plaintext)):
        #         if plaintext[index] == letter and ciphertext[index] not in letterStack:
        #             menuList.append((plaintext[index], ciphertext[index], index))
        #             letterStack.append(ciphertext[index])
        #         if ciphertext[index] == letter and plaintext[index] not in letterStack:
        #             menuList.append((plaintext[index], ciphertext[index], index))
        #             letterStack.append(plaintext[index])
                
        # for index in range(len(plaintext)):
        #     if any(plaintext[index] or ciphertext[index] for letter,count in letterArray):
        #         menuList.append((plaintext[index], ciphertext[index], index))

        menuTuple = tuple(menuList)
        print("normie:", len(normieArray), "(No count limitation)")
        print("limit:", len(letterArray), "(count > 1 + relation limitation)")
        print("MenuTuple:",len(menuTuple),"Content:",menuTuple)
        return menuTuple
    elif len(plaintext) != len(ciphertext):
        print("plaintext/ciphertext length is not valid")
        return 0
    else:
        print("Undefined error at menu builder")
        return 0

def rotorOffset(rotorPosition, offset):
    return [rotorPosition[0],
            rotorPosition[1],
            (rotorPosition[2] + offset) % 26
            ]

def computeScramblers(rotorsUsed, rotorPosision, reflectorUsed, menu):
    newMap = {}

    for plain, cipher, offset in menu:

        # Don't calculate the same offset twice
        if offset in newMap:
            continue

        offsetPosition = rotorOffset(rotorPosision, offset)

        scrambledAlpha = []

        for letter in entry:
            result = scrambler(
                letter,
                rotorsUsed,
                reflectorUsed,
                offsetPosition
            )

            scrambledAlpha.append(result)

        newMap[offset] = scrambledAlpha

    return newMap

def steckerCheck(stecker, L1, L2):
    # T T - Valid + New
    # T F - Valid + known
    # F F - Contradicion
    if L1 in stecker and stecker[L1] != L2:
        return False, False

    if L2 in stecker and stecker[L2] != L1:
        return False, False

    if (
        L1 in stecker
        and L2 in stecker
        and stecker[L1] == L2
        and stecker[L2] == L1
    ):
        return True, False
    stecker[L1] = L2
    stecker[L2] = L1

    return True, True

def hypothesisChecker(menu, scramblerMap, inputLetter, guessedLetter):
    currentHypothesis = {}
    isValid, isNew = steckerCheck(stecker=currentHypothesis, L1=inputLetter, L2=guessedLetter)
    hasChangeOccurred = True
    while hasChangeOccurred:
        hasChangeOccurred = False
        for plainLetter, cipherLetter, offset in menu:
            if plainLetter in currentHypothesis:
                steckeredInput = currentHypothesis[plainLetter]
                result = scramblerMap[offset][entry.index(steckeredInput)]
                isValid, isNew = steckerCheck(stecker=currentHypothesis, L1=cipherLetter, L2=result)
                if not isValid:
                    return False, currentHypothesis
                if isNew:
                    hasChangeOccurred = True
            if cipherLetter in currentHypothesis:
                            steckeredInput = currentHypothesis[cipherLetter]
                            result = scramblerMap[offset][entry.index(steckeredInput)]
                            isValid, isNew = steckerCheck(stecker=currentHypothesis, L1=plainLetter, L2=result)
                            if not isValid:
                                return False, currentHypothesis
                            if isNew:
                                hasChangeOccurred = True
    return True, currentHypothesis       

def bombe(menu, letter, rotorsUsed, reflectorUsed, inpRotorPosition):
    # Menu - Tuple of Tuples - (t1(plain, cipher, index), ... , tn(plain, cipher, index)) - Connection between the ciphertext and plaintext
    # rotorUsed - Int List - Order of individual unique rotors (e.g. V-III-IV)
    startIndex = inpRotorPosition[0] * 26**2 + inpRotorPosition[1] * 26 + inpRotorPosition[2] + 1
    for rotorPosision in islice(product(range(26), repeat=3), startIndex, None):
        rotorPosision = list(rotorPosision)
        scramblerMap = computeScramblers(
            rotorsUsed=rotorsUsed,
            rotorPosision=rotorPosision,
            reflectorUsed=reflectorUsed,
            menu=menu
            ) # Scrambler map of offsetted scrambler positions
        result = []
        resultPlugboard = []
        inputLetter=letter
        for guessLetter in entry:
            hypothesisResult, hypothesisSteckers = hypothesisChecker(menu=menu, scramblerMap=scramblerMap, inputLetter=inputLetter, guessedLetter=guessLetter)
            if hypothesisResult:
                result.append((guessLetter))
                resultPlugboard.append((hypothesisSteckers))
        if result:
            print("------BOMBE STOPPED------")
            print("Rotor Setting:", rotorPosision)
            print("Hypothesised plugboard:")
            # print(resultPlugboard)
            for guessLetter, stecker in zip(result, resultPlugboard):

                print()
                print("Hypothesis:", inputLetter, "<->", guessLetter)
                print("Derived plugboard:")
                knownSteckers = []
                for i in list(stecker.keys()):
                    if i not in knownSteckers:
                        print(i, "<->", stecker[i])
                        knownSteckers.append(stecker[i])
            print("------------------------")
            result = []
            resultPlugboard = []
            return rotorPosision, (inputLetter, guessLetter)
    return None, None

currentMenu = menuBuilder("TODAYSWEATHERREPORTLIGHTRAINANDCOLDTEMPERATUREHEILHITTLER","HUJMQKISNCDPOHCDRWVVXKAQXTHMSMKFNWWCZAIKLEHPPVGFYELFYNRZG")
selectedLetter = "E"
rotorsUsed=[1, 3, 4]
rotorPosition = [0,0,0]
reflectorUsed=1
for i in range(10):
    newRotorPosition, hypothesisTuple = bombe(
        menu=currentMenu,letter=selectedLetter,rotorsUsed=rotorsUsed,reflectorUsed=reflectorUsed, inpRotorPosition=rotorPosition
        )
    if newRotorPosition or hypothesisTuple == None:
        print("None returned by the bome")
        break
    rotorPosition = newRotorPosition
    