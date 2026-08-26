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

# Rotor Turnover points for each rotor respectively
rotorTurnover = ["Q","E","V","J","Z"]

def startEnigma(plainText):
    # Saving the used rotors index in array
    rotorsUsed = [1, 3, 4]

    # Ringstellung setting for the rotors
    ringstellung = [1,20,11]
        
    # Rotor position used
    rotorPosision = [14, 15, 0]

    # Using reverter B for this example
    reflectorUsed = 1
    
    # Plug board setting
    plugboard = {
        "A":"V", "V":"A",
        "B":"S", "S":"B",
        "C":"G", "G":"C",
        "D":"L", "L":"D",
        "F":"U", "U":"F",
        "H":"Z", "Z":"H",
        "I":"N", "N":"I",
        "K":"M", "M":"K",
        "O":"W", "W":"O",
        "R":"X", "X":"R"
    }
    # Cipher text list initalization
    ciphertext = []        
    print("Turnover triggers:",rotorTurnover[rotorsUsed[0]], rotorTurnover[rotorsUsed[1]], rotorTurnover[rotorsUsed[2]])
    print("Starting pos",rotorPosision, entry[rotorPosision[0]], entry[rotorPosision[1]], entry[rotorPosision[2]])
    for letter in plainText:
        # Handling the rightmost rotor incrementation and turnover events
        
        if letter in plugboard:
            letter = plugboard[letter]
            
        hasIncremented = [False,False,False]
        # turnover detection
        for rotorID in rotorsUsed[1:]:
            rotorIndex = rotorsUsed.index(rotorID) # Index of the current rotor being used e.g. rotor formation is IV-III-I the index of IV in the order would be 0, III would be 1 and I would be 2 
            leftwardRotor = rotorsUsed.index(rotorID)-1 # The index of the rotor left of the current rotor
            if rotorPosision[rotorIndex] == entry.index(rotorTurnover[rotorID]):
                rotorPosision[rotorIndex] += 1 # Increment current rotor
                hasIncremented[rotorIndex] = True # Note down rotor incrementation
                print("Turnover! for rotor", rotorsUsed.index(rotorID))
                if rotorsUsed[0] != rotorID: # check if current rotor is leftmost
                    if hasIncremented[leftwardRotor]: # check if already incremented
                        print("Rotor",rotorIndex,"has already been incremented. Skipped.")
                    else:
                        rotorPosision[leftwardRotor] = (rotorPosision[leftwardRotor] + 1)%26
                        hasIncremented[leftwardRotor] = True
                        print("Rotor",rotorIndex,"has been incremented to",entry[rotorPosision[leftwardRotor]])
                rotorPosision[rotorIndex] %= 26

        if not hasIncremented[-1]:
            rotorPosision[-1] += 1
        rotorPosision[-1] %= 26
        # Rotorpos debug
        print(rotorPosision, entry[rotorPosision[0]], entry[rotorPosision[1]], entry[rotorPosision[2]])
        
        currentLetter = entry.index(letter)
        for currentRotor in list(reversed(rotorsUsed)): 
            currentRotorIndex = rotorsUsed.index(currentRotor) # Index of the current rotor
            currentLetter = (currentLetter + rotorPosision[currentRotorIndex] - ringstellung[currentRotorIndex]) % 26
            currentLetter = entry.index(rotor[currentRotor][currentLetter]) 
            currentLetter = (currentLetter - rotorPosision[currentRotorIndex] + ringstellung[currentRotorIndex]) % 26
        
        currentLetter = entry.index(reflector[reflectorUsed][currentLetter])
        
        for currentRotor in rotorsUsed: 
                currentRotorIndex = rotorsUsed.index(currentRotor) # Index of the current rotor
                currentLetter = (currentLetter + rotorPosision[currentRotorIndex] - ringstellung[currentRotorIndex]) % 26
                currentLetter = rotor[currentRotor].index(entry[currentLetter])
                currentLetter = (currentLetter - rotorPosision[currentRotorIndex] + ringstellung[currentRotorIndex]) % 26
        if entry[currentLetter] in plugboard:     
            ciphertext.append(plugboard[entry[currentLetter]])
        else:
            ciphertext.append(entry[currentLetter])
        
    ciphertext = ''.join(ciphertext)
    print("Finished!")
    return ciphertext

print(startEnigma("TODAYSWEATHERREPORTLIGHTRAINANDCOLDTEMPERATUREHEILHITTLER"))