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
diceRegex = re.compile(r"((\d*)" + dieSeperator + r"(\d+)((\+|-)(\d+))?\s?("+ advString + r"|"+ disadvString + r")?)")
diceRollPromptString = "\n\nThe following list represents the results of each die roll requested above, provided in order: "

def chat_input_modifier(inputString, state, is_chat=False):
    """
    In default/notebook modes, modifies the whole prompt.

    In chat mode, it is the same as chat_input_modifier but only applied
    to "text", here called "string", and not to "visible_text".
    """

    resultList = []
    matches = re.search(diceRegex, inputString)
    if(matches):
        # For each instance of dice notation in the string
        for match in re.finditer(diceRegex, inputString):
            # Find all relevant values
            numRolled = match.group(2)
            dieSize = match.group(3)
            opSign = match.group(5)
            opMag = match.group(6)
            advDisadv = match.group(7)
            
            # Roll the dice
            result = roll(numRolled, dieSize)

            # Apply advantage and disadvantage if required
            if(advDisadv):
                advDisadvResult = roll(numRolled, dieSize)
                if((advString in advDisadv and advDisadvResult > result) or (disadvString in advDisadv and advDisadvResult < result)):
                    result = advDisadvResult

            # Apply any additions/subtractions
            if(opSign):
                if("-" in opSign):
                    result = int(result) - int(opMag)
                elif("+" in opSign):
                    result = int(result) + int(opMag)

            logString = "DieRoller has rolled " + numRolled + dieSeperator + dieSize + opSign + opMag
            if(advDisadv):
                logString += " " + advDisadv
            logger.info(logString + " and got a result of " + str(result))
            resultList.append(str(result))
            
    if(resultList):
        seperator = ', '
        resultListString = seperator.join(resultList)
        completePromptString = inputString + diceRollPromptString + resultListString

    return completePromptString, inputString

def roll(num, size):
     return str(random.randint(int(num), int(num)*int(size)))

