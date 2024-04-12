# This class is meant to work as a part of a workflow of translating sentences with foreign language and LaTeX in-line
# or display math equations and has methods to return LaTeX equations into Strings that have been stripped and
# translated.
class DelimterReplacer:

    # This method takes in a String argument and a Dictionary argument, the String argument being a String that has been
    # translated after stripping all LaTeX in-line and display math equations and the Dictionary argument being the
    # Dictionary that contains the stripped out LaTeX equations and their Delimiter Strings that they have been replaced
    # with. The method then does a simple find and replace of all the Delimiter Strings to restore the original
    # equations into the translated String.
    def replaceDelimiters(self, incomingString : str, EquationSet : dict):

        # Loop over all keys in the Dictionary
        for key in EquationSet.keys():

            # Replace the matching Delimiter String in the translated String with the original LaTeX equation
            incomingString = incomingString.replace(key, EquationSet[key])

        return incomingString

