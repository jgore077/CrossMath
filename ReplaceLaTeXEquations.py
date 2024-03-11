# Regex is required for finding LaTeX equations, so we import it
import re

# This class is meant to work as a part of a workflow of translating sentences with foreign language and LaTeX in-line
# or display math equations and has methods to strip LaTeX out of the String in a lossless fashion.
class LaTeXReplacer:

    # This method takes in a String argument and find and replaces all LaTeX in-line and display math equations with
    # enumerated delimiter Strings and returns the modified String and a dictionary containing the
    # Delimiter String:Original Equation for replacing the Delimiter String after translation.
    def ReplaceEquations(self, incomingString : str):

        # Declare int for enumeration
        i = 1
        equations = {}

        # Perform our first search of the String for LaTeX in-line and display math equations
        match = re.search(r'(\\\([^ ]*\\\))|(\$[^ ]*\$)|(\\begin{math}[^ ]*\\end{math})|(\\\[[^ ]*\\\])|'
                          r'(\\begin{displaymath}[^ ]*\\end{displaymath})|(\\begin{equation}[^ ]*\\end{equation})',
                          incomingString)

        # If we find a match, enter the loop
        while match is not None:

            # Place match result in a variable
            pattern = str(match.group())

            # Place match result into dictionary with delimiter String as the key
            equations['XX'+str(i)] = pattern

            # Replace match result with delimiter String
            incomingString = incomingString.replace(pattern, 'XX'+str(i))

            # Search the rest of the modified String for more in-line and display equations, if we find none, we break
            # the loop and return modified String and dictionary of delimiter Strings and equations.
            match = re.search(r'(\\\([^ ]*\\\))|(\$[^ ]*\$)|(\\begin{math}[^ ]*\\end{math})|(\\\[[^ ]*\\\])|'
                              r'(\\begin{displaymath}[^ ]*\\end{displaymath})|(\\begin{equation}[^ ]*\\end{equation})',
                              incomingString)

            # Enumerate
            i = i+1

        return incomingString, equations

