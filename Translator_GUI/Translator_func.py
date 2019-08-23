import tkMessageBox
import Tkinter, tkFileDialog

def translate(file, structure, separator, format, language, ext, elements, bits):
    print(file)
    print(structure)
    print(separator)
    print(format)
    print(language)
    print(elements)
    print(bits)
    print(ext)

    Feedback_list.insert("end", file)

    # Enter list, array, .hex, memconfig
    output_list_separator = separator   # User define, if none, then the list separator is white space
    represent = format                  # Possible options : binary, hex, u-integer, s-integer
    # ["VHDL", "Verilog", "C"]          # Possible output languages
    extention = ext                     # txt/data Output file extention - empty(" ") or user defined.

    eline = int(elements)  # Elements per line
    # Output vector size

    # 60tap Blackman Low-pass FIR FC1k
    # 60tap Blackman High-pass FIR FC3k
    # coeff = open("Archive/60tap Blackman High-pass FIR FC3k.fcf", "r")  # Input file
    coeff = open(file, "r")   # Input file
    # fextn = (coeff.name).split(".")
    # fextn = fextn[1]                            # File extention
    fname = coeff.name
    content = coeff.read()  # Copy data
    coeff.close()  # Close file
    lines = content.splitlines()  # Split input into lines

    bits = int(bits)

    # Internal Parameters
    i = 0
    b = 0
    vals = []
    splt = []
    out = []
    temp = []
    tips = 0

# File formatting
    for x in lines:                  # Make a string of each element in the list and split it in case it contains ","
        # x = x.lstrip()
        # x = x.replace(" ", ",")
        temp = x.split(",")          # split returns lists,
        splt = splt + temp           # hence this statement is used to concatenate the new list to the existing ones

    for x in splt:                          # Here the components of the split list are evaluated,
        try:                            # whether they are a float number or not
            float(x)
            vals.append(x)              # If so, then they are appended to a new list that contains only float numbers
        except ValueError:                  # If not, then an error is reported
            print "Warning: Row", i, "is NaN:", x    # and the the element is reported to the console
            tips = 1
        i = i + 1

    # Number translation from float to 2's Complement
    for n in vals:
        c = float(n)
        k = c
        tr = [0]*bits               # Create a N-bit array filled with '0's

        # Detect value sign
        if c >= 0:                     # Before translating the float value evaluate the polarity of the value
            tr[0] = 0                # '0' fr positive value
        else:
            tr[0] = 1                # and '1' for negative value

        # Binary transform
        for i in range(1, bits):     # Obtain the binary version of the number
            c = 2*abs(c)             # by multipslying it by 2
            if c >= 1:               # and evaluating whether the result is bigger or equal than '1'
                tr[i] = 1            # if so than assign '1' to the corresponging bit of the vector
                c = c % 1            # and extract the mantissa from the current value for the next operation
            else:
                tr[i] = 0            # else assign '0' to the bit vector and continue

        # Detect if the float value = 1.0, if so then set it to the maximal value
        if k >= 1:
            tips = 2
            for i in range(0, bits):
                if i == 0:
                    tr[i] = 0
                else:
                    tr[i] = 1

        # Bit inversion when the value is negative
        if tr[0] == 1:                              # To make the negative values compatible with 2's Complement
            for i in range(1, bits):                # the bts have to be inverted
                if tr[i] == 1:                      # Then to the inverted vector one unit has to be added
                    tr[i] = 0                       # in order to obtain the correct value
                elif tr[i] == 0:
                    tr[i] = 1

            if sum(tr) < bits:                      # if the value is lower than 1-2**(bits-1)
                for i in range(bits-1, 1, -1):      # then increment the inverted result by one unit
                    if tr[i] == 1:
                        tr[i] = 0
                    elif tr[i] == 0:
                        tr[i] = 1
                        break
        out.append(str(tr).replace(",", "").replace(" ", "").replace("[", "").replace("]", ""))

    # Translate the result to integer or hexadecimal if selected
    if represent == "u-integer":                     # Add code
        for n in range(0, len(out)):
            # print out[n][1].
            temp = 0
            for i in range(0, bits):
                # print i
                # print int(out[n][i])
                temp = int(out[n][i])*(2**(bits-(i+1))) + temp
            out[n] = temp
            # print out[n]

    elif represent == "s-integer":                   # Add code
        for n in range(0, len(out)):
            # print out[n][1].
            temp = 0
            for i in range(1, bits):
                # print i
                # print int(out[n][i])
                temp = int(out[n][i])*(2**(bits-(i+1))) + temp

            if int(out[n][0]) == 0:
                out[n] = temp
            else:
                out[n] = temp*(-1)

    elif represent == "hex":
        difference = bits % 4
        if difference == 0:
            bin_length = bits
        else:
            bin_length = bits + (4-difference)

        hex_length = bin_length/4
        hex_value = hex_length*[0]
        bin_value = bin_length*[0]
        print "Warning: Output bit length adjusted to", bin_length, "bits!"

        # Size adjusting
        for n in range(0, len(out)):
            bin_value[bin_length - bits:bin_length] = out[n]
            temp = str(bin_value).replace(",", "").replace(" ", "").replace("[", "").replace("]", "").replace("'", "")
            # Translation to Hexadecimal
            for i in range(0, hex_length):
                comp = str(temp[4 * i:4 * i + 4])
                # print comp
                if comp == "0000":
                    hex_value[i] = "0"
                #    print "0"
                elif comp == "0001":
                    hex_value[i] = "1"
                #    print "1"
                elif comp == "0010":
                    hex_value[i] = "2"
                #    print "2"
                elif comp == "0011":
                    hex_value[i] = "3"
                #    print "3"
                elif comp == "0100":
                    hex_value[i] = "4"
                #    print "4"
                elif comp == "0101":
                    hex_value[i] = "5"
                #    print "5"
                elif comp == "0110":
                    hex_value[i] = "6"
                #    print "6"
                elif comp == "0111":
                    hex_value[i] = "7"
                #    print "7"
                elif comp == "1000":
                    hex_value[i] = "8"
                #    print "8"
                elif comp == "1001":
                    hex_value[i] = "9"
                #    print "9"
                elif comp == "1010":
                    hex_value[i] = "A"
                #    print "A"
                elif comp == "1011":
                    hex_value[i] = "B"
                #    print "B"
                elif comp == "1100":
                    hex_value[i] = "C"
                #    print "C"
                elif comp == "1101":
                    hex_value[i] = "D"
                #    print "D"
                elif comp == "1110":
                    hex_value[i] = "E"
                #    print "E"
                elif comp == "1111":
                    hex_value[i] = "F"
                #    print "F"
            # print hex_value
            out[n] = str(hex_value).replace(",", "").replace(" ", "").replace("[", "").replace("]", "").replace("'", "")

    # Manage file extention
    if represent == "binary":
        fullname = fname.replace(".", "_bin.")
    elif represent == "s-integer":
        fullname = fname.replace(".", "_sint.")
    elif represent == "u-integer":
        fullname = fname.replace(".", "_uint.")
    elif represent == "hex":
        fullname = fname.replace(".", "_hex.")

    if extention != " ":     # Replace file extention
        # fullname = fname.replace(".", "_bin.")
        fextn = fullname.split(".")
        fullname = str("").join([fextn[0], str("."), extention])

    # product = open(fullname, "w")
    product = open(fullname, "w")

    # Writing an Array
    if structure == "Array":
        if language == "VHDL":
            if represent == "hex":
                difference = bits % 4
                if difference != 0:
                    bits = bits + (4 - difference)

            if represent == "binary" or represent == "hex":
                product.write("%s %s%s %s%s\n" % ("type coefficients is array (0 to",
                                                  len(out) - 1, ") of signed(", bits - 1, " downto 0);"))

            elif represent == "u-integer":
                product.write("%s %s%s %s%s\n" % ("type coefficients is array (0 to",
                                                  len(out) - 1, ") of integer range 0 to", 2**bits-1, ";"))

            elif represent == "s-integer":
                product.write("%s %s%s %s %s%s %s\n" % ("type coefficients is array (0 to",
                                                        len(out) - 1, ") of integer range", 0-2**(bits-1),
                                                        "to", 2**(bits-1)-1, ";"))

            product.write("signal coeff: coefficients :=( \n")
            for n in range(0, len(out)):
                if n < len(out)-1:
                    if b < eline-1:
                        if represent == "binary":
                            product.write(""""%s", """ % out[n])
                        elif represent == "hex":
                            product.write("""x"%s", """ % out[n])
                        elif represent == "u-integer" or represent == "s-integer":
                            spaces_length = len(str(2**bits)) - len(str(out[n]))
                            spaces = ["|"]*spaces_length
                            spaces = str(spaces).replace(",", "").replace("[", "")
                            spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                            spaces = spaces.replace("|", " ")
                            out[n] = spaces + str(out[n])
                            product.write(""" %s, """ % out[n])
                        b = b + 1

                    elif b == eline-1:
                        if represent == "binary":
                            product.write(""""%s", \n""" % out[n])
                        elif represent == "hex":
                            product.write("""x"%s", \n""" % out[n])
                        elif represent == "u-integer" or represent == "s-integer":
                            spaces_length = len(str(2**bits)) - len(str(out[n]))
                            spaces = ["|"]*spaces_length
                            spaces = str(spaces).replace(",", "").replace("[", "")
                            spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                            spaces = spaces.replace("|", " ")
                            out[n] = spaces + str(out[n])
                            product.write(""" %s, \n""" % out[n])
                        b = 0

                elif n == len(out)-1:
                    if represent == "binary":
                        product.write(""""%s");""" % out[n])
                    elif represent == "hex":
                        product.write("""x"%s");""" % out[n])
                    elif represent == "u-integer" or represent == "s-integer":
                        spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                        spaces = ["|"] * spaces_length
                        spaces = str(spaces).replace(",", "").replace("[", "")
                        spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                        spaces = spaces.replace("|", " ")
                        out[n] = spaces + str(out[n])
                        product.write(""" %s);""" % out[n])

        elif language == "Verilog":
            product.write("reg[%s:0] " % str(bits-1))
            product.write("coeff[%s:0] = { \n" % str(len(out)-1))
            for n in range(0, len(out)):
                if n < len(out) - 1:
                    if b < eline - 1:
                        if represent == "binary":
                            product.write("%s'b" % bits)
                            product.write("%s, " % out[n])
                        elif represent == "hex":
                            product.write("%s'h" % bits)
                            product.write("%s, " % out[n])
                        elif represent == "u-integer" or represent == "s-integer":
                            spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                            spaces = ["|"] * spaces_length
                            spaces = str(spaces).replace(",", "").replace("[", "")
                            spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                            spaces = spaces.replace("|", " ")
                            out[n] = spaces + str(out[n])
                            if int(out[n]) < 0:
                                product.write("-%s'd" % bits)
                                product.write("%s, " % str(out[n]).replace(" ", "").replace("-", ""))
                            else:
                                product.write("%s'd" % bits)
                                product.write("%s, " % str(out[n]).replace(" ", ""))
                        b = b + 1

                    elif b == eline - 1:
                        if represent == "binary":
                            product.write("%s'b" % bits)
                            product.write("%s, \n" % out[n])
                        elif represent == "hex":
                            product.write("%s'h" % bits)
                            product.write("%s, \n" % out[n])
                        elif represent == "u-integer" or represent == "s-integer":
                            spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                            spaces = ["|"] * spaces_length
                            spaces = str(spaces).replace(",", "").replace("[", "")
                            spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                            spaces = spaces.replace("|", " ")
                            out[n] = spaces + str(out[n])
                            if int(out[n]) < 0:
                                product.write("-%s'd" % bits)
                                product.write("%s, \n" % str(out[n]).replace(" ", "").replace("-", ""))
                            else:
                                product.write(" %s'd" % bits)
                                product.write("%s, \n" % str(out[n]).replace(" ", ""))
                        b = 0

                elif n == len(out) - 1:
                    if represent == "binary":
                        product.write("%s'b" % bits)
                        product.write("%s}; " % out[n])
                    elif represent == "hex":
                        product.write("%s'h" % bits)
                        product.write("%s}; " % out[n])
                    elif represent == "u-integer" or represent == "s-integer":
                        spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                        spaces = ["|"] * spaces_length
                        spaces = str(spaces).replace(",", "").replace("[", "")
                        spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                        spaces = spaces.replace("|", " ")
                        out[n] = spaces + str(out[n])

                        if int(out[n]) < 0:
                            product.write("-%s'd" % bits)
                            product.write("%s, " % str(out[n]).replace(" ", "").replace("-", ""))
                        else:
                            product.write("%s'd" % bits)
                            product.write("%s} " % str(out[n]).replace(" ", ""))

        elif language == "C":
            product.write("int coeff[%s] = { \n" % len(out))
            for n in range(0, len(out)):
                if n < len(out) - 1:
                    if b < eline - 1:
                        if represent == "binary":
                            product.write(""" "0b%s", """ % out[n])
                        elif represent == "hex":
                            product.write(""" 0x%s, """ % out[n])
                        elif represent == "u-integer" or represent == "s-integer":
                            spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                            spaces = ["|"] * spaces_length
                            spaces = str(spaces).replace(",", "").replace("[", "")
                            spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                            spaces = spaces.replace("|", " ")
                            out[n] = spaces + str(out[n])
                            product.write(""" %s, """ % out[n])
                        b = b + 1

                    elif b == eline - 1:
                        if represent == "binary":
                            product.write(""" "0b%s", \n""" % out[n])
                        elif represent == "hex":
                            product.write(""" 0x%s, \n""" % out[n])
                        elif represent == "u-integer" or represent == "s-integer":
                            spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                            spaces = ["|"] * spaces_length
                            spaces = str(spaces).replace(",", "").replace("[", "")
                            spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                            spaces = spaces.replace("|", " ")
                            out[n] = spaces + str(out[n])
                            product.write(""" %s, \n""" % out[n])
                        b = 0

                elif n == len(out) - 1:
                    if represent == "binary":
                        product.write(""" "0b%s"};""" % out[n])
                    elif represent == "hex":
                        product.write(""" 0x%s};""" % out[n])
                    elif represent == "u-integer" or represent == "s-integer":
                        spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                        spaces = ["|"] * spaces_length
                        spaces = str(spaces).replace(",", "").replace("[", "")
                        spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                        spaces = spaces.replace("|", " ")
                        out[n] = spaces + str(out[n])
                        product.write(""" %s};""" % out[n])

    # Writing a List
    elif structure == "List":
        for n in range(0, len(out)):
            if n < len(out) - 1:
                if b < eline - 1:
                    if represent == "binary" or represent == "hex":
                        product.write(" %s " % out[n])
                    else:
                        spaces_length = len(str(2**bits)) - len(str(out[n]))
                        spaces = ["|"]*spaces_length
                        spaces = str(spaces).replace(",", "").replace("[", "")
                        spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                        spaces = spaces.replace("|", " ")
                        out[n] = spaces + str(out[n])
                        product.write(""" %s%s """ % (out[n], output_list_separator))
                    b = b + 1

                elif b == eline - 1:
                    if represent == "binary" or represent == "hex":
                        product.write("%s \n" % out[n])
                    else:
                        spaces_length = len(str(2**bits)) - len(str(out[n]))
                        spaces = ["|"]*spaces_length
                        spaces = str(spaces).replace(",", "").replace("[", "")
                        spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                        spaces = spaces.replace("|", " ")
                        out[n] = spaces + str(out[n])
                        product.write("%s%s \n" % (out[n], output_list_separator))
                    b = 0
            elif n == len(out) - 1:
                if represent == "binary" or represent == "hex":
                    product.write("%s" % out[n])
                else:
                    spaces_length = len(str(2 ** bits)) - len(str(out[n]))
                    spaces = ["|"] * spaces_length
                    spaces = str(spaces).replace(",", "").replace("[", "")
                    spaces = spaces.replace("]", "").replace("'", "").replace(" ", "")
                    spaces = spaces.replace("|", " ")
                    out[n] = spaces + str(out[n])
                    product.write("%s" % out[n])

    else:
        print "Error: Enter correct output format!"

    product.close()

    print "Message: File" """ "%s" """ "is translated!" % fname
    print "Message: Find your results in" """, "%s", """ % fullname

    if tips == 1:
        print "Tip: whitespace should not be used to separate multipsle values per row!"
        print "Tip: characters other than digits and the decimal point may generate warnings!"
    elif tips == 2:
        print "Tip: input values must be fractional ranging between 0.999... and -0.999...!"
        print "Otherwise the results will be saturated to the maximum/minimum."

# Compare Two's Complementary results from this site
# http://www.exploringbinary.com/binary-converter/

# Converting Decimal to Binary
# http://cs.furman.edu/digitaldomain/more/ch6/dec_frac_to_bin.htm
