from tkinter import messagebox
from tkinter import *
from tkinter import filedialog as fd
import PyPDF2
import pdfplumber
import pyttsx3


def select_file():
    file_entry.delete(0, END)
    file = fd.askopenfilename(title="Select file", filetypes=(("PDF Files", "*.pdf"),))
    file_entry.insert(0, file)


def open_pdf():
    text_to_speak = ''
    file = file_entry.get()
    try:
        pdf_file_obj = open(file, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_of_pages = len(pdf_reader.pages)
    except FileNotFoundError:
        messagebox.showinfo("File not found", "File not found")
    else:
        with pdfplumber.open(file) as pdf:
            for i in range(num_of_pages):
                page = pdf.pages[i]
                text_to_speak += page.extract_text()
    return text_to_speak


def speak():
    text_to_speak = open_pdf()
    if text_to_speak:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        voice_select = voice_selection()
        engine.setProperty('voice', voices[voice_select].id)
        engine.say(text_to_speak)
        engine.runAndWait()


def save_mp3():
    text_to_speak = open_pdf()
    if text_to_speak:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        voice_select = voice_selection()
        engine.setProperty('voice', voices[voice_select].id)
        try:
            filename_to_save = fd.asksaveasfilename() + '.mp3'
            engine.save_to_file(text_to_speak, filename_to_save)
            engine.runAndWait()
        except Exception as error:
            messagebox.showerror("Error", f'{error}, the file could not be save.')
        else:
            messagebox.showinfo('Success', 'Job successfully donne.')


def voice_selection():
    selection = var.get()
    return selection


# ----------------UI---------------

window = Tk()
window.title('PDF to Audio')
window.config(padx=50, pady=50)
var = IntVar()  # For radio buttons

file_entry = Entry(width=40)
file_entry.grid(column=1, row=0, padx=10)
file_entry.focus()

r1 = Radiobutton(window, text='Male voice', value=0, command=voice_selection, variable=var)
r1.grid(column=0, row=1, pady=10, sticky='W')

r2 = Radiobutton(window, text='Female voice', value=1, command=voice_selection, variable=var)
r2.grid(column=1, row=1, sticky='E')

open_file_btn = Button(text="Select PDF file", command=select_file)
open_file_btn.grid(column=0, row=0, padx=10)

read_btn = Button(text="Speak", command=speak)
read_btn.grid(column=0, row=2, columnspan=2, sticky="EW", padx=10, pady=10)

read_btn = Button(text="Save to disk", command=save_mp3)
read_btn.grid(column=0, row=3, columnspan=2, sticky="EW", padx=10, pady=10)

window.mainloop()
