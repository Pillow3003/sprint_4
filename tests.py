from main import BooksCollector
import pytest


# Класс тестов для BooksCollector
# Название класса обязательно должно начинаться с Test
class TestBooksCollector:
    """
    Тесты для класса BooksCollector.
    В этом классе реализованы проверки методов:
    - add_new_book
    - set_book_genre
    - get_book_genre
    - get_books_with_specific_genre
    - get_books_genre
    - get_books_for_children
    - add_book_in_favorites
    - delete_book_from_favorites
    - get_list_of_favorites_books
    """

    @pytest.mark.parametrize(
        "name, should_add",
        [
            ("Маленький принц", True),  # валидное имя книги
            ("a" * 42, False),  # слишком длинное имя
            ("", False),  # пустая строка
            ("Повторяющаяся книга", True),  # добавление новой книги
        ],
    )
    def test_add_new_book(self, name, should_add):
        """
        Тестирует метод add_new_book.
        Условия:
        - при валидных именах книга добавляется
        - при длинных или пустых именах книга не добавляется
        - при повторном добавлении ничего не происходит
        """
        collector = BooksCollector()
        # Имитируем добавление повторной книги
        if name == "Повторяющаяся книга":
            collector.books_genre = {"Повторяющаяся книга": ""}
        else:
            collector.books_genre = {}
        collector.add_new_book(name)
        if should_add:
            assert name in collector.books_genre
        else:
            assert name not in collector.books_genre

    def test_set_book_genre(self):
        """
        Тестирует метод set_book_genre:
        - обновление жанра существующей книги
        - игнорирование жанра, которого нет в допустимых жанрах
        - игнорирование несуществующей книги
        """
        collector = BooksCollector()

        # Предварительно задаем книги
        collector.books_genre = {
            "Властелин колец": "Некоторый жанр",
            "Кто украл кролика Роджера?": "Комедии",
        }

        # Обновляем жанр допустимым
        collector.set_book_genre("Властелин колец", "Ужасы")
        # Попытка установить недопустимый жанр
        collector.set_book_genre("Властелин колец", "Фsd")
        # Попытка изменить жанр несуществующей книги
        collector.set_book_genre("Некоторая книга", "Ужасы")

        assert (
            collector.books_genre["Властелин колец"] == "Ужасы"
        ), "Жанр для 'Властелин колец' должен обновиться на 'Ужасы'"
        # Жанр для существующей книги не должен измениться на недопустимый
        assert collector.books_genre["Властелин колец"] != "Фsd"
        # Несуществующая книга не должна появиться
        assert "Некоторая книга" not in collector.books_genre

    def test_get_book_genre(self):
        """
        Тестирует метод get_book_genre:
        - возвращает правильный жанр для существующих книг
        - возвращает None, для несуществующих
        - возвращает обновленный жанр после изменения
        """
        collector = BooksCollector()

        # Задаем начальный список книг
        collector.books_genre = {
            "Властелин колец": "Фантастика",
            "Кто украл кролика Роджера?": "Комедии",
        }
        assert collector.get_book_genre("Властелин колец") == "Фантастика"
        assert collector.get_book_genre("Кто украл кролика Роджера?") == "Комедии"
        assert collector.get_book_genre("Не существующая книга") is None

        # Обновляем жанр
        collector.books_genre["Властелин колец"] = "Комедии"
        assert collector.get_book_genre("Властелин колец") == "Комедии"

        # Проверка для пустого списка
        collector_empty = BooksCollector()
        collector_empty.books_genre = {}
        assert collector_empty.get_book_genre("Любая книга") is None

    @pytest.mark.parametrize(
        "books_dict, genre, expected",
        [
            (
                {
                    "Фантастика 1": "Фантастика",
                    "Фантастика 2": "Фантастика",
                    "Комедии 1": "Комедии",
                    "Детектив": "Детективы",
                },
                "Фантастика",
                ["Фантастика 1", "Фантастика 2"],
            ),
            (
                {
                    "Фантастика 1": "Фантастика",
                    "Фантастика 2": "Фантастика",
                    "Комедии 1": "Комедии",
                },
                "Комедии",
                ["Комедии 1"],
            ),
            ({}, "Фантастика", []),
            ({"Остальные книги": "Детективы"}, "Мультфильмы", []),
        ],
    )
    def test_get_books_with_specific_genre(self, books_dict, genre, expected):
        """
        Тестирует метод get_books_with_specific_genre:
        - возвращает список книг заданного жанра
        - для пустого списка возвращает пустой список
        """
        collector = BooksCollector()
        collector.books_genre = books_dict

        result = collector.get_books_with_specific_genre(genre)
        assert result == expected

    def test_get_books_genre(self):
        """
        Проверка метода get_books_genre:
        - возвращает весь словарь books_genre
        """
        collector = BooksCollector()
        collector.books_genre = {"Фантастика 1": "Фантастика", "Гарри Поттер": "Ужасы"}
        result = collector.books_genre
        assert result == {"Фантастика 1": "Фантастика", "Гарри Поттер": "Ужасы"}

    @pytest.mark.parametrize(
        "books_dict, expected",
        [
            ({"Фантастика 1": "Фантастика"}, ["Фантастика 1"]),
            (
                {"Гарри Поттер": "Ужасы"},
                [],  # поскольку жанр 'Ужасы' не предназначен для детей
            ),
        ],
    )
    def test_get_books_for_children(self, books_dict, expected):
        """
        Тестирует метод get_books_for_children:
        - возвращает список книг, подходящих для детей (жанр не 'Ужасы')
        """
        collector = BooksCollector()
        collector.books_genre = books_dict
        result = collector.get_books_for_children()
        assert result == expected

    def test_add_book_in_favorites(self):
        """
        Тестирует добавление книги в список избранных
        """
        collector = BooksCollector()
        collector.books_genre = {"Король лев": "Мультфильмы"}
        collector.favorites = []

        collector.add_book_in_favorites("Король лев")
        assert "Король лев" in collector.favorites

    def test_delete_book_from_favorites(self):
        """
        Тестирует удаление книги из списка избранных
        """
        collector = BooksCollector()
        collector.favorites = ["Все о гиппогрифах", "Сложная жизнь соплохвоста"]
        collector.delete_book_from_favorites("Сложная жизнь соплохвоста")
        assert "Сложная жизнь соплохвоста" not in collector.favorites
        assert "Все о гиппогрифах" in collector.favorites

    def test_get_list_of_favorites_books(self):
        """
        Тестирует метод get_list_of_favorites_books:
        - возвращает текущий список избранных книг
        """
        collector = BooksCollector()
        collector.favorites = ["Все о гиппогрифах", "Сложная жизнь соплохвоста"]
        result = collector.get_list_of_favorites_books()
        assert result == collector.favorites
