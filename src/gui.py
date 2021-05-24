import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def askopenfilename(*args):
	# get input filename
	filename = filedialog.askopenfilename()
	# open file on your own
	if filename:
		askopenfilename.file = filename
		status.set("loaded file: " + filename + "\n click 'Run' to translate into binary.")

def Hack_Assembler(*args):
	status.set("Converting into binary......")
	os.system('python assembler.py ' + askopenfilename.file)
	status.set("Done. \n check for .hack file generated.")

root = Tk()
root.title("Hack Assembler")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

status = StringVar()

ttk.Button(mainframe, text="Open File", command=askopenfilename).grid(column=3, row=1, sticky=(W, E))
ttk.Label(mainframe, textvariable=status).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Run", command=Hack_Assembler).grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children():
	child.grid_configure(padx=5, pady=5)

root.bind('<Return>', Hack_Assembler)
root.mainloop()
