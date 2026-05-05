import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x500")
        
        # Загружаем данные при старте
        self.movies = self.load_movies()
        # Список для отображения (нужен для фильтрации)
        self.displayed_movies = self.movies.copy()
        
        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        """Создает интерфейс: поля, кнопки и таблицу."""
        
        # --- Блок фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", font=("Arial", 12))
        filter_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(filter_frame, text="Год:").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.filter_year = tk.Entry(filter_frame)
        self.filter_year.grid(row=0, column=3, padx=5, pady=2)

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=10)

        clear_btn = tk.Button(filter_frame, text="Очистить фильтр", command=self.clear_filter)
        clear_btn.grid(row=0, column=5, padx=10)


        # --- Блок добавления ---
        input_frame = tk.LabelFrame(self.root, text="Добавить новый фильм", font=("Arial", 12))
        input_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.title_entry = tk.Entry(input_frame)
        self.title_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.genre_entry = tk.Entry(input_frame)
        self.genre_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=2)

        tk.Label(input_frame, text="Год:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.year_entry = tk.Entry(input_frame)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=2, column=2, padx=5, pady=2, sticky="e")
        self.rating_entry = tk.Entry(input_frame)
        self.rating_entry.grid(row=2, column=3, padx=5, pady=2)

        add_btn = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=3, columnspan=4, pady=15)


        # --- Таблица ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.pack(expand=True, fill="both", padx=20)

    def add_movie(self):
         """Обрабатывает добавление фильма с проверкой данных."""
         title = self.title_entry.get().strip()
         genre = self.genre_entry.get().strip()
         
         if not title or not genre:
             messagebox.showerror("Ошибка", "Поля 'Название' и 'Жанр' обязательны.")
             return

         try:
             year = int(self.year_entry.get().strip())
             if year < 1895 or year > 3000:
                 raise ValueError
             year_str = str(year)
         except ValueError:
             messagebox.showerror("Ошибка", "Год должен быть целым числом (например: 2023).")
             return

         try:
             rating = float(self.rating_entry.get().strip())
             if rating < 0 or rating > 10:
                 raise ValueError
             rating_str = f"{rating:.1f}"
         except ValueError:
             messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
             return

         movie_data = {
             "title": title,
             "genre": genre,
             "year": year_str,
             "rating": rating_str
         }
         
         # Добавляем в ОСНОВНОЙ список и сохраняем в файл
         self.movies.append(movie_data)
         self.save_movies()
         
         # Добавляем в СПИСОК ОТОБРАЖЕНИЯ и обновляем таблицу
         self.displayed_movies.append(movie_data)
         self.update_treeview()
         
         # Очищаем поля ввода
         self.title_entry.delete(0, tk.END)
         self.genre_entry.delete(0, tk.END)
         self.year_entry.delete(0, tk.END)
         self.rating_entry.delete(0, tk.END)
         
    def update_treeview(self):
         """Очищает таблицу и заполняет её данными из списка для отображения."""
         for i in self.tree.get_children():
             self.tree.delete(i)
         for movie in self.displayed_movies:
             self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def save_movies(self):
         """Сохраняет основной список фильмов в JSON."""
         try:
             with open(DATA_FILE, 'w', encoding='utf-8') as f:
                 json.dump(self.movies, f, ensure_ascii=False, indent=4)
         except Exception as e:
             messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")

    def load_movies(self):
         """Загружает фильмы из JSON при запуске."""
         if os.path.exists(DATA_FILE):
             try:
                 with open(DATA_FILE, 'r', encoding='utf-8') as f:
                     return json.load(f)
             except Exception as e:
                 messagebox.showwarning("Ошибка загрузки", f"Не удалось загрузить данные: {e}")
                 return []
         return []
         
    def apply_filter(self):
         """Фильтрует список отображаемых фильмов."""
         filtered_genre = self.filter_genre.get().strip().lower()
         filtered_year = self.filter_year.get().strip()
         
         # Создаем новый список для отображения на основе фильтров
         filtered_list = []
         
         for movie in self.movies: # Фильтруем по основному списку!
             match_genre = True
             match_year = True
             
             if filtered_genre and filtered_genre not in movie["genre"].lower():
                 match_genre = False
                 
             if filtered_year and movie["year"] != filtered_year:
                 match_year = False
                 
             if match_genre and match_year:
                 filtered_list.append(movie)
                 
         self.displayed_movies = filtered_list if (filtered_genre or filtered_year) else self.movies.copy()
         
         self.update_treeview()

    def clear_filter(self):
         """Сбрасывает фильтр и показывает все фильмы."""
         self.filter_genre.delete(0, tk.END)
         self.filter_year.delete(0, tk.END)
         
         # Сбрасываем отображаемый список к полному списку фильмов
         self.displayed_movies = self.movies.copy()
         
         self.update_treeview()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()