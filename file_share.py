import os
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
import ftplib
import tool
import intro
import download
from intro import *
from tool import *
from download import *

class MainWindow2():
    def __init__(self, root):
        self.root = root
        self._file_url = tk.StringVar()
        self._status = tk.StringVar()
        self._status.set("")
        self.should_cancel = False
        root.title("upload files")
        root.configure(bg="#eeeeee")     
        self.l1 = tk.Label(
            root,
            text="Select file to upload",
            bg="#eeeeee",
            anchor=tk.W,
        )
        self.l1.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=0,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.fe = tk.Entry(
            root,
            textvariable=self._file_url,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT,
        )
        self.fe.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=8,
            row=1,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.select = tk.Button(
            root,
            text="SELECT FILE",
            command=self.selectfile_callback,
            width=42,
            bg="#000",
            fg="#fff",
            bd=2,
            relief=tk.FLAT,
        )
        self.select.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=2,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.upload = tk.Button(
            root,
            text="UPLOAD FILE",
            command=self.upload_file,
            bg="#000",
            fg="#fff",
            bd=2,
            relief=tk.FLAT,
        )
        self.upload.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=0,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.clear_btn = tk.Button(
            root,
            text="CLEAR",
            command=self.reset_callback,
            bg="#000",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
        )
        self.clear_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=2,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )
        self.back_btn = tk.Button(
            root,
            text="BACK",
            command=lambda:back(root),
            bg="#000",
            fg="#fff",
            bd=2,
            relief=tk.FLAT,
        )
        self.back_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=10,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )
        self.status_label = tk.Label(
            root,
            textvariable=self._status,
            bg="#eeeeee",
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.FLAT,
            wraplength=350,
        )
        self.status_label.grid(
            padx=12,
            pady=(0, 12),
            ipadx=0,
            ipady=1,
            row=9,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 1, weight=1)
        tk.Grid.columnconfigure(root, 2, weight=1)
        tk.Grid.columnconfigure(root, 3, weight=1)

    def selectfile_callback(self):
        try:
            name = filedialog.askopenfile()
            self._file_url.set(name.name)
        except Exception as e:
            self._status.set(e)
            self.status_label.update()

    def freeze_controls(self):
        self.fe.configure(state="disabled")
        self.select.configure(state="disabled", bg="#aaaaaa")
        self.clear_btn.configure(state="disabled", bg="#aaaaaa")
        self.status_label.update()

    def unfreeze_controls(self):
        self.fe.configure(state="normal")
        self.select.configure(state="normal", bg="#000")
        self.clear_btn.configure(state="normal", bg="#000")
        self.status_label.update()

    def e_check_callback(self):

        newPath = Path(self._file_url.get())
        if newPath.is_file():
            pass
        else:
            messagebox.showinfo("main", "Please Enter a valid File URL !!")
            return

    def d_check_callback(self):

        newPath = Path(self._file_url.get())
        if newPath.is_file():
            pass
        else:
            messagebox.showinfo("main", "Please Enter a valid File URL !!")
            return

    def reset_callback(self):
        self._file_url.set("")
        self._status.set("")

    def cancel_callback(self):
        self.should_cancel = True
    def upload_file(self):
        self.freeze_controls()
        HOSTNAME = "ftp.dlptest.com"
        USERNAME = "dlpuser"
        PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu"
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        filename = self._file_url.get()
        x=os.path.basename(filename)
        with open(x, "xb") as file:
            ftp_server.storbinary('STOR ' + '/' + x,open(filename,'rb'))

        ftp_server.quit()
        self.unfreeze_controls()
def call2():
        ROOT = tk.Tk()
        MAIN_WINDOW = MainWindow2(ROOT)
        screen_width = ROOT.winfo_screenwidth()
        screen_height = ROOT.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (200))
        y_cordinate = int((screen_height/2) - (200))
        ROOT.geometry("{}x{}+{}+{}".format(400, 400, x_cordinate, y_cordinate))
        ROOT.resizable(height=False, width=False)
        ROOT.mainloop()   
def back(root):
    root.destroy()
    intro.call0()
if __name__ == "__main__":
    call2()