import argparse
import threading
import tkinter as tk
from flask import Flask, request, jsonify
from tkinter import ttk

from num_to_word import number_to_words

# сборка exe файла
# pyinstaller --onefile --windowed converter.py


def convert_number(num, ed_param_rub, ed_param_kop):
    if num == 0:
        if ed_param_rub and ed_param_kop:
            result_rub = number_to_words(num, ed_param_rub)
            result_kop = number_to_words(num, ed_param_kop)
            result = result_rub + " " + result_kop
        elif ed_param_kop:
            result = number_to_words(num, ed_param_kop)
        elif ed_param_rub:
            result = number_to_words(num, ed_param_rub)
        else:
            result = number_to_words(num, "")
    else:
        num_rub, num_kop = divmod(num, 100)
        if ed_param_rub and ed_param_kop:
            result_rub = number_to_words(num_rub, ed_param_rub)
            result_kop = number_to_words(num_kop, ed_param_kop)
            result = result_rub + " " + result_kop
        elif ed_param_kop:
            result = number_to_words(num_rub, ed_param_kop)
        elif ed_param_rub:
            result = number_to_words(num_rub, ed_param_rub)
        else:
            result = number_to_words(num_rub, "")
    return result


def window_interface():
    def convert_button():
        try:
            num = float(entry.get())
        except ValueError:
            result_text.config(state='normal')
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Ошибка: введите число")
            result_text.config(state='disabled')
            return

        rub_selected = rub_var.get()
        kop_selected = kop_var.get()

        # Определяем параметр для функции
        ed_param_rub = ""
        ed_param_kop = ""
        if rub_selected:
            ed_param_rub = "rub"
        if kop_selected:
            ed_param_kop = "kop"

        num = int(num * 100)
        result = convert_number(num, ed_param_rub, ed_param_kop)
        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        result_text.config(state='disabled')

    # Создаем главное окно
    root = tk.Tk()
    root.title("Цена прописью")
    root.geometry("500x350")

    # Создаем и размещаем элементы интерфейса
    tk.Label(root, text="Введите число:").pack(pady=5)
    entry = ttk.Entry(root)
    entry.pack(pady=5)

    # Флажки для выбора единиц измерения
    rub_var = tk.BooleanVar()
    kop_var = tk.BooleanVar()

    check_frame = ttk.Frame(root)
    check_frame.pack(pady=5)
    (ttk.Checkbutton(check_frame, text="рубли", variable=rub_var)
        .pack(side=tk.LEFT, padx=10))
    (ttk.Checkbutton(check_frame, text="копейки", variable=kop_var)
        .pack(side=tk.LEFT, padx=10))

    # Кнопка для выполнения преобразования
    (ttk.Button(root, text="Преобразовать", command=convert_button)
        .pack(pady=10))

    # Поле для вывода результата с возможностью копирования
    tk.Label(root, text="Результат:").pack()

    result_frame = ttk.Frame(root)
    result_frame.pack(pady=5, fill=tk.X, padx=10)

    result_text = tk.Text(result_frame, height=4, wrap=tk.WORD)
    scrollbar = ttk.Scrollbar(result_frame, command=result_text.yview)
    result_text.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Делаем поле доступным только для чтения, но с возможностью копирования
    result_text.config(state='disabled')

    # Добавляем контекстное меню для копирования
    def copy_text(event=None):
        root.clipboard_clear()
        text = result_text.get(1.0, tk.END)
        if text.strip():
            root.clipboard_append(text.strip())

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Копировать", command=copy_text)

    def show_menu(event):
        menu.post(event.x_root, event.y_root)

    result_text.bind("<Button-3>", show_menu)

    # Запускаем главный цикл
    root.mainloop()


def api_interface():
    app = Flask(__name__)

    @app.route('/convert', methods=['POST'])
    def api_converter():
        print("request_", request)
        data = request.json
        print("data_", data)
        # logic
        num = float(data.get("price", 0))
        rub = data.get("rubles", False)
        kop = data.get("kopeek", False)
        # Определяем параметр для функции
        ed_param_rub = ""
        ed_param_kop = ""
        if rub:
            ed_param_rub = "rub"
        if kop:
            ed_param_kop = "kop"
        num = int(num * 100)
        converted = convert_number(num, ed_param_rub, ed_param_kop)
        print("converted_", converted)
        return jsonify(result=converted)

    app.run(port=5000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description To Be Here")
    parser.add_argument("--api", action="store_true", help="Run API server")
    args = parser.parse_args()
    if args.api:
        threading.Thread(target=api_interface, daemon=True).start()
    window_interface()
