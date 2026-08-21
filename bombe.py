from multiprocessing import Process
from itertools import product

# If I know what the plugboard does to A, the rotors tell me what the plugboard MUST do to B.

# P(S₁(P(A))) = B means Input A -> Plugboard P -> Scrambler 1 -> Plugboard P = B
# S₁(P(A)) = P(B) means Input A -> Plugboard P -> Scrambler 1 = B -> Plugboard P
# This is basically whats going on in the electrical for each rotation of the scrabbler
# Rotor moves, 26 electrical wirings go through steckered variations
# Example, Rotor turns A--P₁-->K so that P(S₁(P(A))) = K
# Let's say S₁(G) = R is being tested, Bombe would automatically assume A:G --S₁--> K:R
# Why? because S₁(P(A)) and S₁(G) so A is steckered to G.
# therefore, S₁(P(A))) = P(B) is S₁(G) = P(B) and S₁(G) = R meaning that P(B) = R so B is steckered to R.
# S₂ would then be tested and would test for contradictions say B is steckered to O when testing S₂(J) = O
# Thats a contradiction because B cannot be steckered to R and O, it can only be steckered to one letter.

# Diagonal board interprets steckering both ways where B <-> R and R <-> B
# This also makes B:R and R:B which is very important

# The bombe doesn't guess the rotor setting being IV-I-III it is predetermined by the operator

# Each drum have an offset to them, so they simultaniously check for steckers from position 1-6 as an example
# So drum 1 would be base setting + 0, Drum 2 would be base setting + 1 and so on until drum 6 would be at base + 5

# Ringstellung is not figured out by the bombe, it's figured out by cryptographers after through indicators, turnover information and other cryptanalytic information
# Bombe focuses primarily on the rotor-core orientation or rotorPosision as i call it

# Ordinary menus were generally based on the assumption that a turnover did not occur inside the crib
# Hoppity was used incase of a turnover event
# Implementation could use actual enigma states and have accurate turnover behaviour

# The 26 electrical wire setup is the physical implementation of what we'd call constraint propagation today.

# Output: Wheel order, rotor positions and possible stecker. That would be thrown into a checking machine. if not false step, put into enigma/Typex and decrypt

# Checking phase derives multiple steckers instead of raw bombe output. 
# The checker is literally the engima minus the plugboard
# Example:
# A --1--> B and bombe farted out A <-> G
# P(A) = G so we have S₁(G) -> P(B)
# Since we know the rotor positions and the exact rotors used and in which order they were placed,
# We throw G into the scrambler, we get P(B) which we can appoint an example letter of K
# So, by knowing just A <-> G we got B <-> K
# rinse and repeat :D
# Loops/Closures in ciphered messages helped verify hypotheses as it would loop back to the original hypothesis, confirming other hypotheses
# unplugged steckers exist, e.g. P(C) = C
# Only able derive steckers throught the menu
# Do ts automatically and call it the "Scrutator Maximus"

# TLDR:
# The Bombe physically swept through possible rotor-core configurations while 
# an electrical network representing the crib, the simulated Enigma scramblers, 
# and all reciprocal plugboard possibilities propagated constraints in parallel; 
# configurations in which every possible plugboard interpretation became impossible 
# were passed over, while configurations leaving a consistent possibility caused 
# a stop for further checking.


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
    if len(plaintext) == len(ciphertext):
        for i in range(len(plaintext)):
            if plaintext[i] == ciphertext[i]:
                print("plaintext and ciphertext letter equal to eachother, impossible")
                return 0
            menuList.append((plaintext[i], ciphertext[i], i))
        menuTuple = tuple(menuList)
        print("MenuTuple:",menuTuple)
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

# T T - Valid + New
# T F - Valid + known
# F F - Contradicion
def steckerCheck(stecker, L1, L2):
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

def bombe(menu, letter, rotorsUsed, reflectorUsed):
    # Menu - Tuple of Tuples - (t1(plain, cipher, index), ... , tn(plain, cipher, index)) - Connection between the ciphertext and plaintext
    # rotorUsed - Int List - Order of individual unique rotors (e.g. V-III-IV)
    
    for rotorPosision in product(range(26), repeat=3):
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

                for i in list(stecker.keys()):
                    print(i, "<->", stecker[i])
            print("------------------------")
            result = []
            resultPlugboard = []
            break
    return 0

bombe(menu=menuBuilder("NUMBERPHILE","HZICLOWIUIG"),letter="I",rotorsUsed=[1, 3, 4],reflectorUsed=1)