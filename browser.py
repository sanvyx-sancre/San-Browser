from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import re
from urllib.parse import urlparse
from PyQt5.QtWebEngineWidgets import QWebEnginePage

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)

    def triggerAction(self, action, checked=False):
        # Check if the action is fullscreen
        if action == QWebEnginePage.FullScreen:
            self.view().setWindowState(Qt.WindowFullScreen)
        else:
            super(WebEnginePage, self).triggerAction(action, checked)

class SanBrowser(QMainWindow):
    def __init__(self):
        super(SanBrowser, self).__init__()
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



        navbar = QToolBar()
        navbar.setStyleSheet(self.get_navbar_styles())
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        search_btn = QAction('Search', self)
        search_btn.triggered.connect(self.search)
        navbar.addAction(search_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet(self.get_url_bar_styles())
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        self.url_bar.returnPressed.connect(self.search)

        refresh_btn = QAction('Refresh', self)
        refresh_btn.triggered.connect(self.browser.reload)
        navbar.addAction(refresh_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.home)
        navbar.addAction(home_btn)

        self.tabs.currentChanged.connect(self.change_tab)

        addtab_btn = QAction('New Tab', self)
        addtab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(addtab_btn)

    def close_current_tab(self, index):
        self.tabs.removeTab(index)

    def change_tab(self, index):
        if index >= 0:
            self.browser = self.tabs.currentWidget()

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl('http://duckduckgo.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, qurl.host())
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(self.update_url)
        browser.loadFinished.connect(lambda _, i=i: self.tabs.setTabIcon(i, browser.icon()))

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
        self.tabs.setTabText(index, parsed_url.netloc)
        self.tabs.setTabIcon(index, self.browser.icon())


    # Stylesheets for the different components
    def get_styles(self):
        return """
        QMainWindow {
            background-color: #1E1E1E;
            color: #D3D3D3;
            font-family: Arial, sans-serif;
        }
        """

    def get_navbar_styles(self):
        return """
        QToolBar {
            background-color: #333;
            border: none;
            padding: 5px;
        }
        QToolButton {
            color: #FFF;
            background: #555;
            border-radius: 5px;
            padding: 8px;
            margin: 3px;
        }
        QToolButton:hover {
            background: #777;
        }
        QLineEdit {
            background-color: #555;
            color: white;
            padding: 6px;
            border-radius: 5px;
            font-size: 14px;
        }
        """

    def get_url_bar_styles(self):
        return """
        QLineEdit {
            border: none;
            border-radius: 5px;
            padding: 5px;
            background-color: #444;
            color: white;
            font-size: 14px;
        }
        QLineEdit:focus {
            background-color: #333;
            border: 1px solid #4A90E2;
        }
        """

    def get_tab_styles(self):
        return """
        QTabWidget::pane {
            border: 1px solid #444;
            background-color: #333;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #555;
            color: white;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        }
        QTabBar::tab:selected {
            background: #4A90E2;
            color: white;
        }
        QTabBar::tab:hover {
            background: #777;
        }
        """

execution = QApplication([])
execution.setApplicationName('San Browser')
window = SanBrowser()
window.show()
execution.exec_()
