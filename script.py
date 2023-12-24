"""
A simple extension to allow actual dice rolls and automatically add them to your prompt.
Now the question is whether the LLM cna interperate them correctly.
"""

import re
import random
from modules.logging_colors import logger
from modules import shared

params = {
    "display_name": "Dice Roller",
    "is_tab": False,
}

advString = "adv"
disadvString = "disadv"
dieSeperator = 'd'
diceRegex = re.compile(r"((\d*)" + dieSeperator + r"(\d+)((\+|-)(\d+))?\s?("+ disadvString + r"|"+ advString + r")?)", re.IGNORECASE)
#diceRollPromptString = "\n\nThe following list represents the results of each die roll requested above, provided in order: "
#diceRollReplaceString = "my dice, and get a result of "

def chat_input_modifier(inputString: str, visibleString: str, state: dict) -> tuple[str, str]:
    """
    In default/notebook modes, modifies the whole prompt.

    In chat mode, it is the same as chat_input_modifier but only applied
    to "text", here called "string", and not to "visible_text".
    """

    matches = re.search(diceRegex, inputString)
    completePromptString = inputString
    if(matches):
        # For each instance of dice notation in the string
        for match in re.finditer(diceRegex, inputString):
            # Find all relevant values
            numRolled = match.group(2)
            dieSize = match.group(3)
            opSign = match.group(5)
            opMag = match.group(6)
            advDisadv = match.group(7).lower()

            opResult = 0
            advDisadvResult = None
            advDisadvApplies = False
            advDisadvFullString = "Advantage"
            
            # Roll the dice
            dieResult = roll(numRolled, dieSize)

            # Calculate advantage and disadvantage if required
            if(advDisadv):
                advDisadvResult = roll(numRolled, dieSize)
                if((advString == advDisadv and advDisadvResult > dieResult) or (disadvString == advDisadv and advDisadvResult < dieResult)):
                    advDisadvApplies = True

            # Calculate any additions/subtractions
            if(opSign and opMag):
                if("-" == opSign):
                    opResult -= int(opMag)
                elif("+" == opSign):
                    opResult += int(opMag)
                logString += opSign + opMag

            # Assemble logs
            logString = "DieRoller has rolled " + numRolled + dieSeperator + dieSize  + " and got a result of " + str(dieResult)
            if(advDisadv):
                if(disadvString == advDisadv):
                    advDisadvFullString = "Disadvantage"
                logString += ", with their " + advDisadvFullString + " roll giving a result of " + str(advDisadvResult)

            if(opSign and opMag):
                logString += ", with a modifier of " + opSign + opMag
            else:
                logString += "."

            # Calculate final value and log
            if(advDisadvApplies):
                dieResult = advDisadvResult
            result = int(dieResult) + opResult

            logString += " This brings their final total result to " + str(result) + "."
            logger.info(logString)
            
            #completePromptString = re.sub(diceRegex, diceRollReplaceString + str(result), completePromptString, count=1)
            completePromptString = re.sub(diceRegex, str(result), completePromptString, count=1)

    if(matches):
        return completePromptString, visibleString
    else:
        return inputString, visibleString

def roll(num, size):
     return str(random.randint(int(num), int(num)*int(size)))

