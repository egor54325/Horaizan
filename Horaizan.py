from PyQt5.QtWidgets import QMainWindow, QLineEdit, QToolBar, QVBoxLayout, QWidget, QTabWidget, QPushButton, \
    QMessageBox, QAction, QComboBox, QDialog, QLabel, QHBoxLayout, QDialogButtonBox, QApplication, QSlider, QFontDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QSize, Qt, QLocale
from PyQt5.QtGui import QIcon, QFont
import pygame
import json

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
            "Mail.ru": "https://go.mail.ru/search?q=",
            "YouTube": "https://www.youtube.com/results?search_query=",
            "Wikipedia": "https://wikipedia.org/w/index.php?go=Go&search="
        }

        # Выпадающий список для выбора поисковой системы
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(self.search_engines.keys())

        # Кнопки для подтверждения или отмены
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

    def get_search_url(self, query):
        """ Возвращает URL для поискового запроса. """
        return self.search_engines[self.engine_combo.currentText()] + query


class AppearanceSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки внешнего вида")
        self.setGeometry(200, 200, 300, 150)

        # Инициализация переменной для шрифта
        self.selected_font = QFont()  # Инициализируем переменную

        # Выбор шрифта
        self.font_button = QPushButton("Выбрать шрифт")
        self.font_button.clicked.connect(self.choose_font)

        # Масштабирование
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(50)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)

        # Кнопки для подтверждения или отмены
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Основной макет
        layout = QVBoxLayout()
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

    def get_selected_font(self):
        """ Возвращает выбранный шрифт. """
        return self.selected_font

    def get_zoom_level(self):
        """ Возвращает уровень масштабирования. """
        return self.zoom_slider.value()


class LanguageSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки языка")
        self.setGeometry(200, 200, 300, 150)

        # Список доступных языков
        self.languages = {
            "English": QLocale(QLocale.English),
            "Русский": QLocale(QLocale.Russian),
            "Español": QLocale(QLocale.Spanish),
            "Français": QLocale(QLocale.French),
            "Deutsch": QLocale(QLocale.German),
            "中文": QLocale(QLocale.Chinese),
            "日本語": QLocale(QLocale.Japanese)
        }

        # Выпадающий список для выбора языка
        self.language_combo = QComboBox()
        self.language_combo.addItems(self.languages.keys())

        # Кнопки для подтверждения или отмены
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите язык:"))
        layout.addWidget(self.language_combo)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_selected_language(self):
        """ Возвращает выбранный язык. """
        return self.language_combo.currentText()

    def get_locale(self):
        """ Возвращает локаль для выбранного языка. """
        return self.languages[self.language_combo.currentText()]


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

        # Поле для ввода URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL или запрос...")
        layout.addWidget(self.url_input)

        # Поле для ввода поискового запроса
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Введите запрос для поиска...")
        layout.addWidget(self.query_input)

        # Кнопка для перехода на поисковую страницу
        search_button = QPushButton("Перейти к поиску")
        search_button.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 20px;
            border: none;
            background-color: #007BFF;
            color: #fff;
            transition: background-color 0.3s, transform 0.3s;
        """)
        search_button.clicked.connect(self.perform_search)
        search_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(search_button)

        # Кнопка для генерации пароля
        generate_password_button = QPushButton("Сгенерировать логин и пароль")
        generate_password_button.clicked.connect(self.generate_credentials)
        layout.addWidget(generate_password_button)

        self.setLayout(layout)

    def get_animation_html(self):
        """ Возвращает HTML-код с анимацией текста и градиентным фоном с летающими объектами. """
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
                    background: linear-gradient(135deg, #1e3c72, #2a5298);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Arial', sans-serif;
                }

                .title {
                    font-size: 80px;
                    font-weight: bold;
                    color: #fff;
                    text-align: center;
                    animation: float 3s infinite ease-in-out, glow 2s infinite alternate;
                    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2), 0 0 20px rgba(255, 255, 255, 0.1);
                }

                .subtitle {
                    font-size: 24px;
                    font-weight: normal;
                    color: #ccc;
                    text-align: center;
                    animation: fadeIn 2s ease-in-out infinite alternate;
                    cursor: pointer;  /* Добавляем указатель для курсора */
                }

                .object {
                    position: absolute;
                    width: 20px;
                    height: 20px;
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 50%;
                    animation: floatObject 10s infinite ease-in-out;
                }

                @keyframes float {
                    0% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                    100% { transform: translateY(0); }
                }

                @keyframes glow {
                    0% { text-shadow: 0 0 10px rgba(255, 255, 255, 0.2), 0 0 20px rgba(255, 255, 255, 0.1); }
                    100% { text-shadow: 0 0 20px rgba(255, 255, 255, 0.3), 0 0 40px rgba(255, 255, 255, 0.2); }
                }

                @keyframes fadeIn {
                    0% { opacity: 0.5; }
                    100% { opacity: 1; }
                }

                @keyframes floatObject {
                    0% { transform: translate(0, 0); }
                    50% { transform: translate(100px, 100px); }
                    100% { transform: translate(0, 0); }
                }
            </style>
        </head>
        <body>
            <div class="title">Horaizan</div>
            <div class="subtitle" onclick="showMeme()">By Xarays & Wonordel</div>
            <div class="object" style="top: 10%; left: 20%;"></div>
            <div class="object" style="top: 30%; left: 50%;"></div>
            <div class="object" style="top: 70%; left: 10%;"></div>
            <div class="object" style="top: 50%; left: 80%;"></div>
            <script>
                function showMeme() {
                    alert("Horaizan - лучший браузер!");
                }
            </script>
        </body>
        </html>
        """

    def perform_search(self):
        """ Выполняет поиск по введенному запросу или открывает URL. """
        query = self.query_input.text().strip()
        url = self.url_input.text().strip()

        if url:
            self.open_link(url)
        elif query:
            search_dialog = SearchEngineSettings(self)
            if search_dialog.exec_():
                search_url = search_dialog.get_search_url(query)
                self.open_link(search_url)

    def open_link(self, url):
        """ Открывает ссылку в новой вкладке. """
        self.parent.tabs.addTab(BrowserTab(self.parent, url), "Новая вкладка")
        self.parent.tabs.setCurrentIndex(self.parent.tabs.count() - 1)
        self.parent.play_tab_open_sound()  # Воспроизводим звук открытия вкладки

    def generate_credentials(self):
        """ Генерирует случайный логин и пароль. """
        username = self.generate_username()
        password = self.generate_password()

        # Создаем диалоговое окно с кнопками для копирования
        dialog = QDialog(self)
        dialog.setWindowTitle("Сгенерированные данные")
        dialog.setMinimumSize(300, 150)  # Устанавливаем минимальный размер окна

        layout = QVBoxLayout()

        # Логин
        username_layout = QHBoxLayout()
        username_label = QLabel(f"Логин: {username}")
        username_layout.addWidget(username_label)
        copy_username_button = QPushButton("Скопировать")
        copy_username_button.clicked.connect(lambda: self.copy_to_clipboard(username))
        username_layout.addWidget(copy_username_button)
        layout.addLayout(username_layout)

        # Пароль
        password_layout = QHBoxLayout()
        password_label = QLabel(f"Пароль: {password}")
        password_layout.addWidget(password_label)
        copy_password_button = QPushButton("Скопировать")
        copy_password_button.clicked.connect(lambda: self.copy_to_clipboard(password))
        password_layout.addWidget(copy_password_button)
        layout.addLayout(password_layout)

        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def copy_to_clipboard(self, text):
        """ Копирует текст в буфер обмена. """
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def generate_username(self):
        """ Генерирует случайный логин. """
        import random
        import string

        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def generate_password(self):
        """ Генерирует случайный пароль. """
        import random
        import string

        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))


class BrowserTab(QWidget):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui(url)

    def init_ui(self, url):
        """ Инициализация интерфейса вкладки браузера. """
        layout = QVBoxLayout()

        # Панель инструментов с адресной строки и кнопками
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))

        # Кнопка "Назад"
        self.back_button = QAction(QIcon("images/back.png"), "Назад", self)
        self.back_button.triggered.connect(self.navigate_back)
        self.toolbar.addAction(self.back_button)

        # Кнопка "Вперед"
        self.forward_button = QAction(QIcon("images/right.png"), "Вперед", self)
        self.forward_button.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(self.forward_button)

        # Кнопка "Обновить"
        self.reload_button = QAction(QIcon("images/reload.png"), "Обновить", self)
        self.reload_button.triggered.connect(self.reload_page)
        self.toolbar.addAction(self.reload_button)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Кнопка "Домой"
        self.home_button = QAction(QIcon("images/home.png"), "Домой", self)
        self.home_button.triggered.connect(self.navigate_home)
        self.toolbar.addAction(self.home_button)

        layout.addWidget(self.toolbar)

        # Веб-просмотрщик
        self.browser = QWebEngineView()
        if url:
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl("https://www.google.com"))  # Открываем Google по умолчанию
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.urlChanged.connect(self.add_to_history)  # Добавляем URL в историю
        self.browser.iconChanged.connect(self.update_tab_icon)  # Обновляем иконку вкладки
        self.browser.titleChanged.connect(self.update_tab_title)  # Обновляем заголовок вкладки

        # Включаем поддержку полноэкранного режима
        self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.browser.page().fullScreenRequested.connect(self.handle_fullscreen_request)

        layout.addWidget(self.browser)

        self.setLayout(layout)

    def handle_fullscreen_request(self, request):
        """ Обрабатывает запрос на полноэкранный режим. """
        if request.toggleOn():
            self.parent.showFullScreen()
            request.accept()
        else:
            self.parent.showNormal()
            request.accept()

    def navigate_back(self):
        """ Переход на предыдущую страницу. """
        self.browser.back()
        self.parent.play_click_sound()  # Воспроизводим звук клика

    def navigate_forward(self):
        """ Переход на следующую страницу. """
        self.browser.forward()
        self.parent.play_click_sound()  # Воспроизводим звук клика

    def reload_page(self):
        """ Обновление текущей страницы. """
        self.browser.reload()
        self.parent.play_click_sound()  # Воспроизводим звук клика

    def navigate_to_url(self):
        """ Переход по введенному URL. """
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))
        self.parent.play_click_sound()  # Воспроизводим звук клика

    def navigate_home(self):
        """ Переход на домашнюю страницу. """
        self.browser.setUrl(QUrl("https://www.google.com"))  # Переход на домашнюю страницу
        self.parent.play_click_sound()  # Воспроизводим звук клика

    def update_urlbar(self, q):
        """ Обновление адресной строки при изменении URL. """
        self.url_bar.setText(q.toString())

    def add_to_history(self, q):
        """ Добавляет URL в историю посещений. """
        url = q.toString()
        if url not in self.parent.history:
            self.parent.history.append(url)
            self.parent.save_history()  # Сохраняем историю в файл

    def update_tab_icon(self, icon):
        """ Обновляет иконку вкладки. """
        index = self.parent.tabs.indexOf(self)
        self.parent.tabs.setTabIcon(index, icon)

    def update_tab_title(self, title):
        """ Обновляет заголовок вкладки. """
        index = self.parent.tabs.indexOf(self)
        if len(title) > 20:  # Сокращаем длинные названия
            title = title[:20] + "..."
        self.parent.tabs.setTabText(index, title)


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horaizan Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Установка иконки браузера
        self.setWindowIcon(QIcon("images/icon.jpg"))  # Убедитесь, что файл browser_icon.png находится в той же директории

        # Инициализация звуков
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("sounds/click.mp3")
        self.tab_open_sound = pygame.mixer.Sound("sounds/tab_open.mp3")
        self.tab_close_sound = pygame.mixer.Sound("sounds/tab_close.mp3")

        # Инициализация истории посещений
        self.history = []
        self.load_history()  # Загружаем историю из файла

        # Основной макет
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 10px;
                border-radius: 10px;
                background-color: #333;
                margin: 2px;
                transition: background-color 0.3s;
                color: #fff;
            }
            QTabBar::tab:selected {
                background-color: #007BFF;
                color: #fff;
            }
            QTabBar::tab:hover {
                background-color: #0056b3;
                color: #fff;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #222;
            }
        """)
        self.setCentralWidget(self.tabs)

        # Добавление домашней страницы
        self.home_page = HomePage(self)
        self.tabs.addTab(self.home_page, "Домой")

        # Панель меню
        self.init_menu()

        # Переменная для хранения текущей темы
        self.dark_theme = True
        self.apply_theme()

    def init_menu(self):
        """ Инициализация меню браузера. """
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #333;
                color: #fff;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #007BFF;
            }
            QMenu {
                background-color: #333;
                color: #fff;
                border: 1px solid #444;
            }
            QMenu::item:selected {
                background-color: #007BFF;
            }
        """)

        # Меню "Настройки"
        settings_menu = menubar.addMenu("Настройки")
        search_engine_action = QAction("Поисковая система", self)
        search_engine_action.triggered.connect(self.set_search_engine)
        settings_menu.addAction(search_engine_action)

        appearance_action = QAction("Внешний вид", self)
        appearance_action.triggered.connect(self.set_appearance)
        settings_menu.addAction(appearance_action)

        # Меню для смены языка
        language_action = QAction("Язык", self)
        language_action.triggered.connect(self.set_language)
        settings_menu.addAction(language_action)

        # Меню для смены темы
        theme_action = QAction("Сменить тему", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)

        # Меню для просмотра истории
        history_action = QAction("История", self)
        history_action.triggered.connect(self.show_history)
        menubar.addAction(history_action)

    def set_language(self):
        """ Открывает диалог настройки языка. """
        language_dialog = LanguageSettings(self)
        if language_dialog.exec_():
            selected_language = language_dialog.get_selected_language()
            locale = language_dialog.get_locale()
            QLocale.setDefault(locale)
            QMessageBox.information(self, "Успех", f"Выбран язык: {selected_language}")
            self.play_click_sound()  # Воспроизводим звук клика

    def toggle_theme(self):
        """ Переключает между светлой и тёмной темами. """
        self.dark_theme = not self.dark_theme
        self.apply_theme()

    def apply_theme(self):
        """ Применяет текущую тему (светлую или тёмную). """
        if self.dark_theme:
            self.setStyleSheet("""
                QWidget {
                    background-color: #222;
                    color: #fff;
                }
                QLineEdit {
                    background-color: #333;
                    color: #fff;
                    border: 1px solid #444;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QToolBar {
                    background-color: #333;
                    border: none;
                }
                QToolButton {
                    background-color: transparent;
                    color: #fff;
                }
                QToolButton:hover {
                    background-color: #007BFF;
                }
                QMessageBox {
                    background-color: #222;
                    color: #fff;
                }
                QMessageBox QLabel {
                    color: #fff;
                }
                QMessageBox QPushButton {
                    background-color: #007BFF;
                    color: #fff;
                }
                QMessageBox QPushButton:hover {
                    background-color: #0056b3;
                }
                QDialog {
                    background-color: #222;
                    color: #fff;
                }
                QDialog QLabel {
                    color: #fff;
                }
                QDialog QPushButton {
                    background-color: #007BFF;
                    color: #fff;
                }
                QDialog QPushButton:hover {
                    background-color: #0056b3;
                }
                QComboBox {
                    background-color: #333;
                    color: #fff;
                    border: 1px solid #444;
                    padding: 5px;
                }
                QComboBox QAbstractItemView {
                    background-color: #333;
                    color: #fff;
                }
                QSlider::groove:horizontal {
                    background-color: #444;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #007BFF;
                    width: 20px;
                    height: 20px;
                    margin: -6px 0;
                    border-radius: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #fff;
                    color: #000;
                }
                QLineEdit {
                    background-color: #f0f0f0;
                    color: #000;
                    border: 1px solid #ccc;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QToolBar {
                    background-color: #f0f0f0;
                    border: none;
                }
                QToolButton {
                    background-color: transparent;
                    color: #000;
                }
                QToolButton:hover {
                    background-color: #007BFF;
                }
                QMessageBox {
                    background-color: #fff;
                    color: #000;
                }
                QMessageBox QLabel {
                    color: #000;
                }
                QMessageBox QPushButton {
                    background-color: #007BFF;
                    color: #fff;
                }
                QMessageBox QPushButton:hover {
                    background-color: #0056b3;
                }
                QDialog {
                    background-color: #fff;
                    color: #000;
                }
                QDialog QLabel {
                    color: #000;
                }
                QDialog QPushButton {
                    background-color: #007BFF;
                    color: #fff;
                }
                QDialog QPushButton:hover {
                    background-color: #0056b3;
                }
                QComboBox {
                    background-color: #f0f0f0;
                    color: #000;
                    border: 1px solid #ccc;
                    padding: 5px;
                }
                QComboBox QAbstractItemView {
                    background-color: #f0f0f0;
                    color: #000;
                }
                QSlider::groove:horizontal {
                    background-color: #ccc;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #007BFF;
                    width: 20px;
                    height: 20px;
                    margin: -6px 0;
                    border-radius: 10px;
                }
            """)

    def add_new_tab(self):
        """ Добавляет новую вкладку. """
        new_tab = BrowserTab(self)
        self.tabs.addTab(new_tab, "Новая вкладка")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.play_tab_open_sound()  # Воспроизводим звук открытия вкладки

    def close_tab(self, index):
        """ Закрывает вкладку. """
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            self.play_tab_close_sound()  # Воспроизводим звук закрытия вкладки
        else:
            QMessageBox.warning(self, "Ошибка", "Нельзя закрыть последнюю вкладку.")

    def set_search_engine(self):
        """ Открывает диалог настройки поисковой системы. """
        search_engine_dialog = SearchEngineSettings(self)
        if search_engine_dialog.exec_():
            selected_engine = search_engine_dialog.get_selected_engine()
            QMessageBox.information(self, "Успех", f"Выбрана поисковая система: {selected_engine}")
            self.play_click_sound()  # Воспроизводим звук клика

    def set_appearance(self):
        """ Открывает диалог настройки внешнего вида. """
        appearance_dialog = AppearanceSettings(self)
        if appearance_dialog.exec_():
            selected_font = appearance_dialog.get_selected_font()
            zoom_level = appearance_dialog.get_zoom_level()
            self.setFont(selected_font)
            self.tabs.setStyleSheet(f"font-size: {zoom_level}%;")
            self.play_click_sound()  # Воспроизводим звук клика

    def play_click_sound(self):
        """ Воспроизводит звук клика. """
        self.click_sound.play()

    def play_tab_open_sound(self):
        self.tab_open_sound.play()

    def play_tab_close_sound(self):
        """ Воспроизводит звук закрытия вкладки. """
        self.tab_close_sound.play()

    def load_history(self):
        """ Загружает историю посещений из файла. """
        try:
            with open("history.json", "r") as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = []
            with open("history.json", 'w') as f:
                f.write("[]")

    def save_history(self):
        """ Сохраняет историю посещений в файл. """
        with open("history.json", "w") as file:
            json.dump(self.history, file)

    def show_history(self):
        """ Показывает историю посещений. """
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("История посещений")
        history_dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # Список истории
        history_list = QComboBox()
        history_list.addItems(self.history)
        layout.addWidget(history_list)

        # Кнопка для перехода к выбранному URL
        go_button = QPushButton("Перейти")
        go_button.clicked.connect(lambda: self.navigate_to_history_url(history_list.currentText()))
        layout.addWidget(go_button)

        # Кнопка для очистки истории
        clear_button = QPushButton("Очистить историю")
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)

        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(history_dialog.close)
        layout.addWidget(close_button)

        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def navigate_to_history_url(self, url):
        """ Переходит к выбранному URL из истории. """
        self.tabs.addTab(BrowserTab(self, url), "Новая вкладка")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.play_tab_open_sound()  # Воспроизводим звук открытия вкладки

    def clear_history(self):
        """ Очищает историю посещений. """
        self.history = []
        self.save_history()
        QMessageBox.information(self, "Успех", "История очищена.")


def main():
    import sys
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()