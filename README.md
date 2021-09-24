# MATLAB Filter Coefficient Translator
This application is used to translate MATLAB generated .fcf files in order to format the values into 2's complement. 
It expects values ranging from ~ -1 to 1. In other words the result is composed of a sign bit (MSB) and the fraction part of the input (LSB).
Integer values are being rounded to the respective maximum/minimum.
The output file is in the same directory as the input file.

Bugs:
24.09.2021: It has been observed that the separator is missing when using the "List" option.
