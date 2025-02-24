from PyQt5.QtWidgets import QMainWindow, QLineEdit, QToolBar, QVBoxLayout, QWidget, QTabWidget, QPushButton, QMessageBox, QAction, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon
import sys

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horaizan")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon("icon.jpg"))  # Замените на путь к вашей иконке

        # Виджет для вкладок
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # История браузера
        self.history = []

        # Закладки
        self.bookmarks = []

        # Добавляем первую вкладку
        self.add_new_tab("https://www.google.com")

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

        # Кнопка для добавления новой вкладки рядом с вкладками
        new_tab_button = QPushButton("+")
        new_tab_button.setFixedSize(QSize(50, 30))  # Фиксированный размер кнопки
        new_tab_button.clicked.connect(lambda: self.add_new_tab())
        self.tabs.setCornerWidget(new_tab_button)

        self.tabs.tabBar().setMovable(True)  # Даем возможность перетаскивать вкладки

    def add_new_tab(self, url="https://www.google.com"):  # Установите значение по умолчанию для URL
        """ Добавляет новую вкладку с браузером. """
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))  # Здесь url должен быть строкой

        # Панель инструментов с адресной строкой
        toolbar = QToolBar()

        # Кнопки навигации
        back_button = QPushButton(QIcon("back.png"), "")  # Замените на путь к иконке Назад
        back_button.clicked.connect(browser.back)
        toolbar.addWidget(back_button)

        forward_button = QPushButton(QIcon("right.png"), "")  # Замените на путь к иконке Вперед
        forward_button.clicked.connect(browser.forward)
        toolbar.addWidget(forward_button)

        reload_button = QPushButton(QIcon("reload.png"), "")  # Замените на путь к иконке Перезагрузка
        reload_button.clicked.connect(browser.reload)
        toolbar.addWidget(reload_button)

        home_button = QPushButton(QIcon("home.png"), "")  # Замените на путь к иконке Домашняя страница
        home_button.clicked.connect(lambda: browser.setUrl(QUrl("https://www.google.com")))  # Замените на вашу домашнюю страницу
        toolbar.addWidget(home_button)

        bookmark_button = QPushButton(QIcon("bookmark.png"), "")  # Замените на путь к иконке Закладки
        bookmark_button.clicked.connect(lambda: self.add_bookmark(browser))
        toolbar.addWidget(bookmark_button)

        # Адресная строка для URL
        url_bar = QLineEdit()
        url_bar.returnPressed.connect(lambda: self.navigate_to_url(url_bar, browser))
        toolbar.addWidget(url_bar)

        # Поле для общего поиска
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Поиск...")
        search_bar.returnPressed.connect(lambda: self.perform_search(search_bar.text(), browser))
        toolbar.addWidget(search_bar)

        # Обновление адресной строки при изменении URL
        browser.urlChanged.connect(lambda q: self.update_url_bar(url_bar, q))

        # Сохранение истории
        browser.urlChanged.connect(lambda q: self.save_history(q, browser))

        # Обновление заголовка вкладки при изменении названия сайта
        browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))

        # Обновление иконки вкладки при изменении иконки сайта
        browser.iconChanged.connect(lambda icon: self.update_tab_icon(browser, icon))

        # Создаем контейнер для браузера и панели инструментов
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(browser)
        container.setLayout(layout)

        # Добавляем вкладку
        self.tabs.addTab(container, "Новая вкладка")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def save_history(self, q, browser):
        """ Сохраняет URL и название сайта в истории. """
        url = q.toString()
        title = browser.title()  # Получаем название сайта
        if url not in [entry[0] for entry in self.history]:  # Проверяем, есть ли уже в истории
            icon = browser.icon()  # Получаем иконку сайта
            self.history.append((url, title, icon))

    def show_history(self):
        """ Показывает историю браузера. """
        history_str = ""
        for url, title, icon in self.history:
            icon_url = icon.name() if icon else ""  # Получаем имя иконки
            history_str += f"<img src='{icon_url}' style='width:16px;height:16px;vertical-align:middle;'/>" \
                           f"<a href='{url}'>{title}</a><br>"

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
        else:
            QMessageBox.warning(self, "Закладка уже существует", f"{title} уже есть в закладках.")

    def show_bookmarks(self):
        """ Показывает список закладок. """
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
            # Если введен текст, выполняем поиск через Google
            search_url = f"https://www.google.com/search?q={url}"
            browser.setUrl(QUrl(search_url))

    def perform_search(self, query, browser):
        """ Выполняет поиск по запросу. """
        search_url = f"https://www.google.com/search?q={query}"
        browser.setUrl(QUrl(search_url))

    def update_url_bar(self, url_bar, q):
        """ Обновление адресной строки при изменении URL. """
        url_bar.setText(q.toString())

    def update_tab_title(self, browser, title):
        """ Обновление заголовка вкладки на название сайта. """
        index = self.tabs.indexOf(browser.parent())
        if index != -1:
            self.tabs.setTabText(index, title)

    def update_tab_icon(self, browser, icon):
        """ Обновление иконки вкладки. """
        index = self.tabs.indexOf(browser.parent())
        if index != -1:
            self.tabs.setTabIcon(index, icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())