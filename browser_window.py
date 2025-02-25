from PyQt5.QtWidgets import QMainWindow, QLineEdit, QToolBar, QVBoxLayout, QWidget, QTabWidget, QPushButton, \
    QMessageBox, QAction, QComboBox, QDialog, QLabel, QHBoxLayout, QDialogButtonBox, QApplication, QFrame, QSlider, QFontDialog, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QFont
import sys
import pygame
import requests
import json
import random
import string


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
            "YouTube": "https://www.youtube.com/results?search_query="
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

        # Кнопка для выхода из приложения
        exit_button = QPushButton("Выход")
        exit_button.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 20px;
            border: none;
            background-color: #FF4D4D;
            color: #fff;
            transition: background-color 0.3s, transform 0.3s;
        """)
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(exit_button)

        # Кнопка для генерации пароля
        generate_password_button = QPushButton("Сгенерировать логин и пароль")
        generate_password_button.clicked.connect(self.generate_credentials)
        layout.addWidget(generate_password_button)

        # Кнопка для загрузки медиафайла
        load_media_button = QPushButton("Загрузить медиафайл")
        load_media_button.clicked.connect(self.load_media)
        layout.addWidget(load_media_button)

        # Кнопка для перевода текста
        translate_button = QPushButton("Перевести текст")
        translate_button.clicked.connect(self.translate_text)
        layout.addWidget(translate_button)

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
        QMessageBox.information(self, "Сгенерированные данные", f"Логин: {username}\nПароль: {password}")
        self.parent.play_click_sound()  # Воспроизводим звук клика

    def generate_username(self):
        """ Генерирует случайный логин. """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def generate_password(self):
        """ Генерирует случайный пароль. """
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(characters, k=12))

    def load_media(self):
        """ Загружает медиафайл. """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите медиафайл", "", "Media Files (*.mp3 *.mp4 *.wav);;All Files (*)", options=options)
        if file_name:
            self.play_media(file_name)
            self.parent.play_click_sound()  # Воспроизводим звук клика

    def play_media(self, file_path):
        """ Воспроизводит медиафайл. """
        player = QMediaPlayer()
        media_content = QMediaContent(QUrl.fromLocalFile(file_path))
        player.setMedia(media_content)
        player.setVolume(100)
        player.play()

    def translate_text(self):
        """ Переводит текст с использованием Google Translate API. """
        text, ok = QInputDialog.getText(self, "Перевод текста", "Введите текст для перевода:")
        if ok and text:
            translated_text = self.google_translate(text)
            QMessageBox.information(self, "Переведенный текст", translated_text)
            self.parent.play_click_sound()  # Воспроизводим звук клика

    def google_translate(self, text):
        """ Использует Google Translate API для перевода текста. """
        api_key = ""  # Замените на свой ключ API
        url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
        data = {
            'q': text,
            'target': 'en'  # Замените на нужный язык
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()['data']['translations'][0]['translatedText']
        else:
            return "Ошибка перевода"


class BrowserTab(QWidget):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui(url)

    def init_ui(self, url):
        """ Инициализация интерфейса вкладки браузера. """
        layout = QVBoxLayout()

        # Панель инструментов с адресной строкой и кнопками
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))

        # Кнопка "Назад"
        self.back_button = QAction(QIcon("back.png"), "Назад", self)
        self.back_button.triggered.connect(self.navigate_back)
        self.toolbar.addAction(self.back_button)

        # Кнопка "Вперед"
        self.forward_button = QAction(QIcon("right.png"), "Вперед", self)
        self.forward_button.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(self.forward_button)

        # Кнопка "Обновить"
        self.reload_button = QAction(QIcon("reload.png"), "Обновить", self)
        self.reload_button.triggered.connect(self.reload_page)
        self.toolbar.addAction(self.reload_button)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Кнопка "Домой"
        self.home_button = QAction(QIcon("home.png"), "Домой", self)
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
        layout.addWidget(self.browser)

        self.setLayout(layout)

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


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horaizan Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Инициализация звуков
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("click.mp3")
        self.tab_open_sound = pygame.mixer.Sound("tab_open.mp3")
        self.tab_close_sound = pygame.mixer.Sound("tab_close.mp3")

        # Основной макет
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 10px;
                border-radius: 10px;
                background-color: #f0f0f0;
                margin: 2px;
                transition: background-color 0.3s;
            }
            QTabBar::tab:selected {
                background-color: #007BFF;
                color: #fff;
            }
            QTabBar::tab:hover {
                background-color: #0056b3;
                color: #fff;
            }
        """)
        self.setCentralWidget(self.tabs)

        # Добавление домашней страницы
        self.home_page = HomePage(self)
        self.tabs.addTab(self.home_page, "Домой")

        # Панель меню
        self.init_menu()

    def init_menu(self):
        """ Инициализация меню браузера. """
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        new_tab_action = QAction("Новая вкладка", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню "Настройки"
        settings_menu = menubar.addMenu("Настройки")
        search_engine_action = QAction("Поисковая система", self)
        search_engine_action.triggered.connect(self.set_search_engine)
        settings_menu.addAction(search_engine_action)

        appearance_action = QAction("Внешний вид", self)
        appearance_action.triggered.connect(self.set_appearance)
        settings_menu.addAction(appearance_action)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
