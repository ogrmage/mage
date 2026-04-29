import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # Создаём форму ввода
        ttk.Label(root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(root)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = ttk.Entry(root)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(root, text="Количество страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = ttk.Entry(root)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления книги
        ttk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(root, columns=("Название", "Автор", "Жанр", "Страницы"), show="headings")
        self.tree.column("Название", width=150)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=100)
        self.tree.column("Страницы", width=80)
        self.tree.heading("Название", text="Название")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страницы")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        ttk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5)
        self.genre_filter = ttk.Entry(root)
        self.genre_filter.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(root, text="Фильтр по страницам (>):").grid(row=7, column=0, padx=5, pady=5)
        self.pages_filter = ttk.Entry(root)
        self.pages_filter.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(root, text="Применить фильтры", command=self.filter_books).grid(row=8, column=0, padx=5, pady=5)
        ttk.Button(root, text="Очистить фильтры", command=self.clear_filters).grid(row=8, column=1, padx=5, pady=5)

        # Кнопки сохранения/загрузки
        ttk.Button(root, text="Сохранить данные", command=self.save_books).grid(row=9, column=0, padx=5, pady=5)
        ttk.Button(root, text="Загрузить данные", command=self.load_books).grid(row=9, column=1, padx=5, pady=5)

        self.update_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка корректности ввода
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }
        self.books.append(book)
        self.update_table()
        messagebox.showinfo("Успех", "Книга добавлена!")

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        for book in self.books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def filter_books(self):
        genre_filter = self.genre_filter.get().strip().lower()
        pages_filter = self.pages_filter.get().strip()

        filtered_books = self.books
        if genre_filter:
            filtered_books = [book for book in filtered_books if genre_filter in book["genre"].lower()]
        if pages_filter and pages_filter.isdigit():
            filtered_books = [book for book in filtered_books if book["pages"] > int(pages_filter)]

        self.tree.delete(*self.tree.get_children())
        for book in filtered_books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def clear_filters(self):
        self.genre_filter.delete(0, tk.END)
        self.pages_filter.delete(0, tk.END)
        self.update_table()

    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены!")

    def load_books(self):
        if os.path.exists("books.json"):
            try:
                with open("books.json", "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.update_table()
                messagebox.showinfo("Успех", "Данные загружены!")
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Файл books.json повреждён!")
        else:
            self.books = []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
