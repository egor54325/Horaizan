from PyQt5.QtWidgets import QMainWindow, QLineEdit, QToolBar, QVBoxLayout, QWidget, QTabWidget, QPushButton, \
    QMessageBox, QAction, QComboBox, QDialog, QLabel, QHBoxLayout, QDialogButtonBox, QApplication, QTabBar, \
    QListWidget, QListWidgetItem, QPlainTextEdit, QTextEdit, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEngineDownloadItem
from PyQt5.QtCore import QUrl, QSize, Qt, QBuffer, QByteArray
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QSound  # Добавлено для использования QSound
import os
import json

class SearchEngineSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Сохраняем ссылку на родителя для доступа к переводу
        self.setWindowTitle(self.parent.tr("Search Engine Settings"))
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
        layout.addWidget(QLabel(self.parent.tr("Select a search engine:")))
        layout.addWidget(self.engine_combo)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_selected_engine(self):
        """ Возвращает выбранную поисковую систему. """
        return self.engine_combo.currentText()

    def get_search_url(self, query):
        """ Возвращает URL для поискового запроса. """
        return self.search_engines[self.engine_combo.currentText()] + query


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
        self.url_input.setPlaceholderText(self.parent.tr("Enter URL or query..."))
        layout.addWidget(self.url_input)

        # Поле для ввода поискового запроса
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText(self.parent.tr("Enter search query..."))
        layout.addWidget(self.query_input)

        # Кнопка для перехода на поисковую страницу
        self.search_button = QPushButton(self.parent.tr("Search"))
        self.search_button.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 20px;
            border: none;
            background-color: #007BFF;
            color: #fff;
            transition: background-color 0.3s, transform 0.3s;
        """)
        self.search_button.clicked.connect(self.perform_search)
        self.search_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.search_button)

        # Кнопка для генерации пароля
        generate_password_button = QPushButton(self.parent.tr("Generate login and password"))
        generate_password_button.clicked.connect(self.generate_credentials)
        layout.addWidget(generate_password_button)

        self.setLayout(layout)

    def retranslate(self):
        """ Обновление текста интерфейса при смене языка. """
        self.url_input.setPlaceholderText(self.parent.tr("Enter URL or query..."))
        self.query_input.setPlaceholderText(self.parent.tr("Enter search query..."))
        self.search_button.setText(self.parent.tr("Search"))

    def get_animation_html(self):
        """ Возвращает HTML-код с тёмным градиентом на заднем фоне. """
        return """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Horaizan</title>
            <style>
                /* Стили для градиентного фона */
                body, html {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    overflow-x: hidden;
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
                }
                /* Остальные стили остаются без изменений */
                .title {
                    font-size: 80px;
                    font-weight: bold;
                    color: #fff;
                    text-align: center;
                    padding-top: 200px;
                    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                }
            </style>
        </head>
        <body>
            <div class="title">Horaizan Browser</div>
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
        self.parent.tabs.addTab(BrowserTab(self.parent, url), self.parent.tr("New Tab"))
        self.parent.tabs.setCurrentIndex(self.parent.tabs.count() - 1)
        self.parent.play_tab_open_sound()  # Воспроизводим звук открытия вкладки

    def generate_credentials(self):
        """ Генерирует случайный логин и пароль. """
        username = self.generate_username()
        password = self.generate_password()

        # Создаем диалоговое окно с кнопками для копирования
        dialog = QDialog(self)
        dialog.setWindowTitle(self.parent.tr("Generated data"))
        dialog.setMinimumSize(300, 150)  # Устанавливаем минимальный размер окна

        layout = QVBoxLayout()

        # Логин
        username_layout = QHBoxLayout()
        username_label = QLabel(self.parent.tr("Username: {username}").format(username=username))
        username_layout.addWidget(username_label)
        copy_username_button = QPushButton(self.parent.tr("Copy"))
        copy_username_button.clicked.connect(lambda: self.copy_to_clipboard(username))
        username_layout.addWidget(copy_username_button)
        layout.addLayout(username_layout)

        # Пароль
        password_layout = QHBoxLayout()
        password_label = QLabel(self.parent.tr("Password: {password}").format(password=password))
        password_layout.addWidget(password_label)
        copy_password_button = QPushButton(self.parent.tr("Copy"))
        copy_password_button.clicked.connect(lambda: self.copy_to_clipboard(password))
        password_layout.addWidget(copy_password_button)
        layout.addLayout(password_layout)

        # Кнопка закрытия
        close_button = QPushButton(self.parent.tr("Close"))
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
        self.back_button = QAction(QIcon("images/back.png"), self.parent.tr("Back"), self)
        self.back_button.triggered.connect(self.navigate_back)
        self.toolbar.addAction(self.back_button)

        # Кнопка "Вперед"
        self.forward_button = QAction(QIcon("images/right.png"), self.parent.tr("Forward"), self)
        self.forward_button.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(self.forward_button)

        # Кнопка "Обновить"
        self.reload_button = QAction(QIcon("images/reload.png"), self.parent.tr("Reload"), self)
        self.reload_button.triggered.connect(self.reload_page)
        self.toolbar.addAction(self.reload_button)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Кнопка "Домой"
        self.home_button = QAction(QIcon("images/home.png"), self.parent.tr("Home"), self)
        self.home_button.triggered.connect(self.navigate_home)
        self.toolbar.addAction(self.home_button)

        layout.addWidget(self.toolbar)

        # Веб-просмотрщик
        self.browser = QWebEngineView()

        # Обработка загрузки файлов
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

        if url:
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl("https://www.google.com"))  # Открываем Google по умолчанию
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.urlChanged.connect(self.add_to_history)  # Добавляем URL в историю
        self.browser.iconChanged.connect(self.update_tab_icon)  # Обновляем иконку вкладки
        self.browser.titleChanged.connect(self.update_tab_title)  # Обновляем заголовок вкладки
        self.browser.titleChanged.connect(self.update_history_title)
        self.browser.iconChanged.connect(self.update_history_icon)

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
        # Проверяем, что история содержит словари, а не строки
        if not any(isinstance(entry, dict) and entry.get('url') == url for entry in self.parent.history):
            entry = {'url': url, 'title': None, 'icon_data': None}
            self.parent.history.append(entry)
            self.parent.save_history()

    def update_history_title(self, title):
        """ Обновляет заголовок в истории посещений. """
        url = self.browser.url().toString()
        for entry in self.parent.history:
            if entry['url'] == url:
                entry['title'] = title
                self.parent.save_history()
                break

    def update_history_icon(self, icon):
        """ Обновляет иконку в истории посещений. """
        url = self.browser.url().toString()
        for entry in self.parent.history:
            if entry['url'] == url:
                # Сохраняем данные иконки в виде байтов
                pixmap = icon.pixmap(16, 16)
                if not pixmap.isNull():
                    buffer = QBuffer()
                    buffer.open(QBuffer.ReadWrite)
                    pixmap.save(buffer, "PNG")
                    icon_data = buffer.data().toBase64().data().decode()
                    entry['icon_data'] = icon_data
                    self.parent.save_history()
                    break

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

    def on_download_requested(self, download):
        """ Обрабатывает запрос на загрузку файла. """
        suggested_path = download.suggestedFileName()
        # Открываем диалог сохранения файла
        path, _ = QFileDialog.getSaveFileName(self, self.parent.tr("Save File"), suggested_path)
        if path:
            download.setPath(path)
            download.accept()
            download.finished.connect(lambda: self.parent.download_finished(download))

    def closeEvent(self, event):
        """ Обрабатывает закрытие вкладки - останавливает медиа контент. """
        # Останавливаем воспроизведение медиа
        self.browser.page().runJavaScript("var videos = document.querySelectorAll('video');"
                                          "videos.forEach(function(video) { video.pause(); });"
                                          "var audios = document.querySelectorAll('audio');"
                                          "audios.forEach(function(audio) { audio.pause(); });")
        event.accept()


class BrowserWindow(QMainWindow):
    translations = {
        'en': {
            'Settings': 'Settings',
            'Search Engine': 'Search Engine',
            'Change Theme': 'Change Theme',
            'History': 'History',
            'Language': 'Language',
            'Home Page': 'Home Page',
            'Cannot close home page.': 'Cannot close home page.',
            'Cannot close the last tab.': 'Cannot close the last tab.',
            'Error': 'Error',
            'New Tab': 'New Tab',
            'Success': 'Success',
            'Search engine selected: {engine}': 'Search engine selected: {engine}',
            'History cleared.': 'History cleared.',
            'Go': 'Go',
            'Clear History': 'Clear History',
            'Close': 'Close',
            'Generate login and password': 'Generate login and password',
            'Generated data': 'Generated data',
            'Username: {username}': 'Username: {username}',
            'Password: {password}': 'Password: {password}',
            'Copy': 'Copy',
            'Back': 'Back',
            'Forward': 'Forward',
            'Reload': 'Reload',
            'Home': 'Home',
            'Developer Console': 'Developer Console',
            'Enter JavaScript code here...': 'Enter JavaScript code here...',
            'Run JavaScript': 'Run JavaScript',
            'Output:': 'Output:',
            'Select a search engine:': 'Select a search engine:',
            'Enter URL or query...': 'Enter URL or query...',
            'Enter search query...': 'Enter search query...',
            'Search': 'Search',
            'Save File': 'Save File',
            'Download completed: {path}': 'Download completed: {path}',
            'Cannot download file.': 'Cannot download file.',
            'History is empty.': 'History is empty.',
        },
        'ru': {
            'Settings': 'Настройки',
            'Search Engine': 'Поисковая система',
            'Change Theme': 'Сменить тему',
            'History': 'История',
            'Language': 'Язык',
            'Home Page': 'Домашняя страница',
            'Cannot close home page.': 'Нельзя закрыть домашнюю страницу.',
            'Cannot close the last tab.': 'Нельзя закрыть последнюю вкладку.',
            'Error': 'Ошибка',
            'New Tab': 'Новая вкладка',
            'Success': 'Успех',
            'Search engine selected: {engine}': 'Выбрана поисковая система: {engine}',
            'History cleared.': 'История очищена.',
            'Go': 'Перейти',
            'Clear History': 'Очистить историю',
            'Close': 'Закрыть',
            'Generate login and password': 'Сгенерировать логин и пароль',
            'Generated data': 'Сгенерированные данные',
            'Username: {username}': 'Логин: {username}',
            'Password: {password}': 'Пароль: {password}',
            'Copy': 'Скопировать',
            'Back': 'Назад',
            'Forward': 'Вперед',
            'Reload': 'Перезагрузить',
            'Home': 'Домой',
            'Developer Console': 'Консоль разработчика',
            'Enter JavaScript code here...': 'Введите JavaScript код здесь...',
            'Run JavaScript': 'Выполнить JavaScript',
            'Output:': 'Вывод:',
            'Select a search engine:': 'Выберите поисковую систему:',
            'Enter URL or query...': 'Введите URL или запрос...',
            'Enter search query...': 'Введите запрос для поиска...',
            'Search': 'Поиск',
            'Save File': 'Сохранить файл',
            'Download completed: {path}': 'Загрузка завершена: {path}',
            'Cannot download file.': 'Не удалось загрузить файл.',
            'History is empty.': 'История пуста.',
        }
    }

    def __init__(self):
        super().__init__()
        self.language = 'ru'  # Устанавливаем язык по умолчанию - русский
        self.setWindowTitle("Horaizan Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Установка иконки браузера
        self.setWindowIcon(QIcon("images/icon.jpg"))  # Убедитесь, что файл icon.jpg находится в той же директории

        # Инициализация звуков
        # Используем QSound вместо pygame
        self.click_sound = QSound("sounds/click.mp3")
        self.tab_open_sound = QSound("sounds/tab_open.mp3")
        self.tab_close_sound = QSound("sounds/tab_close.mp3")

        # Инициализация истории посещений
        self.history = []
        self.load_history()  # Загружаем историю из файла

        # Основной макет
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Перетаскивание вкладок
        self.tabs.tabBar().setMovable(True)

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
        self.tabs.addTab(self.home_page, self.tr("Home Page"))

        # Убираем кнопку закрытия с домашней страницы
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # Панель меню
        self.init_menu()

        # Переменная для хранения текущей темы
        self.dark_theme = True
        self.apply_theme()

        # Кнопка добавления новой вкладки
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(30, 30)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.tabs.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)

    def tr(self, text):
        """ Переводит текст на выбранный язык. """
        return self.translations[self.language].get(text, text)

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
        self.settings_menu = menubar.addMenu(self.tr("Settings"))
        self.search_engine_action = QAction(self.tr("Search Engine"), self)
        self.search_engine_action.triggered.connect(self.set_search_engine)
        self.settings_menu.addAction(self.search_engine_action)

        # Меню для смены темы
        self.theme_action = QAction(self.tr("Change Theme"), self)
        self.theme_action.triggered.connect(self.toggle_theme)
        self.settings_menu.addAction(self.theme_action)

        # Меню для просмотра истории
        self.history_action = QAction(self.tr("History"), self)
        self.history_action.triggered.connect(self.show_history)
        self.settings_menu.addAction(self.history_action)

        # Консоль разработчика
        self.console_action = QAction(self.tr("Developer Console"), self)
        self.console_action.triggered.connect(self.open_developer_console)
        self.settings_menu.addAction(self.console_action)

        # Подменю "Язык"
        self.language_menu = self.settings_menu.addMenu(self.tr("Language"))
        self.english_action = QAction("English", self)
        self.english_action.triggered.connect(lambda: self.switch_language('en'))
        self.language_menu.addAction(self.english_action)

        self.russian_action = QAction("Русский", self)
        self.russian_action.triggered.connect(lambda: self.switch_language('ru'))
        self.language_menu.addAction(self.russian_action)

    def switch_language(self, lang):
        """ Переключает язык интерфейса. """
        self.language = lang
        self.retranslate_ui()

    def retranslate_ui(self):
        """ Обновляет текст интерфейса при смене языка. """
        self.settings_menu.setTitle(self.tr("Settings"))
        self.search_engine_action.setText(self.tr("Search Engine"))
        self.theme_action.setText(self.tr("Change Theme"))
        self.history_action.setText(self.tr("History"))
        self.language_menu.setTitle(self.tr("Language"))
        self.console_action.setText(self.tr("Developer Console"))
        # Обновляем заголовки вкладок
        for index in range(self.tabs.count()):
            widget = self.tabs.widget(index)
            if widget == self.home_page:
                self.tabs.setTabText(index, self.tr("Home Page"))
        # Обновляем домашнюю страницу
        self.home_page.retranslate()

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
        self.tabs.addTab(new_tab, self.tr("New Tab"))
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.play_tab_open_sound()  # Воспроизводим звук открытия вкладки

    def close_tab(self, index):
        """ Закрывает вкладку. """
        widget = self.tabs.widget(index)
        if widget == self.home_page:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Cannot close home page."))
        elif self.tabs.count() > 1:
            # Удаляем вкладку и останавливаем звуки
            widget.deleteLater()
            self.tabs.removeTab(index)
            self.play_tab_close_sound()  # Воспроизводим звук закрытия вкладки
        else:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Cannot close the last tab."))

    def set_search_engine(self):
        """ Открывает диалог настройки поисковой системы. """
        search_engine_dialog = SearchEngineSettings(self)
        if search_engine_dialog.exec_():
            selected_engine = search_engine_dialog.get_selected_engine()
            QMessageBox.information(self, self.tr("Success"), self.tr("Search engine selected: {engine}").format(engine=selected_engine))
            self.play_click_sound()  # Воспроизводим звук клика

    def play_click_sound(self):
        """ Воспроизводит звук клика. """
        self.click_sound.play()

    def play_tab_open_sound(self):
        """ Воспроизводит звук открытия вкладки. """
        self.tab_open_sound.play()

    def play_tab_close_sound(self):
        """ Воспроизводит звук закрытия вкладки. """
        self.tab_close_sound.play()

    def load_history(self):
        """ Загружает историю посещений из файла. """
        try:
            with open("history.json", "r") as file:
                self.history = json.load(file)
                # Убедимся, что история содержит только словари
                self.history = [entry if isinstance(entry, dict) else {'url': entry, 'title': None, 'icon_data': None} for entry in self.history]
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            with open("history.json", 'w') as f:
                f.write("[]")

    def save_history(self):
        """ Сохраняет историю посещений в файл. """
        with open("history.json", "w") as file:
            json.dump(self.history, file)

    def show_history(self):
        """ Показывает историю посещений. """
        if not self.history:
            QMessageBox.information(self, self.tr("History"), self.tr("History is empty."))
            return

        history_dialog = QDialog(self)
        history_dialog.setWindowTitle(self.tr("History"))
        history_dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # Список истории
        history_list = QListWidget()
        for entry in self.history:
            item = QListWidgetItem()
            title = entry.get('title') or entry['url']
            item.setText(title)
            # Если доступны данные иконки, то устанавливаем иконку
            icon_data = entry.get('icon_data')
            if icon_data:
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray.fromBase64(icon_data.encode()))
                icon = QIcon(pixmap)
                item.setIcon(icon)
            history_list.addItem(item)
        layout.addWidget(history_list)

        # Кнопка для перехода к выбранному URL
        go_button = QPushButton(self.tr("Go"))
        go_button.clicked.connect(lambda: self.navigate_to_history_url(self.history[history_list.currentRow()]['url']))
        layout.addWidget(go_button)

        # Кнопка для очистки истории
        clear_button = QPushButton(self.tr("Clear History"))
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)

        # Кнопка закрытия
        close_button = QPushButton(self.tr("Close"))
        close_button.clicked.connect(history_dialog.close)
        layout.addWidget(close_button)

        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def navigate_to_history_url(self, url):
        """ Переходит к выбранному URL из истории. """
        self.tabs.addTab(BrowserTab(self, url), self.tr("New Tab"))
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.play_tab_open_sound()  # Воспроизводим звук открытия вкладки

    def clear_history(self):
        """ Очищает историю посещений. """
        self.history = []
        self.save_history()
        QMessageBox.information(self, self.tr("Success"), self.tr("History cleared."))

    def open_developer_console(self):
        """ Открывает консоль разработчика. """
        console_dialog = QDialog(self)
        console_dialog.setWindowTitle(self.tr("Developer Console"))
        console_dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        # Текстовый редактор для JavaScript-кода
        code_editor = QPlainTextEdit()
        code_editor.setPlaceholderText(self.tr("Enter JavaScript code here..."))
        layout.addWidget(code_editor)

        # Кнопка для выполнения кода
        run_button = QPushButton(self.tr("Run JavaScript"))
        layout.addWidget(run_button)

        output_label = QLabel(self.tr("Output:"))
        layout.addWidget(output_label)

        output_text = QTextEdit()
        output_text.setReadOnly(True)
        layout.addWidget(output_text)

        run_button.clicked.connect(lambda: self.run_js_code(code_editor.toPlainText(), output_text))

        console_dialog.setLayout(layout)
        console_dialog.exec_()

    def run_js_code(self, code, output_widget):
        """ Выполняет JavaScript код в текущей вкладке. """
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, BrowserTab):
            def callback(result):
                output_widget.append(str(result))
            current_tab.browser.page().runJavaScript(code, callback)

    def download_finished(self, download):
        """ Обрабатывает завершение загрузки файла. """
        if download.state() == QWebEngineDownloadItem.DownloadCompleted:
            QMessageBox.information(self, self.tr("Success"), self.tr("Download completed: {path}").format(path=download.path()))
        else:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Cannot download file."))

def main():
    import sys
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()