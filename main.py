import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import PyPDF2
import pdfplumber
import pyttsx3


def select_file():
    file_entry.delete(0, END)
    file = askopenfilename()
    file_entry.insert(0, file)


def open_pdf():
    text_to_speak = ''
    file = file_entry.get()
    pdf_file_obj = open(file, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    num_of_pages = len(pdf_reader.pages)

    with pdfplumber.open(file) as pdf:
        for i in range(num_of_pages):
            page = pdf.pages[i]
            text_to_speak += page.extract_text()
    return text_to_speak


def speak():
    try:
        text_to_speak = open_pdf()
    except FileNotFoundError:
        tkinter.messagebox.showinfo("File not found", "File not found")
    else:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        print(text_to_speak)
        engine.say(text_to_speak)
        engine.runAndWait()


# UI

window = Tk()
window.title('PDF to Audio')
window.config(padx=50, pady=50)

file_entry = Entry()
file_entry.grid(column=0, row=0)
file_entry.focus()

open_file_btn = Button(text="Select PDF file", command=select_file)
open_file_btn.grid(column=1, row=0)

read_btn = Button(text="Speak", command=speak)
read_btn.grid(column=0, row=2, columnspan=2, sticky="EW")

window.mainloop()
