# ooba_dieroller
An extension for text-generation-webui that adds a basic die roller, to dodge the LLM being biased with it's own rolls.
I made this in my spare time, feel free spin up your own PR and improve it.

## Installation
- Navigate to the .\text-generation-webui\extensions folder in your terminal.
- Run the following command, without quotes: "git clone https://github.com/TheInvisibleMage/ooba_dieroller.git"
- Activate the extension. This can be done via the "Session" tab in the UI, or by directly modifying the "settings.yaml" file in your .\text-generation-webui\ folder

## How to Use
The extension will detect instances of basic dice notation, and roll appropriately, replacing that notation with the result.
- For example, the prompt "I roll 1d20+3 to attack the goblin!" may result in "I roll 17 to attack the goblin!" being passed as the prompt.
As noted above, basic additions and subtractions can be used to affect the result. Advantage and Disadvantage can also be applied, using " adv" for advantage, or " disadv" for disadvantage (again, noting spaces).
Some valid examples are below.
- "2d8"
- "1d4+4"
- "8d6-12"
- "1d20 adv"
- "2d10+7 disadv"

## Caveats and Known Issues
- All this does is replace the desired roll with the result. This means it is still up to your model/character to understand and use that result. Be sure to word your prompts in such a way that it is very clear exactly what the result should be used for!

## TODO
- Add config.
- Add UI for easier config changes.
- Add things you can config (eg. trigger phrases to prefix/postfix dice notation, strings you can prefix/postfix to result to help LLM understand it, etc)
- - In particular, adding support for only recognizing dice notation with user-chosen surrounding characters, to help prevent rolls when none are needed.
- Support more roll operations (exploding, etc).
- Improve interperability by LLM.
