from operation import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3


# Button Action
def load_file1():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            textPlace1.delete(1.0, tk.END)
            textPlace1.insert(tk.END, content)

def load_file2():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            textPlace2.delete(1.0, tk.END)
            textPlace2.insert(tk.END, content)


def highlight_text(text_widget, keyword):
    text_widget.tag_remove("highlight", 1.0, tk.END)
    if keyword:
        start = "1.0"
        while True:
            start = text_widget.search(keyword, start, stopindex=tk.END, nocase = True)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            text_widget.tag_add("highlight", start, end)
            start = end
        text_widget.tag_config("highlight", background="yellow")

def search_and_highlight():
    keyword = search_entry.get()
    highlight_text(textPlace1, keyword)
    highlight_text(textPlace2, keyword)


def compare_texts():
    text1_content = textPlace1.get(1.0, tk.END).strip()
    text2_content = textPlace2.get(1.0, tk.END).strip()
    if not text1_content or not text2_content:
        messagebox.showwarning("Uyarı!", "Her iki metin kutusu da dolu olmak zorundadır.")
        return None

    similarity_ratio = Similarity().percentage(text1_content, text2_content)
    result_label.config(text=f"Benzerlik Yüzdesi: %{similarity_ratio}")

def show_stats1():
    text1_content = textPlace1.get(1.0, tk.END).strip()
    if not text1_content:
        messagebox.showwarning("Uyarı!", "1. Metin kutusu dolu olmak zorunda.")
        return None

    wcount_label.config(text=f"Kelime Sayısı: {TextData(text1_content).get_wordCount()}")
    lcount_label.config(text=f"Harf Sayısı: {TextData(text1_content).get_letterCount()}")
    useless_label.config(text=f"Etkisiz Kelime Sayısı: {TextData(text1_content).get_uselessWordCount()}")
    maxWord.config(text=f"En Çok Geçen Kelimeler: {TextData(text1_content).get_maxWord()}")
    minWord.config(text=f"En Az Geçen Kelimeler: {TextData(text1_content).get_minWord()}")


def show_stats2():
    text2_content = textPlace2.get(1.0, tk.END).strip()
    if not text2_content:
        messagebox.showwarning("Uyarı!", "2. Metin kutusu dolu olmak zorunda.")
        return None

    wcount_label2.config(text=f"Kelime Sayısı: {TextData(text2_content).get_wordCount()}")
    lcount_label2.config(text=f"Harf Sayısı: {TextData(text2_content).get_letterCount()}")
    useless_label2.config(text=f"Etkisiz Kelime Sayısı: {TextData(text2_content).get_uselessWordCount()}")
    maxWord2.config(text=f"En Çok Geçen Kelimeler: {TextData(text2_content).get_maxWord()}")
    minWord2.config(text=f"En Az Geçen Kelimeler: {TextData(text2_content).get_minWord()}")

def upload_db():
    text1_content = textPlace1.get(1.0, tk.END).strip()
    text2_content = textPlace2.get(1.0, tk.END).strip()
    if not text1_content or not text2_content:
        messagebox.showwarning("Uyarı!", "Her iki metin kutusu da dolu olmak zorundadır.")
        return None

    wcount_data1 = f"Kelime Sayısı: {TextData(text1_content).get_wordCount()}"
    lcount_data1 = f"Harf Sayısı: {TextData(text1_content).get_letterCount()}"
    useless_data1 = f"Etkisiz Kelime Sayısı: {TextData(text1_content).get_uselessWordCount()}"
    maxWord_data1 = f"En Çok Geçen Kelimeler: {TextData(text1_content).get_maxWord()}"
    minWord_data1 = f"En Az Geçen Kelimeler: {TextData(text1_content).get_minWord()}"

    wcount_data2 = f"Kelime Sayısı: {TextData(text2_content).get_wordCount()}"
    lcount_data2 = f"Harf Sayısı: {TextData(text2_content).get_letterCount()}"
    useless_data2 = f"Etkisiz Kelime Sayısı: {TextData(text2_content).get_uselessWordCount()}"
    maxWord_data2 = f"En Çok Geçen Kelimeler: {TextData(text2_content).get_maxWord()}"
    minWord_data2 = f"En Az Geçen Kelimeler: {TextData(text2_content).get_minWord()}"

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        # Multi Data
        data = [
            (text1_content, wcount_data1, lcount_data1, useless_data1, maxWord_data1, minWord_data1),
            (text2_content, wcount_data2, lcount_data2, useless_data2, maxWord_data2, minWord_data2)
        ]
        
        cursor.executemany('''
        INSERT INTO stats (text, wcount, lcount, useless, max, min)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', data)

        conn.commit()

    messagebox.showinfo("", "Başarıyla Yüklendi.")

def clear_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stats")

    conn.commit()

    messagebox.showinfo("", "Başarıyla Temizlendi.")

def fetch_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        id = int(spinbox.get())
            
        cursor.execute("SELECT * FROM stats WHERE id = ?", (id,))
        data = cursor.fetchone()
        if data:
            content = data[1]
            wcount = data[2]
            lcount = data[3]
            useless = data[4]
            maxWord = data[5]
            minWord = data[6]

            dataTextPlace.delete(1.0, tk.END)
            dataTextPlace.insert(tk.END, content)
            wcount_label3.config(text=wcount)
            lcount_label3.config(text=lcount)
            useless_label3.config(text=useless)
            maxWord3.config(text=maxWord)
            minWord3.config(text=minWord)

        else:
            dataTextPlace.delete(1.0, tk.END)
            dataTextPlace.insert(tk.END, "Veri Bulunamadı")
            wcount_label3.config(text="")
            lcount_label3.config(text="")
            useless_label3.config(text="")
            maxWord3.config(text="")
            minWord3.config(text="")

with sqlite3.connect("database.db") as conn:

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats
        (id INTEGER PRIMARY KEY, 
        text TEXT, 
        wcount TEXT, 
        lcount TEXT,
        useless TEXT,
        max TEXT,
        min TEXT)
    """)

    conn.commit()


# Window
window = tk.Tk()
window.title("NLP ile Metin Analizi")
window.minsize(width=1300, height=700)


# Label
label = tk.Label(text="Default")
label.config(text="1. Metin")
label.grid(column=0, row=0)

# Text
textPlace1 = tk.Text(height=10, width=30, font="Arial")
textPlace1.focus()
textPlace1.insert(tk.END, "")
print(textPlace1.get("1.0", tk.END))
textPlace1.grid(column=0, row=1, padx=20)

# Load
load_button = tk.Button(window, text="Dosya Yükle", command=load_file1)
load_button.grid(column=0, row=2)

# Search
search_label = tk.Label(window, text="Kelime Arama")
search_label.grid(row=2, column=1)
search_entry = tk.Entry(window)
search_entry.grid(row=3, column=1)
search_button = tk.Button(window, text="Ara ve Vurgula", command=search_and_highlight)
search_button.grid(row=4, column=1)


# Label2
label = tk.Label(text="Default")
label.config(text="2. Metin")
label.grid(column=2, row=0)

# Text
textPlace2 = tk.Text(height=10, width=30, font="Arial")
textPlace2.insert(tk.END, "")
print(textPlace2.get("1.0", tk.END))
textPlace2.grid(column=2, row=1,padx=20)

# Load
load_button = tk.Button(window, text="Dosya Yükle", command=load_file2)
load_button.grid(column=2, row=2)

# Stats
stats_button = tk.Button(window, text="İstatistikleri Göster", command=show_stats1)
stats_button.grid(row=3, column=0)

wcount_label = tk.Label(window)
wcount_label.grid(row=4, column=0)
lcount_label = tk.Label(window)
lcount_label.grid(row=5, column=0)
useless_label = tk.Label(window)
useless_label.grid(row=6, column=0)
maxWord = tk.Label(window, wraplength=200)
maxWord.grid(row=7, column=0)
minWord = tk.Label(window, wraplength=200)
minWord.grid(row=10, column=0)

# Stats 2
wcount_label2 = tk.Label(window)
wcount_label2.grid(row=4, column=2)
lcount_label2 = tk.Label(window)
lcount_label2.grid(row=5, column=2)
useless_label2 = tk.Label(window)
useless_label2.grid(row=6, column=2)
maxWord2 = tk.Label(window, wraplength=200)
maxWord2.grid(row=7, column=2)
minWord2 = tk.Label(window, wraplength=200)
minWord2.grid(row=10, column=2)

stats_button2 = tk.Button(window, text="İstatistikleri Göster", command=show_stats2)
stats_button2.grid(row=3, column=2)


# Similarity
compare_button = tk.Button(window, text="Benzerliği Karşılaştır", command=compare_texts)
compare_button.grid(row=5, column=1)
result_label = tk.Label(window, text="Benzerlik Yüzdesi: ")
result_label.grid(row=6, column=1)

# Send Database
dbsend = tk.Button(window, text="Veritabanına Yükle", command=upload_db)
dbsend.grid(row=1, column=1, pady=0)


# Fetch Spinbox
def spinbox_used():
    id = spinbox.get()
    return id


spinbox = tk.Spinbox(from_=1, to=20, width=5, command=None)
spinbox.grid(row=0,column=4,pady=20)

# Fetch Text
dataTextPlace = tk.Text(height=10, width=30, font="Arial")
dataTextPlace.focus()
dataTextPlace.insert(tk.END, "")
print(dataTextPlace.get("1.0", tk.END))
dataTextPlace.grid(column=4, row=1,padx= 20)

# Stats 3
wcount_label3 = tk.Label(window)
wcount_label3.grid(row=3, column=4)
lcount_label3 = tk.Label(window)
lcount_label3.grid(row=4, column=4)
useless_label3 = tk.Label(window)
useless_label3.grid(row=5, column=4)
maxWord3 = tk.Label(window, wraplength=200)
maxWord3.grid(row=6, column=4)
minWord3 = tk.Label(window, wraplength=200)
minWord3.grid(row=7, column=4)

# Fetch Database
fetch_data = tk.Button(window, text="Veritabanından Çek", command=fetch_db)
fetch_data.grid(row=2, column=4)

# Clear Database
clear_data = tk.Button(window, text="Veritabanını Temizle", command=clear_db)
clear_data.grid(row=1, column=3)

window.mainloop()


