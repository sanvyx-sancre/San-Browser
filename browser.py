from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from urllib.parse import urlparse

class Zenith(QMainWindow):
    def __init__(self):
        super(Zenith, self).__init__()
        self.setWindowTitle('San Browser')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_styles())

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet(self.get_tab_styles())
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.browser = QWebEngineView()
        self.browser.load(QUrl('http://duckduckgo.com'))
        self.tabs.addTab(self.browser, 'Home')

        self.back_shortcut = QShortcut(QKeySequence(Qt.MouseButton.BackButton), self)
        self.back_shortcut.activated.connect(self.browser.back)

        self.forward_shortcut = QShortcut(QKeySequence(Qt.MouseButton.ForwardButton), self)
        self.forward_shortcut.activated.connect(self.browser.forward)

        navbar = QToolBar()
        navbar.setStyleSheet(self.get_navbar_styles())
        self.addToolBar(navbar)

        back_btn = QAction('⮜', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('⮞', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        refresh_btn = QAction('⭯', self)
        refresh_btn.triggered.connect(self.browser.reload)
        navbar.addAction(refresh_btn)

        home_btn = QAction('🏠', self)
        home_btn.triggered.connect(self.home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet(self.get_url_bar_styles())
        navbar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url)
        self.url_bar.returnPressed.connect(self.search)

        search_btn = QAction('🔍', self)
        search_btn.triggered.connect(self.search)
        navbar.addAction(search_btn)

        addtab_btn = QAction('+', self)
        navbar.addAction(addtab_btn)
        addtab_btn.triggered.connect(lambda: self.add_new_tab())


    def close_current_tab(self, index):
        self.tabs.removeTab(index)

    def add_new_tab(self, qurl=QUrl('http://duckduckgo.com')):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url)

    # Add a new tab with the browser widget
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)



    def home(self):
        self.browser.setUrl(QUrl('http://duckduckgo.com'))

    def search(self):
        url = self.url_bar.text()

        # Check if the URL ends with a common domain extension
        if self.is_valid_url(url):
            self.browser.setUrl(QUrl("http://" + url))
        else:
            # Perform DuckDuckGo search if it's not a valid URL
            search_url = f'https://duckduckgo.com/?q={url}'
            self.browser.setUrl(QUrl(search_url))

    def is_valid_url(self, url):
        # Check if the URL ends with a common domain extension
        valid_extensions = ['.com', '.net', '.org', '.gov', '.edu', '.io', '.co']
        return any(url.endswith(ext) for ext in valid_extensions)

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        index = self.tabs.currentIndex()
        parsed_url = urlparse(q.toString())
        self.tabs.setTabText(index, parsed_url.netloc or "New Tab")


    def get_styles(self):
        return """
        QMainWindow {
            background-color: #1E1E28;
            color: #CDD6F4;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        """

    def get_navbar_styles(self):
        return """
        QToolBar {
            background-color: #181825;
            border: none;
            padding: 5px;
        }
        QToolButton {
            color: #F5C2E7;
            background: #313244;
            border-radius: 5px;
            padding: 6px;
            margin: 2px;
            font-size: 14px;
        }
        QToolButton:hover {
            background: #45475A;
        }
        QLineEdit {
            background-color: #313244;
            color: #CDD6F4;
            padding: 5px;
            border-radius: 5px;
            font-size: 14px;
        }
        QLineEdit:focus {
            background-color: #45475A;
            border: 1px solid #89B4FA;
        }
        """

    def get_tab_styles(self):
        return """
        QTabWidget::pane {
            border: 1px solid #313244;
            background-color: #1E1E28;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #313244;
            color: #CDD6F4;
            padding: 8px;
            border-radius: 5px;
            margin: 2px;
        }
        QTabBar::tab:selected {
            background: #89B4FA;
            color: #1E1E28;
        }
        QTabBar::tab:hover {
            background: #45475A;
        }
        """

    def get_url_bar_styles(self):
        return """
        QLineEdit {
            border: none;
            border-radius: 5px;
            padding: 5px;
            background-color: #313244;
            color: #CDD6F4;
            font-size: 14px;
        }
        QLineEdit:focus {
            background-color: #45475A;
            border: 1px solid #89B4FA;
        }
        """

execution = QApplication([])
execution.setApplicationName('Zenith')
window = Zenith()
window.show()
execution.exec_()
