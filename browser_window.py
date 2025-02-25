from PyQt5.QtWidgets import QMainWindow, QLineEdit, QToolBar, QVBoxLayout, QWidget, QTabWidget, QPushButton, \
    QMessageBox, QAction, QComboBox, QDialog, QLabel, QHBoxLayout, QDialogButtonBox, QApplication, QFrame, QSlider, QFontDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QFont
import sys
import pygame


class SearchEngineSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки поисковой системы")
        self.setGeometry(200, 200, 300, 150)

        # Список популярных поисковых систем
        self.search_engines = {
            "Google": "https://www.google.com/search?q=",
            "Yandex": "https://yandex.ru/search/?text=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Bing": "https://www.bing.com/search?q=",
            "Mail.ru": "https://go.mail.ru/search?q="
        }

        # Выпадающий список для выбора поисковой системы
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(self.search_engines.keys())

        # Кнопки для подтверждения или отменя
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите поисковую систему:"))
        layout.addWidget(self.engine_combo)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_selected_engine(self):
        """ Возвращает выбранную поисковую систему. """
        return self.engine_combo.currentText()


class AppearanceSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки внешнего вида")
        self.setGeometry(200, 200, 300, 200)

        # Инициализация переменной для шрифта
        self.selected_font = QFont()  # Инициализируем переменную

        # Выбор темы
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая", "Тёмная"])

        # Выбор шрифта
        self.font_button = QPushButton("Выбрать шрифт")
        self.font_button.clicked.connect(self.choose_font)

        # Масштабирование
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(50)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)

        # Кнопки для подтверждения или отменя
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите тему:"))
        layout.addWidget(self.theme_combo)
        layout.addWidget(QLabel("Выберите шрифт:"))
        layout.addWidget(self.font_button)
        layout.addWidget(QLabel("Масштабирование:"))
        layout.addWidget(self.zoom_slider)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def choose_font(self):
        """ Открывает диалог выбора шрифта. """
        font, ok = QFontDialog.getFont()
        if ok:
            self.selected_font = font

    def get_selected_theme(self):
        """ Возвращает выбранную тему. """
        return self.theme_combo.currentText()

    def get_selected_font(self):
        """ Возвращает выбранный шрифт. """
        return self.selected_font

    def get_zoom_level(self):
        """ Возвращает уровень масштабирования. """
        return self.zoom_slider.value()


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Сохраняем ссылку на родительский объект (BrowserWindow)
        self.init_ui()

    def init_ui(self):
        """ Инициализация интерфейса домашней страницы. """
        layout = QVBoxLayout()

        # Создаем QWebEngineView для отображения анимации
        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.get_animation_html())
        layout.addWidget(self.web_view)

        # Кнопка для перехода на поисковую страницу
        search_button = QPushButton("Перейти к поиску")
        search_button.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
            background-color: #007BFF;
            color: #fff;
            transition: background-color 0.3s;
        """)
        search_button.clicked.connect(lambda: self.open_link("https://www.google.com"))
        search_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(search_button)

        # Кнопка для выхода из приложения
        exit_button = QPushButton("Выход")
        exit_button.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
            background-color: #FF4D4D;
            color: #fff;
            transition: background-color 0.3s;
        """)
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def get_animation_html(self):
        """ Возвращает HTML-код с анимацией текста и минималистичным фоном. """
        return """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    background: linear-gradient(135deg, #f0f0f0, #e0e0e0); /* Минималистичный фон */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Arial', sans-serif;
                }

                .title {
                    font-size: 64px;
                    font-weight: bold;
                    color: #333;
                    text-align: center;
                    animation: float 3s infinite ease-in-out, glow 2s infinite alternate;
                    text-shadow: 0 0 10px rgba(0, 0, 0, 0.2), 0 0 20px rgba(0, 0, 0, 0.1);
                }

                .subtitle {
                    font-size: 24px;
                    font-weight: normal;
                    color: #666;
                    text-align: center;
                    animation: fadeIn 2s ease-in-out infinite alternate;
                }

                @keyframes float {
                    0% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-10px);
                    }
                    100% {
                        transform: translateY(0);
                    }
                }

                @keyframes glow {
                    0% {
                        text-shadow: 0 0 10px rgba(0, 0, 0, 0.2), 0 0 20px rgba(0, 0, 0, 0.1);
                    }
                    100% {
                        text-shadow: 0 0 20px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.2);
                    }
                }

                @keyframes fadeIn {
                    0% {
                        opacity: 0.5;
                    }
                    100% {
                        opacity: 1;
                    }
                }
            </style>
        </head>
        <body>
            <div class="title">Horaizan</div>
            <div class="subtitle">By Xarays & Wonordel</div>
        </body>
        </html>
        """

    def open_link(self, url):
        """ Открывает ссылку в браузере. """
        self.parent.add_new_tab(url)

class BrowserWindow(QMainWindow):
    def __init__(self, url=None):
        super().__init__()
        self.setWindowTitle("Horaizan")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon("icon.jpg"))  # Замените на путь к вашей иконке

        # Инициализация Pygame
        pygame.init()
        pygame.mixer.init()  # Инициализация микшера
        self.click_sound = pygame.mixer.Sound("click.mp3")  # Замените на путь к вашему звуковому файлу
        self.tab_open_sound = pygame.mixer.Sound("tab_open.mp3")  # Замените на путь к вашему звуковому файлу

        # Виджет для вкладок
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # История браузера
        self.history = []

        # Закладки
        self.bookmarks = []

        # Поисковая система по умолчанию
        self.search_engine = "Google"
        self.search_url = "https://www.google.com/search?q="

        # Тема по умолчанию
        self.theme = "Светлая"
        self.font = QFont("Arial", 12)
        self.zoom_level = 100

        # Добавляем первую вкладку (домашняя страница)
        self.add_new_tab(url if url else None)

        # Создаем меню "Файл" с возможностью показать историю
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Меню")

        # Добавляем действие "История"
        history_action = QAction(QIcon("history.png"), "История", self)  # Замените на путь к иконке
        history_action.triggered.connect(self.show_history)
        file_menu.addAction(history_action)

        # Добавляем действие "Закладки"
        bookmarks_action = QAction(QIcon("bookmarks.png"), "Закладки", self)  # Замените на путь к иконке
        bookmarks_action.triggered.connect(self.show_bookmarks)
        file_menu.addAction(bookmarks_action)

        # Добавляем действие "Настройки поисковой системы"
        search_engine_action = QAction(QIcon("search.png"), "Настройки поисковой системы", self)  # Замените на путь к иконке
        search_engine_action.triggered.connect(self.change_search_engine)
        file_menu.addAction(search_engine_action)

        # Добавляем действие "Настройки внешнего вида"
        appearance_action = QAction(QIcon("appearance.png"), "Настройки внешнего вида", self)  # Замените на путь к иконке
        appearance_action.triggered.connect(self.change_appearance)
        file_menu.addAction(appearance_action)

        # Кнопка для добавления новой вкладки рядом с вкладками
        new_tab_button = QPushButton("+")
        new_tab_button.setFixedSize(QSize(50, 30))  # Фиксированный размер кнопки
        new_tab_button.clicked.connect(self.add_new_tab)
        self.tabs.setCornerWidget(new_tab_button)

        self.tabs.tabBar().setMovable(True)  # Даем возможность перетаскивать вкладки

    def add_new_tab(self, url=None):
        """ Добавляет новую вкладку с браузером или домашней страницой. """
        if url is None or not isinstance(url, str):
            # Создаем домашнюю страницу
            home_page = HomePage(self)
            container = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(home_page)
            container.setLayout(layout)
            self.tabs.addTab(container, "Домашняя страница")
        else:
            # Проверяем, что url является строкой
            if isinstance(url, str):
                # Создаем браузер
                browser = QWebEngineView()
                browser.setUrl(QUrl(url))

                # Обёртка для браузера с закруглёнными краями
                frame = QFrame()
                frame.setStyleSheet(
                    "border-radius: 15px; border: 1px solid #ccc; overflow: hidden;")  # Закругление и рамка
                browser.setStyleSheet("border: none;")  # Убираем рамку у браузера

                # Панель инструментов с адресной строкой
                toolbar = QToolBar()

                # Кнопки навигации
                back_button = QPushButton(QIcon("back.png"), "")  # Замените на путь к иконке Назад
                back_button.clicked.connect(lambda: (self.play_click_sound(), browser.back()))
                toolbar.addWidget(back_button)

                forward_button = QPushButton(QIcon("right.png"), "")  # Замените на путь к иконке Вперед
                forward_button.clicked.connect(lambda: (self.play_click_sound(), browser.forward()))
                toolbar.addWidget(forward_button)

                reload_button = QPushButton(QIcon("reload.png"), "")  # Замените на путь к иконке Перезагрузка
                reload_button.clicked.connect(lambda: (self.play_click_sound(), browser.reload()))
                toolbar.addWidget(reload_button)

                home_button = QPushButton(QIcon("home.png"), "")  # Замените на путь к иконке Домашняя страница
                home_button.clicked.connect(
                    lambda: (self.play_click_sound(), self.add_new_tab()))  # Открываем домашнюю страницу
                toolbar.addWidget(home_button)

                bookmark_button = QPushButton(QIcon("bookmark.png"), "")  # Замените на путь к иконке Закладки
                bookmark_button.clicked.connect(lambda: (self.play_click_sound(), self.add_bookmark(browser)))
                toolbar.addWidget(bookmark_button)

                # Адресная строка для URL
                url_bar = QLineEdit()
                url_bar.returnPressed.connect(lambda: (self.play_click_sound(), self.navigate_to_url(url_bar, browser)))
                toolbar.addWidget(url_bar)

                # Обновление адресной строки при изменении URL
                browser.urlChanged.connect(lambda q: self.update_url_bar(url_bar, q))

                # Сохранение истории
                browser.urlChanged.connect(lambda q: self.save_history(q, browser))

                # Обновление заголовка и иконки вкладки при изменении названия сайта
                browser.titleChanged.connect(lambda title: self.update_tab_title_and_icon(browser, title))

                # Создаем контейнер для браузера и панели инструментов
                container = QWidget()
                layout = QVBoxLayout()
                layout.addWidget(toolbar)
                layout.addWidget(frame)  # Добавляем QFrame
                frame_layout = QVBoxLayout(frame)
                frame_layout.addWidget(browser)  # Добавляем браузер в QFrame
                container.setLayout(layout)

                # Добавляем вкладку
                self.tabs.addTab(container, "Вкладка")  # Название по умолчанию
                self.tabs.setCurrentIndex(self.tabs.count() - 1)  # Переключаемся на новую вкладку

                # Воспроизводим звук открытия вкладки
                self.play_tab_open_sound()

    def play_click_sound(self):
        """ Воспроизводит звук клика. """
        self.click_sound.play()

    def play_tab_open_sound(self):
        """ Воспроизводит звук открытия вкладки. """
        self.tab_open_sound.play()

    def update_tab_title_and_icon(self, browser, title):
        """ Обновление заголовка вкладки и иконки. """
        index = self.tabs.indexOf(browser.parent())
        if index != -1:
            self.tabs.setTabText(index, title)  # Устанавливаем название вкладки
            icon = browser.icon()
            self.tabs.setTabIcon(index, icon)  # Устанавливаем иконку вкладки

    def save_history(self, q, browser):
        """ Сохраняет URL и название сайта в истории. """
        url = q.toString()
        title = browser.title()
        if url not in [entry[0] for entry in self.history]:
            icon = browser.icon()
            self.history.append((url, title, icon))

    def show_history(self):
        """ Показывает историю браузера. """
        history_str = ""
        for url, title, icon in self.history:
            history_str += f"<a href='{url}'>{title}</a><br>"

        history_window = QMessageBox(self)
        history_window.setWindowTitle("История браузера")
        history_window.setTextFormat(0)  # Устанавливаем текстовый формат как HTML
        history_window.setInformativeText(history_str if history_str else "История пуста.")
        history_window.exec_()

    def add_bookmark(self, browser):
        """ Добавляет текущую страницу в закладки. """
        url = browser.url().toString()
        title = browser.title()
        if (url, title) not in self.bookmarks:
            self.bookmarks.append((url, title))
            QMessageBox.information(self, "Закладка добавлена", f"{title} добавлена в закладки.")
            # Воспроизводим звук клика
            self.play_click_sound()
        else:
            QMessageBox.warning(self, "Закладка уже существует", f"{title} уже есть в закладках.")

    def show_bookmarks(self):
        """ Показывает список закладки. """
        bookmarks_str = ""
        for url, title in self.bookmarks:
            bookmarks_str += f"<a href='{url}'>{title}</a><br>"

        bookmarks_window = QMessageBox(self)
        bookmarks_window.setWindowTitle("Закладки")
        bookmarks_window.setTextFormat(0)  # Устанавливаем текстовый формат как HTML
        bookmarks_window.setInformativeText(bookmarks_str if bookmarks_str else "Закладки пусты.")
        bookmarks_window.exec_()

    def close_tab(self, index):
        """ Закрывает вкладку по индексу. """
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self, url_bar, browser):
        """ Переход по URL. """
        url = url_bar.text()
        if url.startswith("http://") or url.startswith("https://"):
            browser.setUrl(QUrl(url))
        else:
            search_url = f"{self.search_url}{url}"
            browser.setUrl(QUrl(search_url))

    def update_url_bar(self, url_bar, q):
        """ Обновление адресной строки при изменении URL. """
        url_bar.setText(q.toString())

    def change_search_engine(self):
        """ Открывает диалог для изменения поисковой системы. """
        settings_dialog = SearchEngineSettings(self)
        if settings_dialog.exec_() == QDialog.Accepted:
            self.search_engine = settings_dialog.get_selected_engine()
            self.search_url = settings_dialog.search_engines[self.search_engine]  # Обновляем search_url

    def change_appearance(self):
        """ Открывает диалог для изменения внешнего вида. """
        settings_dialog = AppearanceSettings(self)
        if settings_dialog.exec_() == QDialog.Accepted:
            self.theme = settings_dialog.get_selected_theme()
            self.font = settings_dialog.get_selected_font()
            self.zoom_level = settings_dialog.get_zoom_level()
            self.apply_appearance_settings()

    def apply_appearance_settings(self):
        """ Применяет настройки внешнего вида. """
        if self.theme == "Тёмная":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QTabWidget::pane {
                    border: 1px solid #444;
                    background-color: #2d2d2d;
                }
                QTabBar::tab {
                    background-color: #444;
                    color: #ffffff;
                    padding: 10px;
                }
                QTabBar::tab:selected {
                    background-color: #555;
                }
                QToolBar {
                    background-color: #333;
                    border: none;
                }
                QLineEdit {
                    background-color: #444;
                    color: #ffffff;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #555;
                    color: #ffffff;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QFrame {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                }
            """)
        else:
            self.setStyleSheet("")

        self.setFont(self.font)
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if isinstance(widget, QWebEngineView):
                widget.setZoomFactor(self.zoom_level / 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Получаем URL из аргументов командной строки
    url = sys.argv[1] if len(sys.argv) > 1 else None
    window = BrowserWindow(url)
    window.show()
    sys.exit(app.exec_())