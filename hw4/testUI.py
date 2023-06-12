import tkinter as tk
from tkinter import filedialog


def start_processing():
    filepath = filedialog.askopenfilename()
    print(filepath)
    text_output.delete('1.0', tk.END)  # Очищаем текстовый блок
    text_output.insert(tk.END, 'text\nsss\npipi')  # Выводим текст в текстовый блок
    text_output.insert(tk.END, 'wiwiwiwiwi')  # Выводим текст в текстовый блок
    # if filepath:
    #     with open(filepath, 'r') as file:
    #         text = file.read()
    #         text_output.delete('1.0', tk.END)  # Очищаем текстовый блок
    #         text_output.insert(tk.END, 'text\nsss\npipi')  # Выводим текст в текстовый блок


root = tk.Tk()

# Создаем поле выбора файла
file_button = tk.Button(root, text="Выбрать файл", command=start_processing)
file_button.pack()

# Создаем текстовый блок
text_output = tk.Text(root)
text_output.pack()

root.mainloop()
