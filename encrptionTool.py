# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 00:40:08 2020

@author: ankit kumar
"""

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


keyPassword = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)

def encrypt_file_button():
    master.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pdf files","*.pdf"),("word files","*.doc"),("word files","*.docx"),("text files","*.txt"),("all files","*.*")))
    password = e1.get()
    if not password:
        messagebox.showinfo("Warning", "Password is empty")
    else:
        key = PBKDF2(password, keyPassword, dkLen=32)
        encrypt_file(master.filename, key)
        messagebox.showinfo("Success", "Encryption Done")
    
def decrypt_file_button():
    master.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("encrypted files","*.enc"),("all files","*.*")))
    password = e1.get()
    if not password:
        messagebox.showinfo("Warning", "Password is empty")
    else:
        key = PBKDF2(password, keyPassword, dkLen=32)
        decrypt_file(master.filename, key)
        messagebox.showinfo("Success", "Decryption Done")


master = tk.Tk()

master.title('Encryption Tool')

tk.Label(master, 
         text="Password").grid(row=0)

e1 = tk.Entry(master)

e1.grid(row=0, column=1)

tk.Button(master, 
          text='Encrypt', 
          command=encrypt_file_button).grid(row=3, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
tk.Button(master, 
          text='Decrypt', command=decrypt_file_button).grid(row=3, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)

tk.Button(master, 
          text='Quit', command=master.quit).grid(row=3, 
                                                       column=2, 
                                                       sticky=tk.W, 
                                                       pady=4)

tk.mainloop()

#pyinstaller --onefile --noconsole encrptionTool.py