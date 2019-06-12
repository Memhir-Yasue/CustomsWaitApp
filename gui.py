import tkinter
import tkinter.messagebox
from tkinter import *
import subprocess
import sys, os


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
            # cwd = str(os.getcwd())
            def resource_path(relative_path):
                if hasattr(sys, '_MEIPASS'):
                    return os.path.join(sys._MEIPASS, relative_path)
                return os.path.join(os.path.abspath("."), relative_path)

            # pwd = os.path.dirname(PROJECT_ROOT)

            messagebox.showinfo('Info', 'Please wait a moment'+os.path.abspath(__file__))
            subprocess.call(['python', resource_path('Customs.py')], shell = False)
            subprocess.call(['Rscript', resource_path('rscript.R')], shell=False)
            subprocess.call(['python', resource_path('by_month.py')], shell = False)
            messagebox.showinfo('Info', 'Process completed for '+str(self.entry.get()))

if __name__ == '__main__':
    window = CustomsGUI()
    window.mainloop()
