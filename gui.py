import tkinter
import tkinter.messagebox
from tkinter import *
import subprocess
import sys
from functools import partial


class CustomsGUI(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.geometry = self.set_window_size(self,X = 300, Y = 450)
        self.instruction = Label(text = "Please enter the year(s) you want to report seperated by a comma")
        self.entry = tkinter.Entry(self)
        self.btn_process = tkinter.Button(self, text = "Make charts",highlightbackground = 'green',height = 5, width = 10, command = self.process)
        self.exit = tkinter.Button(self, text = 'Exit', highlightbackground='red', height = 5, width = 10,command = self.quit)
        self.instruction.grid(row=0, column=2, pady=5)
        self.entry.grid(row = 1, column = 2, pady=5)
        self.btn_process.grid(row = 2, column = 2, pady=5)
        self.exit.grid(row = 3, column = 2)

    def quit(self):
        sys.exit()

    def set_window_size(self,window,X,Y):
        window_height = X
        window_width = Y
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_cord = (screen_width/2) - (window_width/2)
        y_cord = (screen_height/2) - (window_height/2)
        window.geometry("%dx%d+%d+%d" % (window_width,window_height,x_cord,y_cord))

    def process(self):
        response = tkinter.messagebox.askquestion("Warning","Are you sure you want to proceed? Previous graphs will get replaced")
        if response == 'yes':
          messagebox.showinfo('Info', 'Please wait a momment')
          subprocess.call(['python', 'Customs.py'], shell = False)
          subprocess.check_call(['Rscript', 'r_script.R'], shell=False)
          subprocess.call(['python', 'by_month.py'], shell = False)
          messagebox.showinfo('Info', 'Process completed for '+str(self.entry.get()))

window = CustomsGUI()
window.mainloop()




# window = tkinter.Tk()
#
# window_width = 450
# window_height = 300
# set_window_size(window,window_height,window_width)
# window.title("Customs wait time processor")
#
# disp = Label(text = "Please enter the year(s) you want to report seperated by a comma")
#
# years_entry = tkinter.Entry(window) # this is placed in 0 1
#
# btn_process = tkinter.Button(window, text = "Make charts",highlightbackground = 'green',height = 5, width = 10, command = hide_window)
#
# btn_quit = tkinter.Button(window, text = 'Exit', highlightbackground='red', height = 5, width = 10,command = quit)
#
# disp.grid(row=0, column=2, pady=5)
# years_entry.grid(row = 1, column = 2, pady=10)
#
# btn_process.grid(row = 3, column = 2,pady=10)
# btn_quit.grid(row = 5, column = 2)
#
# window.mainloop()
