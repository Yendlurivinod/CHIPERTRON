import hashlib
import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
from Cryptodome.Cipher import AES
import intro
import file_share
import download
from intro import *
from file_share import *
from download import *

class EncryptionTool:
    def __init__(self,user_file,user_key,user_salt,):
        self.user_file = user_file
        self.input_file_size = os.path.getsize(self.user_file)
        self.chunk_size = 1024
        self.total_chunks = self.input_file_size // self.chunk_size + 1
        self.user_key = bytes(user_key, "utf-8")
        self.user_salt = bytes(user_key[::-1], "utf-8")
        self.file_extension = self.user_file.split(".")[-1]
        self.hash_type = "SHA256"
        self.encrypt_output_file = (
            ".".join(self.user_file.split(".")[:-1])
            + "."
            + self.file_extension
            + ".encr"
        )
        self.decrypt_output_file = self.user_file[:-5].split(".")
        self.decrypt_output_file = (
            ".".join(self.decrypt_output_file[:-1])
            + "_decrypted."
            + self.decrypt_output_file[-1]
        )
        self.hashed_key_salt = dict()
        self.hash_key_salt()

    def read_in_chunks(self, file_object, chunk_size=1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def encrypt(self):
        cipher_object = AES.new(
            self.hashed_key_salt["key"], AES.MODE_CFB, self.hashed_key_salt["salt"]
        )
        self.abort() 
        input_file = open(self.user_file, "rb")
        output_file = open(self.encrypt_output_file, "ab")
        done_chunks = 0

        for piece in self.read_in_chunks(input_file, self.chunk_size):
            encrypted_content = cipher_object.encrypt(piece)
            output_file.write(encrypted_content)
            done_chunks += 1
            yield done_chunks / self.total_chunks * 100

        input_file.close()
        output_file.close()

        del cipher_object

    def decrypt(self):

        cipher_object = AES.new(
            self.hashed_key_salt["key"], AES.MODE_CFB, self.hashed_key_salt["salt"]
        )

        self.abort()  

        input_file = open(self.user_file, "rb")
        output_file = open(self.decrypt_output_file, "xb")
        done_chunks = 0

        for piece in self.read_in_chunks(input_file):
            decrypted_content = cipher_object.decrypt(piece)
            output_file.write(decrypted_content)
            done_chunks += 1
            yield done_chunks / self.total_chunks * 100

        input_file.close()
        output_file.close()

        del cipher_object
    def abort(self):
        if os.path.isfile(self.encrypt_output_file):
            os.remove(self.encrypt_output_file)
        if os.path.isfile(self.decrypt_output_file):
            os.remove(self.decrypt_output_file)

    def hash_key_salt(self):
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_key)
        self.hashed_key_salt["key"] = bytes(hasher.hexdigest()[:32], "utf-8")

        del hasher

        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_salt)

        self.hashed_key_salt["salt"] = bytes(hasher.hexdigest()[:16], "utf-8")

        del hasher

class MainWindow():
    def __init__(self, root):
        self.root = root
        self._cipher = None
        self._file_url = tk.StringVar()
        self._secret_key = tk.StringVar()
        self._salt = tk.StringVar()
        self._status = tk.StringVar()
        self._status.set("")

        self.should_cancel = False
        root.title("main")
        root.configure(bg="#eeeeee")
        self.menu_bar = tk.Menu(root, bg="#eeeeee")
        root.configure(menu=self.menu_bar)       
        self.l1 = tk.Label(
            root,
            text="Enter File Path Or Select file",
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

        self.pass1 = tk.Label(
            root,
            text="Enter password",
            bg="#eeeeee",
            anchor=tk.W,
        )
        self.pass1.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=3,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.pass2 = tk.Entry(
            root,
            textvariable=self._secret_key,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT,
        )
        self.pass2.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=8,
            row=4,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )       
        self.encrypt_btn = tk.Button(
            root,
            text="ENCRYPT",
            command=self.e_check_callback,
            bg="#000",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
        )
        self.encrypt_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=0,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.decrypt_btn = tk.Button(
            root,
            text="DECRYPT",
            command=self.d_check_callback,
            bg="#000",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
        )
        self.decrypt_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=2,
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
            row=8,
            column=0,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        self.stop_btn = tk.Button(
            root,
            text="STOP",
            command=self.cancel_callback,
            bg="#aaaaaa",
            fg="#ffffff",
            bd=2,
            state="disabled",
            relief=tk.FLAT,
        )
        self.stop_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=8,
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
        self.pass2.configure(state="disabled")
        self.select.configure(state="disabled", bg="#aaaaaa")
        self.encrypt_btn.configure(state="disabled", bg="#aaaaaa")
        self.decrypt_btn.configure(state="disabled", bg="#aaaaaa")
        self.clear_btn.configure(state="disabled", bg="#aaaaaa")
        self.stop_btn.configure(state="normal", bg="#e74c3c")
        self.status_label.update()

    def unfreeze_controls(self):
        self.fe.configure(state="normal")
        self.pass2.configure(state="normal")
        self.select.configure(state="normal", bg="#000")
        self.encrypt_btn.configure(state="normal", bg="#000")
        self.decrypt_btn.configure(state="normal", bg="#000")
        self.clear_btn.configure(state="normal", bg="#000")
        self.stop_btn.configure(state="disabled", bg="#aaaaaa")
        self.status_label.update()

    def e_check_callback(self):

        newPath = Path(self._file_url.get())
        if newPath.is_file():
            pass
        else:
            messagebox.showinfo("main", "Please Enter a valid File URL !!")
            return

        if len(self._secret_key.get()) == 0:
            messagebox.showinfo("main", "Please Enter a valid Secret Key !!")
            return
        self.encrypt_callback()

    def d_check_callback(self):

        newPath = Path(self._file_url.get())
        if newPath.is_file():
            pass
        else:
            messagebox.showinfo("main", "Please Enter a valid File URL !!")
            return

        if self._file_url.get()[-4:] != "encr":
            messagebox.showinfo(
                "main",
                """File is not an Encrypted File !!
Please Enter an Encrypted File to Decrypt.""",
            )
            return

        if len(self._secret_key.get()) == 0:
            messagebox.showinfo("main", "Please Enter a Secret Key !!")
            return
        
        self.decrypt_callback()

    def encrypt_callback(self):
        t1 = threading.Thread(target=self.encrypt_execute)
        t1.start()

    def encrypt_execute(self):
        self.freeze_controls()
        try:
            self._cipher = EncryptionTool(
                self._file_url.get(), self._secret_key.get(), self._salt.get()
            )
            for percentage in self._cipher.encrypt():
                if self.should_cancel:
                    break
                percentage = "{0:.2f}% completed".format(percentage)
                self._status.set(percentage)
                self.status_label.update()

            if self.should_cancel:
                self._cipher.abort()
                self._status.set("Cancellation Successful !!")
                self._cipher = None
                self.should_cancel = False
                self.unfreeze_controls()
                return
            self._cipher = None
            self.should_cancel = False
            self._status.set("File Encryption Successful !!")
        except Exception as e:

            self._status.set(e)

        self.unfreeze_controls()

    def decrypt_callback(self):
        t2 = threading.Thread(target=self.decrypt_execute)
        t2.start()

    def decrypt_execute(self):
        self.freeze_controls()

        try:
            self._cipher = EncryptionTool(
                self._file_url.get(), self._secret_key.get(), self._salt.get()
            )
            for percentage in self._cipher.decrypt():
                if self.should_cancel:
                    break
                percentage = "{0:.2f}% completed".format(percentage)
                self._status.set(percentage)
                self.status_label.update()

            if self.should_cancel:
                self._cipher.abort()
                self._status.set("Cancellation Successful !!")
                self._cipher = None
                self.should_cancel = False
                self.unfreeze_controls()
                return
            self._cipher = None
            self.should_cancel = False
            self._status.set("File Decryption Successful !!")
        except Exception as e:
            self._status.set(e)

        self.unfreeze_controls()

    def reset_callback(self):
        self._cipher = None
        self._file_url.set("")
        self._secret_key.set("")
        self._salt.set("")
        self._status.set("")

    def cancel_callback(self):
        self.should_cancel = True
def call1():
        ROOT = tk.Tk()
        screen_width = ROOT.winfo_screenwidth()
        screen_height = ROOT.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (200))
        y_cordinate = int((screen_height/2) - (200))
        ROOT.geometry("{}x{}+{}+{}".format(400, 400, x_cordinate, y_cordinate))
        MAIN_WINDOW = MainWindow(ROOT)
        ROOT.resizable(height=False, width=False)
        ROOT.mainloop() 
def back(root):
    root.destroy()
    intro.call0()    
if __name__ == "__main__":
    call1()