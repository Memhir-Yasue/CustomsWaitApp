import tkinter
import tkinter.messagebox
from tkinter import *
import subprocess
import sys
from functools import partial


def process():
    # subprocess.call(['python', 'Customs.py'], shell = False)
    subprocess.check_call(['Rscript', 'r_script.R'], shell=False)
    messagebox.showinfo('Info', 'Process completed!')

def quit():
    sys.exit()

def set_window_size(window,X,Y):
    window_width = Y
    window_height = X
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cord = (screen_width/2) - (window_width/2)
    y_cord = (screen_height/2) - (window_height/2)
    window.geometry("%dx%d+%d+%d" % (window_width,window_height,x_cord,y_cord))

def hide_window():
    response = tkinter.messagebox.askquestion("Warning","Are you sure you want to proceed? Previous graphs will get replaced")
    if response == 'yes':
      messagebox.showinfo('Info', 'Please wait a momment')
      subprocess.call(['python', 'Customs.py'], shell = False)
      subprocess.check_call(['Rscript', 'r_script.R'], shell=False)
      subprocess.call(['python', 'by_month.py'], shell = False)
      messagebox.showinfo('Info', 'Process completed!')
      # processing_message = tkinter.Toplevel()
      # exit_message = window = tkinter.Tk()
      # set_window_size(processing_message,150,200)
      # set_window_size(exit_message,150,200)
      # status = tkinter.Label(processing_message, text="Charts are being generated!").grid(row=0,column=0)

      # window.after(100,processing_message.destroy())
      # window.after(100,messagebox.showinfo('Info', 'Process completed!'))




window = tkinter.Tk()

window_width = 450
window_height = 300
set_window_size(window,window_height,window_width)
window.title("Customs wait time processor")

disp = Label(text = "Please enter the year(s) you want to report seperated by a comma")

years_entry = tkinter.Entry(window) # this is placed in 0 1

btn_process = tkinter.Button(window, text = "Make charts",highlightbackground = 'green',height = 5, width = 10, command = hide_window)

btn_quit = tkinter.Button(window, text = 'Exit', highlightbackground='red', height = 5, width = 10,command = quit)

disp.grid(row=0, column=2, pady=5)
years_entry.grid(row = 1, column = 2, pady=10)

btn_process.grid(row = 3, column = 2,pady=10)
btn_quit.grid(row = 5, column = 2)

window.mainloop()
