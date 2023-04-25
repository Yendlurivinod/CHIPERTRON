from tkinter import * 
import tkinter.font as tkf
import tool
import file_share
import download
from tool import *
from file_share import *
from download import *

def start(root):
    l1=Label( root,
            text="CIPHER-TRON",
            bg="#eeeeee",
            fg="#ec7c3c",
            font=('Helvetica bold',34),).grid(padx=12,
            pady=(30, 65),
            ipadx=0,
            ipady=1,
            row=0,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E,)
    b1=Button(root,text='Encryption Tool',font=20,background="#000",fg="#fff",command=lambda:change(root)).grid(padx=12,
            pady=8,
            ipadx=0,
            ipady=4,
            row=1,
            column=0,
            columnspan=1,
            sticky=tk.W + tk.E + tk.N + tk.S,)
    b2=Button(root,text='Upload Files',font=20,background="#000",fg="#fff",command=lambda:change2(root)).grid(padx=12,
            pady=8,
            ipadx=0,
            ipady=4,
            row=2,
            column=0,
            columnspan=1,
            sticky=tk.W + tk.E + tk.N + tk.S,)
    b2=Button(root,text='Download Files',font=20,background="#000",fg="#fff",command=lambda:change3(root)).grid(padx=12,
            pady=8,
            ipadx=0,
            ipady=4,
            row=3,
            column=0,
            columnspan=1,
            sticky=tk.W + tk.E + tk.N + tk.S,)
    root.title('mainpage')
    #root.geometry('400x400')
    tk.Grid.columnconfigure(root, 0, weight=1)
    
def change(root):
    root.destroy()
    tool.call1()

def change2(root):
    root.destroy()
    file_share.call2()

def change3(root):
    root.destroy()
    download.call3()

def call0():
    root=Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (200))
    y_cordinate = int((screen_height/2) - (200))
    root.geometry("{}x{}+{}+{}".format(400, 400, x_cordinate, y_cordinate))
    start(root)
    root.mainloop()
if __name__ == "__main__":
    call0()

  