import tkMessageBox
import Tkinter, tkFileDialog

root = Tkinter.Tk()

frame_canvas = Tkinter.Frame(root, width=38)
frame_canvas.grid(row=16, column=0, columnspan=3)
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

scrollbarr = Tkinter.Scrollbar(frame_canvas)
scrollbarr.pack(side="right", fill="y")

lisbox = Tkinter.Listbox(frame_canvas)
lisbox.pack()

for i in range(100):
        lisbox.insert("end", i)

scrollbarr.config(command=lisbox.yview)
lisbox.config(yscrollcommand=scrollbarr.set)



root.mainloop()