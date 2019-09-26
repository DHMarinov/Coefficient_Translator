import tkMessageBox
import Tkinter, tkFileDialog
#from Translator_func import *

# ================================================================================================================
# Python
# ================================================================================================================


# def translate(file, structure, separator, format, language, ext, elements, bits):
#    print(file)
#    print(structure)
#    print(separator)
#    print(format)
#    print(language)
#    print(elements)
#    print(bits)
#    print(ext)

def translate(file, structure, separator, format, language, ext, elements, bits):

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
    fullname = coeff.name
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
            #print "Warning: Row", i, "is NaN:", x    # and the the element is reported to the console
            Feedback_list.insert("end", "Warning: Row " + str(i) + " is NaN: " + str(x))
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
        #print "Warning: Output bit length adjusted to", bin_length, "bits!"
        Feedback_list.insert("end", "Warning: Output bit length adjusted to " + str(bin_length) + " bits!")

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
        #print "Error: Enter correct output format!"
        Feedback_list.insert("end", "Error: Enter correct output format!")

    product.close()

    # print "Message: File" """ "%s" """ "is translated!" % fname
    # print "Message: Find your results in" """, "%s", """ % fullname
    Feedback_list.insert("end", "Message: File" """ "%s" """ "is translated!" % fname)
    Feedback_list.insert("end", "Message: Find your results in" """, "%s", """ % fullname)

    if tips == 1:
        # print "Tip: whitespace should not be used to separate multipsle values per row!"
        # print "Tip: characters other than digits and the decimal point may generate warnings!"
        Feedback_list.insert("end", "Tip: in the input file whitespace should not be used to separate multipsle values per row!")
        Feedback_list.insert("end", "Tip: in the input file characters other than digits and the decimal point may generate warnings!")
    elif tips == 2:
        # print "Tip: input values must be fractional ranging between 0.999... and -0.999...!"
        # print "Otherwise the results will be saturated to the maximum/minimum."
        Feedback_list.insert("end", "Rule: input values must be fractional ranging between 0.999... and -0.999...!")
        Feedback_list.insert("end", "Otherwise the results will be saturated to the maximum/minimum.")

# Compare Two's Complementary results from this site
# http://www.exploringbinary.com/binary-converter/

# Converting Decimal to Binary
# http://cs.furman.edu/digitaldomain/more/ch6/dec_frac_to_bin.htm




# ================================================================================================================
# TKinter
# ================================================================================================================

GUI = Tkinter.Tk()
GUI.title("Coefficient Translator")
GUI.resizable(0, 0)
GUI.iconbitmap(r'D:\Workspaces\Python\Translator_GUI\Sim5.ico')

File_var = Tkinter.StringVar()
Struc_var = Tkinter.StringVar()
Struc_var.set(0)                 # If this value is 0, then error
Err_var = Tkinter.IntVar()
Err_var.set(0)


def translate_func():
   try:
      int(Tkinter.Entry.get(El_entry))
   except ValueError:
      Err_var.set(1)
      tkMessageBox.showinfo("The element value must be an integer!", "Ok!")

   try:
      int(Tkinter.Entry.get(Width_entry))
   except ValueError:
      Err_var.set(1)
      tkMessageBox.showinfo("The bit width value must be an integer!", "Ok!")

   if Err_var.get() == 0:
        # print(Tkinter.Entry.get(Browse_entry))
        # print(Struc_var.get())
        # print(Sep_entry.get())
        # print(Form_var.get())
        # print(Lang_var.get())
        # print()
        # print()
        # print()
        translate(Tkinter.Entry.get(Browse_entry),
                Struc_var.get(), Sep_entry.get(),
                Form_var.get(), Lang_var.get(), Ext_entry.get(),
                Tkinter.Entry.get(El_entry), Tkinter.Entry.get(Width_entry))

   Feedback_list.insert("end", "")

def file_func():
   # for line in range(100):
   #    #Feedback_list.config({"height": line})
   #    Feedback_list.insert("end", "This is line number " + str(line))
   #
   # Feedback_list.insert("end", "")

   filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
   filetypes = (("fcf files", "*.fcf"), ("text files", "*.txt"), ("all files", "*.*")))
   Browse_entry.insert(0, filename)


def struc_func():
   if Struc_var.get() == "Array":
      Sep_entry.config({"state": "disabled"})
      Lang_radio_1.config({"state": "normal"})
      Lang_radio_2.config({"state": "normal"})
      Lang_radio_3.config({"state": "normal"})

   elif Struc_var.get() == "List":
      Sep_entry.config({"state": "normal"})
      Lang_radio_1.config({"state": "disabled"})
      Lang_radio_2.config({"state": "disabled"})
      Lang_radio_3.config({"state": "disabled"})


Browse_label = Tkinter.Label(GUI, text="Select file")
Browse_button = Tkinter.Button(GUI, text="Browse", bd=1, relief="raised", command=file_func)
Browse_entry = Tkinter.Entry(GUI, bd=1)

Lang_var = Tkinter.StringVar()
Form_var = Tkinter.StringVar()

Struc_label = Tkinter.Label(GUI, text="Select output file structure")
Struc_radio_1 = Tkinter.Radiobutton(GUI, text="Array", variable=Struc_var, value="Array", command=struc_func)
Struc_radio_2 = Tkinter.Radiobutton(GUI, text="List", variable=Struc_var, value="List", command=struc_func)
Struc_radio_1.select()

Sep_label = Tkinter.Label(GUI, text="Enter file separator")
Sep_entry = Tkinter.Entry(GUI, bd=1, state="disable")
Sep_entry.insert(0, '')

Lang_label = Tkinter.Label(GUI, text="Select language")
Lang_radio_1 = Tkinter.Radiobutton(GUI, text="VHDL", variable=Lang_var, value="VHDL")
Lang_radio_2 = Tkinter.Radiobutton(GUI, text="Verilog", variable=Lang_var, value="Verilog")
Lang_radio_3 = Tkinter.Radiobutton(GUI, text="C", variable=Lang_var, value="C")
Lang_radio_1.select()

Form_label = Tkinter.Label(GUI, text="Select format")
Form_radio_1 = Tkinter.Radiobutton(GUI, text="Binary", variable=Form_var, value="binary")
Form_radio_2 = Tkinter.Radiobutton(GUI, text="Hexadecimal", variable=Form_var, value="hex")
Form_radio_3 = Tkinter.Radiobutton(GUI, text="Signed Integer", variable=Form_var, value="s-integer")
Form_radio_4 = Tkinter.Radiobutton(GUI, text="Unsigned Integer", variable=Form_var, value="u-integer")
Form_radio_1.select()

El_label = Tkinter.Label(GUI, text="Elements per line")
El_entry = Tkinter.Entry(GUI, bd=1)
El_entry.insert(0, '1')

Width_label = Tkinter.Label(GUI, text="Output bit width")
Width_entry = Tkinter.Entry(GUI, bd=1)
Width_entry.insert(0, '16')

Ext_label = Tkinter.Label(GUI, text="File extension")
Ext_entry = Tkinter.Entry(GUI, bd=1)
Ext_entry.insert(0, 'txt')

Translate_button = Tkinter.Button(GUI, text="Translate", bd=1, relief="raised", width=38, command=translate_func)


# Create a frame for the canvas with non-zero row&column weights
frame_canvas = Tkinter.Frame(GUI, width=38)
frame_canvas.grid(row=16, column=0, columnspan=3)
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = Tkinter.Canvas(frame_canvas)
canvas.grid(row=0, column=0, sticky="news")

# canvas.configure(yscrollcommand=vsb.set)
# canvas.configure(xscrollcommand=hsb.set)

# Create a frame to contain the buttons
frame_buttons = Tkinter.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# Add 9-by-5 buttons to the frame
rows = 19
columns = 15
buttons = [[Tkinter.Button() for j in xrange(columns)] for i in xrange(rows)]

#Link a scrollbar to the canvas
vsb = Tkinter.Scrollbar(frame_canvas, orient="vertical")
vsb.grid(row=0, column=1, sticky='ns')
hsb = Tkinter.Scrollbar(frame_canvas, orient="horizontal")
hsb.grid(row=1, column=0, sticky='we')

Feedback_list = Tkinter.Listbox(frame_buttons, width=42, height=12)
Feedback_list.pack() # grid(row=0, column=0)
vsb.config(command = Feedback_list.yview)
hsb.config(command = Feedback_list.xview)
Feedback_list.config(yscrollcommand=vsb.set)
Feedback_list.config(xscrollcommand=hsb.set)

# scrollbarr = Tkinter.Scrollbar(frame_canvas)
# scrollbarr.pack(side="right", fill="y")
#
# Feedback_list = Tkinter.Listbox(frame_canvas)
# Feedback_list.pack()
#
# # for i in range(100):
# #         lisbox.insert("end", i)
#
# scrollbarr.config(command=Feedback_list.yview)
# Feedback_list.config(yscrollcommand=scrollbarr.set)

# for i in range(0, rows):
#     for j in range(0, columns):
#         buttons[i][j] = Tkinter.Button(frame_buttons, text=("%d,%d" % (i+1, j+1)))
#         buttons[i][j].grid(row=i, column=j, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
#print(first5columns_width + vsb.winfo_width())
first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
#print(first5rows_height)
frame_canvas.config(width=270, height=200)
# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))



# Feedback_canvas = Tkinter.Frame(GUI)
# Feedback_canvas.grid(row=15, column=0, pady=(5, 0), sticky='nw')
# Feedback_canvas.grid_rowconfigure(0, weight=1)
# Feedback_canvas.grid_columnconfigure(0, weight=1)
#
# canvas = Tkinter.Canvas(Feedback_canvas)
# canvas.grid(row=15, column=0, sticky="news")
#
# vsb = Tkinter.Scrollbar(Feedback_canvas, orient="vertical", command=canvas.yview)
# vsb.grid(row=0, column=1, sticky='ns')
# canvas.configure(yscrollcommand=vsb.set)
#
# # Feedback_canvas = Tkinter.Canvas(frame_canvas)
# # canvas.grid(row=0, column=0, sticky="news")
#
# # Display = Tkinter.Canvas(GUI);
# scroll_y = Tkinter.Scrollbar(GUI)
# # scroll_x = Tkinter.Scrollbar(GUI)
# Feedback_list = Tkinter.Listbox(GUI, width=38)

# ----------==========|Structure|==========----------
Browse_label.grid(row=0, column=0, sticky='W')
Browse_button.grid(row=0, column=1)
Browse_entry.grid(row=0, column=2)

Struc_label.grid(row=1, column=0, columnspan=2)
Struc_radio_1.grid(row=1, column=2, sticky='W')
Struc_radio_2.grid(row=2, column=2, sticky='W')

Sep_label.grid(row=3, column=0, columnspan=2, sticky='W')
Sep_entry.grid(row=3, column=2)

Lang_label.grid(row=4, column=0, columnspan=2, sticky='W')
Lang_radio_1.grid(row=4, column=2, sticky='W')
Lang_radio_2.grid(row=5, column=2, sticky='W')
Lang_radio_3.grid(row=6, column=2, sticky='W')

Form_label.grid(row=7, column=0, columnspan=2, sticky='W')
Form_radio_1.grid(row=7, column=2, sticky='W')
Form_radio_2.grid(row=8, column=2, sticky='W')
Form_radio_3.grid(row=9, column=2, sticky='W')
Form_radio_4.grid(row=10, column=2, sticky='W')

El_label.grid(row=11, column=0, columnspan=2, sticky='W')
El_entry.grid(row=11, column=2)

Width_label.grid(row=12, column=0, columnspan=2, sticky='W')
Width_entry.grid(row=12, column=2)

Ext_label.grid(row=13, column=0, columnspan=2, sticky='W')
Ext_entry.grid(row=13, column=2)

Translate_button.grid(row=14, columnspan=3)

#Display.grid(row=14, columnspan=3, rowspan=4)

#Feedback_list.grid(row=14, columnspan=5, rowspan=4)
#scroll_y.grid(row=14, rowspan=4, sticky='E')
# scroll_x.grid(row=18, sticky='S')

GUI.mainloop()

# Translating floating point to 2s compliment format.
# The input values must raange between 0.999... and -0.999...
# Values exceeding the above-mentioned limits will be saturated
